---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/PrimitiveHoveredItem
scraped_at: 2025-12-01T14:31:41.346960
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/PrimitiveHoveredItem

# Interface: PrimitiveHoveredItem

Data representing the currently hovered object from the Hit test.

## Properties

### cursorStyle?

`optional`

cursorStyle:`string`

CSS cursor style as defined here: MDN: CSS Cursor or `undefined`

if you want the library to use the default cursor style instead.

### externalId

externalId:`string`

Hovered objects external ID. Can be used to identify the source item within a mouse subscriber event.

### zOrder

zOrder:`PrimitivePaneViewZOrder`

The zOrder of the hovered item.

### isBackground?

`optional`

isBackground:`boolean`

Set to true if the object is rendered using `drawBackground`

instead of `draw`

.