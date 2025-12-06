---
source: https://tradingview.github.io/lightweight-charts/docs/api/functions/createOptionsChart
scraped_at: 2025-12-01T14:31:38.228967
---

# https://tradingview.github.io/lightweight-charts/docs/api/functions/createOptionsChart

# Function: createOptionsChart()

createOptionsChart(`container`

,`options`

?):`IChartApiBase`

<`number`

>

Creates an 'options' chart with price values on the horizontal scale.

This function is used to create a specialized chart type where the horizontal scale represents price values instead of time. It's particularly useful for visualizing option chains, price distributions, or any data where price is the primary x-axis metric.

## Parameters

• **container**: `string`

| `HTMLElement`

The DOM element or its id where the chart will be rendered.

• **options?**: `DeepPartial`

<`PriceChartOptions`

>

Optional configuration options for the price chart.

## Returns

`IChartApiBase`

<`number`

>

An instance of IChartApiBase configured for price-based horizontal scaling.