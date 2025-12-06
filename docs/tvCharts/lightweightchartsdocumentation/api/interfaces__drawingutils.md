---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/DrawingUtils
scraped_at: 2025-12-01T14:31:39.074731
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/DrawingUtils

# Interface: DrawingUtils

Helper drawing utilities exposed by the library to a Primitive (a.k.a plugin).

## Properties

### setLineStyle()

`readonly`

setLineStyle: (`ctx`

,`lineStyle`

) =>`void`

Drawing utility to change the line style on the canvas context to one of the built-in line styles.

#### Parameters

• **ctx**: `CanvasRenderingContext2D`

2D rendering context for the target canvas.

• **lineStyle**: `LineStyle`

Built-in LineStyle to set on the canvas context.

#### Returns

`void`