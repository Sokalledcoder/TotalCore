---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/BarsInfo
scraped_at: 2025-12-01T14:31:38.674505
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/BarsInfo

# Interface: BarsInfo<HorzScaleItem>

Represents a range of bars and the number of bars outside the range.

## Extends

`Partial`

<`IRange`

<`HorzScaleItem`

>>

## Type parameters

• **HorzScaleItem**

## Properties

### barsBefore

barsBefore:`number`

The number of bars before the start of the range. Positive value means that there are some bars before (out of logical range from the left) the IRange.from logical index in the series. Negative value means that the first series' bar is inside the passed logical range, and between the first series' bar and the IRange.from logical index are some bars.

### barsAfter

barsAfter:`number`

The number of bars after the end of the range.
Positive value in the `barsAfter`

field means that there are some bars after (out of logical range from the right) the IRange.to logical index in the series.
Negative value means that the last series' bar is inside the passed logical range, and between the last series' bar and the IRange.to logical index are some bars.

### from?

`optional`

from:`HorzScaleItem`

The from value. The start of the range.

#### Inherited from

`Partial.from`

### to?

`optional`

to:`HorzScaleItem`

The to value. The end of the range.

#### Inherited from

`Partial.to`