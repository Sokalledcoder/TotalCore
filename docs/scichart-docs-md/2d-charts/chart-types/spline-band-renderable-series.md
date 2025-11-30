---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/spline-band-renderable-series
scraped_at: 2025-11-28T18:24:45.193425
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/spline-band-renderable-series

# The Spline (Smoothed) Band Series Type

Spline Band or Smoothed High/Low Fill Series can be created using the SplineBandRenderableSeries📘 type.

The JavaScript Spline Band Chart Example can be found in the SciChart.Js Examples Suite > Spline Band Series on Github, or our live demo at scichart.com/demo

## Create a Spline Band Series

To create a Javascript Spline Band Chart📘 with SciChart.js, use the following code:

- TS
- Builder API (JSON Config)

`// Demonstrates how to create a Spline Band chart using SciChart.js`

const {

SciChartSurface,

NumericAxis,

SplineBandRenderableSeries,

XyyDataSeries,

SciChartJsNavyTheme,

EllipsePointMarker

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

const xValues = [];

const yValues = [];

const y1Values = [];

for (let i = 0; i < 10; i++) {

xValues.push(i);

yValues.push(2 + 0.2 * Math.sin(i) - Math.cos(i * 0.12));

y1Values.push(1.8 + 0.19 * Math.sin(i * 2) - Math.cos(i * 0.24));

}

const dataSeries = new XyyDataSeries(wasmContext, { xValues, yValues, y1Values });

const bandSeries = new SplineBandRenderableSeries(wasmContext, {

dataSeries,

stroke: "#F48420",

strokeY1: "#50C7E0",

fill: "#F4842033",

fillY1: "#50C7E033",

strokeThickness: 2,

interpolationPoints: 20, // the larger the number, the smoother the band

// Add a pointmarker to show where the datapoints are

pointMarker: new EllipsePointMarker(wasmContext, {

width: 7,

height: 7,

fill: "white",

strokeThickness: 0

})

});

sciChartSurface.renderableSeries.add(bandSeries);

`// Demonstrates how to create a band chart with SciChart.js using the Builder API`

const { chartBuilder, ESeriesType, EThemeProviderType, EPointMarkerType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const xValues = [];

const yValues = [];

const y1Values = [];

for (let i = 0; i < 10; i++) {

xValues.push(i);

yValues.push(2 + 0.2 * Math.sin(i) - Math.cos(i * 0.12));

y1Values.push(1.8 + 0.19 * Math.sin(i * 2) - Math.cos(i * 0.24));

}

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

series: [

{

type: ESeriesType.SplineBandSeries,

xyyData: {

xValues,

yValues,

y1Values

},

options: {

stroke: "#FF1919FF",

strokeY1: "#279B27FF",

fill: "#279B2733",

fillY1: "#FF191933",

strokeThickness: 2,

interpolationPoints: 20, // the larger the number, the smoother the band

pointMarker: {

type: EPointMarkerType.Ellipse,

options: {

width: 7,

height: 7,

strokeThickness: 1,

fill: "steelblue",

stroke: "LightSteelBlue"

}

}

}

}

]

});

In the code above:

- A Spline Band Series instance is created and added to the SciChartSurface.renderableSeries📘 collection.
- We set the stroke, strokeY1, strokethickness properties
- We assign an XyyDataSeries - which stores the Xyy data to render.
- We set the number of interpolationPoints📘 - how many points between real Xy data points will be interpolated using a Spline interpolation algorithm.

This results in the following output:

## Performance Tips in Spline Series

When the SplineBandRenderableSeries.interpolationPoints📘 property is set to zero, then this series renders and displays exactly like a FastLineRenderableSeries.

When the interpolationPoints📘 property is set to another number, e.g. 10, then SciChart.js will calculate 10 points for each Xy datapoint you add to the XyDataSeries. This means you will be displaying 10x the number of datapoints.

*SciChart.js can handle millions of datapoints, but this is something to be aware of. You might want to adjust down the interpolationPoints depending on amount of data on the chart, or zoom level.*

## Render a Gap in a Spline Band Series

It is possible to have null points or gaps in a Spline Band Series by passing a data point with a **NaN** value as the **Y** value. Please refer to the Common Series Features - Draw Gaps in Series article for more details.

## Add Point Markers onto a Spline Band Series

Every data point of a Spline Band Series can be marked with a PointMarker📘. To add Point Markers to the Spline Mountain Series, see the PointMarkers API Documentation.

**Note:** PointMarkers are only applied to the original data-points, not the spline interpolated points which are for display purposes only.

To learn more about the types of Point Marker in SciChart.js, see the Point Markers API documentation.

There is also a dedicated Scatter Series type and a Bubble Series type with some more options.

## Painting Spline Band Segments with Different Colors

It is possible to define the colour of line and band segments individually using the PaletteProvider API.

For more info on how to do this, see the PaletteProvider - Per-point colouring of Band Charts documentation page. The same technique applies to spline line charts.