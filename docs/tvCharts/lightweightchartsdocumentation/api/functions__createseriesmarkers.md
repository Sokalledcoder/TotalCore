---
source: https://tradingview.github.io/lightweight-charts/docs/api/functions/createSeriesMarkers
scraped_at: 2025-12-01T14:31:38.217389
---

# https://tradingview.github.io/lightweight-charts/docs/api/functions/createSeriesMarkers

# Function: createSeriesMarkers()

createSeriesMarkers<`HorzScaleItem`

>(`series`

,`markers`

?,`options`

?):`ISeriesMarkersPluginApi`

<`HorzScaleItem`

>

A function to create a series markers primitive.

## Type parameters

• **HorzScaleItem**

## Parameters

• **series**: `ISeriesApi`

<keyof `SeriesOptionsMap`

, `HorzScaleItem`

, `AreaData`

<`HorzScaleItem`

> | `WhitespaceData`

<`HorzScaleItem`

> | `BarData`

<`HorzScaleItem`

> | `CandlestickData`

<`HorzScaleItem`

> | `BaselineData`

<`HorzScaleItem`

> | `LineData`

<`HorzScaleItem`

> | `HistogramData`

<`HorzScaleItem`

> | `CustomData`

<`HorzScaleItem`

> | `CustomSeriesWhitespaceData`

<`HorzScaleItem`

>, `CustomSeriesOptions`

| `AreaSeriesOptions`

| `BarSeriesOptions`

| `CandlestickSeriesOptions`

| `BaselineSeriesOptions`

| `LineSeriesOptions`

| `HistogramSeriesOptions`

, `DeepPartial`

<`AreaStyleOptions`

& `SeriesOptionsCommon`

> | `DeepPartial`

<`BarStyleOptions`

& `SeriesOptionsCommon`

> | `DeepPartial`

<`CandlestickStyleOptions`

& `SeriesOptionsCommon`

> | `DeepPartial`

<`BaselineStyleOptions`

& `SeriesOptionsCommon`

> | `DeepPartial`

<`LineStyleOptions`

& `SeriesOptionsCommon`

> | `DeepPartial`

<`HistogramStyleOptions`

& `SeriesOptionsCommon`

> | `DeepPartial`

<`CustomStyleOptions`

& `SeriesOptionsCommon`

>>

The series to which the primitive will be attached.

• **markers?**: `SeriesMarker`

<`HorzScaleItem`

>[]

An array of markers to be displayed on the series.

• **options?**: `DeepPartial`

<`SeriesMarkersOptions`

>

Options for the series markers plugin.

## Returns

`ISeriesMarkersPluginApi`

<`HorzScaleItem`

>

## Example

`import { createSeriesMarkers } from 'lightweight-charts';`

const seriesMarkers = createSeriesMarkers(

series,

[

{

color: 'green',

position: 'inBar',

shape: 'arrowDown',

time: 1556880900,

},

]

);

// and then you can modify the markers

// set it to empty array to remove all markers

seriesMarkers.setMarkers([]);

// `seriesMarkers.markers()` returns current markers