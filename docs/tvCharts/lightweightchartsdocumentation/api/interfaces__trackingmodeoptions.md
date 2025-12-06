---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/TrackingModeOptions
scraped_at: 2025-12-01T14:31:42.246036
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/TrackingModeOptions

# Interface: TrackingModeOptions

Represent options for the tracking mode's behavior.

Mobile users will not have the ability to see the values/dates like they do on desktop. To see it, they should enter the tracking mode. The tracking mode will deactivate the scrolling and make it possible to check values and dates.

## Properties

### exitMode

exitMode:`TrackingModeExitMode`

Determine how to exit the tracking mode.

By default, mobile users will long press to deactivate the scroll and have the ability to check values and dates. Another press is required to activate the scroll, be able to move left/right, zoom, etc.

#### Default Value

`{@link TrackingModeExitMode.OnNextTap}`