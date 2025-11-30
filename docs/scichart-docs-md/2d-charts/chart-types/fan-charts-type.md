---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/fan-charts-type
scraped_at: 2025-11-28T18:24:25.618339
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/fan-charts-type

# The Fan Charts Type

Fan Charts are provided by using multiple Band Series on the same chart.

tip

The JavaScript Fan Chart Example can be found in the SciChart.Js Examples Suite on Github, or our live demo at scichart.com/demo

Above: The JavaScript Fan Chart example from the SciChart.js Demo

## Create a Fan Chart

There is no Fan Chart type out of the box in SciChart.js, but it is easy to create one using multiple Band series. Start with the following code:

- TS
- Builder API (JSON Config)

`// Demonstrates how to create a fan chart using SciChart.js`

const {

SciChartSurface,

NumericAxis,

FastLineRenderableSeries,

FastBandRenderableSeries,

XyDataSeries,

XyyDataSeries,

SciChartJsNavyTheme

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

// get data for the fan chart

// format is [{ date, actual, varMax, var4, var3, var2, var1, varMin }]

const varianceData = getVarianceData();

const xValues = varianceData.map(v => v.date);

// Add a line series with the Xy data (the actual data)

sciChartSurface.renderableSeries.add(

new FastLineRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: varianceData.map(v => v.actual) }),

stroke: "#3388FF"

})

);

// Add band series with progressively higher opacity for the fan variance data

sciChartSurface.renderableSeries.add(

new FastBandRenderableSeries(wasmContext, {

dataSeries: new XyyDataSeries(wasmContext, {

xValues,

yValues: varianceData.map(v => v.varMin),

y1Values: varianceData.map(v => v.varMax)

}),

opacity: 0.15,

fill: "#3388FF",

stroke: "#00000000",

strokeY1: "#00000000"

})

);

sciChartSurface.renderableSeries.add(

new FastBandRenderableSeries(wasmContext, {

dataSeries: new XyyDataSeries(wasmContext, {

xValues,

yValues: varianceData.map(v => v.var1),

y1Values: varianceData.map(v => v.var4)

}),

opacity: 0.33,

fill: "#3388FF",

stroke: "#00000000",

strokeY1: "#00000000"

})

);

sciChartSurface.renderableSeries.add(

new FastBandRenderableSeries(wasmContext, {

dataSeries: new XyyDataSeries(wasmContext, {

xValues,

yValues: varianceData.map(v => v.var2),

y1Values: varianceData.map(v => v.var3)

}),

opacity: 0.5,

fill: "#3388FF",

stroke: "#00000000",

strokeY1: "#00000000"

})

);

`// Demonstrates how to create a band chart with SciChart.js using the Builder API`

const { chartBuilder, ESeriesType, EThemeProviderType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

// get data for the fan chart

// format is [{ date, actual, varMax, var4, var3, var2, var1, varMin }]

const varianceData = getVarianceData();

// Convert to arrays expected by scichart.js. There are more efficient ways to do this!

const xValues = varianceData.map(v => v.date);

const yValues = varianceData.map(v => v.actual);

const varMinValues = varianceData.map(v => v.varMin);

const varMaxValues = varianceData.map(v => v.varMax);

const var1Values = varianceData.map(v => v.var1);

const var2Values = varianceData.map(v => v.var2);

const var3Values = varianceData.map(v => v.var3);

const var4Values = varianceData.map(v => v.var4);

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

series: [

{

type: ESeriesType.LineSeries,

xyData: { xValues, yValues },

options: {

stroke: "#3388FF"

}

},

{

type: ESeriesType.BandSeries,

xyyData: { xValues, yValues: varMinValues, y1Values: varMaxValues },

options: {

opacity: 0.15,

fill: "#3388FF",

strokeY1: "#00000000"

}

},

{

type: ESeriesType.BandSeries,

xyyData: { xValues, yValues: var1Values, y1Values: var4Values },

options: {

opacity: 0.33,

fill: "#3388FF",

strokeY1: "#00000000"

}

},

{

type: ESeriesType.BandSeries,

xyyData: { xValues, yValues: var2Values, y1Values: var3Values },

options: {

opacity: 0.5,

fill: "#3388FF",

strokeY1: "#00000000"

}

}

]

});

This results in the following output:

In the example above:

- Some variance data is first created and returned as an array of objects.
- A Line series is created to display the actual X,Y value
- Several Band Series are created and added to the SciChartSurface.renderableSeries📘 collection to render the variance bands.
- We set the stroke, fill properties and opacity of each series (more info over at FastBandRenderableSeries in TypeDoc📘).
- We assign a DataSeries📘 - in this case an XyyDataSeries📘 which stores X, Y1, Y2 data for bands, and XyDataSeries📘 for lines.