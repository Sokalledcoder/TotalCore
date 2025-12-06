---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/TimeScaleOptions
scraped_at: 2025-12-01T14:31:41.978947
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/TimeScaleOptions

# Interface: TimeScaleOptions

Extended time scale options for time-based horizontal scale

## Extends

## Properties

### rightOffset

rightOffset:`number`

The margin space in bars from the right side of the chart.

#### Default Value

`0`

#### Inherited from

`HorzScaleOptions`

. `rightOffset`

### rightOffsetPixels?

`optional`

rightOffsetPixels:`number`

The margin space in pixels from the right side of the chart.
This option has priority over `rightOffset`

.

#### Default Value

`undefined`

#### Inherited from

`HorzScaleOptions`

. `rightOffsetPixels`

### barSpacing

barSpacing:`number`

The space between bars in pixels.

#### Default Value

`6`

#### Inherited from

### minBarSpacing

minBarSpacing:`number`

The minimum space between bars in pixels.

#### Default Value

`0.5`

#### Inherited from

`HorzScaleOptions`

. `minBarSpacing`

### maxBarSpacing

maxBarSpacing:`number`

The maximum space between bars in pixels.

Has no effect if value is set to `0`

.

#### Default Value

`0`

#### Inherited from

`HorzScaleOptions`

. `maxBarSpacing`

### fixLeftEdge

fixLeftEdge:`boolean`

Prevent scrolling to the left of the first bar.

#### Default Value

`false`

#### Inherited from

`HorzScaleOptions`

. `fixLeftEdge`

### fixRightEdge

fixRightEdge:`boolean`

Prevent scrolling to the right of the most recent bar.

#### Default Value

`false`

#### Inherited from

`HorzScaleOptions`

. `fixRightEdge`

### lockVisibleTimeRangeOnResize

lockVisibleTimeRangeOnResize:`boolean`

Prevent changing the visible time range during chart resizing.

#### Default Value

`false`

#### Inherited from

`HorzScaleOptions`

. `lockVisibleTimeRangeOnResize`

### rightBarStaysOnScroll

rightBarStaysOnScroll:`boolean`

Prevent the hovered bar from moving when scrolling.

#### Default Value

`false`

#### Inherited from

`HorzScaleOptions`

. `rightBarStaysOnScroll`

### borderVisible

borderVisible:`boolean`

Show the time scale border.

#### Default Value

`true`

#### Inherited from

`HorzScaleOptions`

. `borderVisible`

### borderColor

borderColor:`string`

The time scale border color.

#### Default Value

`'#2B2B43'`

#### Inherited from

`HorzScaleOptions`

. `borderColor`

### visible

visible:`boolean`

Show the time scale.

#### Default Value

`true`

#### Inherited from

### timeVisible

timeVisible:`boolean`

Show the time, not just the date, in the time scale and vertical crosshair label.

#### Default Value

`false`

#### Inherited from

`HorzScaleOptions`

. `timeVisible`

### secondsVisible

secondsVisible:`boolean`

Show seconds in the time scale and vertical crosshair label in `hh:mm:ss`

format for intraday data.

#### Default Value

`true`

#### Inherited from

`HorzScaleOptions`

. `secondsVisible`

### shiftVisibleRangeOnNewBar

shiftVisibleRangeOnNewBar:`boolean`

Shift the visible range to the right (into the future) by the number of new bars when new data is added.

Note that this only applies when the last bar is visible.

#### Default Value

`true`

#### Inherited from

`HorzScaleOptions`

. `shiftVisibleRangeOnNewBar`

### allowShiftVisibleRangeOnWhitespaceReplacement

allowShiftVisibleRangeOnWhitespaceReplacement:`boolean`

Allow the visible range to be shifted to the right when a new bar is added which is replacing an existing whitespace time point on the chart.

Note that this only applies when the last bar is visible & `shiftVisibleRangeOnNewBar`

is enabled.

#### Default Value

`false`

#### Inherited from

`HorzScaleOptions`

. `allowShiftVisibleRangeOnWhitespaceReplacement`

### ticksVisible

ticksVisible:`boolean`

Draw small vertical line on time axis labels.

#### Default Value

`false`

#### Inherited from

`HorzScaleOptions`

. `ticksVisible`

### tickMarkMaxCharacterLength?

`optional`

tickMarkMaxCharacterLength:`number`

Maximum tick mark label length. Used to override the default 8 character maximum length.

#### Default Value

`undefined`

#### Inherited from

`HorzScaleOptions`

. `tickMarkMaxCharacterLength`

### uniformDistribution

uniformDistribution:`boolean`

Changes horizontal scale marks generation.
With this flag equal to `true`

, marks of the same weight are either all drawn or none are drawn at all.

#### Inherited from

`HorzScaleOptions`

. `uniformDistribution`

### minimumHeight

minimumHeight:`number`

Define a minimum height for the time scale. Note: This value will be exceeded if the time scale needs more space to display it's contents.

Setting a minimum height could be useful for ensuring that multiple charts positioned in a horizontal stack each have an identical time scale height, or for plugins which require a bit more space within the time scale pane.

#### Default Value

`0`

#### Inherited from

`HorzScaleOptions`

. `minimumHeight`

### allowBoldLabels

allowBoldLabels:`boolean`

Allow major time scale labels to be rendered in a bolder font weight.

#### Default Value

`true`

#### Inherited from

`HorzScaleOptions`

. `allowBoldLabels`

### ignoreWhitespaceIndices

ignoreWhitespaceIndices:`boolean`

Ignore time scale points containing only whitespace (for all series) when drawing grid lines, tick marks, and snapping the crosshair to time scale points.

For the yield curve chart type it defaults to `true`

.

#### Default Value

`false`

#### Inherited from

`HorzScaleOptions`

. `ignoreWhitespaceIndices`

### tickMarkFormatter?

`optional`

tickMarkFormatter:`TickMarkFormatter`

Tick marks formatter can be used to customize tick marks labels on the time axis.

#### Default Value

`undefined`