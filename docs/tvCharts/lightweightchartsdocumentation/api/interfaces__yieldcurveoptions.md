---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/YieldCurveOptions
scraped_at: 2025-12-01T14:31:42.182226
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/YieldCurveOptions

# Interface: YieldCurveOptions

Options specific to yield curve charts.

## Properties

### baseResolution

baseResolution:`number`

The smallest time unit for the yield curve, typically representing one month. This value determines the granularity of the time scale.

#### Default Value

`1`

### minimumTimeRange

minimumTimeRange:`number`

The minimum time range to be displayed on the chart, in units of baseResolution. This ensures that the chart always shows at least this much time range, even if there's less data.

#### Default Value

`120 (10 years)`

### startTimeRange

startTimeRange:`number`

The starting time value for the chart, in units of baseResolution. This determines where the time scale begins.

#### Default Value

`0`

### formatTime()?

`optional`

formatTime: (`months`

) =>`string`

Optional custom formatter for time values on the horizontal axis. If not provided, a default formatter will be used.

#### Parameters

• **months**: `number`

The number of months (or baseResolution units) to format

#### Returns

`string`