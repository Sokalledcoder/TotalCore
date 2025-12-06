---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/MouseEventParams
scraped_at: 2025-12-01T14:31:40.910496
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/MouseEventParams

# Interface: MouseEventParams<HorzScaleItem>

Represents a mouse event.

## Type parameters

• **HorzScaleItem** = `Time`

## Properties

### time?

`optional`

time:`HorzScaleItem`

Time of the data at the location of the mouse event.

The value will be `undefined`

if the location of the event in the chart is outside the range of available data.

### logical?

`optional`

logical:`Logical`

Logical index

### point?

`optional`

point:`Point`

Location of the event in the chart.

The value will be `undefined`

if the event is fired outside the chart, for example a mouse leave event.

### paneIndex?

`optional`

paneIndex:`number`

The index of the Pane

### seriesData

seriesData:`Map`

<`ISeriesApi`

<keyof`SeriesOptionsMap`

,`HorzScaleItem`

,`AreaData`

<`HorzScaleItem`

> |`WhitespaceData`

<`HorzScaleItem`

> |`BarData`

<`HorzScaleItem`

> |`CandlestickData`

<`HorzScaleItem`

> |`BaselineData`

<`HorzScaleItem`

> |`LineData`

<`HorzScaleItem`

> |`HistogramData`

<`HorzScaleItem`

> |`CustomData`

<`HorzScaleItem`

> |`CustomSeriesWhitespaceData`

<`HorzScaleItem`

>,`CustomSeriesOptions`

|`AreaSeriesOptions`

|`BarSeriesOptions`

|`CandlestickSeriesOptions`

|`BaselineSeriesOptions`

|`LineSeriesOptions`

|`HistogramSeriesOptions`

,`DeepPartial`

<`AreaStyleOptions`

&`SeriesOptionsCommon`

> |`DeepPartial`

<`BarStyleOptions`

&`SeriesOptionsCommon`

> |`DeepPartial`

<`CandlestickStyleOptions`

&`SeriesOptionsCommon`

> |`DeepPartial`

<`BaselineStyleOptions`

&`SeriesOptionsCommon`

> |`DeepPartial`

<`LineStyleOptions`

&`SeriesOptionsCommon`

> |`DeepPartial`

<`HistogramStyleOptions`

&`SeriesOptionsCommon`

> |`DeepPartial`

<`CustomStyleOptions`

&`SeriesOptionsCommon`

>>,`BarData`

<`HorzScaleItem`

> |`LineData`

<`HorzScaleItem`

> |`HistogramData`

<`HorzScaleItem`

> |`CustomData`

<`HorzScaleItem`

>>

Data of all series at the location of the event in the chart.

Keys of the map are ISeriesApi instances. Values are prices. Values of the map are original data items

### hoveredSeries?

`optional`

hoveredSeries:`ISeriesApi`

<keyof`SeriesOptionsMap`

,`HorzScaleItem`

,`AreaData`

<`HorzScaleItem`

> |`WhitespaceData`

<`HorzScaleItem`

> |`BarData`

<`HorzScaleItem`

> |`CandlestickData`

<`HorzScaleItem`

> |`BaselineData`

<`HorzScaleItem`

> |`LineData`

<`HorzScaleItem`

> |`HistogramData`

<`HorzScaleItem`

> |`CustomData`

<`HorzScaleItem`

> |`CustomSeriesWhitespaceData`

<`HorzScaleItem`

>,`CustomSeriesOptions`

|`AreaSeriesOptions`

|`BarSeriesOptions`

|`CandlestickSeriesOptions`

|`BaselineSeriesOptions`

|`LineSeriesOptions`

|`HistogramSeriesOptions`

,`DeepPartial`

<`AreaStyleOptions`

&`SeriesOptionsCommon`

> |`DeepPartial`

<`BarStyleOptions`

&`SeriesOptionsCommon`

> |`DeepPartial`

<`CandlestickStyleOptions`

&`SeriesOptionsCommon`

> |`DeepPartial`

<`BaselineStyleOptions`

&`SeriesOptionsCommon`

> |`DeepPartial`

<`LineStyleOptions`

&`SeriesOptionsCommon`

> |`DeepPartial`

<`HistogramStyleOptions`

&`SeriesOptionsCommon`

> |`DeepPartial`

<`CustomStyleOptions`

&`SeriesOptionsCommon`

>>

The ISeriesApi for the series at the point of the mouse event.

### hoveredObjectId?

`optional`

hoveredObjectId:`unknown`

The ID of the object at the point of the mouse event.

### sourceEvent?

`optional`

sourceEvent:`TouchMouseEventData`

The underlying source mouse or touch event data, if available