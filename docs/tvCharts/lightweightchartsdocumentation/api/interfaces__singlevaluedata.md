---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/SingleValueData
scraped_at: 2025-12-01T14:31:41.862893
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/SingleValueData

# Interface: SingleValueData<HorzScaleItem>

A base interface for a data point of single-value series.

## Extends

`WhitespaceData`

<`HorzScaleItem`

>

## Extended by

## Type parameters

• **HorzScaleItem** = `Time`

## Properties

### time

time:`HorzScaleItem`

The time of the data.

#### Overrides

### value

value:`number`

Price value of the data.

### customValues?

`optional`

customValues:`Record`

<`string`

,`unknown`

>

Additional custom values which will be ignored by the library, but could be used by plugins.