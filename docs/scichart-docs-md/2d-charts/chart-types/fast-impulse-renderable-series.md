---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/fast-impulse-renderable-series
scraped_at: 2025-11-28T18:24:27.948545
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/fast-impulse-renderable-series

# The Lollipop (Impulse or Stem) Chart Type

Lollipop Charts, otherwise known as Impulse or Stem charts, can be created using the FastImpulseRenderableSeries📘 type.

The JavaScript Impulse Series Example can be found in the SciChart.Js Examples Suite on Github, or our live demo at scichart.com/demo.

## Create an Impulse Series

To create a Javascript Impulse Chart with SciChart.js, use the following code:

- TS
- Builder API (JSON Config)

`// Demonstrates how to create an Impulse (or Stem, Lollipop) chart with SciChart.js`

const {

SciChartSurface,

NumericAxis,

FastImpulseRenderableSeries,

XyDataSeries,

EllipsePointMarker,

SciChartJsNavyTheme,

NumberRange

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { growBy: new NumberRange(0, 0.1) }));

// Create some data

const xValues = [];

const yValues = [];

for (let i = 0; i < 100; i++) {

xValues.push(i);

yValues.push(Math.sin(i * 0.2) * Math.log(i / 100));

}

// Create and add a column series

const impulseSeries = new FastImpulseRenderableSeries(wasmContext, {

fill: "rgba(176, 196, 222, 0.5)",

stroke: "rgba(176, 196, 222, 1)",

strokeThickness: 2,

size: 10,

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues }),

// Optional: define the pointmarker type. Note: size, stroke, fill properties are on the parent series

pointMarker: new EllipsePointMarker(wasmContext)

});

sciChartSurface.renderableSeries.add(impulseSeries);

`// Demonstrates how to create a line chart with SciChart.js using the Builder API`

const { chartBuilder, ESeriesType, EThemeProviderType, EPointMarkerType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

// Create some data

const xValues = [];

const yValues = [];

for (let i = 0; i < 100; i++) {

xValues.push(i);

yValues.push(Math.sin(i * 0.2) * Math.log(i / 100));

}

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

series: [

{

type: ESeriesType.ImpulseSeries,

xyData: {

xValues,

yValues

},

options: {

fill: "rgba(176, 196, 222, 0.5)",

stroke: "rgba(176, 196, 222, 1)",

strokeThickness: 2,

size: 10,

pointMarker: { type: EPointMarkerType.Ellipse }

}

}

]

});

This results in the following output:

In the code above:

- A Impulse Series instance is created and added to the
`SciChartSurface.renderableSeries`

collection. - We set the fill📘 property that controls the color of connector and point of each dataset
- We can update the size of each point by updating size📘 property (default value is
`10.0`

) - We assign a FastImpulseRenderableSeries.dataSeries📘 - which stores the Xy data to render.

## Setting the PointMarker on an Impulse Series

Every data point of an Impulse Series is marked with a PointMarker📘. To change the pointmarker type, or size, use the following code. Note that the fill, size property on `FastImpulseRenderableSeries`

overrides the width, height, fill, stroke on the `TrianglePointMarker`

.

`const impulseSeries = new FastImpulseRenderableSeries(wasmContext, {`

fill: "#26c6da",

strokeThickness: 1,

dataSeries,

pointMarker: new TrianglePointMarker(wasmContext),

size: 10,

});

Different pointmarkers are supported including Ellipse, Box, Triangle, Cross or custom markers. See the Scatter Chart documentation for more information on supported pointmarkers.

## Render a Gap in an Impulse Series

It is possible to have null points or gaps in a Impulse Series by passing a data point with a **NaN** value as the **Y** value. Please refer to the Common Series Features - Draw Gaps in Series article for more details.

## Painting Impulse Series Points with Different Colors

It is possible to define the colour individual datapoints differently using the PaletteProvider API.

For more info on how to do this, see the PaletteProvider - Per-point colouring of Impulse Charts documentation page.