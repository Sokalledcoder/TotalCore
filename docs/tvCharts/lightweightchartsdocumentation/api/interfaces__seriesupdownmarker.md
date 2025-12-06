---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/SeriesUpDownMarker
scraped_at: 2025-12-01T14:31:41.710618
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/SeriesUpDownMarker

# Interface: SeriesUpDownMarker<T>

Represents a marker drawn above or below a data point to indicate a price change update.

## Type parameters

• **T** = `Time`

The type of the time value, defaults to Time.

## Properties

### time

time:`T`

The point on the horizontal scale.

### value

value:`number`

The price value for the data point.

### sign

sign:`MarkerSign`

The direction of the price change.