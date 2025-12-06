---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/IPrimitivePaneRenderer
scraped_at: 2025-12-01T14:31:40.040529
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/IPrimitivePaneRenderer

# Interface: IPrimitivePaneRenderer

This interface represents rendering some element on the canvas

## Methods

### draw()

draw(`target`

,`utils`

?):`void`

Method to draw main content of the element

#### Parameters

• **target**: `CanvasRenderingTarget2D`

canvas context to draw on, refer to FancyCanvas library for more details about this class

• **utils?**: `DrawingUtils`

exposes drawing utilities (such as setLineStyle) from the library to plugins

#### Returns

`void`

### drawBackground()?

`optional`

drawBackground(`target`

,`utils`

?):`void`

Optional method to draw the background. Some elements could implement this method to draw on the background of the chart. Usually this is some kind of watermarks or time areas highlighting.

#### Parameters

• **target**: `CanvasRenderingTarget2D`

canvas context to draw on, refer FancyCanvas library for more details about this class

• **utils?**: `DrawingUtils`

exposes drawing utilities (such as setLineStyle) from the library to plugins

#### Returns

`void`