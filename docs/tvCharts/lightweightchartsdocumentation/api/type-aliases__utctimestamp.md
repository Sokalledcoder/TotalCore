---
source: https://tradingview.github.io/lightweight-charts/docs/api/type-aliases/UTCTimestamp
scraped_at: 2025-12-01T14:31:44.744794
---

# https://tradingview.github.io/lightweight-charts/docs/api/type-aliases/UTCTimestamp

# Type alias: UTCTimestamp

UTCTimestamp:`Nominal`

<`number`

,`"UTCTimestamp"`

>

Represents a time as a UNIX timestamp.

If your chart displays an intraday interval you should use a UNIX Timestamp.

Note that JavaScript Date APIs like `Date.now`

return a number of milliseconds but UTCTimestamp expects a number of seconds.

Note that to prevent errors, you should cast the numeric type of the time to `UTCTimestamp`

type from the package (`value as UTCTimestamp`

) in TypeScript code.

## Example

`const timestamp = 1529899200 as UTCTimestamp; // Literal timestamp representing 2018-06-25T04:00:00.000Z`

const timestamp2 = (Date.now() / 1000) as UTCTimestamp;