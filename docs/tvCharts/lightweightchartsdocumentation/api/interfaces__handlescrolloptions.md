---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/HandleScrollOptions
scraped_at: 2025-12-01T14:31:39.387545
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/HandleScrollOptions

# Interface: HandleScrollOptions

Represents options for how the chart is scrolled by the mouse and touch gestures.

## Properties

### mouseWheel

mouseWheel:`boolean`

Enable scrolling with the mouse wheel.

#### Default Value

`true`

### pressedMouseMove

pressedMouseMove:`boolean`

Enable scrolling by holding down the left mouse button and moving the mouse.

#### Default Value

`true`

### horzTouchDrag

horzTouchDrag:`boolean`

Enable horizontal touch scrolling.

When enabled the chart handles touch gestures that would normally scroll the webpage horizontally.

#### Default Value

`true`

### vertTouchDrag

vertTouchDrag:`boolean`

Enable vertical touch scrolling.

When enabled the chart handles touch gestures that would normally scroll the webpage vertically.

#### Default Value

`true`