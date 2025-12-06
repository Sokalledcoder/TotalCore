---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/SeriesAttachedParameter
scraped_at: 2025-12-01T14:31:41.502043
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/SeriesAttachedParameter

# Interface: SeriesAttachedParameter<HorzScaleItem, TSeriesType>

Object containing references to the chart and series instances, and a requestUpdate method for triggering a refresh of the chart.

## Type parameters

• **HorzScaleItem** = `Time`

• **TSeriesType** *extends* `SeriesType`

= keyof `SeriesOptionsMap`

## Properties

### chart

chart:`IChartApiBase`

<`HorzScaleItem`

>

Chart instance.

### series

series:`ISeriesApi`

<`TSeriesType`

,`HorzScaleItem`

,`SeriesDataItemTypeMap`

<`HorzScaleItem`

>[`TSeriesType`

],`SeriesOptionsMap`

[`TSeriesType`

],`SeriesPartialOptionsMap`

[`TSeriesType`

]>

Series to which the Primitive is attached.

### requestUpdate()

requestUpdate: () =>`void`

Request an update (redraw the chart)

#### Returns

`void`

### horzScaleBehavior

horzScaleBehavior:`IHorzScaleBehavior`

<`HorzScaleItem`

>

Horizontal Scale Behaviour for the chart.