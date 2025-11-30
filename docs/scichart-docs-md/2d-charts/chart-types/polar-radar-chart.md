---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/polar-radar-chart
scraped_at: 2025-11-28T18:24:41.010856
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/polar-radar-chart

# The Polar Radar Chart Type

The Radar chart (or Spider chart) type displays data in a circular layout, where each axis represents a different variable, most often a category. The axes are connected drawn to form a polygon, allowing for easy comparison of multiple variables.

The data is usually plotted using the PolarLineRenderableSeries📘 or PolarMountainRenderableSeries📘 classes, which are specialized for polar coordinates.

Above: The JavaScript Polar Radar Chart example from the SciChart.js Demo

## Create a Basic Polar Radar Series

To create a Javascript Polar Radar Series with SciChart.js, use the following code:

`const {`

SciChartPolarSurface,

SciChartJsNavyTheme,

PolarNumericAxis,

NumberRange,

PolarCategoryAxis,

PolarMountainRenderableSeries,

EPolarAxisMode,

EPolarGridlineMode,

XyDataSeries,

} = SciChart;

// or for npm import { SciChartPolarSurface, ... } from "scichart"

const { sciChartSurface, wasmContext } = await SciChartPolarSurface.create(rootElement, {

theme: new SciChartJsNavyTheme()

});

const angularXAxis = new PolarCategoryAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Angular,

labels: [ "Offense", "Shooting", "Defense", "Rebounds", "Passing", "Bench" ], // categories

startAngle: Math.PI / 2, // start at 12 o'clock

flippedCoordinates: true, // go clockwise

majorGridLineStyle: { color: "#88888844" },

drawMinorGridLines: false,

});

sciChartSurface.xAxes.add(angularXAxis);

const radialYAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Radial,

gridlineMode: EPolarGridlineMode.Polygons, // this creates the radar chart look

visibleRange: new NumberRange(0, 10),

startAngle: Math.PI / 2, // start at 12 o'clock

labelPrecision: 0,

majorGridLineStyle: { color: "#88888844" },

drawMinorGridLines: false,

drawMajorTickLines: false,

drawMinorTickLines: false,

});

sciChartSurface.yAxes.add(radialYAxis);

const xValues = [0, 1, 2, 3, 4, 5];

const yValues = [9, 10, 7, 5, 8, 6]; // values for: "Offense", "Shooting", "Defense", "Rebounds", "Passing", "Bench"

// Radar / Spider Charts may also work with `PolarLineRenderableSeries`

const polarMountain = new PolarMountainRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: [...xValues, xValues[xValues.length] + 1], // + 1 to close the loop

yValues: [...yValues, yValues[0]], // re-plot first point to close the loop

dataSeriesName: "Golden State Warriors",

}),

stroke: "#FFC72C", // Golden State Warriors gold

fill: "#1D428A80", // Golden State Warriors blue with 50% opacity

strokeThickness: 4,

});

sciChartSurface.renderableSeries.add(polarMountain);

Key aspects of the code above:

- This
**radar**/**spider**/**cobweb**chart look is achieved by using`gridlineMode`

: EPolarGridlineMode.Polygons📘 on the radial axis (yAxis), which draws straight lines in between gridlines instead of arcs. - We set
`labels: [ "Offense", "Shooting", ... ]`

on the angular axis (xAxis) to display the categories. - While defining the XyDataSeries📘 for the PolarMountainRenderableSeries📘, we use this trick on the
`xValues`

array to reach the 1st point from the end of the series, so that the polygon closes correctly:

`xValues: [...xValues, xValues[xValues.length] + 1], // assuming step = 1`

- For the
`yValues`

array we do this by re-using the 1st value:

`yValues: [...yValues, yValues[0]]`