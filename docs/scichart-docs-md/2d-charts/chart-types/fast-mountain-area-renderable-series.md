---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/fast-mountain-area-renderable-series
scraped_at: 2025-11-28T18:24:28.386987
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/fast-mountain-area-renderable-series

# The Mountain (Area) Series Type

Mountain (or Area) Series can be created using the FastMountainRenderableSeries📘 type.

The JavaScript Mountain Chart Example can be found in the SciChart.Js Examples Suite > Mountain Chart on Github, or our live demo at scichart.com/demo.

## Create a Mountain Series

To create a Javascript Mountain Chart with SciChart.js, use the following code:

- TS
- Builder API (JSON Config)

`// Demonstrates how to create a Mountain (Area) chart with SciChart.js`

const {

SciChartSurface,

NumericAxis,

FastMountainRenderableSeries,

GradientParams,

XyDataSeries,

Point,

SciChartJsNavyTheme

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

// Create some data

let yLast = 100.0;

const xValues = [];

const yValues = [];

for (let i = 0; i <= 250; i++) {

const y = yLast + (Math.random() - 0.48);

yLast = y;

xValues.push(i);

yValues.push(y);

}

// Create a mountain series & add to the chart

const mountainSeries = new FastMountainRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues }),

stroke: "#4682b4",

strokeThickness: 3,

zeroLineY: 0.0,

// when a solid color is required, use fill

fill: "rgba(176, 196, 222, 0.7)",

// when a gradient is required, use fillLinearGradient

fillLinearGradient: new GradientParams(new Point(0, 0), new Point(0, 1), [

{ color: "rgba(70,130,180,0.77)", offset: 0 },

{ color: "rgba(70,130,180,0.0)", offset: 1 }

])

});

sciChartSurface.renderableSeries.add(mountainSeries);

`// Demonstrates how to create a line chart with SciChart.js using the Builder API`

const { chartBuilder, ESeriesType, EThemeProviderType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

// Create some data

let yLast = 100.0;

const xValues = [];

const yValues = [];

for (let i = 0; i <= 250; i++) {

const y = yLast + (Math.random() - 0.48);

yLast = y;

xValues.push(i);

yValues.push(y);

}

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

series: [

{

type: ESeriesType.MountainSeries,

xyData: {

xValues,

yValues

},

options: {

stroke: "#4682b4",

strokeThickness: 3,

zeroLineY: 0.0,

fill: "rgba(176, 196, 222, 0.7)", // when a solid color is required, use fill

fillLinearGradient: {

gradientStops: [

{ color: "rgba(70,130,180,0.77)", offset: 0.0 },

{ color: "rgba(70,130,180,0.0)", offset: 1 }

],

startPoint: { x: 0, y: 0 },

endPoint: { x: 0, y: 1 }

}

}

}

]

});

This results in the following output:

In the code above:

- A Mountain Series instance is created and added to the SciChartSurface.renderableSeries📘 collection.
- We set the stroke, strokethickness and fill properties
- ZeroLineY defines where the zero crossing is. The default is
`0.0`

- We assign a DataSeries - which stores the Xy data to render.

## Render a Gap in a Mountain Series

It is possible to have null points or gaps in a Mountain Series by passing a data point with a **NaN** value as the **Y** value. Please refer to the Common Series Features - Draw Gaps in Series article for more details.

## Add Point Markers onto a Mountain Series

It is possible to put scatter point markers of varying type (Ellipse, Square, Triangle, Cross, Custom) onto a Mountain Series via the PointMarker API. To learn more, see the documentation page Drawing PointMarkers on Series.

To learn more about the types of Point Marker in SciChart.js, see the Point Markers API documentation.

There is also a dedicated Scatter Series type and a Bubble Series type with some more options.

## Painting Mountain Segments with Different Colors

It is possible to define the colour of line segments as well as mountain fills individually using the PaletteProvider API.

For more info on how to do this, see the PaletteProvider - Per-point colouring of Mountain Charts documentation page.