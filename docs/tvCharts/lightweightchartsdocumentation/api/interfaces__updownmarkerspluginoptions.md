---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/UpDownMarkersPluginOptions
scraped_at: 2025-12-01T14:31:42.229880
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/UpDownMarkersPluginOptions

# Interface: UpDownMarkersPluginOptions

Configuration options for the UpDownMarkers plugin.

## Properties

### positiveColor

positiveColor:`string`

The color used for markers indicating a positive price change. This color will be applied to markers shown above data points where the price has increased.

### negativeColor

negativeColor:`string`

The color used for markers indicating a negative price change. This color will be applied to markers shown below data points where the price has decreased.

### updateVisibilityDuration

updateVisibilityDuration:`number`

The duration (in milliseconds) for which update markers remain visible on the chart. After this duration, the markers will automatically disappear. Set to 0 for markers to remain indefinitely until the next update.