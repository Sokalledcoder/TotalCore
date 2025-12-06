---
source: https://tradingview.github.io/lightweight-charts/docs/api/functions/createUpDownMarkers
scraped_at: 2025-12-01T14:31:38.342968
---

# https://tradingview.github.io/lightweight-charts/docs/api/functions/createUpDownMarkers

# Function: createUpDownMarkers()

createUpDownMarkers<`T`

>(`series`

,`options`

?):`ISeriesUpDownMarkerPluginApi`

<`T`

>

Creates and attaches the Series Up Down Markers Plugin.

## Type parameters

• **T**

## Parameters

• **series**: `ISeriesApi`

<keyof `SeriesOptionsMap`

, `T`

, `AreaData`

<`T`

> | `WhitespaceData`

<`T`

> | `BarData`

<`T`

> | `CandlestickData`

<`T`

> | `BaselineData`

<`T`

> | `LineData`

<`T`

> | `HistogramData`

<`T`

> | `CustomData`

<`T`

> | `CustomSeriesWhitespaceData`

<`T`

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

Series to which attach the Up Down Markers Plugin

• **options?**: `Partial`

<`UpDownMarkersPluginOptions`

>

options for the Up Down Markers Plugin

## Returns

`ISeriesUpDownMarkerPluginApi`

<`T`

>

Api for Series Up Down Marker Plugin. ISeriesUpDownMarkerPluginApi

## Example

`import { createUpDownMarkers, createChart, LineSeries } from 'lightweight-charts';`

const chart = createChart('container');

const lineSeries = chart.addSeries(LineSeries);

const upDownMarkers = createUpDownMarkers(lineSeries, {

positiveColor: '#22AB94',

negativeColor: '#F7525F',

updateVisibilityDuration: 5000,

});

// to add some data

upDownMarkers.setData(

[

{ time: '2020-02-02', value: 12.34 },

//... more line series data

]

);

// ... Update some values

upDownMarkers.update({ time: '2020-02-02', value: 13.54 }, true);

// to remove plugin from the series

upDownMarkers.detach();