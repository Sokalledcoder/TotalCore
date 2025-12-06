---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/PaneAttachedParameter
scraped_at: 2025-12-01T14:31:40.928866
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/PaneAttachedParameter

# Interface: PaneAttachedParameter<HorzScaleItem>

Object containing references to the chart instance, and a requestUpdate method for triggering a refresh of the chart.

## Type parameters

• **HorzScaleItem** = `Time`

## Properties

### chart

chart:`IChartApiBase`

<`HorzScaleItem`

>

Chart instance.

### requestUpdate()

requestUpdate: () =>`void`

Request an update (redraw the chart)

#### Returns

`void`