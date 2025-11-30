---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/fast-ohlc-renderable-series
scraped_at: 2025-11-28T18:24:28.794356
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/fast-ohlc-renderable-series

# The OHLC Series Type

Ohlc Series or JavaScript Stock Charts can be created using the **FastOhlcRenderableSeries** type.

The JavaScript Ohlc Chart Example can be found in the SciChart.Js Examples Suite > OHLC Chart on Github, or our live demo at scichart.com/demo.

## Create an Ohlc Series

To create a Javascript Ohlc Chart with SciChart.js, use the following code:

- TS
- Builder API (JSON Config)

`// Demonstrates how to create an OHLC (or Bar) chart with SciChart.js`

const {

SciChartSurface,

CategoryAxis,

NumericAxis,

FastOhlcRenderableSeries,

OhlcDataSeries,

SciChartJsNavyTheme

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new CategoryAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { labelPrefix: "$", labelPrecision: 2 }));

// Data format is { dateValues[], openValues[], highValues[], lowValues[], closeValues[] }

const { dateValues, openValues, highValues, lowValues, closeValues, volumeValues } = await getCandles(

"BTCUSDT",

"1h",

100

);

// Create a OhlcDataSeries with open, high, low, close values

const dataSeries = new OhlcDataSeries(wasmContext, {

xValues: dateValues,

openValues,

highValues,

lowValues,

closeValues

});

// Create and add the OhlcSeries series

const ohlcSeries = new FastOhlcRenderableSeries(wasmContext, {

dataSeries,

strokeThickness: 1,

dataPointWidth: 1,

strokeUp: "#77ff77",

strokeDown: "#ff7777"

});

sciChartSurface.renderableSeries.add(ohlcSeries);

`// Demonstrates how to create an OHLC chart with SciChart.js using the Builder API`

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

type: ESeriesType.OhlcSeries,

ohlcData: {

xValues: dateValues,

openValues,

highValues,

lowValues,

closeValues

},

options: {

dataPointWidth: 1,

strokeUp: "#77ff77",

strokeDown: "#ff7777",

strokeThickness: 1

}

}

]

});

This results in the following output:

In the code above:

- A Ohlc Series instance is created and added to the
**SciChartSurface.renderableSeries**collection. - This requires a special dataseries type: OhlcDataSeries, which accepts
`X`

,`Open`

,`High`

,`Low`

,`Close`

values - We set the up/down stroke color via properties strokeUp📘, strokeDown📘.
- We set dataPointWidth📘 - which defines the fraction of width to occupy
- We use a special axis type called the CategoryAxis which removes gaps in stock market data.

A CategoryAxis📘 is necessary if you have Forex or Stock market data which includes weekend or overnight gaps, as this axis type measures by x-index, not by x-value. For CryptoCurrency data the NumericAxis📘 can be used as these are 24/7 markets.

You can format the date labels on the xAxis by following the instructions on the Axis Label Formatting page.

## Adding Volume Bars to an OHLC Chart

The Candlestick Chart example shows a technique to add volume bars docked to the bottom of the chart. The technique is the same for OHLC series so please see the candlestick docs.

## Painting Ohlc bars with Different Colors

It is possible to define the colour of specific OHLC Bars using the PaletteProvider API.

For more info on how to do this, see the PaletteProvider - Per-point colouring of Candlestick/Ohlc Charts documentation page.