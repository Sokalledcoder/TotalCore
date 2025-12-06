---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/IPriceFormatter
scraped_at: 2025-12-01T14:31:39.946077
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/IPriceFormatter

# Interface: IPriceFormatter

Interface to be implemented by the object in order to be used as a price formatter

## Methods

### format()

format(`price`

):`string`

Formatting function

#### Parameters

• **price**: `number`

Original price to be formatted

#### Returns

`string`

Formatted price

### formatTickmarks()

formatTickmarks(`prices`

):`string`

[]

A formatting function for price scale tick marks. Use this function to define formatting rules based on all provided price values.

#### Parameters

• **prices**: readonly `number`

[]

Prices to be formatted

#### Returns

`string`

[]

Formatted prices