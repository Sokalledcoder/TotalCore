---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/spline-mountain-renderable-series
scraped_at: 2025-11-28T18:24:44.817805
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/spline-mountain-renderable-series

# The Spline (Smoothed) Mountain Series Type

Spline Mountain or Smoothed Area Series can be created using the SplineMountainRenderableSeries📘 type.

The JavaScript Spline Mountain Chart Example can be found in the SciChart.Js Examples Suite > Spline Mountain Chart on Github, or our live demo at scichart.com/demo

## Create a Spline Mountain Series

To create a Javascript Spline Mountain Chart with SciChart.js, use the following code:

- TS
- Builder API (JSON Config)

`// Demonstrates how to create a spline mountain chart with SciChart.js`

const {

SciChartSurface,

NumericAxis,

SplineMountainRenderableSeries,

EllipsePointMarker,

XyDataSeries,

SciChartJsNavyTheme,

NumberRange,

GradientParams,

Point

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { growBy: new NumberRange(0.1, 0.1) }));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { growBy: new NumberRange(0.1, 0.1) }));

const xValues = [];

const yValues = [];

for (let i = 0; i < 10; i++) {

xValues.push(i);

yValues.push(2 + 0.2 * Math.sin(i) - Math.cos(i * 0.12));

}

// Create a spline mountain series

const splineMountainSeries = new SplineMountainRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues,

yValues

}),

stroke: "#4682b4",

// when a solid color is required, use fill

fill: "rgba(176, 196, 222, 0.7)",

// when a gradient is required, use fillLinearGradient

fillLinearGradient: new GradientParams(new Point(0, 0), new Point(0, 1), [

{ color: "rgba(70,130,180,0.77)", offset: 0 },

{ color: "rgba(70,130,180,0.0)", offset: 1 }

]),

strokeThickness: 5,

zeroLineY: 0.0,

// Set interpolation points to decide the amount of smoothing

interpolationPoints: 10,

// Add a pointmarker to show where the datapoints are

pointMarker: new EllipsePointMarker(wasmContext, {

width: 7,

height: 7,

fill: "white",

strokeThickness: 0

})

});

sciChartSurface.renderableSeries.add(splineMountainSeries);

`// Demonstrates how to create a spline mountain chart with SciChart.js using the Builder API`

const { chartBuilder, ESeriesType, EThemeProviderType, EPointMarkerType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const xValues = [];

const yValues = [];

for (let i = 0; i < 10; i++) {

xValues.push(i);

yValues.push(2 + 0.2 * Math.sin(i) - Math.cos(i * 0.12));

}

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

series: [

{

type: ESeriesType.SplineMountainSeries,

xyData: {

xValues,

yValues

},

options: {

stroke: "#FF6600",

strokeThickness: 5,

zeroLineY: 0.0,

fillLinearGradient: {

gradientStops: [

{ color: "rgba(70,130,180,0.77)", offset: 0.0 },

{ color: "rgba(70,130,180,0.0)", offset: 1 }

],

startPoint: { x: 0, y: 0 },

endPoint: { x: 0, y: 1 }

},

pointMarker: {

type: EPointMarkerType.Ellipse,

options: {

width: 7,

height: 7,

fill: "white",

strokeThickness: 0

}

},

interpolationPoints: 10, // the larger the number, the smoother the mountain

}

}

]

});

In the code above:

- A Spline Mountain Series instance is created and added to the SciChartSurface.renderableSeries📘 collection.
- We set the stroke📘, strokeThickness📘 properties
- We assign a DataSeries - which stores the Xy data to render.
- We set the number of interpolationPoints📘 - how many points between real Xy data points will be interpolated using a Spline interpolation algorithm.

This results in the following output:

## Performance Tips in Spline Series

When the SplineMountainRenderableSeries.interpolationPoints📘 property is set to zero, then this series renders and displays exactly like a FastLineRenderableSeries.

When the interpolationPoints📘 property is set to another number, e.g. 10, then SciChart.js will calculate 10 points for each Xy datapoint you add to the XyDataSeries. This means you will be displaying 10x the number of datapoints.

*SciChart.js can handle millions of datapoints, but this is something to be aware of. You might want to adjust down the interpolationPoints depending on amount of data on the chart, or zoom level.*

## Render a Gap in a Spline Mountain Series

It is possible to have null points or gaps in a Mountain Series by passing a data point with a **NaN** value as the **Y** value. Please refer to the Common Series Features - Draw Gaps in Series article for more details.

## Add Point Markers onto a Spline Line Series

Every data point of a Spline Mountain Series can be marked with a PointMarker📘. To add Point Markers to the Spline Mountain Series, see the PointMarkers API Documentation.

**Note:** PointMarkers are only applied to the original data-points, not the spline interpolated points which are for display purposes only.

To learn more about the types of Point Marker in SciChart.js, see the Point Markers API documentation.

There is also a dedicated Scatter Series type and a Bubble Series type with some more options.

## Painting Spline Mountain Segments with Different Colors

It is possible to define the colour of line and mountain segments individually using the PaletteProvider API.

For more info on how to do this, see the PaletteProvider - Per-point colouring of Mountain Charts documentation page. The same technique applies to spline line charts.