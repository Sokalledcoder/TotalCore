---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/polar-text-renderable-series
scraped_at: 2025-11-28T18:24:42.274782
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/polar-text-renderable-series

# The Polar Text Series Type

There are several ways to add text to a SciChart.js polar chart. These include the TextAnnotation / NativeTextAnnotation, renderable series DataLabels and also the PolarTextRenderableSeries (Text Series).

Text Series should be used when you want to render a lot of text, not necessarily at X,Y positions of other chart series. The PolarTextRenderableSeries📘 is an extension of FastTextRenderableSeries📘, so there is some

The JavaScript Text / Word Cloud Chart Example can be found in the SciChart.Js Examples Suite > Text Series Chart on Github, or our live demo at scichart.com/demo

## Creating a Polar Text Series

To create a chart using PolarTextRenderableSeries📘 use the following code.

**Note** that it is required to set `style: { fontSize: X }`

and `color`

in the dataLabels property in order for text to be drawn.

PolarTextRenderableSeries uses the special XyTextDataSeries📘 which allows you to supply text values directly on the dataSeries, rather than having to use metadata.

- TS

`// Demonstrates how to create a basic polar triangle series chart using SciChart.js`

const {

SciChartPolarSurface,

PolarNumericAxis,

PolarTextRenderableSeries,

EPolarAxisMode,

XyTextDataSeries,

SciChartJsNavyTheme,

NumberRange

} = SciChart;

// or, for npm, import { SciChartPolarSurface, ... } from "scichart"

const { sciChartSurface, wasmContext } = await SciChartPolarSurface.create(divElementId, {

theme: new SciChartJsNavyTheme(),

});

const radialYAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Radial,

visibleRange: new NumberRange(0, 7),

startAngle: Math.PI,

});

sciChartSurface.yAxes.add(radialYAxis);

const angularXAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Angular,

visibleRange: new NumberRange(1, 8),

flippedCoordinates: true,

startAngle: Math.PI,

});

sciChartSurface.xAxes.add(angularXAxis);

const textSeries = new PolarTextRenderableSeries(wasmContext, {

dataSeries: new XyTextDataSeries(wasmContext, {

xValues: [1, 2, 3, 4, 5, 6],

yValues: [4, 3, 4, 4, 3, 3],

textValues: ["This", "text", "is", "drawn", "using", "PolarTextRenderableSeries"]

}),

// font size & color are required for text to be drawn

dataLabels: {

style: {

fontSize: 18

},

color: "#ffffff"

}

});

sciChartSurface.renderableSeries.add(textSeries);

This results in the following output: