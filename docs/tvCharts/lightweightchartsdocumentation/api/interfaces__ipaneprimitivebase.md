---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/IPanePrimitiveBase
scraped_at: 2025-12-01T14:31:39.909577
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/IPanePrimitiveBase

# Interface: IPanePrimitiveBase<TPaneAttachedParameters>

Base interface for series primitives. It must be implemented to add some external graphics to series

## Type parameters

• **TPaneAttachedParameters** = `unknown`

## Methods

### updateAllViews()?

`optional`

updateAllViews():`void`

This method is called when viewport has been changed, so primitive have to recalculate / invalidate its data

#### Returns

`void`

### paneViews()?

`optional`

paneViews(): readonly`IPanePrimitivePaneView`

[]

Returns array of objects representing primitive in the main area of the chart

#### Returns

readonly `IPanePrimitivePaneView`

[]

array of objects; each of then must implement IPrimitivePaneView interface

For performance reasons, the lightweight library uses internal caches based on references to arrays So, this method must return new array if set of views has changed and should try to return the same array if nothing changed

### attached()?

`optional`

attached(`param`

):`void`

Attached Lifecycle hook.

#### Parameters

• **param**: `TPaneAttachedParameters`

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