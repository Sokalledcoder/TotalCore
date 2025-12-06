---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ICustomSeriesPaneView
scraped_at: 2025-12-01T14:31:39.748848
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ICustomSeriesPaneView

# Interface: ICustomSeriesPaneView<HorzScaleItem, TData, TSeriesOptions>

This interface represents the view for the custom series

## Type parameters

• **HorzScaleItem** = `Time`

• **TData** *extends* `CustomData`

<`HorzScaleItem`

> = `CustomData`

<`HorzScaleItem`

>

• **TSeriesOptions** *extends* `CustomSeriesOptions`

= `CustomSeriesOptions`

## Methods

### renderer()

renderer():`ICustomSeriesPaneRenderer`

This method returns a renderer - special object to draw data for the series on the main chart pane.

#### Returns

an renderer object to be used for drawing.

### update()

update(`data`

,`seriesOptions`

):`void`

This method will be called with the latest data for the renderer to use during the next paint.

#### Parameters

• **data**: `PaneRendererCustomData`

<`HorzScaleItem`

, `TData`

>

• **seriesOptions**: `TSeriesOptions`

#### Returns

`void`

### priceValueBuilder()

priceValueBuilder(`plotRow`

):`CustomSeriesPricePlotValues`

A function for interpreting the custom series data and returning an array of numbers representing the price values for the item. These price values are used by the chart to determine the auto-scaling (to ensure the items are in view) and the crosshair and price line positions. The last value in the array will be used as the current value. You shouldn't need to have more than 3 values in this array since the library only needs a largest, smallest, and current value.

#### Parameters

• **plotRow**: `TData`

#### Returns

### isWhitespace()

isWhitespace(`data`

):`data is CustomSeriesWhitespaceData<HorzScaleItem>`

A function for testing whether a data point should be considered fully specified, or if it should
be considered as whitespace. Should return `true`

if is whitespace.

#### Parameters

• **data**: `TData`

| `CustomSeriesWhitespaceData`

<`HorzScaleItem`

>

data point to be tested

#### Returns

`data is CustomSeriesWhitespaceData<HorzScaleItem>`

### defaultOptions()

defaultOptions():`TSeriesOptions`

Default options

#### Returns

`TSeriesOptions`

### destroy()?

`optional`

destroy():`void`

This method will be evoked when the series has been removed from the chart. This method should be used to clean up any objects, references, and other items that could potentially cause memory leaks.

This method should contain all the necessary code to clean up the object before it is removed from memory. This includes removing any event listeners or timers that are attached to the object, removing any references to other objects, and resetting any values or properties that were modified during the lifetime of the object.

#### Returns

`void`