---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/IPanePrimitivePaneView
scraped_at: 2025-12-01T14:31:39.995921
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/IPanePrimitivePaneView

# Interface: IPanePrimitivePaneView

This interface represents the primitive for one of the pane of the chart (main chart area, time scale, price scale).

## Methods

### zOrder()?

`optional`

zOrder():`PrimitivePaneViewZOrder`

Defines where in the visual layer stack the renderer should be executed. Default is `'normal'`

.

#### Returns

the desired position in the visual layer stack.

#### See

### renderer()

renderer():`IPrimitivePaneRenderer`

This method returns a renderer - special object to draw data

#### Returns

an renderer object to be used for drawing, or `null`

if we have nothing to draw.