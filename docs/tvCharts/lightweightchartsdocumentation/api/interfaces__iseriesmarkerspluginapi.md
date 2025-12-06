---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ISeriesMarkersPluginApi
scraped_at: 2025-12-01T14:31:40.290567
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ISeriesMarkersPluginApi

# Interface: ISeriesMarkersPluginApi<HorzScaleItem>

Interface for a series markers plugin

## Extends

`ISeriesPrimitiveWrapper`

<`HorzScaleItem`

>

## Type parameters

• **HorzScaleItem**

## Properties

### setMarkers()

setMarkers: (`markers`

) =>`void`

Set markers to the series.

#### Parameters

• **markers**: `SeriesMarker`

<`HorzScaleItem`

>[]

An array of markers to be displayed on the series.

#### Returns

`void`

### markers()

markers: () => readonly`SeriesMarker`

<`HorzScaleItem`

>[]

Returns current markers.

#### Returns

readonly `SeriesMarker`

<`HorzScaleItem`

>[]

### detach()

detach: () =>`void`

Detaches the plugin from the series.

#### Returns

`void`

#### Overrides

`ISeriesPrimitiveWrapper`

. `detach`

### getSeries()

getSeries: () =>`ISeriesApi`

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

Returns the current series.

#### Returns

`ISeriesApi`

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

#### Inherited from

`ISeriesPrimitiveWrapper`

. `getSeries`

### applyOptions()?

`optional`

applyOptions: (`options`

) =>`void`

Applies options to the primitive.

#### Parameters

• **options**: `DeepPartial`

<`unknown`

>

Options to apply. The options are deeply merged with the current options.

#### Returns

`void`