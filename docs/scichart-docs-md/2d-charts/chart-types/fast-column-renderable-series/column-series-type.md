---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/fast-column-renderable-series/column-series-type
scraped_at: 2025-11-28T18:24:26.922149
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/fast-column-renderable-series/column-series-type

# The Column Series Type

Column Series can be created using the FastColumnRenderableSeries📘 type.

The JavaScript Column Chart Example can be found in the SciChart.Js Examples Suite > Column Chart on Github, or our live demo at scichart.com/demo.

## Create a Column Series

To create a Javascript Column Chart with SciChart.js, use the following code:

- TS
- Builder API (JSON Config)

`// Demonstrates how to create a Column chart with SciChart.js`

const {

SciChartSurface,

NumericAxis,

FastColumnRenderableSeries,

XyDataSeries,

SciChartJsNavyTheme,

GradientParams,

EDataPointWidthMode,

Point,

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

// Create and add a column series

const columnSeries = new FastColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],

yValues: [0.1, 0.2, 0.4, 0.8, 1.1, 1.5, 2.4, 4.6, 8.1, 11.7, 14.4, 16, 13.7, 10.1, 6.4, 3.5, 2.5, 1.4, 0.4, 0.1]

}),

// When solid fill required, use fill

fill: "rgba(176, 196, 222, 0.5)",

// When gradient fill required, use fillGradient

fillLinearGradient: new GradientParams(new Point(0, 0), new Point(0, 1), [

{ color: "rgba(70,130,180,0.77)", offset: 0 },

{ color: "rgba(70,130,180,0.0)", offset: 1 }

]),

stroke: "#FFFFFF77",

strokeThickness: 2,

cornerRadius: 4, // optional cornerradius

// Defines the relative width of columns

dataPointWidth: 0.7,

dataPointWidthMode: EDataPointWidthMode.Relative

});

sciChartSurface.renderableSeries.add(columnSeries);

`// Demonstrates how to create a Column chart with SciChart.js using the Builder API`

const { chartBuilder, ESeriesType, EThemeProviderType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

series: [

{

type: ESeriesType.ColumnSeries,

xyData: {

xValues: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],

yValues: [0.1, 0.2, 0.4, 0.8, 1.1, 1.5, 2.4, 4.6, 8.1, 11.7, 14.4, 16, 13.7, 10.1, 6.4, 3.5, 2.5, 1.4, 0.4, 0.1]

},

options: {

fill: "rgba(176, 196, 222, 0.5)",

stroke: "rgba(176, 196, 222, 1)",

strokeThickness: 2,

dataPointWidth: 0.7

}

}

]

});

This results in the following output:

In the code above:

- A Column Series instance is created and added to the SciChartSurface.renderableSeries📘 collection.
- We set the stroke, strokethickness and fill properties
- We set FastColumnRenderableSeries.dataPointWidth📘 - which defines the fraction of width to occupy
- We assign a FastColumnRenderableSeries.dataSeries📘 - which stores the Xy data to render.

## Render a Gap in a Column Series

It is possible to have null points or gaps in a Column Series by passing a data point with a **NaN** value as the **Y** value. Please refer to the Common Series Features - Draw Gaps in Series article for more details.

## Add Point Markers onto a Column Series

It is possible to put scatter point markers of varying type (Ellipse, Square, Triangle, Cross, Custom) onto a Column Series via the PointMarker API. To learn more, see the documentation page Drawing PointMarkers on Series.

To learn more about the types of Point Marker in SciChart.js, see the Point Markers API documentation.

There is also a dedicated Scatter Series type and a Bubble Series type with some more options.

## Painting Columns with Different Colors

It is possible to define the colour of column stroke & fill individually using the PaletteProvider API.

For more info on how to do this, see the PaletteProvider - Per-point colouring of Column Charts documentation page.