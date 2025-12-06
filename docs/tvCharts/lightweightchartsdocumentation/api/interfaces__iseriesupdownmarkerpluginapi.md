---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ISeriesUpDownMarkerPluginApi
scraped_at: 2025-12-01T14:31:40.601541
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ISeriesUpDownMarkerPluginApi

# Interface: ISeriesUpDownMarkerPluginApi<HorzScaleItem, TData>

UpDownMarkersPrimitive Plugin for showing the direction of price changes on the chart. This plugin can only be used with Line and Area series types.

- Manual control:

- Use the
`setMarkers`

method to manually add markers to the chart. This will replace any existing markers. - Use
`clearMarkers`

to remove all markers.

- Automatic updates:

Use `setData`

and `update`

from this primitive instead of the those on the series to let the
primitive handle the creation of price change markers automatically.

- Use
`setData`

to initialize or replace all data points. - Use
`update`

to modify individual data points. This will automatically create markers for price changes on existing data points. - The
`updateVisibilityDuration`

option controls how long markers remain visible.

## Extends

`ISeriesPrimitiveWrapper`

<`HorzScaleItem`

>

## Type parameters

• **HorzScaleItem**

• **TData** *extends* `SeriesDataItemTypeMap`

<`HorzScaleItem`

>[`UpDownMarkersSupportedSeriesTypes`

] = `SeriesDataItemTypeMap`

<`HorzScaleItem`

>[`"Line"`

]

## Properties

### detach()

detach: () =>`void`

Detaches the plugin from the series.

#### Returns

`void`

#### Inherited from

`ISeriesPrimitiveWrapper`

. `detach`

### getSeries()

getSeries: () =>`ISeriesApi`

<keyof`SeriesOptionsMap`

,`HorzScaleItem`

,`WhitespaceData`

<`HorzScaleItem`

> |`LineData`

<`HorzScaleItem`

> |`AreaData`

<`HorzScaleItem`

> |`BarData`

<`HorzScaleItem`

> |`CandlestickData`

<`HorzScaleItem`

> |`BaselineData`

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

, `WhitespaceData`

<`HorzScaleItem`

> | `LineData`

<`HorzScaleItem`

> | `AreaData`

<`HorzScaleItem`

> | `BarData`

<`HorzScaleItem`

> | `CandlestickData`

<`HorzScaleItem`

> | `BaselineData`

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

### applyOptions()

applyOptions: (`options`

) =>`void`

Applies new options to the plugin.

#### Parameters

• **options**: `Partial`

<`UpDownMarkersPluginOptions`

>

Partial options to apply.

#### Returns

`void`

#### Overrides

`ISeriesPrimitiveWrapper`

. `applyOptions`

### setData()

setData: (`data`

) =>`void`

Sets the data for the series and manages data points for marker updates.

#### Parameters

• **data**: `TData`

[]

Array of data points to set.

#### Returns

`void`

### update()

update: (`data`

,`historicalUpdate`

?) =>`void`

Updates a single data point and manages marker updates for existing data points.

#### Parameters

• **data**: `TData`

The data point to update.

• **historicalUpdate?**: `boolean`

Optional flag for historical updates.

#### Returns

`void`

### markers()

markers: () => readonly`SeriesUpDownMarker`

<`HorzScaleItem`

>[]

Retrieves the current markers on the chart.

#### Returns

readonly `SeriesUpDownMarker`

<`HorzScaleItem`

>[]

### setMarkers()

setMarkers: (`markers`

) =>`void`

Manually sets markers on the chart.

#### Parameters

• **markers**: `SeriesUpDownMarker`

<`HorzScaleItem`

>[]

Array of SeriesUpDownMarker to set.

#### Returns

`void`

### clearMarkers()

clearMarkers: () =>`void`

Clears all markers from the chart.

#### Returns

`void`