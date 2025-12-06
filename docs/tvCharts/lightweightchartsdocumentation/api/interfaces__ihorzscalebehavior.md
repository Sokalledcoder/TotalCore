---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/IHorzScaleBehavior
scraped_at: 2025-12-01T14:31:39.814793
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/IHorzScaleBehavior

# Interface: IHorzScaleBehavior<HorzScaleItem>

Class interface for Horizontal scale behavior

## Type parameters

• **HorzScaleItem**

## Methods

### options()

options():`ChartOptionsImpl`

<`HorzScaleItem`

>

Structure describing options of the chart.

#### Returns

`ChartOptionsImpl`

<`HorzScaleItem`

>

ChartOptionsBase

### setOptions()

setOptions(`options`

):`void`

Set the chart options. Note that this is different to `applyOptions`

since the provided options will overwrite the current options
instead of merging with the current options.

#### Parameters

• **options**: `ChartOptionsImpl`

<`HorzScaleItem`

>

Chart options to be set

#### Returns

`void`

void

### preprocessData()

preprocessData(`data`

):`void`

Method to preprocess the data.

#### Parameters

• **data**: `DataItem`

<`HorzScaleItem`

> | `DataItem`

<`HorzScaleItem`

>[]

Data items for the series

#### Returns

`void`

void

### convertHorzItemToInternal()

convertHorzItemToInternal(`item`

):`object`

Convert horizontal scale item into an internal horizontal scale item.

#### Parameters

• **item**: `HorzScaleItem`

item to be converted

#### Returns

`object`

InternalHorzScaleItem

##### [species]

[species]:`"InternalHorzScaleItem"`

The 'name' or species of the nominal.

### createConverterToInternalObj()

createConverterToInternalObj(`data`

):`HorzScaleItemConverterToInternalObj`

<`HorzScaleItem`

>

Creates and returns a converter for changing series data into internal horizontal scale items.

#### Parameters

• **data**: (`AreaData`

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

>)[]

series data

#### Returns

`HorzScaleItemConverterToInternalObj`

<`HorzScaleItem`

>

HorzScaleItemConverterToInternalObj

### key()

key(`internalItem`

):`InternalHorzScaleItemKey`

Returns the key for the specified horizontal scale item.

#### Parameters

• **internalItem**: `HorzScaleItem`

| `object`

horizontal scale item for which the key should be returned

#### Returns

InternalHorzScaleItemKey

### cacheKey()

cacheKey(`internalItem`

):`number`

Returns the cache key for the specified horizontal scale item.

#### Parameters

• **internalItem**

horizontal scale item for which the cache key should be returned

• **internalItem.[species]**: `"InternalHorzScaleItem"`

The 'name' or species of the nominal.

#### Returns

`number`

number

### updateFormatter()

updateFormatter(`options`

):`void`

Update the formatter with the localization options.

#### Parameters

• **options**: `LocalizationOptions`

<`HorzScaleItem`

>

Localization options

#### Returns

`void`

void

### formatHorzItem()

formatHorzItem(`item`

):`string`

Format the horizontal scale item into a display string.

#### Parameters

• **item**

horizontal scale item to be formatted as a string

• **item.[species]**: `"InternalHorzScaleItem"`

The 'name' or species of the nominal.

#### Returns

`string`

string

### formatTickmark()

formatTickmark(`item`

,`localizationOptions`

):`string`

Format the horizontal scale tickmark into a display string.

#### Parameters

• **item**: `TickMark`

tickmark item

• **localizationOptions**: `LocalizationOptions`

<`HorzScaleItem`

>

Localization options

#### Returns

`string`

string

### maxTickMarkWeight()

maxTickMarkWeight(`marks`

):`TickMarkWeightValue`

Returns the maximum tickmark weight value for the specified tickmarks on the time scale.

#### Parameters

• **marks**: `TimeMark`

[]

Timescale tick marks

#### Returns

TickMarkWeightValue

### fillWeightsForPoints()

fillWeightsForPoints(`sortedTimePoints`

,`startIndex`

):`void`

Fill the weights for the sorted time scale points.

#### Parameters

• **sortedTimePoints**: readonly `Mutable`

<`TimeScalePoint`

>[]

sorted time scale points

• **startIndex**: `number`

starting index

#### Returns

`void`

void

### shouldResetTickmarkLabels()?

`optional`

shouldResetTickmarkLabels(`tickMarks`

):`boolean`

If returns true, then the tick mark formatter will be called for all the visible tick marks even if the formatter has previously been called for a specific tick mark. This allows you to change the formatting on all the tick marks.

#### Parameters

• **tickMarks**: readonly `TickMark`

[]

array of tick marks

#### Returns

`boolean`

boolean