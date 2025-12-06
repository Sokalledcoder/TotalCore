---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/IPaneApi
scraped_at: 2025-12-01T14:31:39.879703
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/IPaneApi

# Interface: IPaneApi<HorzScaleItem>

Represents the interface for interacting with a pane in a lightweight chart.

## Type parameters

• **HorzScaleItem**

## Methods

### getHeight()

getHeight():`number`

Retrieves the height of the pane in pixels.

#### Returns

`number`

The height of the pane in pixels.

### setHeight()

setHeight(`height`

):`void`

Sets the height of the pane.

#### Parameters

• **height**: `number`

The number of pixels to set as the height of the pane.

#### Returns

`void`

### moveTo()

moveTo(`paneIndex`

):`void`

Moves the pane to a new position.

#### Parameters

• **paneIndex**: `number`

The target index of the pane. Should be a number between 0 and the total number of panes - 1.

#### Returns

`void`

### paneIndex()

paneIndex():`number`

Retrieves the index of the pane.

#### Returns

`number`

The index of the pane. It is a number between 0 and the total number of panes - 1.

### getSeries()

getSeries():`ISeriesApi`

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

>>[]

Retrieves the array of series for the current pane.

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

>>[]

An array of series.

### getHTMLElement()

getHTMLElement():`HTMLElement`

Retrieves the HTML element of the pane.

#### Returns

`HTMLElement`

The HTML element of the pane or null if pane wasn't created yet.

### attachPrimitive()

attachPrimitive(`primitive`

):`void`

Attaches additional drawing primitive to the pane

#### Parameters

• **primitive**: `IPanePrimitive`

<`HorzScaleItem`

>

any implementation of IPanePrimitive interface

#### Returns

`void`

### detachPrimitive()

detachPrimitive(`primitive`

):`void`

Detaches additional drawing primitive from the pane

#### Parameters

• **primitive**: `IPanePrimitive`

<`HorzScaleItem`

>

implementation of IPanePrimitive interface attached before Does nothing if specified primitive was not attached

#### Returns

`void`

### priceScale()

priceScale(`priceScaleId`

):`IPriceScaleApi`

Returns the price scale with the given id.

#### Parameters

• **priceScaleId**: `string`

ID of the price scale to find

#### Returns

#### Throws

If the price scale with the given id is not found in this pane

### setPreserveEmptyPane()

setPreserveEmptyPane(`preserve`

):`void`

Sets whether to preserve the empty pane

#### Parameters

• **preserve**: `boolean`

Whether to preserve the empty pane

#### Returns

`void`

### preserveEmptyPane()

preserveEmptyPane():`boolean`

Returns whether to preserve the empty pane

#### Returns

`boolean`

Whether to preserve the empty pane

### getStretchFactor()

getStretchFactor():`number`

Returns the stretch factor of the pane. Stretch factor determines the relative size of the pane compared to other panes.

#### Returns

`number`

The stretch factor of the pane. Default is 1

### setStretchFactor()

setStretchFactor(`stretchFactor`

):`void`

Sets the stretch factor of the pane. When you creating a pane, the stretch factor is 1 by default. So if you have three panes, and you want to make the first pane twice as big as the second and third panes, you can set the stretch factor of the first pane to 2000. Example:

`const pane1 = chart.addPane();`

const pane2 = chart.addPane();

const pane3 = chart.addPane();

pane1.setStretchFactor(0.2);

pane2.setStretchFactor(0.3);

pane3.setStretchFactor(0.5);

// Now the first pane will be 20% of the total height, the second pane will be 30% of the total height, and the third pane will be 50% of the total height.

// Note: if you have one pane with default stretch factor of 1 and set other pane's stretch factor to 50,

// library will try to make second pane 50 times smaller than the first pane

#### Parameters

• **stretchFactor**: `number`

The stretch factor of the pane.

#### Returns

`void`

### addCustomSeries()

addCustomSeries<`TData`

,`TOptions`

,`TPartialOptions`

>(`customPaneView`

,`customOptions`

?):`ISeriesApi`

<`"Custom"`

,`HorzScaleItem`

,`WhitespaceData`

<`HorzScaleItem`

> |`TData`

,`TOptions`

,`TPartialOptions`

>

Creates a custom series with specified parameters.

A custom series is a generic series which can be extended with a custom renderer to implement chart types which the library doesn't support by default.

#### Type parameters

• **TData** *extends* `CustomData`

<`HorzScaleItem`

>

• **TOptions** *extends* `CustomSeriesOptions`

• **TPartialOptions** *extends* `DeepPartial`

<`TOptions`

& `SeriesOptionsCommon`

> = `DeepPartial`

<`TOptions`

& `SeriesOptionsCommon`

>

#### Parameters

• **customPaneView**: `ICustomSeriesPaneView`

<`HorzScaleItem`

, `TData`

, `TOptions`

>

A custom series pane view which implements the custom renderer.

• **customOptions?**: `DeepPartial`

<`TOptions`

& `SeriesOptionsCommon`

>

Customization parameters of the series being created.

`const series = pane.addCustomSeries(myCustomPaneView);`

#### Returns

`ISeriesApi`

<`"Custom"`

, `HorzScaleItem`

, `WhitespaceData`

<`HorzScaleItem`

> | `TData`

, `TOptions`

, `TPartialOptions`

>

### addSeries()

addSeries<`T`

>(`definition`

,`options`

?):`ISeriesApi`

<`T`

,`HorzScaleItem`

,`SeriesDataItemTypeMap`

<`HorzScaleItem`

>[`T`

],`SeriesOptionsMap`

[`T`

],`SeriesPartialOptionsMap`

[`T`

]>

Creates a series with specified parameters.

#### Type parameters

• **T** *extends* keyof `SeriesOptionsMap`

#### Parameters

• **definition**: `SeriesDefinition`

<`T`

>

A series definition.

• **options?**: `SeriesPartialOptionsMap`

[`T`

]

Customization parameters of the series being created.

`const series = pane.addSeries(LineSeries, { lineWidth: 2 });`

#### Returns

`ISeriesApi`

<`T`

, `HorzScaleItem`

, `SeriesDataItemTypeMap`

<`HorzScaleItem`

>[`T`

], `SeriesOptionsMap`

[`T`

], `SeriesPartialOptionsMap`

[`T`

]>