---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ISeriesPrimitiveBase
scraped_at: 2025-12-01T14:31:40.363671
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ISeriesPrimitiveBase

# Interface: ISeriesPrimitiveBase<TSeriesAttachedParameters>

Base interface for series primitives. It must be implemented to add some external graphics to series

## Type parameters

• **TSeriesAttachedParameters** = `unknown`

## Methods

### updateAllViews()?

`optional`

updateAllViews():`void`

This method is called when viewport has been changed, so primitive have to recalculate / invalidate its data

#### Returns

`void`

### priceAxisViews()?

`optional`

priceAxisViews(): readonly`ISeriesPrimitiveAxisView`

[]

Returns array of labels to be drawn on the price axis used by the series

#### Returns

readonly `ISeriesPrimitiveAxisView`

[]

array of objects; each of then must implement ISeriesPrimitiveAxisView interface

For performance reasons, the lightweight library uses internal caches based on references to arrays So, this method must return new array if set of views has changed and should try to return the same array if nothing changed

### timeAxisViews()?

`optional`

timeAxisViews(): readonly`ISeriesPrimitiveAxisView`

[]

Returns array of labels to be drawn on the time axis

#### Returns

readonly `ISeriesPrimitiveAxisView`

[]

array of objects; each of then must implement ISeriesPrimitiveAxisView interface

For performance reasons, the lightweight library uses internal caches based on references to arrays So, this method must return new array if set of views has changed and should try to return the same array if nothing changed

### paneViews()?

`optional`

paneViews(): readonly`IPrimitivePaneView`

[]

Returns array of objects representing primitive in the main area of the chart

#### Returns

readonly `IPrimitivePaneView`

[]

array of objects; each of then must implement ISeriesPrimitivePaneView interface

For performance reasons, the lightweight library uses internal caches based on references to arrays So, this method must return new array if set of views has changed and should try to return the same array if nothing changed

### priceAxisPaneViews()?

`optional`

priceAxisPaneViews(): readonly`IPrimitivePaneView`

[]

Returns array of objects representing primitive in the price axis area of the chart

#### Returns

readonly `IPrimitivePaneView`

[]

array of objects; each of then must implement ISeriesPrimitivePaneView interface

For performance reasons, the lightweight library uses internal caches based on references to arrays So, this method must return new array if set of views has changed and should try to return the same array if nothing changed

### timeAxisPaneViews()?

`optional`

timeAxisPaneViews(): readonly`IPrimitivePaneView`

[]

Returns array of objects representing primitive in the time axis area of the chart

#### Returns

readonly `IPrimitivePaneView`

[]

array of objects; each of then must implement ISeriesPrimitivePaneView interface

For performance reasons, the lightweight library uses internal caches based on references to arrays So, this method must return new array if set of views has changed and should try to return the same array if nothing changed

### autoscaleInfo()?

`optional`

autoscaleInfo(`startTimePoint`

,`endTimePoint`

):`AutoscaleInfo`

Return autoscaleInfo which will be merged with the series base autoscaleInfo. You can use this to expand the autoscale range to include visual elements drawn outside of the series' current visible price range.

**Important**: Please note that this method will be evoked very often during scrolling and zooming of the chart, thus it
is recommended that this method is either simple to execute, or makes use of optimisations such as caching to ensure that
the chart remains responsive.

#### Parameters

• **startTimePoint**: `Logical`

start time point for the current visible range

• **endTimePoint**: `Logical`

end time point for the current visible range

#### Returns

AutoscaleInfo

### attached()?

`optional`

attached(`param`

):`void`

Attached Lifecycle hook.

#### Parameters

• **param**: `TSeriesAttachedParameters`

An object containing useful references for the attached primitive to use.

#### Returns

`void`

void

### detached()?

`optional`

detached():`void`

Detached Lifecycle hook.

#### Returns

`void`

void

### hitTest()?

`optional`

hitTest(`x`

,`y`

):`PrimitiveHoveredItem`

Hit test method which will be called by the library when the cursor is moved. Use this to register object ids being hovered for use within the crosshairMoved and click events emitted by the chart. Additionally, the hit test result can specify a preferred cursor type to display for the main chart pane. This method should return the top most hit for this primitive if more than one object is being intersected.

#### Parameters

• **x**: `number`

x Coordinate of mouse event

• **y**: `number`

y Coordinate of mouse event