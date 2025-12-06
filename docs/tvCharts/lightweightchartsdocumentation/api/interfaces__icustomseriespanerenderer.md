---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ICustomSeriesPaneRenderer
scraped_at: 2025-12-01T14:31:39.359073
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ICustomSeriesPaneRenderer

# Interface: ICustomSeriesPaneRenderer

Renderer for the custom series. This paints on the main chart pane.

## Methods

### draw()

draw(`target`

,`priceConverter`

,`isHovered`

,`hitTestData`

?):`void`

Draw function for the renderer.

#### Parameters

• **target**: `CanvasRenderingTarget2D`

canvas context to draw on, refer to FancyCanvas library for more details about this class.

• **priceConverter**: `PriceToCoordinateConverter`

converter function for changing prices into vertical coordinate values.

• **isHovered**: `boolean`

Whether the series is hovered.

• **hitTestData?**: `unknown`

Optional hit test data for the series.

#### Returns

`void`