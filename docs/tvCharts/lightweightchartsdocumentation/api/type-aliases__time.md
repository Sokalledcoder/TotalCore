---
source: https://tradingview.github.io/lightweight-charts/docs/api/type-aliases/Time
scraped_at: 2025-12-01T14:31:44.385694
---

# https://tradingview.github.io/lightweight-charts/docs/api/type-aliases/Time

# Type alias: Time

Time:`UTCTimestamp`

|`BusinessDay`

|`string`

The Time type is used to represent the time of data items.

Values can be a UTCTimestamp, a BusinessDay, or a business day string in ISO format.

## Example

`const timestamp = 1529899200; // Literal timestamp representing 2018-06-25T04:00:00.000Z`

const businessDay = { year: 2019, month: 6, day: 1 }; // June 1, 2019

const businessDayString = '2021-02-03'; // Business day string literal