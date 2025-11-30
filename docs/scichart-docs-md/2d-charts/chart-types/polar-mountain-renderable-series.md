---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/polar-mountain-renderable-series
scraped_at: 2025-11-28T18:24:40.902610
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/polar-mountain-renderable-series

# The Polar Mountain Chart Type

The PolarMountainRenderableSeries📘 is a type of renderable series that displays data in a polar mountain format.

tip

The JavaScript Polar Mountain Chart can be found in the SciChart.Js Examples Suite > Polar Mountain Chart on Github, or our live demo at scichart.com/demo.

Above: The JavaScript Polar Mountain Series Chart example from the SciChart.js Demo

## Properties

Some of IPolarMountainRenderableSeriesOptions📘's key properties include:

- dataSeries📘 - The XyDataSeries📘 containing
`xValues`

and`yValues`

arrays - stroke📘 - Stroke color for the line
- strokeThickness📘 - Thickness of the line
- interpolateLine📘 - When true, line segments draw as arcs instead of straight lines
- clipToTotalAngle📘 - When true, clips data outside the total angle range
- pointMarker📘 - Optional markers to display at data points
- paletteProvider📘 - Custom coloring provider for dynamic styling
- dataLabels📘 - Configuration for optional data labels on points

## Create a Basic Polar Mountain Series

To create a Javascript Polar Mountain Series📘 with SciChart.js, use the following code:

- Creating a Polar Mountain Series

`// Demonstrates how to create a basic polar mountain chart using SciChart.js`

const {

SciChartPolarSurface,

SciChartJsNavyTheme,

PolarNumericAxis,

PolarMountainRenderableSeries,

EPolarAxisMode,

EAxisAlignment,

NumberRange,

XyDataSeries,

EPolarLabelMode

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { sciChartSurface, wasmContext } = await SciChartPolarSurface.create(divElementId, {

theme: new SciChartJsNavyTheme(),

});

const angularXAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Angular,

axisAlignment: EAxisAlignment.Top,

visibleRange: new NumberRange(0, 19),

polarLabelMode: EPolarLabelMode.Parallel,

});

sciChartSurface.xAxes.add(angularXAxis);

const radialYAxis = new PolarNumericAxis(wasmContext, {

axisAlignment: EAxisAlignment.Right,

polarAxisMode: EPolarAxisMode.Radial,

visibleRange: new NumberRange(0, 8),

labelPrecision: 0,

});

sciChartSurface.yAxes.add(radialYAxis);

const polarMountain = new PolarMountainRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: Array.from({ length: 20 }, (_, i) => i),

yValues: Array.from({ length: 20 }, (_, i) => Math.sin(i) * 3 + 4),

}),

stroke: "pink",

strokeThickness: 4,

interpolateLine: false, // set to true for rounded lines

});

sciChartSurface.renderableSeries.add(polarMountain);

In the code above:

- We create a PolarMountainRenderableSeries📘 instance and append it to the renderableSeries collection.
- Add an XyDataSeries📘 to the series, which stores the Xy data to render.
- Note that the line wraps for 1 and a half turns around the angular axis, since it calculates xValues as
`xVal % visibleRange.max`

and visible range is fixed to (0, 8)