---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/PriceChartLocalizationOptions
scraped_at: 2025-12-01T14:31:41.117898
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/PriceChartLocalizationOptions

# Interface: PriceChartLocalizationOptions

Extends LocalizationOptions for price-based charts. Includes settings specific to formatting price values on the horizontal scale.

## Extends

## Properties

### timeFormatter?

`optional`

timeFormatter:`TimeFormatterFn`

<`number`

>

Override formatting of the time scale crosshair label.

#### Default Value

`undefined`

#### Inherited from

`LocalizationOptions`

. `timeFormatter`

### dateFormat

dateFormat:`string`

Date formatting string.

Can contain `yyyy`

, `yy`

, `MMMM`

, `MMM`

, `MM`

and `dd`

literals which will be replaced with corresponding date's value.

Ignored if timeFormatter has been specified.

#### Default Value

`'dd MMM \'yy'`

#### Inherited from

`LocalizationOptions`

. `dateFormat`

### locale

locale:`string`

Current locale used to format dates. Uses the browser's language settings by default.

#### See

#### Default Value

`navigator.language`

#### Inherited from

### priceFormatter?

`optional`

priceFormatter:`PriceFormatterFn`

Override formatting of the price scale tick marks, labels and crosshair labels. Can be used for cases that can't be covered with built-in price formats.

#### See

#### Default Value

`undefined`

#### Inherited from

`LocalizationOptions`

. `priceFormatter`

### tickmarksPriceFormatter?

`optional`

tickmarksPriceFormatter:`TickmarksPriceFormatterFn`

Overrides the formatting of price scale tick marks. Use this to define formatting rules based on all provided price values.

#### Default Value

`undefined`

#### Inherited from

`LocalizationOptions`

. `tickmarksPriceFormatter`

### percentageFormatter?

`optional`

percentageFormatter:`PercentageFormatterFn`

Overrides the formatting of percentage scale tick marks.

#### Default Value

`undefined`

#### Inherited from

`LocalizationOptions`

. `percentageFormatter`

### tickmarksPercentageFormatter?

`optional`

tickmarksPercentageFormatter:`TickmarksPercentageFormatterFn`

Override formatting of the percentage scale tick marks. Can be used if formatting should be adjusted based on all the values being formatted

#### Default Value

`undefined`

#### Inherited from

`LocalizationOptions`

. `tickmarksPercentageFormatter`

### precision

precision:`number`

The number of decimal places to display for price values on the horizontal scale.