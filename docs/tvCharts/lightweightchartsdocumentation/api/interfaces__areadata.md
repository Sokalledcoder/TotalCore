---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/AreaData
scraped_at: 2025-12-01T14:31:38.462623
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/AreaData

# Interface: AreaData<HorzScaleItem>

Structure describing a single item of data for area series

## Extends

`SingleValueData`

<`HorzScaleItem`

>

## Type parameters

• **HorzScaleItem** = `Time`

## Properties

### lineColor?

`optional`

lineColor:`string`

Optional line color value for certain data item. If missed, color from options is used

### topColor?

`optional`

topColor:`string`

Optional top color value for certain data item. If missed, color from options is used

### bottomColor?

`optional`

bottomColor:`string`

Optional bottom color value for certain data item. If missed, color from options is used

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