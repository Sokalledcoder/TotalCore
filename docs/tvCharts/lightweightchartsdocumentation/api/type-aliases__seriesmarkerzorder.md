---
source: https://tradingview.github.io/lightweight-charts/docs/api/type-aliases/SeriesMarkerZOrder
scraped_at: 2025-12-01T14:31:44.052850
---

# https://tradingview.github.io/lightweight-charts/docs/api/type-aliases/SeriesMarkerZOrder

# Type alias: SeriesMarkerZOrder

SeriesMarkerZOrder:`"top"`

|`"aboveSeries"`

|`"normal"`

The visual stacking order for the markers within the chart.

`normal`

: Markers are drawn together with the series they belong to. They can appear below other series depending on the series stacking order.`aboveSeries`

: Markers are drawn above all series but below primitives that use the 'top' zOrder layer.`top`

: Markers are drawn on the topmost primitive layer, above all series and (most) other primitives.