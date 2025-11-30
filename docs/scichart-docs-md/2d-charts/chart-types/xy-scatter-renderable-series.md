---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/xy-scatter-renderable-series
scraped_at: 2025-11-28T18:24:46.296473
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/xy-scatter-renderable-series

# The Scatter Series Type

Scatter Series can be created using the XyScatterRenderableSeries📘 type.

The JavaScript Scatter Chart Example can be found in the SciChart.Js Examples Suite > Scatter Chart on Github, or our live demo at scichart.com/demo.

## Create a Scatter Series

To create a Javascript Scatter Chart with SciChart.js, use the following code:

- TS
- Builder API (JSON Config)

`// Demonstrates how to create a scatter chart with SciChart.js`

const {

SciChartSurface,

NumericAxis,

XyDataSeries,

XyScatterRenderableSeries,

EllipsePointMarker,

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

yValues.push(0.2 * Math.sin(i * 0.1) - Math.cos(i * 0.01));

}

const scatterSeries = new XyScatterRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues,

yValues

}),

pointMarker: new EllipsePointMarker(wasmContext, {

width: 7,

height: 7,

strokeThickness: 2,

fill: "steelblue",

stroke: "LightSteelBlue"

})

});

sciChartSurface.renderableSeries.add(scatterSeries);

`// Demonstrates how to create a scatter with SciChart.js using the Builder API`

const { chartBuilder, ESeriesType, EPointMarkerType, EThemeProviderType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const xValues = [];

const yValues = [];

for (let i = 0; i < 100; i++) {

xValues.push(i);

yValues.push(0.2 * Math.sin(i * 0.1) - Math.cos(i * 0.01));

}

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

series: [

{

type: ESeriesType.ScatterSeries,

xyData: {

xValues,

yValues

},

options: {

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

This results in the following:

In the code above:

- A Scatter Series instance is created and added to the SciChartSurface.renderableSeries📘 collection.
- We set a PointMarker📘. Several types such as Ellipse, Triangle, Cross and Custom are available (see here for more info)
- We assign a DataSeries - which stores the Xy data to render.

## Render a Gap in a Scatter Series

It is possible to have null points or gaps in a Scatter Series by passing a data point with a **NaN** value as the **Y** value. Or, by simply skipping a point if using a value-axis. Please refer to the Common Series Features - Draw Gaps in Series article for more details.

## Drawing Last Point only in a Scatter Series

New to SciChart.js v3.2! The PointMarker type has a property isLastPointOnly📘. When true, only the last point of a scatter series is drawn. This can be useful to highlight a point in say a sweeping ECG chart.

## Different Point-Markers on a Scatter Series

Every data point of a Scatter Series is marked with a PointMarker📘. Several different types of PointMarker are available in SciChart.js.

To learn more about the types of Point Marker in SciChart.js, see the Point Markers API documentation.

There is also a TypeScript example of custom pointmarkers in the SciChart.js Demo.

Finally, there is a dedicated Bubble Series type with some more options such as per-point sizing.

## Painting Scatter Points with Different Colors

It is possible to define the colour of PointMarkers individually using the PaletteProvider API.

For more info on how to do this, see the PaletteProvider - Per-point colouring of Scatter Charts documentation page.