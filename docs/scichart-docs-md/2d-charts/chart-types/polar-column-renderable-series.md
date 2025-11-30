---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/polar-column-renderable-series
scraped_at: 2025-11-28T18:24:39.764600
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/polar-column-renderable-series

# The Polar Column Chart Type

The PolarColumnRenderableSeries📘 creates columns in a polar coordinate system, displaying data as vertical bars positioned at specific angles and radial distances from the center, or as angular bars drawn around the center. This chart type is ideal for visualizing cyclic data or data with angular relationships.

The JavaScript Polar Column Chart can be found in the SciChart.Js Examples Suite > Polar Column Chart on Github, or our live demo at scichart.com/demo.

## Properties

Some of IPolarColumnRenderableSeriesOptions📘's key properties include:

- dataSeries📘 - The XyDataSeries📘, XyxDataSeries📘 or XyxyDataSeries📘 defining the data points of the columns.
- fill📘 - Fill color for the columns
- stroke📘 - Stroke color for column borders
- strokeThickness📘 - Thickness of the column borders
- dataPointWidth📘 - Width of each column
- dataPointWidthMode📘 - How the
`dataPointWidth`

is applied, see EDataPointWidthMode📘 for all options. - columnXMode📘 - How x values are interpreted for column positioning. See EColumnMode📘 for more info.
- defaultY1📘 - Sets the zero line - where the column starts at defaulting at
`0`

, but is only needed for XyDataSeries📘 - dataLabels📘 - Configuration for data labels on columns
- paletteProvider📘 - Custom coloring provider for dynamic styling

## Examples

### Basic Angular Polar Column Series

`// Demonstrates how to create a basic polar column chart using SciChart.js`

const {

SciChartPolarSurface,

PolarNumericAxis,

SciChartJsNavyTheme,

PolarColumnRenderableSeries,

EPolarAxisMode,

EAxisAlignment,

EPolarLabelMode,

NumberRange,

XyDataSeries,

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { sciChartSurface, wasmContext } = await SciChartPolarSurface.create(divElementId, {

theme: new SciChartJsNavyTheme(),

});

const angularXAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Angular, // Angular == "goes around the center, drawn by arcs"

axisAlignment: EAxisAlignment.Top,

visibleRange: new NumberRange(0, 20),

flippedCoordinates: true, // go clockwise

});

sciChartSurface.xAxes.add(angularXAxis);

const radialYAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Radial, // Radial == "goes from center out, drawn by straight lines"

axisAlignment: EAxisAlignment.Right,

visibleRange: new NumberRange(0, 6),

drawLabels: false, // don't draw labels

innerRadius: 0.1, // donut hole

});

sciChartSurface.yAxes.add(radialYAxis);

const polarColumn = new PolarColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: Array.from({ length: 20 }, (_, i) => i),

yValues: Array.from({ length: 20 }, (_, i) => Math.random() * 5 + 1),

}),

stroke: "white",

fill: "#0088FF66",

strokeThickness: 2,

dataPointWidth: 1,

dataLabels: { // optionally - add data labels

color: "white",

style: {

fontSize: 14,

fontFamily: "Default",

},

polarLabelMode: EPolarLabelMode.Parallel,

},

});

sciChartSurface.renderableSeries.add(polarColumn);

In the code above:

- A PolarColumnRenderableSeries📘 instance is created and added to the
`sciChartSurface.renderableSeries`

collection. - We assign an XyDataSeries📘 which stores X and Y value arrays.
- We set the stroke📘, fill📘, strokeThickness📘, and dataPointWidth📘 properties.
- Optional dataLabels📘 are configured to display values on each column.

### Polar Radial Polar Column Series

The same renderable series can be used as radial columns by swapping the axis configurations. This creates columns that extend radially outward from the center:

`const radialXAxis = new PolarNumericAxis(wasmContext, {`

polarAxisMode: EPolarAxisMode.Radial, // radial axis -> xAxis

axisAlignment: EAxisAlignment.Right,

innerRadius: 0.1,

startAngle: 0,

});

sciChartSurface.xAxes.add(radialXAxis);

const angularYAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Angular, // angular axis -> yAxis

axisAlignment: EAxisAlignment.Top,

visibleRange: new NumberRange(0, 10),

useNativeText: true,

startAngle: 0,

totalAngle: Math.PI, // 180 degrees

flippedCoordinates: true, // go clockwise

});

sciChartSurface.yAxes.add(angularYAxis);

// The Polar renderable series do not require extra config, only control the Angular / Radial look.

const polarColumn = new PolarColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: [1, 2, 3, 4, 5, 6],

yValues: [6.6, 8.7, 3.5, 5.7, 3.8, 6.8]

}),

stroke: "white",

fill: "#0088FF66",

strokeThickness: 2,

dataPointWidth: 0.8,

dataLabels: { // optionally - add data labels

color: "white",

style: {

fontSize: 14,

},

polarLabelMode: EPolarLabelMode.Parallel,

labelYPositionMode: EColumnDataLabelPosition.Outside,

},

});

sciChartSurface.renderableSeries.add(polarColumn);

In the code above:

- The xAxis📘 is configured with EPolarAxisMode.Radial📘 to control the radial positioning.
- The yAxis📘 is configured with EPolarAxisMode.Angular📘 to control the angular positioning.
- The axisAlignment📘 is also swapped.
- (optional) The angular axis now has 180 degrees (1 * PI radians), meaning a half-circle, due to the totalAngle📘.
- (optional) The angular axis also grows clockwise, via flippedCoordinates📘.

### Column Mode Configuration

The columnXMode📘 property controls how columns are positioned and sized along the X-axis:

`const polarColumn = new PolarColumnRenderableSeries(wasmContext, {`

dataSeries: new XyxDataSeries(wasmContext, {

xValues: [ 1, 2, 3, 5, 6.5, 9.5],

x1Values: [1.5, 2.5, 4.5, 6, 9, 10 ], // columns go from 1 -> 1.5 // 2 -> 2.5, etc

yValues: [6.6, 8.7, 3.5, 5.7, 3.8, 6.8], // dictates the height of the column

}),

columnXMode: EColumnMode.StartEnd, // go from start to end (x to x1)

stroke: "white",

fill: "#0088FF66",

strokeThickness: 2,

});

sciChartSurface.renderableSeries.add(polarColumn);

In the code above:

- We use an XyxDataSeries📘 with
`xValues`

,`x1Values`

, and`yValues`

arrays. - The columnXMode📘 is set to EColumnMode.StartEnd📘 to define column start and end positions.
- Each column extends from its
`xValue`

to its`x1Value`

, allowing for variable-width columns.

- Start📘, Mid📘 - work with XyDataSeries📘
- StartEnd📘, StartWidth📘, and MidWidth📘 - require XyxDataSeries📘 or XyxyDataSeries📘

### PaletteProvider for Polar Column Series

By extending DefaultPaletteProvider📘 you can create a custom palette for your Polar Column Series, to achieve dynamic coloring based on data values. See more about this topic here Palette Provider API - Polar Column Series.