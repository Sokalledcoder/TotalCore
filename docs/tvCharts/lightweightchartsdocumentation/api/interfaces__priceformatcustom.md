---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/PriceFormatCustom
scraped_at: 2025-12-01T14:31:41.082451
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/PriceFormatCustom

# Interface: PriceFormatCustom

Represents series value formatting options.

## Properties

### type

type:`"custom"`

The custom price format.

### formatter

formatter:`PriceFormatterFn`

Override price formatting behaviour. Can be used for cases that can't be covered with built-in price formats.

### tickmarksFormatter?

`optional`

tickmarksFormatter:`TickmarksPriceFormatterFn`

Override price formatting for multiple prices. Can be used if formatter should be adjusted based of all values being formatted.

### minMove

minMove:`number`

The minimum possible step size for price value movement.

#### Default Value

`0.01`

### base?

`optional`

base:`number`

The base value for the price format. It should equal to 1 / minMove.
If this option is specified, we ignore the minMove option.
It can be useful for cases with very small price movements like `1e-18`

where we can reach limitations of floating point precision.