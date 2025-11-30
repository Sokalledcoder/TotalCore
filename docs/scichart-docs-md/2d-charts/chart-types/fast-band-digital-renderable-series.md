---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/fast-band-digital-renderable-series
scraped_at: 2025-11-28T18:24:25.758592
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/fast-band-digital-renderable-series

# The Digital (Step) Band Series Type

A Digital Band Series, or High-Low Fill between two Digital or Step lines can be created using the FastBandRenderableSeries📘 type.

The JavaScript Digital Band Chart Example can be found in the SciChart.Js Examples Suite > Band Series on Github, or our live demo at scichart.com/demo.

## Create a Digital Band Series

To create a Javascript Digital Band Chart with SciChart.js, use the following code:

- TS
- Builder API (JSON Config)

`// Demonstrates how to create a band chart using SciChart.js`

const {

SciChartSurface,

NumericAxis,

FastBandRenderableSeries,

XyyDataSeries,

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

const y1Values = [];

const POINTS = 100;

const STEP = (3 * Math.PI) / POINTS;

for (let i = 0; i <= POINTS; i++) {

const k = 1 - i / (POINTS * 2);

xValues.push(i);

yValues.push(Math.sin(i * STEP) * k * 0.7);

y1Values.push(Math.cos(i * STEP) * k);

}

const bandSeries = new FastBandRenderableSeries(wasmContext, {

dataSeries: new XyyDataSeries(wasmContext, {

xValues,

yValues,

y1Values

}),

stroke: "#F48420",

strokeY1: "#50C7E0",

fill: "#F4842033",

fillY1: "#50C7E033",

strokeThickness: 2,

// optional parameter defines a step-line

isDigitalLine: true

});

sciChartSurface.renderableSeries.add(bandSeries);

`// Demonstrates how to create a band chart with SciChart.js using the Builder API`

const { chartBuilder, ESeriesType, EThemeProviderType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const xValues = [];

const yValues = [];

const y1Values = [];

const POINTS = 100;

const STEP = (3 * Math.PI) / POINTS;

for (let i = 0; i <= POINTS; i++) {

const k = 1 - i / (POINTS * 2);

xValues.push(i);

yValues.push(Math.sin(i * STEP) * k * 0.7);

y1Values.push(Math.cos(i * STEP) * k);

}

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

series: [

{

type: ESeriesType.BandSeries,

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

// optional parameter defines a step-line

isDigitalLine: true

}

}

]

});

This results in the following output:

In the code above:

- A Band Series instance is created and added to the SciChartSurface.renderableSeries📘 collection.
- We set the stroke, fill properties for when Y > Y1 and vice versa (more info over at FastBandRenderableSeries📘 in TypeDoc).
- We set the
**isDigitalLine**property to true. - We assign a DataSeries📘 - in this case an XyyDataSeries📘 which stores X, Y, Y1 data.

## Render a Gap in a Digital Band Series

It is possible to have null points or gaps in a Digital Band Series by passing a data point with a **NaN** value as the **Y** value. Please refer to the Common Series Features - Draw Gaps in Series article for more details.

## Add Point Markers onto a Band Series

It is possible to put scatter point markers of varying type (Ellipse, Square, Triangle, Cross, Custom) onto a Band Series via the PointMarker API. To learn more, see the documentation page Drawing PointMarkers on Series.

To learn more about the types of Point Marker in SciChart.js, see the Point Markers API documentation.

There is also a dedicated Scatter Series type and a Bubble Series type with some more options.

## Painting Band Segments with Different Colors

It is possible to define the colour of band segments individually using the PaletteProvider API.

For more info on how to do this, see the PaletteProvider - Per-point colouring of Band Charts documentation page.