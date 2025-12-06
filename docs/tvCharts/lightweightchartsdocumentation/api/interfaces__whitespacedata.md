---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/WhitespaceData
scraped_at: 2025-12-01T14:31:42.213353
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/WhitespaceData

# Interface: WhitespaceData<HorzScaleItem>

Represents a whitespace data item, which is a data point without a value.

## Example

`const data = [`

{ time: '2018-12-03', value: 27.02 },

{ time: '2018-12-04' }, // whitespace

{ time: '2018-12-05' }, // whitespace

{ time: '2018-12-06' }, // whitespace

{ time: '2018-12-07' }, // whitespace

{ time: '2018-12-08', value: 23.92 },

{ time: '2018-12-13', value: 30.74 },

];

## Extended by

## Type parameters

• **HorzScaleItem** = `Time`

## Properties

### time

time:`HorzScaleItem`

The time of the data.

### customValues?

`optional`

customValues:`Record`

<`string`

,`unknown`

>

Additional custom values which will be ignored by the library, but could be used by plugins.