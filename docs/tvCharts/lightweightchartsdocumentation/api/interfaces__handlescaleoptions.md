---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/HandleScaleOptions
scraped_at: 2025-12-01T14:31:39.517337
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/HandleScaleOptions

# Interface: HandleScaleOptions

Represents options for how the chart is scaled by the mouse and touch gestures.

## Properties

### mouseWheel

mouseWheel:`boolean`

Enable scaling with the mouse wheel.

#### Default Value

`true`

### pinch

pinch:`boolean`

Enable scaling with pinch/zoom gestures.

#### Default Value

`true`

### axisPressedMouseMove

axisPressedMouseMove:`boolean`

|`AxisPressedMouseMoveOptions`

Enable scaling the price and/or time scales by holding down the left mouse button and moving the mouse.

### axisDoubleClickReset

axisDoubleClickReset:`boolean`

|`AxisDoubleClickOptions`

Enable resetting scaling by double-clicking the left mouse button.