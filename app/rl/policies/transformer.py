"""Transformer-based feature extractor for SB3 MultiInputPolicy."""
from __future__ import annotations

from typing import Optional

import torch
from gymnasium import spaces
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
from torch import nn


class TransformerFeatureExtractor(BaseFeaturesExtractor):
    """Encodes the market window with a transformer and combines it with account features."""

    def __init__(
        self,
        observation_space: spaces.Dict,
        features_dim: int = 512,
        d_model: int = 256,
        nhead: int = 4,
        num_layers: int = 2,
        dim_feedforward: int = 512,
        dropout: float = 0.1,
        use_cls_token: bool = True,
    ) -> None:
        super().__init__(observation_space, features_dim)

        self.market_space = observation_space["market"]
        self.account_space = observation_space["account"]
        self.window_size = self.market_space.shape[0]
        self.market_features = self.market_space.shape[1]
        self.account_features = self.account_space.shape[0]
        self.d_model = d_model
        self.use_cls = use_cls_token

        self.market_proj = nn.Linear(self.market_features, d_model)
        self.account_proj = nn.Sequential(
            nn.Linear(self.account_features, d_model),
            nn.GELU(),
        )

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            batch_first=True,
            norm_first=True,
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)

        token_count = self.window_size + (1 if use_cls_token else 0)
        self.positional = nn.Parameter(torch.zeros(1, token_count, d_model))
        self.cls_token: Optional[nn.Parameter] = None
        if use_cls_token:
            self.cls_token = nn.Parameter(torch.zeros(1, 1, d_model))

        combined_dim = d_model * 2
        self.output = nn.Sequential(
            nn.LayerNorm(combined_dim),
            nn.Linear(combined_dim, features_dim),
            nn.GELU(),
        )

        self._reset_parameters()

    def _reset_parameters(self) -> None:
        nn.init.trunc_normal_(self.market_proj.weight, std=0.02)
        nn.init.zeros_(self.market_proj.bias)
        if isinstance(self.account_proj[0], nn.Linear):
            nn.init.trunc_normal_(self.account_proj[0].weight, std=0.02)
            nn.init.zeros_(self.account_proj[0].bias)
        nn.init.trunc_normal_(self.positional, std=0.02)
        if self.cls_token is not None:
            nn.init.trunc_normal_(self.cls_token, std=0.02)

    def forward(self, observations: dict[str, torch.Tensor]) -> torch.Tensor:
        market = observations["market"]  # (B, window, features)
        account = observations["account"]  # (B, account_features)

        x = self.market_proj(market)
        if self.use_cls and self.cls_token is not None:
            cls_token = self.cls_token.expand(market.size(0), -1, -1)
            x = torch.cat([cls_token, x], dim=1)
        pos = self.positional[:, : x.size(1), :]
        x = x + pos
        encoded = self.encoder(x)
        if self.use_cls:
            pooled = encoded[:, 0, :]
        else:
            pooled = encoded.mean(dim=1)

        account_embed = self.account_proj(account)
        combined = torch.cat([pooled, account_embed], dim=1)
        return self.output(combined)
