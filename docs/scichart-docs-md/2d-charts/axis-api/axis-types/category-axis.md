---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-types/category-axis
scraped_at: 2025-11-28T18:24:07.974417
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-types/category-axis

# The Category Axis

The CategoryAxis📘 treats values a little differently. This is a special axis type which uses the X-Index not the X-Value to measure chart series.

Learn more about the commonalities between axis here.

## Difference between CategoryAxis and NumericAxis

Imagine you want to plot the data:

Age (XAxis) | Cats | Dogs | Fish |
|---|---|---|---|
| 1 | 7 | 7 | 8 |
| 9 | 6 | 5 | 7 |
| 10 | 5 | 4 | 3 |
| 20 | 4 | 3 | 2 |

A standard NumericAxis📘 (which is a value-axis) and the CategoryAxis📘 would display the data differently.

Here's the code to setup the chart.

- TS
- Builder API (JSON Config)

`// With the following data`

const xValues = [1, 9, 10, 20];

const cats = [7, 6, 5, 4];

const dogs = [7, 5, 4, 3];

const fish = [8, 7, 3, 2];

// create a chart

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

// Add a Category XAxis with numeric formatting

sciChartSurface.xAxes.add(

new CategoryAxis(wasmContext, {

axisTitle: "Category Axis",

labelFormat: ENumericFormat.Decimal

})

);

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { growBy: new NumberRange(0.2, 0.2) }));

`// With the following data`

const xValues = [1, 9, 10, 20];

const cats = [7, 6, 5, 4];

const dogs = [7, 5, 4, 3];

const fish = [8, 7, 3, 2];

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { axisTitle: "Numeric Axis" }));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { growBy: new NumberRange(0.2, 0.2) }));

addChartTitle(sciChartSurface, "Value XAxis", "X Values are used to measure X-Distance");

addLineSeries(sciChartSurface, xValues, cats, "#50C7E0", "Cats");

addLineSeries(sciChartSurface, xValues, dogs, "#F48420", "Dogs");

addLineSeries(sciChartSurface, xValues, fish, "#C52E60", "Fish");

addLegend(sciChartSurface);

Why is this important? **In the case where you are plotting stock market data, you want to use a** **CategoryAxis**📘**.**

*This is because stock market data has gaps in it (consider the stock market has data on Monday, Tuesday, Wednesday, Thursday, Friday but not weekends). The* *CategoryAxis*📘 *collapses the gaps and treats each datapoint as equidistant, ignoring the X-Value.*

## Using and Configuring a CategoryAxis

The Category Axis won't draw without either:

**At least one series with some data**on the chart,- or, CategoryAxis.defaultXStart📘 and defaultXStep📘 (allows a chart without any series)
- or CategoryAxis.defaultXValues📘 (allows a chart without any series)

Because the CategoryAxis measures xValues using index, you need to have data on the chart to calculate x-coordinate from data index. However, we can still create a chart by specifying some defaults with the properties above.

## Creating a CategoryAxis (without Data) using Defaults

The first example we're going to show uses the default properties on the CategoryAxis to display a chart without data.

- TS
- Builder API (JSON Config)

`const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {`

theme: new SciChartJsNavyTheme()

});

// Unix Epoch for March 1st 2023 & March 2nd 2023

const march1st2023 = new Date("2023-03-1").getTime(); // = 1677628800000 ms since 1/1/1970

const march2nd2023 = new Date("2023-03-2").getTime(); // = 1677715200000 ms since 1/1/1970

const oneDay = march2nd2023 - march1st2023; // = 86400000 milliseconds in one day

// Creating a CategoryAxis as an XAxis on the bottom

sciChartSurface.xAxes.add(

new CategoryAxis(wasmContext, {

// set Defaults so that category axis can draw. Once you add series and data these will be overridden

// All Linux Timestamp properties in scichart.js must be divided by 1,000 to go from milliseconds to seconds

defaultXStart: march1st2023 / 1000,

defaultXStep: oneDay / 1000,

// set other properties

drawMajorGridLines: true,

drawMinorGridLines: true,

axisTitle: "Category X Axis",

axisAlignment: EAxisAlignment.Bottom,

// set a date format for labels

labelFormat: ENumericFormat.Date_DDMMYY

})

);

// Create a YAxis on the left

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

axisTitle: "Numeric Y Axis",

axisAlignment: EAxisAlignment.Left

})

);

`// Unix Epoch for March 1st 2023 & March 2nd 2023`

const march1st2023 = new Date("2023-03-1").getTime(); // = 1677628800000 ms since 1/1/1970

const march2nd2023 = new Date("2023-03-2").getTime(); // = 1677715200000 ms since 1/1/1970

const oneDay = march2nd2023 - march1st2023; // = 86400000 milliseconds in one day

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: {

type: EAxisType.CategoryAxis,

options: {

// set Defaults so that category axis can draw. Once you add series and data these will be overridden

// All Linux Timestamp properties in scichart.js must be divided by 1,000 to go from milliseconds to seconds

defaultXStart: march1st2023 / 1000,

defaultXStep: oneDay / 1000,

// set other properties

drawMajorGridLines: true,

drawMinorGridLines: true,

axisTitle: "Category X Axis",

axisAlignment: EAxisAlignment.Bottom,

// set a date format for labels

labelFormat: ENumericFormat.Date_DDMMYY

}

},

yAxes: {

type: EAxisType.NumericAxis,

options: {

axisTitle: "Numeric Y Axis",

axisAlignment: EAxisAlignment.Left

}

}

});

This results in the following:

In the above code sample we set the CategoryAxis.defaultXStart = unix timestamp for March 1st 2023, and defaultXStep = number of seconds in one day. This tells SciChart.js to default the index calculation to 1-datapoint = 1 day and to start the xAxis from 1st March.

Once you apply data to the CategoryAxis these properties will be ignored. They are only required to create and show a chart using CategoryAxis without data.

## Creating a CategoryAxis with Financial Data

Let's create a chart with CategoryAxis by supplying some data below:

- TS

`// Demonstrates how to create a chart with a CategoryAxis in SciChart.js`

const {

SciChartSurface,

CategoryAxis,

SciChartJsNavyTheme,

EAxisAlignment,

NumericAxis,

ZoomPanModifier,

MouseWheelZoomModifier,

TextAnnotation,

ECoordinateMode,

EHorizontalAnchorPoint,

EVerticalAnchorPoint,

ENumericFormat,

FastCandlestickRenderableSeries,

OhlcDataSeries,

SmartDateLabelProvider,

NumberRange,

EAutoRange

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

// Creating a CategoryAxis as an XAxis on the bottom

sciChartSurface.xAxes.add(

new CategoryAxis(wasmContext, {

// set other properties

drawMajorGridLines: true,

drawMinorGridLines: true,

axisTitle: "Category X Axis",

axisAlignment: EAxisAlignment.Bottom,

// set a date format for labels

labelProvider: new SmartDateLabelProvider()

})

);

// Create a YAxis on the left

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

axisTitle: "Numeric Y Axis",

labelPrefix: "$",

labelPrecision: 2,

labelFormat: ENumericFormat.Decimal,

axisAlignment: EAxisAlignment.Right,

autoRange: EAutoRange.Always,

growBy: new NumberRange(0.1, 0.1)

})

);

// The category axis requires some data to work (unless you set defaultStartX/StepX properties)

// so, lets add some data with dates to the chart

// Data format is { dateValues[], openValues[], highValues[], lowValues[], closeValues[] }

const { dateValues, openValues, highValues, lowValues, closeValues, volumeValues } = await getCandles(

"BTCUSDT",

"1h",

100

);

// Create and add the Candlestick series

const candlestickSeries = new FastCandlestickRenderableSeries(wasmContext, {

strokeThickness: 1,

dataSeries: new OhlcDataSeries(wasmContext, {

xValues: dateValues,

openValues,

highValues,

lowValues,

closeValues

}),

dataPointWidth: 0.7,

brushUp: "#33ff3377",

brushDown: "#ff333377",

strokeUp: "#77ff77",

strokeDown: "#ff7777"

});

sciChartSurface.renderableSeries.add(candlestickSeries);

This results in the following output:

The above example makes a web call to Binance to fetch Bitcoin/USD prices. If you see a blank chart, check the Js console as this web call may be blocked. You can always edit the Codepen to substitute your own data!