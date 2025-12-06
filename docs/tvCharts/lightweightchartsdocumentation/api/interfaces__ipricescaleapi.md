---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/IPriceScaleApi
scraped_at: 2025-12-01T14:31:40.068398
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/IPriceScaleApi

# Interface: IPriceScaleApi

Interface to control chart's price scale

## Methods

### applyOptions()

applyOptions(`options`

):`void`

Applies new options to the price scale

#### Parameters

• **options**: `DeepPartial`

<`PriceScaleOptions`

>

Any subset of options.

#### Returns

`void`

### options()

options():`Readonly`

<`PriceScaleOptions`

>

Returns currently applied options of the price scale

#### Returns

`Readonly`

<`PriceScaleOptions`

>

Full set of currently applied options, including defaults

### width()

width():`number`

Returns a width of the price scale if it's visible or 0 if invisible.

#### Returns

`number`

### setVisibleRange()

setVisibleRange(`range`

):`void`

Sets the visible range of the price scale.

#### Parameters

• **range**: `IRange`

<`number`

>

The visible range to set, with `from`

and `to`

properties.

#### Returns

`void`

### getVisibleRange()

getVisibleRange():`IRange`

<`number`

>

Returns the visible range of the price scale.

#### Returns

`IRange`

<`number`

>

The visible range of the price scale, or null if the range is not set.

### setAutoScale()

setAutoScale(`on`

):`void`

Sets the auto scale mode of the price scale.

#### Parameters

• **on**: `boolean`

If true, enables auto scaling; if false, disables it.

#### Returns

`void`