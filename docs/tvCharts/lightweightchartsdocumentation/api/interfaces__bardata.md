---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/BarData
scraped_at: 2025-12-01T14:31:38.642270
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/BarData

# Interface: BarData<HorzScaleItem>

Structure describing a single item of data for bar series

## Extends

`OhlcData`

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

The bar time.

#### Inherited from

### open

open:`number`

The open price.

#### Inherited from

### high

high:`number`

The high price.

#### Inherited from

### low

low:`number`

The low price.

#### Inherited from

### close

close:`number`

The close price.

#### Inherited from

### customValues?

`optional`

customValues:`Record`

<`string`

,`unknown`

>

Additional custom values which will be ignored by the library, but could be used by plugins.