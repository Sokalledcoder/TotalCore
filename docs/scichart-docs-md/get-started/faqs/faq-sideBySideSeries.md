---
source: https://www.scichart.com/documentation/js/v4/get-started/faqs/faq-sideBySideSeries
scraped_at: 2025-11-28T18:24:59.580079
---

# https://www.scichart.com/documentation/js/v4/get-started/faqs/faq-sideBySideSeries

# Custom Side-By-Side Series

While SciChart.js provides the built-in StackedColumnCollection📘 for stacking Column Series side-by-side or top-to-bottom, many developers need more flexibility to position different types of series alongside each other.

Above: The JavaScript Built-in Stacked Column Chart Side-by-Side example from the SciChart.js Demo

## The Challenge

What if you want to display different series types - candlesticks, impulse series, error bars, or any combination - positioned side-by-side at the same X coordinates? The built-in stacking only works for column series of the same type.

## The Solution: Custom Positioning

Here's the result - three different series types (Candlestick, Impulse, and Error Bars) positioned side-by-side:

## Key Implementation Points

**Calculate X-offsets**: Use the`calculateShift`

function to position each series with new x-values**Consistent spacing**: Maintain uniform gaps between series for visual clarity**Flexible series count**: The algorithm adapts to any number of side-by-side series**Series type independence**: Works with any combination of renderable series types

## How It Works

The `calculateShift`

function takes your original X-value and calculates an offset based on:

**Series index**: Which position in the group (0, 1, 2, etc.)**Total count**: How many series you're positioning side-by-side**Spacing**: Optional gap between series (defaults to 2% of a unit)

- ts

`/**`

* e.g. for 3 columns, you get WIDTH == 0.25, so you'd have:

* ```

* 0.125 Spacing - [0.25 Col1, 0.25 Col2, 0.25 col3] - 0.125 Spacing === 1 collection unit

* ```

* outer spacing decreases as inner spacing between columns grows

*

* @param {*} initialVal - x initial value

* @param {*} index - index of the column

* @param {*} totalCount - number of columns

* @param {*} spacing - (optional) spacing in between columns

* @returns

*/

function calculateShift(initialVal: number, index: number, totalCount: number, spacing = 0.02) {

const WIDTH = 1 / (6 + 1); // how much space should one series take

return initialVal - (WIDTH + spacing) * (totalCount / 2.0 - (index + 0.5));

}

const drawExample = async (rootElement: string) => {

const { wasmContext, sciChartSurface } = await SciChartSurface.create(rootElement);

// Create x/y axes

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, {

growBy: new NumberRange(0.05, 0.05),

labelPrecision: 0,

autoTicks: false,

majorDelta: 1,

}));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, {

growBy: new NumberRange(0.01, 0.2),

labelPrecision: 0

}));

// Create the Column / Error bar series

const xValues = [1, 2, 3, 4];

const SERIES_PER_X_VALUE = 3;

const candleStick = new FastCandlestickRenderableSeries(wasmContext, {

dataSeries: new OhlcDataSeries(wasmContext, {

xValues: xValues.map((x) => calculateShift(x, 0, SERIES_PER_X_VALUE)),

lowValues: [3, 5, 4, 5],

openValues: [4, 6, 4.5, 6.5],

closeValues: [4.8, 7.2, 6, 7],

highValues: [6, 8, 7, 8.5],

dataSeriesName: "Candlestick"

}),

stroke: "#00AA00",

strokeThickness: 3,

dataPointWidth: 0.15,

strokeUp: "#00AA00",

brushUp: "#006600",

strokeDown: "#AA0000",

brushDown: "#660000",

});

const impulse = new FastImpulseRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: xValues.map((x) => calculateShift(x, 1, SERIES_PER_X_VALUE)),

yValues: [5, 6, 7, 8],

dataSeriesName: "Impulse"

}),

stroke: "#3388FF",

strokeThickness: 4

});

const errorBar = new FastErrorBarsRenderableSeries(wasmContext, {

dataSeries: new HlcDataSeries(wasmContext, {

xValues: xValues.map((x) => calculateShift(x, 2, SERIES_PER_X_VALUE)),

yValues: [5, 6, 7, 8],

lowValues: [4, 5, 6, 7],

highValues: [6, 7, 8, 9],

dataSeriesName: "Error Bars"

}),

stroke: "#F55",

strokeThickness: 4,

dataPointWidth: 0.15,

});

sciChartSurface.renderableSeries.add(candleStick, impulse, errorBar);

sciChartSurface.chartModifiers.add(

new ZoomExtentsModifier(),

new ZoomPanModifier(),

new MouseWheelZoomModifier(),

new LegendModifier()

);

return { wasmContext, sciChartSurface };

};

## Usage Tips

**Start with index 0**: Always begin your series indexing from 0 for proper centering**Adjust dataPointWidth**: For series with width properties (like candlesticks), set`dataPointWidth`

to prevent overlap**Consistent spacing**: Use the same spacing value across all series for uniform appearance**Scale with data**: The algorithm automatically scales positioning based on your total series count**Related demos**: Check out other related CodePens, like: