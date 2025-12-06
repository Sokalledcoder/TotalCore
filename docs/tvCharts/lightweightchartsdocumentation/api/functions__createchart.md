---
source: https://tradingview.github.io/lightweight-charts/docs/api/functions/createChart
scraped_at: 2025-12-01T14:31:38.055978
---

# https://tradingview.github.io/lightweight-charts/docs/api/functions/createChart

# Function: createChart()

createChart(`container`

,`options`

?):`IChartApi`

This function is the simplified main entry point of the Lightweight Charting Library with time points for the horizontal scale.

## Parameters

• **container**: `string`

| `HTMLElement`

ID of HTML element or element itself

• **options?**: `DeepPartial`

<`TimeChartOptions`

>

Any subset of options to be applied at start.

## Returns

An interface to the created chart