---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/spline-line-renderable-series
scraped_at: 2025-11-28T18:24:45.019959
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/spline-line-renderable-series

# The Spline (Smoothed) Line Series Type

Spline Line or Smoothed Series can be created using the SplineLineRenderableSeries📘 type.

The JavaScript Spline Line Chart Example can be found in the SciChart.Js Examples Suite > Spline Line Chart on Github, or our live demo at scichart.com/demo

## Create a Spline Line Series

To create a Javascript Spline Line Chart with SciChart.js, use the following code:

- TS
- Builder API (JSON Config)

`// Demonstrates how to create a line chart with SciChart.js`

const {

SciChartSurface,

NumericAxis,

SplineLineRenderableSeries,

EllipsePointMarker,

XyDataSeries,

SciChartJsNavyTheme,

NumberRange

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { growBy: new NumberRange(0.1, 0.1) }));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { growBy: new NumberRange(0.1, 0.1) }));

// Create a spline line series

const splineLineSeries = new SplineLineRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: Array.from({length: 10}, (_, i) => i), // [0, 1, 2, ..., 9]

yValues: Array.from({length: 10}, (_, i) => 0.2 * Math.sin(i) - Math.cos(i * 0.12))

}),

stroke: "#FF6600",

strokeThickness: 5,

// Set interpolation points to decide the amount of smoothing - the larger the number, the smoother the line

interpolationPoints: 20,

// Add a pointmarker to show where the datapoints are

pointMarker: new EllipsePointMarker(wasmContext, {

width: 7,

height: 7,

fill: "white",

strokeThickness: 0

})

});

sciChartSurface.renderableSeries.add(splineLineSeries);

`// Demonstrates how to create a line chart with SciChart.js using the Builder API`

const { chartBuilder, ESeriesType, EThemeProviderType, EPointMarkerType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

series: [

{

type: ESeriesType.SplineLineSeries,

xyData: {

xValues: Array.from({length: 10}, (_, i) => i), // [0, 1, 2, ..., 9]

yValues: Array.from({length: 10}, (_, i) => 0.2 * Math.sin(i) - Math.cos(i * 0.12))

},

options: {

stroke: "#FF6600",

strokeThickness: 5,

interpolationPoints: 20, // the larger the number, the smoother the line

pointMarker: {

type: EPointMarkerType.Ellipse,

options: {

width: 7,

height: 7,

fill: "white",

strokeThickness: 0

}

}

}

}

]

});

In the code above:

- A Spline Line Series instance is created and added to the SciChartSurface.renderableSeries📘 collection.
- We set the stroke, strokethickness properties
- We assign a DataSeries - which stores the Xy data to render.
- We set the number of interpolationPoints📘 - how many points between real Xy data points will be interpolated using a Spline interpolation algorithm.

This results in the following output:

## Performance Tips in Spline Lines

When the SplineLineRenderableSeries.interpolationPoints📘 property is set to zero, then this series renders and displays exactly like a FastLineRenderableSeries.

When the interpolationPoints📘 property is set to another number, e.g. 10, then SciChart.js will calculate 10 points for each Xy datapoint you add to the XyDataSeries. This means you will be displaying 10x the number of datapoints.

*SciChart.js can handle millions of datapoints, but this is something to be aware of. You might want to adjust down the interpolationPoints depending on amount of data on the chart, or zoom level.*

## Render a Gap in a Spline Line Series

It is possible to have null points or gaps in a Line Series by passing a data point with a **NaN** value as the **Y** value. Please refer to the Common Series Features - Draw Gaps in Series article for more details.

## Add Point Markers onto a Line Series

Every data point of a Spline Line Series can be marked with a PointMarker📘. To add Point Markers to the Spline Line Series, see the PointMarkers API Documentation.

PointMarkers are only applied to the original data-points, not the spline interpolated points which are for display purposes only.

To learn more about the types of Point Marker in SciChart.js, see the Point Markers API documentation.

There is also a dedicated Scatter Series type and a Bubble Series type with some more options.

## Painting Spline Line Segments with Different Colors

It is possible to define the colour of line segments individually using the PaletteProvider API.

For more info on how to do this, see the PaletteProvider - Per-point colouring of Line Charts documentation page. The same technique applies to spline line charts.