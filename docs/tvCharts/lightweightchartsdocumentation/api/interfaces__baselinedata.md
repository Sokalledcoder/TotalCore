---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/BaselineData
scraped_at: 2025-12-01T14:31:38.737682
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/BaselineData

# Interface: BaselineData<HorzScaleItem>

Structure describing a single item of data for baseline series

## Extends

`SingleValueData`

<`HorzScaleItem`

>

## Type parameters

• **HorzScaleItem** = `Time`

## Properties

### topFillColor1?

`optional`

topFillColor1:`string`

Optional top area top fill color value for certain data item. If missed, color from options is used

### topFillColor2?

`optional`

topFillColor2:`string`

Optional top area bottom fill color value for certain data item. If missed, color from options is used

### topLineColor?

`optional`

topLineColor:`string`

Optional top area line color value for certain data item. If missed, color from options is used

### bottomFillColor1?

`optional`

bottomFillColor1:`string`

Optional bottom area top fill color value for certain data item. If missed, color from options is used

### bottomFillColor2?

`optional`

bottomFillColor2:`string`

Optional bottom area bottom fill color value for certain data item. If missed, color from options is used

### bottomLineColor?

`optional`

bottomLineColor:`string`

Optional bottom area line color value for certain data item. If missed, color from options is used

### time

time:`HorzScaleItem`

The time of the data.

#### Inherited from

### value

value:`number`

Price value of the data.

#### Inherited from

### customValues?

`optional`

customValues:`Record`

<`string`

,`unknown`

>

Additional custom values which will be ignored by the library, but could be used by plugins.