---
source: https://tradingview.github.io/lightweight-charts/docs/api/type-aliases/CustomSeriesPricePlotValues
scraped_at: 2025-12-01T14:31:42.944957
---

# https://tradingview.github.io/lightweight-charts/docs/api/type-aliases/CustomSeriesPricePlotValues

# Type alias: CustomSeriesPricePlotValues

CustomSeriesPricePlotValues:`number`

[]

Price values for the custom series. This list should include the largest, smallest, and current price values for the data point. The last value in the array will be used for the current value. You shouldn't need to have more than 3 values in this array since the library only needs a largest, smallest, and current value.

Examples:

- For a line series, this would contain a single number representing the current value.
- For a candle series, this would contain the high, low, and close values. Where the last value would be the close value.