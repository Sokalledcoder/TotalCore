---
source: https://tradingview.github.io/lightweight-charts/docs/api/type-aliases/TickMarkFormatter
scraped_at: 2025-12-01T14:31:44.254165
---

# https://tradingview.github.io/lightweight-charts/docs/api/type-aliases/TickMarkFormatter

# Type alias: TickMarkFormatter()

TickMarkFormatter: (`time`

,`tickMarkType`

,`locale`

) =>`string`

|`null`

The `TickMarkFormatter`

is used to customize tick mark labels on the time scale.

This function should return `time`

as a string formatted according to `tickMarkType`

type (year, month, etc) and `locale`

.

Note that the returned string should be the shortest possible value and should have no more than 8 characters. Otherwise, the tick marks will overlap each other.

If the formatter function returns `null`

then the default tick mark formatter will be used as a fallback.

## Example

`const customFormatter = (time, tickMarkType, locale) => {`

// your code here

};

## Parameters

• **time**: `Time`

• **tickMarkType**: `TickMarkType`

• **locale**: `string`

## Returns

`string`

| `null`