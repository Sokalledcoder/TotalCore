---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/fast-line-renderable-series
scraped_at: 2025-11-28T18:24:27.885245
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/fast-line-renderable-series

# The Line Series Type

Line Series can be created using the FastLineRenderableSeries📘 type.

The JavaScript Line Chart Example can be found in the SciChart.Js Examples Suite > Line Chart on Github, or our live demo at scichart.com/demo.

## Create a Line Series

To create a Javascript Line Chart with SciChart.js, use the following code:

- TS
- Builder API (JSON Config)

`// Demonstrates how to create a line chart with SciChart.js`

const {

SciChartSurface,

NumericAxis,

FastLineRenderableSeries,

XyDataSeries,

SciChartJsNavyTheme

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

// Add X and Y axes to the chart

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

const xValues = [];

const yValues = [];

for (let i = 0; i < 100; i++) {

xValues.push(i);

yValues.push(0.2 * Math.sin(i * 0.1) - Math.cos(i * 0.01));

}

// Create a line series with the XY data we generated

const lineSeries = new FastLineRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues,

yValues

}),

stroke: "#FF6600",

strokeThickness: 5,

});

sciChartSurface.renderableSeries.add(lineSeries);

`// Demonstrates how to create a line chart with SciChart.js using the Builder API`

const { chartBuilder, ESeriesType, EThemeProviderType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

series: [

{

type: ESeriesType.LineSeries,

xyData: {

xValues: [0, 1, 2, 3, 4, 5, 6, 7, 8],

yValues: [2.5, 3.5, 3.7, 4.0, 5.0, 5.5, 5.0, 4.0, 3.0]

},

options: {

stroke: "#0066FF",

strokeThickness: 5

}

}

]

});

This results in the following:

In the code above:

- A FastLineRenderableSeries📘 instance is created and added to the SciChartSurface.renderableSeries📘 collection.
- We set the stroke, strokeThickness properties
- We assign an XyDataSeries📘 as our line's
`dataSeries`

- which stores the Xy data to render.

## Render a Gap in a Line Series

It is possible to have null points or gaps in a Line Series by passing a data point with a **NaN** value as the **Y** value. Please refer to the Common Series Features - Draw Gaps in Series article for more details.

## Add Point Markers onto a Line Series

It is possible to put scatter point markers of varying type (Ellipse, Square, Triangle, Cross, Custom) onto a Line Series via the PointMarker API. To learn more, see the documentation page Drawing PointMarkers on Series.

To learn more about the types of Point Marker in SciChart.js, see the Point Markers API documentation.

There is also a dedicated Scatter Series type and a Bubble Series type with some more options.

## Painting Line Segments with Different Colors

It is possible to define the colour of line segments individually using the PaletteProvider API.

For more info on how to do this, see the PaletteProvider - Per-point colouring of Line Charts documentation page.