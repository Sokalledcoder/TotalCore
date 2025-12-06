---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/OhlcData
scraped_at: 2025-12-01T14:31:40.952147
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/OhlcData

# Interface: OhlcData<HorzScaleItem>

Represents a bar with a Time and open, high, low, and close prices.

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

The bar time.

#### Overrides

### open

open:`number`

The open price.

### high

high:`number`

The high price.

### low

low:`number`

The low price.

### close

close:`number`

The close price.

### customValues?

`optional`

customValues:`Record`

<`string`

,`unknown`

>

Additional custom values which will be ignored by the library, but could be used by plugins.