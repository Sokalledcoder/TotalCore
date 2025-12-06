---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/SeriesOptionsCommon
scraped_at: 2025-12-01T14:31:41.691524
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/SeriesOptionsCommon

# Interface: SeriesOptionsCommon

Represents options common for all types of series

## Properties

### lastValueVisible

lastValueVisible:`boolean`

Visibility of the label with the latest visible price on the price scale.

#### Default Value

`true`

, `false`

for yield curve charts

### title

title:`string`

You can name series when adding it to a chart. This name will be displayed on the label next to the last value label.

#### Default Value

`''`

### priceScaleId?

`optional`

priceScaleId:`string`

Target price scale to bind new series to.

#### Default Value

`'right'`

if right scale is visible and `'left'`

otherwise

### visible

visible:`boolean`

Visibility of the series. If the series is hidden, everything including price lines, baseline, price labels and markers, will also be hidden. Please note that hiding a series is not equivalent to deleting it, since hiding does not affect the timeline at all, unlike deleting where the timeline can be changed (some points can be deleted).

#### Default Value

`true`

### priceLineVisible

priceLineVisible:`boolean`

Show the price line. Price line is a horizontal line indicating the last price of the series.

#### Default Value

`true`

, `false`

for yield curve charts

### priceLineSource

priceLineSource:`PriceLineSource`

The source to use for the value of the price line.

#### Default Value

`{@link PriceLineSource.LastBar}`

### priceLineWidth

priceLineWidth:`LineWidth`

Width of the price line.

#### Default Value

`1`

### priceLineColor

priceLineColor:`string`

Color of the price line. By default, its color is set by the last bar color (or by line color on Line and Area charts).

#### Default Value

`''`

### priceLineStyle

priceLineStyle:`LineStyle`

Price line style.

#### Default Value

`{@link LineStyle.Dashed}`

### priceFormat

priceFormat:`PriceFormat`

Price format.

#### Default Value

`{ type: 'price', precision: 2, minMove: 0.01 }`

### baseLineVisible

baseLineVisible:`boolean`

Visibility of base line. Suitable for percentage and `IndexedTo100`

scales.

#### Default Value

`true`

### baseLineColor

baseLineColor:`string`

Color of the base line in `IndexedTo100`

mode.

#### Default Value

`'#B2B5BE'`

### baseLineWidth

baseLineWidth:`LineWidth`

Base line width. Suitable for percentage and `IndexedTo10`

scales.

#### Default Value

`1`

### baseLineStyle

baseLineStyle:`LineStyle`

Base line style. Suitable for percentage and indexedTo100 scales.

#### Default Value

`{@link LineStyle.Solid}`

### autoscaleInfoProvider?

`optional`

autoscaleInfoProvider:`AutoscaleInfoProvider`

Override the default AutoscaleInfo provider. By default, the chart scales data automatically based on visible data range. However, for some reasons one could require overriding this behavior.

#### Default Value

`undefined`

#### Examples

`const firstSeries = chart.addSeries(LineSeries, {`

autoscaleInfoProvider: () => ({

priceRange: {

minValue: 0,

maxValue: 100,

},

}),

});

`const firstSeries = chart.addSeries(LineSeries, {`

autoscaleInfoProvider: () => ({

priceRange: {

minValue: 0,

maxValue: 100,

},

margins: {

above: 10,

below: 10,

},

}),

});

`const firstSeries = chart.addSeries(LineSeries, {`

autoscaleInfoProvider: original => {

const res = original();

if (res !== null) {

res.priceRange.minValue -= 10;

res.priceRange.maxValue += 10;

}

return res;

},

});