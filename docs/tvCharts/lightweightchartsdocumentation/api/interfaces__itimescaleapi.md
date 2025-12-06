---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ITimeScaleApi
scraped_at: 2025-12-01T14:31:40.444313
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ITimeScaleApi

# Interface: ITimeScaleApi<HorzScaleItem>

Interface to chart time scale

## Type parameters

• **HorzScaleItem**

## Methods

### scrollPosition()

scrollPosition():`number`

Return the distance from the right edge of the time scale to the lastest bar of the series measured in bars.

#### Returns

`number`

### scrollToPosition()

scrollToPosition(`position`

,`animated`

):`void`

Scrolls the chart to the specified position.

#### Parameters

• **position**: `number`

Target data position

• **animated**: `boolean`

Setting this to true makes the chart scrolling smooth and adds animation

#### Returns

`void`

### scrollToRealTime()

scrollToRealTime():`void`

Restores default scroll position of the chart. This process is always animated.

#### Returns

`void`

### getVisibleRange()

getVisibleRange():`IRange`

<`HorzScaleItem`

>

Returns current visible time range of the chart.

Note that this method cannot extrapolate time and will use the only currently existent data. To get complete information about current visible range, please use getVisibleLogicalRange and ISeriesApi.barsInLogicalRange.

#### Returns

`IRange`

<`HorzScaleItem`

>

Visible range or null if the chart has no data at all.

### setVisibleRange()

setVisibleRange(`range`

):`void`

Sets visible range of data.

Note that this method cannot extrapolate time and will use the only currently existent data.
Thus, for example, if currently a chart doesn't have data prior `2018-01-01`

date and you set visible range with `from`

date `2016-01-01`

, it will be automatically adjusted to `2018-01-01`

(and the same for `to`

date).

But if you can approximate indexes on your own - you could use setVisibleLogicalRange instead.

#### Parameters

• **range**: `IRange`

<`HorzScaleItem`

>

Target visible range of data.

#### Returns

`void`

#### Example

`chart.timeScale().setVisibleRange({`

from: (new Date(Date.UTC(2018, 0, 1, 0, 0, 0, 0))).getTime() / 1000,

to: (new Date(Date.UTC(2018, 1, 1, 0, 0, 0, 0))).getTime() / 1000,

});

### getVisibleLogicalRange()

getVisibleLogicalRange():`LogicalRange`

Returns the current visible logical range of the chart as an object with the first and last time points of the logical range, or returns `null`

if the chart has no data.

#### Returns

Visible range or null if the chart has no data at all.

### setVisibleLogicalRange()

setVisibleLogicalRange(`range`

):`void`

Sets visible logical range of data.

#### Parameters

• **range**: `IRange`

<`number`

>

Target visible logical range of data.

#### Returns

`void`

#### Example

`chart.timeScale().setVisibleLogicalRange({ from: 0, to: 10 });`

### resetTimeScale()

resetTimeScale():`void`

Restores default zoom level and scroll position of the time scale.

#### Returns

`void`

### fitContent()

fitContent():`void`

Automatically calculates the visible range to fit all data from all series.

#### Returns

`void`

### logicalToCoordinate()

logicalToCoordinate(`logical`

):`Coordinate`

Converts a logical index to local x coordinate.

#### Parameters

• **logical**: `Logical`

Logical index needs to be converted

#### Returns

x coordinate of that time or `null`

if the chart doesn't have data

### coordinateToLogical()

coordinateToLogical(`x`

):`Logical`

Converts a coordinate to logical index.

#### Parameters

• **x**: `number`

Coordinate needs to be converted

#### Returns

Logical index that is located on that coordinate or `null`

if the chart doesn't have data

### timeToIndex()

timeToIndex(`time`

,`findNearest`

?):`TimePointIndex`

Converts a time to local x coordinate.

#### Parameters

• **time**: `HorzScaleItem`

Time needs to be converted

• **findNearest?**: `boolean`

#### Returns

X coordinate of that time or `null`

if no time found on time scale

### timeToCoordinate()

timeToCoordinate(`time`

):`Coordinate`

Converts a time to local x coordinate.

#### Parameters

• **time**: `HorzScaleItem`

Time needs to be converted

#### Returns

X coordinate of that time or `null`

if no time found on time scale

### coordinateToTime()

coordinateToTime(`x`

):`HorzScaleItem`

Converts a coordinate to time.

#### Parameters

• **x**: `number`

Coordinate needs to be converted.

#### Returns

`HorzScaleItem`

Time of a bar that is located on that coordinate or `null`

if there are no bars found on that coordinate.

### width()

width():`number`

Returns a width of the time scale.

#### Returns

`number`

### height()

height():`number`

Returns a height of the time scale.

#### Returns

`number`

### subscribeVisibleTimeRangeChange()

subscribeVisibleTimeRangeChange(`handler`

):`void`

Subscribe to the visible time range change events.

The argument passed to the handler function is an object with `from`

and `to`

properties of type Time, or `null`

if there is no visible data.

#### Parameters

• **handler**: `TimeRangeChangeEventHandler`

<`HorzScaleItem`

>

Handler (function) to be called when the visible indexes change.

#### Returns

`void`

#### Example

`function myVisibleTimeRangeChangeHandler(newVisibleTimeRange) {`

if (newVisibleTimeRange === null) {

// handle null

}

// handle new logical range

}

chart.timeScale().subscribeVisibleTimeRangeChange(myVisibleTimeRangeChangeHandler);

### unsubscribeVisibleTimeRangeChange()

unsubscribeVisibleTimeRangeChange(`handler`

):`void`

Unsubscribe a handler that was previously subscribed using subscribeVisibleTimeRangeChange.

#### Parameters

• **handler**: `TimeRangeChangeEventHandler`

<`HorzScaleItem`

>

Previously subscribed handler

#### Returns

`void`

#### Example

`chart.timeScale().unsubscribeVisibleTimeRangeChange(myVisibleTimeRangeChangeHandler);`

### subscribeVisibleLogicalRangeChange()

subscribeVisibleLogicalRangeChange(`handler`

):`void`

Subscribe to the visible logical range change events.

The argument passed to the handler function is an object with `from`

and `to`

properties of type `number`

, or `null`

if there is no visible data.

#### Parameters

• **handler**: `LogicalRangeChangeEventHandler`

Handler (function) to be called when the visible indexes change.

#### Returns

`void`

#### Example

`function myVisibleLogicalRangeChangeHandler(newVisibleLogicalRange) {`

if (newVisibleLogicalRange === null) {

// handle null

}

// handle new logical range

}

chart.timeScale().subscribeVisibleLogicalRangeChange(myVisibleLogicalRangeChangeHandler);

### unsubscribeVisibleLogicalRangeChange()

unsubscribeVisibleLogicalRangeChange(`handler`

):`void`

Unsubscribe a handler that was previously subscribed using subscribeVisibleLogicalRangeChange.

#### Parameters

• **handler**: `LogicalRangeChangeEventHandler`

Previously subscribed handler

#### Returns

`void`

#### Example

`chart.timeScale().unsubscribeVisibleLogicalRangeChange(myVisibleLogicalRangeChangeHandler);`

### subscribeSizeChange()

subscribeSizeChange(`handler`

):`void`

Adds a subscription to time scale size changes

#### Parameters

• **handler**: `SizeChangeEventHandler`

Handler (function) to be called when the time scale size changes

#### Returns

`void`

### unsubscribeSizeChange()

unsubscribeSizeChange(`handler`

):`void`

Removes a subscription to time scale size changes

#### Parameters

• **handler**: `SizeChangeEventHandler`

Previously subscribed handler

#### Returns

`void`

### applyOptions()

applyOptions(`options`

):`void`

Applies new options to the time scale.

#### Parameters

• **options**: `DeepPartial`

<`HorzScaleOptions`

>

Any subset of options.

#### Returns

`void`

### options()

options():`Readonly`

<`HorzScaleOptions`

>

Returns current options

#### Returns

`Readonly`

<`HorzScaleOptions`

>

Currently applied options