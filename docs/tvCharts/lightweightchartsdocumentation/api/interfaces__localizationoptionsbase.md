---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/LocalizationOptionsBase
scraped_at: 2025-12-01T14:31:40.814068
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/LocalizationOptionsBase

# Interface: LocalizationOptionsBase

Represents basic localization options

## Extended by

## Properties

### locale

locale:`string`

Current locale used to format dates. Uses the browser's language settings by default.

#### See

#### Default Value

`navigator.language`

### priceFormatter?

`optional`

priceFormatter:`PriceFormatterFn`

Override formatting of the price scale tick marks, labels and crosshair labels. Can be used for cases that can't be covered with built-in price formats.

#### See

#### Default Value

`undefined`

### tickmarksPriceFormatter?

`optional`

tickmarksPriceFormatter:`TickmarksPriceFormatterFn`

Overrides the formatting of price scale tick marks. Use this to define formatting rules based on all provided price values.

#### Default Value

`undefined`

### percentageFormatter?

`optional`

percentageFormatter:`PercentageFormatterFn`

Overrides the formatting of percentage scale tick marks.

#### Default Value

`undefined`

### tickmarksPercentageFormatter?

`optional`

tickmarksPercentageFormatter:`TickmarksPercentageFormatterFn`

Override formatting of the percentage scale tick marks. Can be used if formatting should be adjusted based on all the values being formatted

#### Default Value

`undefined`