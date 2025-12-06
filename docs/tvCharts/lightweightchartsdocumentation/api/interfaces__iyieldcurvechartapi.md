---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/IYieldCurveChartApi
scraped_at: 2025-12-01T14:31:40.569037
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/IYieldCurveChartApi

# Interface: IYieldCurveChartApi

The main interface of a single yield curve chart.

## Extends

`Omit`

<`IChartApiBase`

<`number`

>,`"addSeries"`

>

## Methods

### remove()

remove():`void`

Removes the chart object including all DOM elements. This is an irreversible operation, you cannot do anything with the chart after removing it.

#### Returns

`void`

#### Inherited from

`Omit.remove`

### resize()

resize(`width`

,`height`

,`forceRepaint`

?):`void`

Sets fixed size of the chart. By default chart takes up 100% of its container.

If chart has the `autoSize`

option enabled, and the ResizeObserver is available then
the width and height values will be ignored.

#### Parameters

• **width**: `number`

Target width of the chart.

• **height**: `number`

Target height of the chart.

• **forceRepaint?**: `boolean`

True to initiate resize immediately. One could need this to get screenshot immediately after resize.

#### Returns

`void`

#### Inherited from

`Omit.resize`

### addCustomSeries()

addCustomSeries<`TData`

,`TOptions`

,`TPartialOptions`

>(`customPaneView`

,`customOptions`

?,`paneIndex`

?):`ISeriesApi`

<`"Custom"`

,`number`

,`WhitespaceData`

<`number`

> |`TData`

,`TOptions`

,`TPartialOptions`

>

Creates a custom series with specified parameters.

A custom series is a generic series which can be extended with a custom renderer to implement chart types which the library doesn't support by default.

#### Type parameters

• **TData** *extends* `CustomData`

<`number`

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

<`number`

, `TData`

, `TOptions`

>

A custom series pane view which implements the custom renderer.

• **customOptions?**: `DeepPartial`

<`TOptions`

& `SeriesOptionsCommon`

>

Customization parameters of the series being created.

`const series = chart.addCustomSeries(myCustomPaneView);`

• **paneIndex?**: `number`

#### Returns

`ISeriesApi`

<`"Custom"`

, `number`

, `WhitespaceData`

<`number`

> | `TData`

, `TOptions`

, `TPartialOptions`

>

#### Inherited from

`Omit.addCustomSeries`

### removeSeries()

removeSeries(`seriesApi`

):`void`

Removes a series of any type. This is an irreversible operation, you cannot do anything with the series after removing it.

#### Parameters

• **seriesApi**: `ISeriesApi`

<keyof `SeriesOptionsMap`

, `number`

, `WhitespaceData`

<`number`

> | `LineData`

<`number`

> | `CustomData`

<`number`

> | `AreaData`

<`number`

> | `BarData`

<`number`

> | `CandlestickData`

<`number`

> | `BaselineData`

<`number`

> | `HistogramData`

<`number`

> | `CustomSeriesWhitespaceData`

<`number`

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

#### Returns

`void`

#### Inherited from

`Omit.removeSeries`

#### Example

`chart.removeSeries(series);`

### subscribeClick()

subscribeClick(`handler`

):`void`

Subscribe to the chart click event.

#### Parameters

• **handler**: `MouseEventHandler`

<`number`

>

Handler to be called on mouse click.

#### Returns

`void`

#### Inherited from

`Omit.subscribeClick`

#### Example

`function myClickHandler(param) {`

if (!param.point) {

return;

}

console.log(`Click at ${param.point.x}, ${param.point.y}. The time is ${param.time}.`);

}

chart.subscribeClick(myClickHandler);

### unsubscribeClick()

unsubscribeClick(`handler`

):`void`

Unsubscribe a handler that was previously subscribed using subscribeClick.

#### Parameters

• **handler**: `MouseEventHandler`

<`number`

>

Previously subscribed handler

#### Returns

`void`

#### Inherited from

`Omit.unsubscribeClick`

#### Example

`chart.unsubscribeClick(myClickHandler);`

### subscribeDblClick()

subscribeDblClick(`handler`

):`void`

Subscribe to the chart double-click event.

#### Parameters

• **handler**: `MouseEventHandler`

<`number`

>

Handler to be called on mouse double-click.

#### Returns

`void`

#### Inherited from

`Omit.subscribeDblClick`

#### Example

`function myDblClickHandler(param) {`

if (!param.point) {

return;

}

console.log(`Double Click at ${param.point.x}, ${param.point.y}. The time is ${param.time}.`);

}

chart.subscribeDblClick(myDblClickHandler);

### unsubscribeDblClick()

unsubscribeDblClick(`handler`

):`void`

Unsubscribe a handler that was previously subscribed using subscribeDblClick.

#### Parameters

• **handler**: `MouseEventHandler`

<`number`

>

Previously subscribed handler

#### Returns

`void`

#### Inherited from

`Omit.unsubscribeDblClick`

#### Example

`chart.unsubscribeDblClick(myDblClickHandler);`

### subscribeCrosshairMove()

subscribeCrosshairMove(`handler`

):`void`

Subscribe to the crosshair move event.

#### Parameters

• **handler**: `MouseEventHandler`

<`number`

>

Handler to be called on crosshair move.

#### Returns

`void`

#### Inherited from

`Omit.subscribeCrosshairMove`

#### Example

`function myCrosshairMoveHandler(param) {`

if (!param.point) {

return;

}

console.log(`Crosshair moved to ${param.point.x}, ${param.point.y}. The time is ${param.time}.`);

}

chart.subscribeCrosshairMove(myCrosshairMoveHandler);

### unsubscribeCrosshairMove()

unsubscribeCrosshairMove(`handler`

):`void`

Unsubscribe a handler that was previously subscribed using subscribeCrosshairMove.

#### Parameters

• **handler**: `MouseEventHandler`

<`number`

>

Previously subscribed handler

#### Returns

`void`

#### Inherited from

`Omit.unsubscribeCrosshairMove`

#### Example

`chart.unsubscribeCrosshairMove(myCrosshairMoveHandler);`

### priceScale()

priceScale(`priceScaleId`

,`paneIndex`

?):`IPriceScaleApi`

Returns API to manipulate a price scale.

#### Parameters

• **priceScaleId**: `string`

ID of the price scale.

• **paneIndex?**: `number`

Index of the pane (default: 0)

#### Returns

Price scale API.

#### Inherited from

`Omit.priceScale`

### timeScale()

timeScale():`ITimeScaleApi`

<`number`

>

Returns API to manipulate the time scale

#### Returns

`ITimeScaleApi`

<`number`

>

Target API

#### Inherited from

`Omit.timeScale`

### applyOptions()

applyOptions(`options`

):`void`

Applies new options to the chart

#### Parameters

• **options**: `DeepPartial`

<`ChartOptionsImpl`

<`number`

>>

Any subset of options.

#### Returns

`void`

#### Inherited from

`Omit.applyOptions`

### options()

options():`Readonly`

<`ChartOptionsImpl`

<`number`

>>

Returns currently applied options

#### Returns

`Readonly`

<`ChartOptionsImpl`

<`number`

>>

Full set of currently applied options, including defaults

#### Inherited from

`Omit.options`

### takeScreenshot()

takeScreenshot(`addTopLayer`

?,`includeCrosshair`

?):`HTMLCanvasElement`

Make a screenshot of the chart with all the elements excluding crosshair.

#### Parameters

• **addTopLayer?**: `boolean`

if true, the top layer and primitives will be included in the screenshot (default: false)

• **includeCrosshair?**: `boolean`

works only if addTopLayer is enabled. If true, the crosshair will be included in the screenshot (default: false)

#### Returns

`HTMLCanvasElement`

A canvas with the chart drawn on. Any `Canvas`

methods like `toDataURL()`

or `toBlob()`

can be used to serialize the result.

#### Inherited from

`Omit.takeScreenshot`

### addPane()

addPane(`preserveEmptyPane`

?):`IPaneApi`

<`number`

>

Add a pane to the chart

#### Parameters

• **preserveEmptyPane?**: `boolean`

Whether to preserve the empty pane

#### Returns

`IPaneApi`

<`number`

>

The pane API

#### Inherited from

`Omit.addPane`

### panes()

panes():`IPaneApi`

<`number`

>[]

Returns array of panes' API

#### Returns

`IPaneApi`

<`number`

>[]

array of pane's Api

#### Inherited from

`Omit.panes`

### removePane()

removePane(`index`

):`void`

Removes a pane with index

#### Parameters

• **index**: `number`

the pane to be removed

#### Returns

`void`

#### Inherited from

`Omit.removePane`

### swapPanes()

swapPanes(`first`

,`second`

):`void`

swap the position of two panes.

#### Parameters

• **first**: `number`

the first index

• **second**: `number`

the second index

#### Returns

`void`

#### Inherited from

`Omit.swapPanes`

### autoSizeActive()

autoSizeActive():`boolean`

Returns the active state of the `autoSize`

option. This can be used to check
whether the chart is handling resizing automatically with a `ResizeObserver`

.

#### Returns

`boolean`

Whether the `autoSize`

option is enabled and the active.

#### Inherited from

`Omit.autoSizeActive`

### chartElement()

chartElement():`HTMLDivElement`

Returns the generated div element containing the chart. This can be used for adding your own additional event listeners, or for measuring the elements dimensions and position within the document.

#### Returns

`HTMLDivElement`

generated div element containing the chart.

#### Inherited from

`Omit.chartElement`

### setCrosshairPosition()

setCrosshairPosition(`price`

,`horizontalPosition`

,`seriesApi`

):`void`

Set the crosshair position within the chart.

Usually the crosshair position is set automatically by the user's actions. However in some cases you may want to set it explicitly.

For example if you want to synchronise the crosshairs of two separate charts.

#### Parameters

• **price**: `number`

The price (vertical coordinate) of the new crosshair position.

• **horizontalPosition**: `number`

The horizontal coordinate (time by default) of the new crosshair position.

• **seriesApi**: `ISeriesApi`

<keyof `SeriesOptionsMap`

, `number`

, `WhitespaceData`

<`number`

> | `LineData`

<`number`

> | `CustomData`

<`number`

> | `AreaData`

<`number`

> | `BarData`

<`number`

> | `CandlestickData`

<`number`

> | `BaselineData`

<`number`

> | `HistogramData`

<`number`

> | `CustomSeriesWhitespaceData`

<`number`

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

#### Returns

`void`

#### Inherited from

`Omit.setCrosshairPosition`

### clearCrosshairPosition()

clearCrosshairPosition():`void`

Clear the crosshair position within the chart.

#### Returns

`void`

#### Inherited from

`Omit.clearCrosshairPosition`

### paneSize()

paneSize(`paneIndex`

?):`PaneSize`

Returns the dimensions of the chart pane (the plot surface which excludes time and price scales). This would typically only be useful for plugin development.

#### Parameters

• **paneIndex?**: `number`

The index of the pane

#### Returns

Dimensions of the chart pane

#### Inherited from

`Omit.paneSize`

#### Default Value

`0`

### horzBehaviour()

horzBehaviour():`IHorzScaleBehavior`

<`number`

>

Returns the horizontal scale behaviour.

#### Returns

`IHorzScaleBehavior`

<`number`

>

#### Inherited from

`Omit.horzBehaviour`

### addSeries()

addSeries<`T`

>(`definition`

,`options`

?,`paneIndex`

?):`ISeriesApi`

<`T`

,`number`

,`WhitespaceData`

<`number`

> |`LineData`

<`number`

>,`SeriesOptionsMap`

[`T`

],`SeriesPartialOptionsMap`

[`T`

]>

Creates a series with specified parameters.

Note that the Yield Curve chart only supports the Area and Line series types.

#### Type parameters

• **T** *extends* `YieldCurveSeriesType`

#### Parameters

• **definition**: `SeriesDefinition`

<`T`

>

A series definition for either AreaSeries or LineSeries.

• **options?**: `SeriesPartialOptionsMap`

[`T`

]

Customization parameters of the series being created.

• **paneIndex?**: `number`

An index of the pane where the series should be created.

`const series = chart.addSeries(LineSeries, { lineWidth: 2 });`

#### Returns

`ISeriesApi`

<`T`

, `number`

, `WhitespaceData`

<`number`

> | `LineData`

<`number`

>, `SeriesOptionsMap`

[`T`

], `SeriesPartialOptionsMap`

[`T`

]>