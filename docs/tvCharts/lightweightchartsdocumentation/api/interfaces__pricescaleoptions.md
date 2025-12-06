---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/PriceScaleOptions
scraped_at: 2025-12-01T14:31:41.456696
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/PriceScaleOptions

# Interface: PriceScaleOptions

Structure that describes price scale options

## Properties

### autoScale

autoScale:`boolean`

Autoscaling is a feature that automatically adjusts a price scale to fit the visible range of data. Note that overlay price scales are always auto-scaled.

#### Default Value

`true`

### mode

mode:`PriceScaleMode`

Price scale mode.

#### Default Value

`{@link PriceScaleMode.Normal}`

### invertScale

invertScale:`boolean`

Invert the price scale, so that a upwards trend is shown as a downwards trend and vice versa. Affects both the price scale and the data on the chart.

#### Default Value

`false`

### alignLabels

alignLabels:`boolean`

Align price scale labels to prevent them from overlapping.

#### Default Value

`true`

### scaleMargins

scaleMargins:`PriceScaleMargins`

Price scale margins.

#### Default Value

`{ bottom: 0.1, top: 0.2 }`

#### Example

`chart.priceScale('right').applyOptions({`

scaleMargins: {

top: 0.8,

bottom: 0,

},

});

### borderVisible

borderVisible:`boolean`

Set true to draw a border between the price scale and the chart area.

#### Default Value

`true`

### borderColor

borderColor:`string`

Price scale border color.

#### Default Value

`'#2B2B43'`

### textColor?

`optional`

textColor:`string`

Price scale text color. If not provided LayoutOptions.textColor is used.

#### Default Value

`undefined`

### entireTextOnly

entireTextOnly:`boolean`

Show top and bottom corner labels only if entire text is visible.

#### Default Value

`false`

### visible

visible:`boolean`

Indicates if this price scale visible. Ignored by overlay price scales.

#### Default Value

`true`

for the right price scale and `false`

for the left.
For the yield curve chart, the default is for the left scale to be visible.

### ticksVisible

ticksVisible:`boolean`

Draw small horizontal line on price axis labels.

#### Default Value

`false`

### minimumWidth

minimumWidth:`number`

Define a minimum width for the price scale. Note: This value will be exceeded if the price scale needs more space to display it's contents.

Setting a minimum width could be useful for ensuring that multiple charts positioned in a vertical stack each have an identical price scale width, or for plugins which require a bit more space within the price scale pane.

#### Default Value

`0`

### ensureEdgeTickMarksVisible

ensureEdgeTickMarksVisible:`boolean`

Ensures that tick marks are always visible at the very top and bottom of the price scale, regardless of the data range. When enabled, a tick mark will be drawn at both edges of the scale, providing clear boundary indicators.

#### Default Value

`false`