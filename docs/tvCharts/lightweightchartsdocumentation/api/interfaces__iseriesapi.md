---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ISeriesApi
scraped_at: 2025-12-01T14:31:40.260598
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ISeriesApi

# Interface: ISeriesApi<TSeriesType, HorzScaleItem, TData, TOptions, TPartialOptions>

Represents the interface for interacting with series.

## Type parameters

• **TSeriesType** *extends* `SeriesType`

• **HorzScaleItem** = `Time`

• **TData** = `SeriesDataItemTypeMap`

<`HorzScaleItem`

>[`TSeriesType`

]

• **TOptions** = `SeriesOptionsMap`

[`TSeriesType`

]

• **TPartialOptions** = `SeriesPartialOptionsMap`

[`TSeriesType`

]

## Methods

### priceFormatter()

priceFormatter():`IPriceFormatter`

Returns current price formatter

#### Returns

Interface to the price formatter object that can be used to format prices in the same way as the chart does

### priceToCoordinate()

priceToCoordinate(`price`

):`Coordinate`

Converts specified series price to pixel coordinate according to the series price scale

#### Parameters

• **price**: `number`

Input price to be converted

#### Returns

Pixel coordinate of the price level on the chart

### coordinateToPrice()

coordinateToPrice(`coordinate`

):`BarPrice`

Converts specified coordinate to price value according to the series price scale

#### Parameters

• **coordinate**: `number`

Input coordinate to be converted

#### Returns

Price value of the coordinate on the chart

### barsInLogicalRange()

barsInLogicalRange(`range`

):`BarsInfo`

<`HorzScaleItem`

>

Returns bars information for the series in the provided logical range or `null`

, if no series data has been found in the requested range.
This method can be used, for instance, to implement downloading historical data while scrolling to prevent a user from seeing empty space.

#### Parameters

• **range**: `IRange`

<`number`

>

The logical range to retrieve info for.

#### Returns

`BarsInfo`

<`HorzScaleItem`

>

The bars info for the given logical range.

#### Examples

`const barsInfo = series.barsInLogicalRange(chart.timeScale().getVisibleLogicalRange());`

console.log(barsInfo);

`function onVisibleLogicalRangeChanged(newVisibleLogicalRange) {`

const barsInfo = series.barsInLogicalRange(newVisibleLogicalRange);

// if there less than 50 bars to the left of the visible area

if (barsInfo !== null && barsInfo.barsBefore < 50) {

// try to load additional historical data and prepend it to the series data

}

}

chart.timeScale().subscribeVisibleLogicalRangeChange(onVisibleLogicalRangeChanged);

### applyOptions()

applyOptions(`options`

):`void`

Applies new options to the existing series
You can set options initially when you create series or use the `applyOptions`

method of the series to change the existing options.
Note that you can only pass options you want to change.

#### Parameters

• **options**: `TPartialOptions`

Any subset of options.

#### Returns

`void`

### options()

options():`Readonly`

<`TOptions`

>

Returns currently applied options

#### Returns

`Readonly`

<`TOptions`

>

Full set of currently applied options, including defaults

### priceScale()

priceScale():`IPriceScaleApi`

Returns the API interface for controlling the price scale that this series is currently attached to.

#### Returns

IPriceScaleApi An interface for controlling the price scale (axis component) currently used by this series

#### Remarks

Important: The returned PriceScaleApi is bound to the specific price scale (by ID and pane) that the series is using at the time this method is called. If you later move the series to a different pane or attach it to a different price scale (e.g., from 'right' to 'left'), the previously returned PriceScaleApi will NOT follow the series. It will continue to control the original price scale it was created for.

To control the new price scale after moving a series, you must call this method again to get a fresh PriceScaleApi instance for the current price scale.

### setData()

setData(`data`

):`void`

Sets or replaces series data.

#### Parameters

• **data**: `TData`

[]

Ordered (earlier time point goes first) array of data items. Old data is fully replaced with the new one.

#### Returns

`void`

#### Examples

`lineSeries.setData([`

{ time: '2018-12-12', value: 24.11 },

{ time: '2018-12-13', value: 31.74 },

]);

`barSeries.setData([`

{ time: '2018-12-19', open: 141.77, high: 170.39, low: 120.25, close: 145.72 },

{ time: '2018-12-20', open: 145.72, high: 147.99, low: 100.11, close: 108.19 },

]);

### update()

update(`bar`

,`historicalUpdate`

?):`void`

Adds new data item to the existing set (or updates the latest item if times of the passed/latest items are equal).

#### Parameters

• **bar**: `TData`

A single data item to be added. Time of the new item must be greater or equal to the latest existing time point. If the new item's time is equal to the last existing item's time, then the existing item is replaced with the new one.

• **historicalUpdate?**: `boolean`

If true, allows updating an existing data point that is not the latest bar. Default is false.
Updating older data using `historicalUpdate`

will be slower than updating the most recent data point.

#### Returns

`void`

#### Examples

`lineSeries.update({`

time: '2018-12-12',

value: 24.11,

});

`barSeries.update({`

time: '2018-12-19',

open: 141.77,

high: 170.39,

low: 120.25,

close: 145.72,

});

### pop()

pop(`count`

):`TData`

[]

Removes one or more data items from the end of the series.

#### Parameters

• **count**: `number`

The number of data items to remove.

#### Returns

`TData`

[]

The removed data items.

#### Example

`const removedData = lineSeries.pop(1);`

console.log(removedData);

### dataByIndex()

dataByIndex(`logicalIndex`

,`mismatchDirection`

?):`TData`

Returns a bar data by provided logical index.

#### Parameters

• **logicalIndex**: `number`

Logical index

• **mismatchDirection?**: `MismatchDirection`

Search direction if no data found at provided logical index.

#### Returns

`TData`

Original data item provided via setData or update methods.

#### Example

`const originalData = series.dataByIndex(10, LightweightCharts.MismatchDirection.NearestLeft);`

### data()

data(): readonly`TData`

[]

Returns all the bar data for the series.

#### Returns

readonly `TData`

[]

Original data items provided via setData or update methods.

#### Example

`const originalData = series.data();`

### subscribeDataChanged()

subscribeDataChanged(`handler`

):`void`

Subscribe to the data changed event. This event is fired whenever the `update`

or `setData`

method is evoked
on the series.

#### Parameters

• **handler**: `DataChangedHandler`

Handler to be called on a data changed event.

#### Returns

`void`

#### Example

`function myHandler() {`

const data = series.data();

console.log(`The data has changed. New Data length: ${data.length}`);

}

series.subscribeDataChanged(myHandler);

### unsubscribeDataChanged()

unsubscribeDataChanged(`handler`

):`void`

Unsubscribe a handler that was previously subscribed using subscribeDataChanged.

#### Parameters

• **handler**: `DataChangedHandler`

Previously subscribed handler

#### Returns

`void`

#### Example

`chart.unsubscribeDataChanged(myHandler);`

### createPriceLine()

createPriceLine(`options`

):`IPriceLine`

Creates a new price line

#### Parameters

• **options**: `CreatePriceLineOptions`

Any subset of options, however `price`

is required.

#### Returns

#### Example

`const priceLine = series.createPriceLine({`

price: 80.0,

color: 'green',

lineWidth: 2,

lineStyle: LightweightCharts.LineStyle.Dotted,

axisLabelVisible: true,

title: 'P/L 500',

});

### removePriceLine()

removePriceLine(`line`

):`void`

Removes the price line that was created before.

#### Parameters

• **line**: `IPriceLine`

A line to remove.

#### Returns

`void`

#### Example

`const priceLine = series.createPriceLine({ price: 80.0 });`

series.removePriceLine(priceLine);

### priceLines()

priceLines():`IPriceLine`

[]

Returns an array of price lines.

#### Returns

### seriesType()

seriesType():`TSeriesType`

Return current series type.

#### Returns

`TSeriesType`

Type of the series.

#### Example

`const lineSeries = chart.addSeries(LineSeries);`

console.log(lineSeries.seriesType()); // "Line"

const candlestickSeries = chart.addCandlestickSeries();

console.log(candlestickSeries.seriesType()); // "Candlestick"

### lastValueData()

lastValueData(`globalLast`

):`LastValueDataResult`

Return the last value data of the series.

#### Parameters

• **globalLast**: `boolean`

If false, get the last value in the current visible range. Otherwise, fetch the absolute last value

#### Returns

The last value data of the series.

#### Example

`const lineSeries = chart.addSeries(LineSeries);`

console.log(lineSeries.lastValueData(true)); // { noData: false, price: 24.11, color: '#000000' }

const candlestickSeries = chart.addCandlestickSeries();

console.log(candlestickSeries.lastValueData(false)); // { noData: false, price: 145.72, color: '#000000' }

### attachPrimitive()

attachPrimitive(`primitive`

):`void`

Attaches additional drawing primitive to the series

#### Parameters

• **primitive**: `ISeriesPrimitive`

<`HorzScaleItem`

>

any implementation of ISeriesPrimitive interface

#### Returns

`void`

### detachPrimitive()

detachPrimitive(`primitive`

):`void`

Detaches additional drawing primitive from the series

#### Parameters

• **primitive**: `ISeriesPrimitive`

<`HorzScaleItem`

>

implementation of ISeriesPrimitive interface attached before Does nothing if specified primitive was not attached

#### Returns

`void`

### moveToPane()

moveToPane(`paneIndex`

):`void`

Move the series to another pane.

If the pane with the specified index does not exist, the pane will be created.

#### Parameters

• **paneIndex**: `number`

The index of the pane. Should be a number between 0 and the total number of panes.

#### Returns

`void`

### seriesOrder()

seriesOrder():`number`

Gets the zero-based index of this series within the list of all series on the current pane.

#### Returns

`number`

The current index of the series in the pane's series collection.

### setSeriesOrder()

setSeriesOrder(`order`

):`void`

Sets the zero-based index of this series within the pane's series collection, thereby adjusting its rendering order.

Note:

- The chart may automatically recalculate this index after operations such as removing other series or moving this series to a different pane.
- If the provided index is less than 0, equal to, or greater than the number of series, it will be clamped to a valid range.
- Price scales derive their formatters from the series with the lowest index; changing the order may affect the price scale's formatting

#### Parameters

• **order**: `number`

The desired zero-based index to set for this series within the pane.

#### Returns

`void`

### getPane()

getPane():`IPaneApi`

<`HorzScaleItem`

>

Returns the pane to which the series is currently attached.

#### Returns

`IPaneApi`

<`HorzScaleItem`

>

Pane API object to control the pane