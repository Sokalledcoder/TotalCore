---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/fast-candlestick-renderable-series
scraped_at: 2025-11-28T18:24:27.530856
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/fast-candlestick-renderable-series

# The Candlestick Series type

Candlestick Series or JavaScript Stock Charts can be created using the FastCandlestickRenderableSeries type📘.

The JavaScript Candlestick Chart Example can be found in the SciChart.Js Examples Suite > Candlestick Chart on Github, or our live demo at scichart.com/demo.

## Create a Candlestick Series

To create a Javascript Candlestick Chart with SciChart.js, use the following code:

- TS
- Builder API (JSON Config)

`// Demonstrates how to create a Candlestick chart with SciChart.js`

const {

SciChartSurface,

CategoryAxis,

NumericAxis,

FastCandlestickRenderableSeries,

OhlcDataSeries,

SciChartJsNavyTheme

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new CategoryAxis(wasmContext));

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

labelPrefix: "$",

labelPrecision: 2

})

);

// Data format is { dateValues[], openValues[], highValues[], lowValues[], closeValues[] }

const { dateValues, openValues, highValues, lowValues, closeValues, volumeValues } = await getCandles(

"BTCUSDT",

"1h",

100

);

// Create and add the Candlestick series

const candlestickSeries = new FastCandlestickRenderableSeries(wasmContext, {

dataSeries: new OhlcDataSeries(wasmContext, {

xValues: dateValues,

openValues,

highValues,

lowValues,

closeValues

}),

strokeThickness: 1,

dataPointWidth: 0.7,

brushUp: "#33ff3377",

brushDown: "#ff333377",

strokeUp: "#77ff77",

strokeDown: "#ff7777"

});

sciChartSurface.renderableSeries.add(candlestickSeries);

`// Demonstrates how to create a line chart with SciChart.js using the Builder API`

const { chartBuilder, ESeriesType, EThemeProviderType, EAxisType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

// Data format is { dateValues[], openValues[], highValues[], lowValues[], closeValues[] }

const { dateValues, openValues, highValues, lowValues, closeValues, volumeValues } = await getCandles(

"BTCUSDT",

"1h",

100

);

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: [{ type: EAxisType.CategoryAxis }],

yAxes: [{ type: EAxisType.NumericAxis, options: { labelPrefix: "$", labelPrecision: 2 } }],

series: [

{

type: ESeriesType.CandlestickSeries,

ohlcData: {

xValues: dateValues,

openValues,

highValues,

lowValues,

closeValues

},

options: {

dataPointWidth: 0.7,

brushUp: "#33ff3377",

brushDown: "#ff333377",

strokeUp: "#77ff77",

strokeDown: "#ff7777",

strokeThickness: 1

}

}

]

});

This results in the following output:

The above example makes a web call to Binance to fetch Bitcoin/USD prices. If you see a blank chart, check the Js console as this web call may be blocked. You can always edit the Codepen to substitute your own data!

In the example above:

- A Candlestick Series instance is created and added to the SciChartSurface.renderableSeries📘 collection.
- This requires a special dataseries type: OhlcDataSeries📘, which accepts X, Open, High, Low, Close values as arrays of values.
- We set the up/down stroke and fill colors via properties brushUp📘, brushDown📘, strokeUp📘, strokeDown📘 properties.
- We set dataPointWidth📘 - which defines the fraction of width to occupy
- We use a special axis type called the CategoryAxis📘 which removes gaps in stock market data.

A CategoryAxis📘 is necessary if you have Forex or Stock market data which includes weekend or overnight gaps, as this axis type measures by x-index, not by x-value. For CryptoCurrency data the DateTimeNumericAxis📘 can be used as these are 24/7 markets.

You can format the date labels on the XAxis by following the instructions on the Axis Label Formatting page.

## Adding Volume Bars to a Candlestick Chart

In the SciChart.js demo - Candlestick Charts - volume bars are docked to the bottom of the chart. Here's how to do this with SciChart.js.

- TS
- Builder API (JSON Config)

`// Add a secondary axis for the volume bars`

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

id: "VolumeAxisId",

isVisible: false,

growBy: new NumberRange(0, 4)

})

);

// Fetch data. Format is { dates[], opens[], highs[], lows[], closes[], volumes[] }

const { dateValues, openValues, highValues, lowValues, closeValues, volumeValues } = await getCandles(

"BTCUSDT",

"4h",

100

);

// Add a column series to render the volume bars

sciChartSurface.renderableSeries.add(

new FastColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: dateValues,

yValues: volumeValues

}),

yAxisId: "VolumeAxisId",

strokeThickness: 0,

dataPointWidth: 0.7,

opacity: 0.47

})

);

// continue to add the candlestick series to the chart...

`const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {`

xAxes: [{ type: EAxisType.CategoryAxis }],

yAxes: [

{

type: EAxisType.NumericAxis,

options: { labelPrefix: "$", labelPrecision: 2 }

},

{

type: EAxisType.NumericAxis,

options: { isVisible: false, id: "VolumeAxisId", growBy: new NumberRange(0, 4) }

}

],

series: [

{

type: ESeriesType.CandlestickSeries,

ohlcData: {

xValues: dateValues,

openValues,

highValues,

lowValues,

closeValues

},

options: {

dataPointWidth: 0.7,

brushUp: "#33ff3377",

brushDown: "#ff333377",

strokeUp: "#77ff77",

strokeDown: "#ff7777",

strokeThickness: 1

}

},

{

type: ESeriesType.ColumnSeries,

xyData: {

xValues: dateValues,

yValues: volumeValues

},

options: {

yAxisId: "VolumeAxisId",

strokeThickness: 0,

dataPointWidth: 0.7,

opacity: 0.47

}

}

]

});

Here's how the example looks now:

## Painting Candles with Different Colors

It is possible to define the colour of specific OHLC Bars using the PaletteProvider API.

For more info on how to do this, see the PaletteProvider - Per-point colouring of Candlestick/Ohlc Charts documentation page.