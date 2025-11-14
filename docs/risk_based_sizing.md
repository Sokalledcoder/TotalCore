# Risk-Based Position Sizing Preset

This preset enforces the stop-driven sizing rule discussed during Session 5. Every trade must define a stop distance, and the allowable position size is computed dynamically:

```
allowed_units = (equity * risk_pct * bucket_multiplier) / abs(entry_price - stop_price)
```

- `risk_pct` comes from the environment config (`0.01` by default).
- `bucket_multiplier` maps to the `action.size_buckets` array so the policy can risk 0.5x, 1x, 1.5x, or 2x the baseline exposure.
- Stops are still selected via the `stop_loss_steps` head; in the `btcusd_1m_risk_based` config each step is 0.25% of price.

The environment guarantees:
- Orders always include a stop (`risk_sizing_mode = "risk_based"`).
- Position sizing ignores the legacy `max_position_size = 0.5 BTC`; instead, we cap only at `max_position_size = 10 BTC` to avoid runaway leverage while still allowing multi-BTC trades when stops are tight.
- Rewards still subtract actual maker/taker fees plus drawdown penalties, so churning without edge hurts returns.

To run the preset on GPU, use the `configs/train/ppo_gpu_risk_medium.json` training config (8 env workers, cuda device, extended indicator set). This retains all Session 5 GPU optimizations but swaps in the new environment.
