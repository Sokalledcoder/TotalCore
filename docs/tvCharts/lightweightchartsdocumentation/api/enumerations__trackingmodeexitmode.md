---
source: https://tradingview.github.io/lightweight-charts/docs/api/enumerations/TrackingModeExitMode
scraped_at: 2025-12-01T14:31:37.957383
---

# https://tradingview.github.io/lightweight-charts/docs/api/enumerations/TrackingModeExitMode

# Enumeration: TrackingModeExitMode

Determine how to exit the tracking mode.

By default, mobile users will long press to deactivate the scroll and have the ability to check values and dates. Another press is required to activate the scroll, be able to move left/right, zoom, etc.

## Enumeration Members

### OnTouchEnd

OnTouchEnd:`0`

Tracking Mode will be deactivated on touch end event.

### OnNextTap

OnNextTap:`1`

Tracking Mode will be deactivated on the next tap event.