---
source: https://tradingview.github.io/lightweight-charts/docs/api/functions/createYieldCurveChart
scraped_at: 2025-12-01T14:31:38.240480
---

# https://tradingview.github.io/lightweight-charts/docs/api/functions/createYieldCurveChart

# Function: createYieldCurveChart()

createYieldCurveChart(`container`

,`options`

?):`IYieldCurveChartApi`

Creates a yield curve chart with the specified options.

A yield curve chart differs from the default chart type in the following ways:

- Horizontal scale is linearly spaced, and defined in monthly time duration units
- Whitespace is ignored for the crosshair and grid lines

## Parameters

• **container**: `string`

| `HTMLElement`

ID of HTML element or element itself

• **options?**: `DeepPartial`

<`YieldCurveChartOptions`

>

The yield chart options.

## Returns

An interface to the created chart