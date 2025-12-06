---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/SeriesMarkersOptions
scraped_at: 2025-12-01T14:31:41.561209
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/SeriesMarkersOptions

# Interface: SeriesMarkersOptions

Configuration options for the series markers plugin. These options affect all markers managed by the plugin.

## Properties

### autoScale

autoScale:`boolean`

Specifies whether the auto-scaling calculation should expand to include the size of markers.

When `true`

, the auto-scale feature will adjust the price scale's range to ensure
series markers are fully visible and not cropped by the chart's edges.

When `false`

, the scale will only fit the series data points, which may cause
markers to be partially hidden.

Note: This option only has an effect when auto-scaling is enabled for the price scale.

#### Default Value

`true`

### zOrder

zOrder:`SeriesMarkerZOrder`

Defines the stacking order of the markers relative to the series and other primitives.

#### Default Value

`normal`