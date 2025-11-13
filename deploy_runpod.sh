#!/usr/bin/env bash
set -euo pipefail
source .env
cat <<'PAYLOAD' > /tmp/payload.json
{"query":"mutation { podFindAndDeployOnDemand(input: { name: \"tradecore-a4500-verify\", imageName: \"runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404\", gpuTypeId: \"NVIDIA RTX A4500\", gpuCount: 1, cloudType: SECURE, dataCenterId: \"EU-RO-1\", containerDiskInGb: 40, ports: \"22/tcp,8888/http\", volumeInGb: 0, volumeMountPath: \"/workspace\", networkVolumeId: \"6wlciwn57c\", dockerArgs: \"bash -lc 'cd /workspace/TradeCore && sleep infinity'\" }) { id } }"}
PAYLOAD
curl https://api.runpod.io/graphql -H "Authorization: Bearer $RUNPOD_API_KEY" -H "Content-Type: application/json" -d @/tmp/payload.json
