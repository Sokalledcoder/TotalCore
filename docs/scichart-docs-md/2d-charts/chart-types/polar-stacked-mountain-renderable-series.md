---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/polar-stacked-mountain-renderable-series
scraped_at: 2025-11-28T18:24:41.354549
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/polar-stacked-mountain-renderable-series

# The Polar Stacked Mountain Chart Type

The Polar Stacked Mountain Chart Type is created using a PolarStackedMountainCollection📘 to manage multiple series of PolarStackedMountainRenderableSeries📘, which represent the individual stacked mountains in the chart.

The JavaScript Polar Stacked Mountain Chart can be found in the SciChart.Js Examples Suite > Polar Stacked Mountain Chart on Github, or our live demo at scichart.com/demo.

## Create a Basic Polar Stacked Mountain Series

To create a Javascript Polar Stacked Mountain Series📘 with SciChart.js, use the following code:

- TS
- Builder API (JSON Config)

`// Demonstrates how to create a basic polar mountain chart using SciChart.js`

const {

SciChartPolarSurface,

PolarNumericAxis,

SciChartJsNavyTheme,

PolarStackedMountainCollection,

PolarStackedMountainRenderableSeries,

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

visibleRange: new NumberRange(0, 6),

flippedCoordinates: true, // go clockwise

});

sciChartSurface.xAxes.add(angularXAxis);

const radialYAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Radial, // Radial == "goes from center out, drawn by straight lines"

visibleRange: new NumberRange(0, 10),

drawLabels: false, // hide radial labels

});

sciChartSurface.yAxes.add(radialYAxis);

// Create the collection the stacked mountains will be added to

const polarCollection = new PolarStackedMountainCollection(wasmContext);

const xValues = [0, 1, 2, 3, 4, 5]; // x values for the mountains

const yValues1 = Array.from({ length: 6 }, (_, i) => Math.random() * 6 + 2);

const yValues2 = Array.from({ length: 6 }, (_, i) => Math.random() * 1 + 1);

const polarMountain1 = new PolarStackedMountainRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: [...xValues, xValues[0]], // +1 to close the loop

yValues: [...yValues1, yValues1[0]] // connect first and last points

}),

fill: "#FF3344AA",

stroke: "white",

strokeThickness: 3,

});

const polarMountain2 = new PolarStackedMountainRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: [...xValues, xValues[0]], // +1 to close the loop

yValues: [...yValues2, yValues2[0]] // connect first and last points

}),

fill: "#5588FFAA",

stroke: "white",

strokeThickness: 3,

});

// Add the mountains to the collection

polarCollection.add(polarMountain1, polarMountain2);

// Add the mountains to the collection

sciChartSurface.renderableSeries.add(polarCollection);

`// Demonstrates how to create a band chart with SciChart.js using the Builder API`

const {

chartBuilder,

SciChartJsNavyTheme,

EAxisType,

ESeriesType,

EPolarAxisMode,

EAxisAlignment,

NumberRange,

} = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DPolarChart(divElementId, {

surface: { theme: new SciChartJsNavyTheme() },

xAxes: [

{

type: EAxisType.PolarNumericAxis,

options: {

polarAxisMode: EPolarAxisMode.Angular,

axisAlignment: EAxisAlignment.Top,

visibleRange: new NumberRange(0, 6),

}

}

],

yAxes: [

{

type: EAxisType.PolarNumericAxis,

options: {

axisAlignment: EAxisAlignment.Right,

polarAxisMode: EPolarAxisMode.Radial,

visibleRange: new NumberRange(0, 10),

}

}

],

series: [

{

type: ESeriesType.PolarMountainSeries,

xyData: {

xValues: [0, 1, 2, 3, 4, 5, 0], // +1 to close the loop

yValues: [2, 3, 5, 4, 6, 5, 2] // connect first and last points

},

options: {

fill: "#FF3344AA",

stroke: "white",

strokeThickness: 3,

}

},

{

type: ESeriesType.PolarMountainSeries,

xyData: {

xValues: [0, 1, 2, 3, 4, 5, 0], // +1 to close the loop

yValues: [1, 1.5, 2, 2.5, 3, 2.5, 1] // connect first and last points

},

options: {

fill: "#5588FFAA",

stroke: "white",

strokeThickness: 3,

}

}

]

});

return { sciChartSurface, wasmContext };

Above:

We created 2 PolarStackedMountainRenderableSeries📘 and added them to a PolarStackedMountainCollection📘. Each PolarStackedMountainRenderableSeries📘 represents a single mountain in the chart, and they are stacked on top of each other. The StackedMountainCollection itself is added to sciChartSurface.renderableSeries📘 collection, not the individual mountain series.

This results in the following output: