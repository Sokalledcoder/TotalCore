---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ISeriesPrimitiveWrapper
scraped_at: 2025-12-01T14:31:40.666914
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ISeriesPrimitiveWrapper

# Interface: ISeriesPrimitiveWrapper<T, Options>

Interface for a series primitive.

## Extended by

## Type parameters

• **T**

• **Options** = `unknown`

## Properties

### detach()

detach: () =>`void`

Detaches the plugin from the series.

#### Returns

`void`

### getSeries()

getSeries: () =>`ISeriesApi`

<keyof`SeriesOptionsMap`

,`T`

,`AreaData`

<`T`

> |`WhitespaceData`

<`T`

> |`BarData`

<`T`

> |`CandlestickData`

<`T`

> |`BaselineData`

<`T`

> |`LineData`

<`T`

> |`HistogramData`

<`T`

> |`CustomData`

<`T`

> |`CustomSeriesWhitespaceData`

<`T`

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

### applyOptions()?

`optional`

applyOptions: (`options`

) =>`void`

Applies options to the primitive.

#### Parameters

• **options**: `DeepPartial`

<`Options`

>

Options to apply. The options are deeply merged with the current options.

#### Returns

`void`