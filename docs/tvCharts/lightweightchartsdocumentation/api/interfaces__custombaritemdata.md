---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/CustomBarItemData
scraped_at: 2025-12-01T14:31:39.175282
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/CustomBarItemData

# Interface: CustomBarItemData<HorzScaleItem, TData>

Renderer data for an item within the custom series.

## Type parameters

• **HorzScaleItem**

• **TData** *extends* `CustomData`

<`HorzScaleItem`

> = `CustomData`

<`HorzScaleItem`

>

## Properties

### x

x:`number`

Horizontal coordinate for the item. Measured from the left edge of the pane in pixels.

### time

time:`number`

Time scale index for the item. This isn't the timestamp but rather the logical index.

### originalData

originalData:`TData`

Original data for the item.

### barColor

barColor:`string`

Color assigned for the item, typically used for price line and price scale label.