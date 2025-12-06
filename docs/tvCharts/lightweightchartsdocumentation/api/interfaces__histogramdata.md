---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/HistogramData
scraped_at: 2025-12-01T14:31:39.293271
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/HistogramData

# Interface: HistogramData<HorzScaleItem>

Structure describing a single item of data for histogram series

## Extends

`SingleValueData`

<`HorzScaleItem`

>

## Type parameters

• **HorzScaleItem** = `Time`

## Properties

### color?

`optional`

color:`string`

Optional color value for certain data item. If missed, color from options is used

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