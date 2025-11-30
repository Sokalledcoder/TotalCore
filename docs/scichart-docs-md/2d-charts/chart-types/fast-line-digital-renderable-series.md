---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/fast-line-digital-renderable-series
scraped_at: 2025-11-28T18:24:27.835070
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/fast-line-digital-renderable-series

# The Digital (Step) Line Series

Digital, or Step Line Series can be created using the FastLineRenderableSeries📘 type, and setting the isDigitalLine📘 flag to `true`

.

The JavaScript Digital Line Chart Example can be found in the SciChart.Js Examples Suite > Digital Line Chart on Github, or our live demo at scichart.com/demo.

## Create a Digital (Step) Line Series

To create a JavaScript Digital Line Chart with SciChart.js, use the following code:

- TS
- Builder API (JSON Config)

`// Demonstrates how to create a digitral line chart with SciChart.js`

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

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

const xValues = [];

const yValues = [];

for (let i = 0; i < 100; i++) {

xValues.push(i);

yValues.push(Math.sin(i * 0.1));

}

const lineSeries = new FastLineRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues,

yValues

}),

stroke: "#FF6600",

strokeThickness: 5,

isDigitalLine: true // enable a digital (step) line

});

sciChartSurface.renderableSeries.add(lineSeries);

`// Demonstrates how to create a digital line chart with SciChart.js using the Builder API`

const { chartBuilder, ESeriesType, EThemeProviderType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const xValues = [];

const yValues = [];

for (let i = 0; i < 100; i++) {

xValues.push(i);

yValues.push(Math.sin(i * 0.1));

}

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

series: [

{

type: ESeriesType.LineSeries,

xyData: {

xValues,

yValues

},

options: {

stroke: "#0066FF",

strokeThickness: 5,

// set flag isDigitalLine = true to enable a digital (step) line

isDigitalLine: true

}

}

]

});

This results in the following:

In the code above:

- A Line Series instance is created and added to the SciChartSurface.renderableSeries📘 collection.
- We set the stroke, strokeThickness properties
- We set the isDigitalLine📘 property to
`true`

to enable a digital (step) line mode. - We assign a DataSeries - which stores the Xy data to render.

## Render a Gap in a Digital (Step) Line Series

It is possible to have null points or gaps in a Digital Line Series by passing a data point with a **NaN** value as the **Y** value. Please refer to the Common Series Features - Draw Gaps in Series article for more details.

## Add Point Markers onto a Digital (Step) Line Series

It is possible to put scatter point markers of varying type (Ellipse, Square, Triangle, Cross, Custom) onto a Digital Line via the PointMarker API. To learn more, see the documentation page Drawing PointMarkers on Series.

To learn more about the types of Point Marker in SciChart.js, see the Point Markers API documentation.

There is also a dedicated Scatter Series type and a Bubble Series type with some more options.

## Painting Digital Line Segments with Different Colors

It is possible to define the colour of line segments individually using the PaletteProvider API.

For more info on how to do this, see the PaletteProvider - Per-point colouring of Line Charts documentation page.