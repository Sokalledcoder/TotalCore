---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/LocalizationOptions
scraped_at: 2025-12-01T14:31:40.863379
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/LocalizationOptions

# Interface: LocalizationOptions<HorzScaleItem>

Represents options for formatting dates, times, and prices according to a locale.

## Extends

## Extended by

## Type parameters

• **HorzScaleItem**

## Properties

### timeFormatter?

`optional`

timeFormatter:`TimeFormatterFn`

<`HorzScaleItem`

>

Override formatting of the time scale crosshair label.

#### Default Value

`undefined`

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

### locale

locale:`string`

Current locale used to format dates. Uses the browser's language settings by default.

#### See

#### Default Value

`navigator.language`

#### Inherited from

`LocalizationOptionsBase`

. `locale`

### priceFormatter?

`optional`

priceFormatter:`PriceFormatterFn`

Override formatting of the price scale tick marks, labels and crosshair labels. Can be used for cases that can't be covered with built-in price formats.

#### See

#### Default Value

`undefined`

#### Inherited from

`LocalizationOptionsBase`

. `priceFormatter`

### tickmarksPriceFormatter?

`optional`

tickmarksPriceFormatter:`TickmarksPriceFormatterFn`

Overrides the formatting of price scale tick marks. Use this to define formatting rules based on all provided price values.

#### Default Value

`undefined`

#### Inherited from

`LocalizationOptionsBase`

. `tickmarksPriceFormatter`

### percentageFormatter?

`optional`

percentageFormatter:`PercentageFormatterFn`

Overrides the formatting of percentage scale tick marks.

#### Default Value

`undefined`

#### Inherited from

`LocalizationOptionsBase`

. `percentageFormatter`

### tickmarksPercentageFormatter?

`optional`

tickmarksPercentageFormatter:`TickmarksPercentageFormatterFn`

Override formatting of the percentage scale tick marks. Can be used if formatting should be adjusted based on all the values being formatted

#### Default Value

`undefined`