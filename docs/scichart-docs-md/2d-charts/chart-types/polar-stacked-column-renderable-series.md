---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/polar-stacked-column-renderable-series
scraped_at: 2025-11-28T18:24:41.160844
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/polar-stacked-column-renderable-series

# The Polar Stacked Column Chart Type

The JavaScript Polar Stacked Column Chart can be found in the SciChart.Js Examples Suite > Polar Windrose Chart on Github, or our live demo at scichart.com/demo.

The Polar Stacked Column Chart Type is created using a PolarStackedColumnCollection📘 to manage multiple series of PolarStackedColumnRenderableSeries📘, which represent the individual stacked columns in the chart.

## Create a Basic Polar Stacked Column Series

To create a Javascript Polar Stacked Column Series📘 with SciChart.js, use the following code:

- TS

`// Demonstrates how to create a basic polar column chart using SciChart.js`

const {

SciChartPolarSurface,

PolarNumericAxis,

SciChartJsNavyTheme,

PolarStackedColumnCollection,

PolarStackedColumnRenderableSeries,

EPolarAxisMode,

NumberRange,

XyDataSeries,

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { sciChartSurface, wasmContext } = await SciChartPolarSurface.create(divElementId, {

theme: new SciChartJsNavyTheme(),

});

const angularXAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Angular, // Angular == "goes around the center, drawn by arcs"

visibleRange: new NumberRange(0, 10), // to keep column #1 and #10 from touching

flippedCoordinates: true, // go clockwise

});

sciChartSurface.xAxes.add(angularXAxis);

const radialYAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Radial, // Radial == "goes from center out, drawn by straight lines"

innerRadius: 0.1, // donut hole

labelPrecision: 0, // no decimals

});

sciChartSurface.yAxes.add(radialYAxis);

// Create the collection the stacked columns will be added to

const polarCollection = new PolarStackedColumnCollection(wasmContext, {

isOneHundredPercent: false // set to true to make columns stack to 100%

});

const polarColumn1 = new PolarStackedColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],

yValues: Array.from({ length: 10 }, (_, i) => Math.random() * 11 + 1)

}),

fill: "#FF3344AA",

stroke: "white",

strokeThickness: 2,

});

const polarColumn2 = new PolarStackedColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],

yValues: Array.from({ length: 10 }, (_, i) => Math.random() * 2 + 1)

}),

fill: "#5588FFAA",

});

// Add the columns to the collection

polarCollection.add(polarColumn1, polarColumn2);

// Add the columns to the collection

sciChartSurface.renderableSeries.add(polarCollection);

In the code above:

- Set xAxis' polarAxisMode📘 to
`EPolarAxisMode.Angular`

to create an Angular axis - the way most Polar charts are created. - Set yAxis' polarAxisMode📘 to
`EPolarAxisMode.Radial`

to create a Radial axis which represents the height of the columns. - We create a PolarStackedColumnCollection📘 to hold the renderable series.
- We add 2 PolarStackedColumnRenderableSeries📘 to the collection, each with its own data and styling.

This type of plot is called a

WindRose, orRosechart, as it is often used to visualize wind speed and direction data.

## Create a Basic **Radial** Polar Stacked Column Series

To create a Javascript **Radial** Polar Stacked Column Series📘 with SciChart.js, use the code from above, but replace the **xAxis** and **yAxis** config with this snippet:

`const radialXAxis = new PolarNumericAxis(wasmContext, {`

polarAxisMode: EPolarAxisMode.Radial, // radial axis -> xAxis

axisAlignment: EAxisAlignment.Right,

innerRadius: 0.1, // donut hole

labelPrecision: 0, // no decimals

});

sciChartSurface.xAxes.add(radialXAxis);

const angularYAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Angular, // angular axis -> yAxis

axisAlignment: EAxisAlignment.Top,

visibleRange: new NumberRange(0, 15),

useNativeText: true,

flippedCoordinates: true, // go clockwise

});

sciChartSurface.yAxes.add(angularYAxis);

In the code above:

- Set xAxis' polarAxisMode📘 to
`EPolarAxisMode.Radial`

to create a Radial axis. - Set yAxis' polarAxisMode📘 to
`EPolarAxisMode.Angular`

to create an Angular axis.Both of these settings now create a

`vertical`

or`radial`

chart, where x-axis represents the height of the columns, and y-axis represents the angle. If this is something you want to replicate,