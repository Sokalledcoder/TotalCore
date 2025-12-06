---
source: https://tradingview.github.io/lightweight-charts/docs/api/type-aliases/LogicalRange
scraped_at: 2025-12-01T14:31:43.539679
---

# https://tradingview.github.io/lightweight-charts/docs/api/type-aliases/LogicalRange

# Type alias: LogicalRange

A logical range is an object with 2 properties: `from`

and `to`

, which are numbers and represent logical indexes on the time scale.

The starting point of the time scale's logical range is the first data item among all series. Before that point all indexes are negative, starting from that point - positive.

Indexes might have fractional parts, for instance 4.2, due to the time-scale being continuous rather than discrete.

Integer part of the logical index means index of the fully visible bar.
Thus, if we have 5.2 as the last visible logical index (`to`

field), that means that the last visible bar has index 5, but we also have partially visible (for 20%) 6th bar.
Half (e.g. 1.5, 3.5, 10.5) means exactly a middle of the bar.