---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/polar-line-renderable-series
scraped_at: 2025-11-28T18:24:39.644866
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/polar-line-renderable-series

# The Polar Line Chart Type

The PolarLineRenderableSeries📘 creates lines in a polar coordinate system, connecting data points with either straight line segments or interpolated arcs. This chart type is ideal for visualizing cyclical data, radar charts, or any data that benefits from a circular representation.

tip

The JavaScript Polar Line Chart can be found in the SciChart.Js Examples Suite > Polar Line Chart on Github, or our live demo at scichart.com/demo.

Above: The JavaScript Polar Line Series Chart example from the SciChart.js Demo

## Properties

Some of IPolarLineRenderableSeriesOptions📘's key properties include:

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

## Examples

### Basic Polar Line Series

`// Demonstrates how to create a basic polar line chart using SciChart.js`

const {

SciChartPolarSurface,

SciChartJsNavyTheme,

PolarNumericAxis,

PolarLineRenderableSeries,

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

visibleRange: new NumberRange(0, 12),

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

const polarLine = new PolarLineRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: Array.from({ length: 20 }, (_, i) => i),

yValues: Array.from({ length: 20 }, (_, i) => 1 + i / 3)

}),

stroke: "pink",

strokeThickness: 4,

interpolateLine: false, // set to true for rounded lines

clipToTotalAngle: false // set to true to clip anything outside the total angle

});

sciChartSurface.renderableSeries.add(polarLine);

In the code above:

- A PolarLineRenderableSeries📘 instance is created and added to the
`sciChartSurface.renderableSeries`

collection - The clipToTotalAngle📘 is kept as
`false`

to allow wrapping

### PaletteProvider for Dynamic Line Coloring

By extending DefaultPaletteProvider📘 you can create custom coloring for your Polar Line Series, achieving dynamic styling based on data values:

`// Demonstrates how to create an interpolated polar line chart using SciChart.js`

import {

SciChartPolarSurface,

DefaultPaletteProvider,

PolarNumericAxis,

PolarLineRenderableSeries,

EPolarAxisMode,

EAxisAlignment,

SciChartJsNavyTheme,

NumberRange,

XyDataSeries,

Thickness,

EStrokePaletteMode,

parseColorToUIntArgb,

IPointMetadata

} from "scichart";

export async function PolarLinePaletteProvider(divElementId: string) {

const { sciChartSurface, wasmContext } = await SciChartPolarSurface.create(divElementId, {

padding: Thickness.fromNumber(30),

theme: new SciChartJsNavyTheme(),

});

const angularXAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Angular,

axisAlignment: EAxisAlignment.Top,

visibleRange: new NumberRange(0, 12),

});

sciChartSurface.xAxes.add(angularXAxis);

const radialYAxis = new PolarNumericAxis(wasmContext, {

axisAlignment: EAxisAlignment.Right,

polarAxisMode: EPolarAxisMode.Radial,

visibleRange: new NumberRange(0, 8),

});

sciChartSurface.yAxes.add(radialYAxis);

class ThresholdLinePaletteProvider extends DefaultPaletteProvider {

rule: (yValue: number, xValue: number) => boolean;

stroke2: number;

constructor(rule: (yValue: number, xValue: number) => boolean, stroke2: string) {

super();

this.rule = rule;

this.stroke2 = parseColorToUIntArgb(stroke2);

this.strokePaletteMode = EStrokePaletteMode.SOLID;

}

overrideStrokeArgb(xValue: number, yValue: number, index: number, opacity: number, metadata: IPointMetadata) {

return this.rule(yValue, xValue) // when rule is met, return the stroke color

? this.stroke2

: undefined;

}

}

const polarLine = new PolarLineRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: Array.from({ length: 34 }, (_, i) => i),

yValues: Array.from({ length: 34 }, (_, i) => 1 + i / 5)

}),

stroke: "#00AA00", // Stroke color used when overrideStrokeArgb returns `undefined`

strokeThickness: 5,

interpolateLine: true,

paletteProvider: new ThresholdLinePaletteProvider(

(yValue, xValue) => (Math.floor(xValue / 3) % 2 === 0), // set the rule for threshold

"#FFFFFF",

),

});

sciChartSurface.renderableSeries.add(polarLine);

tip

Learn more about the Palette Provider API - Polar Line Series.