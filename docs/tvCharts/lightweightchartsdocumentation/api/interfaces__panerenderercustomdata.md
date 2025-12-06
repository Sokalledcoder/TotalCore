---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/PaneRendererCustomData
scraped_at: 2025-12-01T14:31:41.211971
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/PaneRendererCustomData

# Interface: PaneRendererCustomData<HorzScaleItem, TData>

Data provide to the custom series pane view which can be used within the renderer for drawing the series data.

## Type parameters

• **HorzScaleItem**

• **TData** *extends* `CustomData`

<`HorzScaleItem`

>

## Properties

### bars

bars: readonly`CustomBarItemData`

<`HorzScaleItem`

,`TData`

>[]

List of all the series' items and their x coordinates.

### barSpacing

barSpacing:`number`

Spacing between consecutive bars.

### visibleRange

visibleRange:`IRange`

<`number`

>

The current visible range of items on the chart.