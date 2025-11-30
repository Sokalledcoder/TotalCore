---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/polar-gauge-chart
scraped_at: 2025-11-28T18:24:40.079209
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/polar-gauge-chart

# The Polar Gauge Chart Type

The Polar Gauge Chart is used to visualize data in a polar coordinate system as a circular gauge or meter, where values are represented by angular position and radial distance. This chart type is ideal for displaying progress indicators, performance metrics, or any data that benefits from a circular visualization.

The JavaScript Polar Gauge Chart can be found in the SciChart.Js Examples Suite > Polar Gauge Chart on Github, or our live demo at scichart.com/demo.

In SciChart.js, gauge charts are not specific renderable series, and can be created using either PolarArcAnnotation📘 for simple arc-based gauges or PolarColumnRenderableSeries📘 for column-based gauges. Both approaches offer different advantages depending on your specific use case.

## Properties

Polar gauge charts typically consist of:

**Angular Axis**- PolarNumericAxis📘 / PolarCategoryAxis📘 with polarAxisMode.Angular📘, which controls the sweep angle and range of the gauge**Radial Axis**- PolarNumericAxis📘 / PolarCategoryAxis📘 with polarAxisMode.Radial📘, which defines the radial scale and range**Background Elements**- Arcs / Columns for optional visual indicators showing the full range as a gradient**Value Elements**- The actual data representation (arc or column)**Annotations**- Additional elements like pointers, centered dataLabels

## Examples

### Basic Gauge using PolarArcAnnotation

The PolarArcAnnotation📘 approach is ideal for simple gauges with smooth arc representations:

`// Demonstrates how to create a gauge chart using ArcAnnotation & PolarPointerAnnotation using SciChart.js`

const {

SciChartPolarSurface,

SciChartJsNavyTheme,

NumberRange,

PolarArcAnnotation,

PolarNumericAxis,

EPolarAxisMode,

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await SciChartPolarSurface.create(divElementId, {

theme: new SciChartJsNavyTheme(),

});

// The gauge angle

const gaugeTotalAngle = Math.PI * 1.2;

const gaugeRange = new NumberRange(0, 100); // the range of the gauge

// Add the axes

const angularXAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Angular,

visibleRange: gaugeRange, // 0 - 100

flippedCoordinates: true, // go clockwise

totalAngle: gaugeTotalAngle,

startAngle: (Math.PI - gaugeTotalAngle) / 2, // to center the bottom gap

isVisible: false,

});

sciChartSurface.xAxes.add(angularXAxis);

const radialYAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Radial,

visibleRange: new NumberRange(0, 10), // 0 - 10

isVisible: false,

});

sciChartSurface.yAxes.add(radialYAxis);

// (optional) add a gray background Arc

const backgroundArc = new PolarArcAnnotation({

y1: 10, // outer radius of the arc relative to the center of the gauge

y2: 8, // inner radius of the arc

x1: gaugeRange.min, // start angle -> 0

x2: gaugeRange.max, // end angle -> 100

fill: "#88888822",

strokeThickness: 0

});

// The Value Arc

const valueArc = new PolarArcAnnotation({

y1: 10, // outer radius

y2: 8, // inner radius

x1: gaugeRange.min, // start angle -> 0

x2: 50 + Math.random() * 30, // current value (end of arc)

fill: "#3388FF",

stroke: "#FFFFFF",

strokeThickness: 3

});

sciChartSurface.annotations.add(backgroundArc, valueArc);

In the code above:

- We configure the angular axis's totalAngle📘 property to define the gauge's sweep angle.
- Also calculate the startAngle📘 property to set the starting point of the gauge.
- Both axes have isVisible📘 set to
`false`

to hide gridlines, ticks, and labels for a clean gauge appearance - An optional gray
**background arc**shows the full potential range of the gauge - The
**value arc**represents the current data value as such: PolarArcAnnotation📘's`x1`

,`x2`

properties to set the start / end angle, and`y1`

,`y2`

properties to set the outer and inner radius (manipulating the arc thickness)

### Basic Gauge using PolarColumnRenderableSeries

The PolarColumnRenderableSeries📘 approach offers more flexibility for data-driven gauges and gradient fills:

`// (optional) add a gray column to show the potential full range of the gauge`

const grayColumn = new PolarColumnRenderableSeries(wasmContext, {

dataSeries: new XyxyDataSeries(wasmContext, {

y1Values: [10], // outer radius

yValues: [8], // inner radius

x1Values: [gaugeRange.max], // start of visible range -> 0

xValues: [gaugeRange.min], // end of visible range -> 100

}),

columnXMode: EColumnMode.StartEnd,

fill: "#88888844",

strokeThickness: 0,

});

sciChartSurface.renderableSeries.add(grayColumn);

// add the value column:

const columnSeries = new PolarColumnRenderableSeries(wasmContext, {

dataSeries: new XyxyDataSeries(wasmContext, {

y1Values: [10], // outer radius

yValues: [8], // inner radius

x1Values: [gaugeRange.min], // start of the gauge -> 0

xValues: [50 + Math.random() * 40], // current value of gauge

}),

columnXMode: EColumnMode.StartEnd,

stroke: "#FFFFFF",

strokeThickness: 3,

fillLinearGradient: new GradientParams(

new Point(0, 0),

new Point(1, 0),

[

{ offset: 0, color: "#AA2200" },

{ offset: 1, color: "#FFDD00" },

]

),

});

sciChartSurface.renderableSeries.add(columnSeries);

In the code above:

- We use XyxyDataSeries📘 to define both the radial dimensions (
`yValues`

,`y1Values`

) and angular range (`xValues`

,`x1Values`

) - The columnXMode📘 is set to EColumnMode.StartEnd📘 for precise control over the gauge arc
- This approach is better suited for gauges that need to display multiple data points or dynamic updates

### Advanced Multi-Threshold Gauge

For more complex gauge requirements with multiple thresholds, indicators, and styling:

`const GAUGE_THRESHOLDS = [50, 75, 100];`

const GAUGE_COLORS = [ "#DD2222", "#FFCC22", "#22AA22"];

const GAUGE_VALUE = 50 + Math.random() * 30; // random val for the gauge

// add thin arcs, outlining the thresholds of the gauge

GAUGE_THRESHOLDS.forEach((threshold, i) => {

sciChartSurface.annotations.add(

new PolarArcAnnotation({

y1: 10, // outer radius

y2: 9.7, // inner radius

x1: GAUGE_THRESHOLDS[i - 1] || gaugeRange.min, // start angle -> 0 or previous threshold

x2: threshold, // end angle -> current threshold

fill: GAUGE_COLORS[i],

strokeThickness: 0

})

);

});

// (optional) gray background Arc

const backgroundArc = new PolarArcAnnotation({

y1: 9.6, // outer radius

y2: 7, // inner radius

x1: gaugeRange.min, // start angle -> 0

x2: gaugeRange.max, // end angle -> 100

fill: "#88888822",

strokeThickness: 0

});

// The Value Arc

const valueArc = new PolarArcAnnotation({

y1: 9.3, // outer radius

y2: 7, // inner radius

x1: gaugeRange.min, // start angle -> 0

x2: GAUGE_VALUE, // current value (end of arc)

strokeThickness: 0,

// smart fill color based on the threshold it's in

fill: GAUGE_COLORS.find((_, i) => GAUGE_VALUE <= GAUGE_THRESHOLDS[i])

});

sciChartSurface.annotations.add(backgroundArc, valueArc);

// For more details, you can use either:

// 1. PolarPointerAnnotation to show the current value

const arrowPointer = new PolarPointerAnnotation({

x1: GAUGE_VALUE, // pointer angle

y1: 7, // pointer length

xCoordinateMode: ECoordinateMode.DataValue,

yCoordinateMode: ECoordinateMode.DataValue,

pointerStyle: {

baseSize: 0.03,

stroke: "#F00",

fill: "#F00",

backExtensionSize: 0.3, // how much the pointer extends back

},

pointerCenterStyle: {

size: 0.2, // relative to the pointer length

fill: "#111",

}

});

sciChartSurface.annotations.add(arrowPointer);

// 2. TextAnnotation to show the value in the center of the gauge

const centeredText = new TextAnnotation({

x1: 0,

y1: 0, // centered at (0, 0)

xCoordinateMode: ECoordinateMode.DataValue,

yCoordinateMode: ECoordinateMode.DataValue,

text: `${GAUGE_VALUE.toFixed(2)}%`,

fontSize: 50,

textColor: GAUGE_COLORS.find((_, i) => GAUGE_VALUE <= GAUGE_THRESHOLDS[i]),

horizontalAnchorPoint: EHorizontalAnchorPoint.Center,

verticalAnchorPoint: EVerticalAnchorPoint.Center,

});

// sciChartSurface.annotations.add(centeredText); // uncomment to see it

In the code above:

**Multiple threshold arcs📘**are created using different colors to represent various performance zones**Smart color selection**automatically chooses the appropriate color based on the current value and thresholds- A PolarPointerAnnotation📘 provides a precise indicator of the current value
- Optional TextAnnotation📘 or PolarPointerAnnotation📘 can further highlight the numeric value in the center

## Choosing the Right Approach

**Use PolarArcAnnotation📘 when:**

- Creating simple, static gauges
- The gauge represents a single value
- Minimal code complexity is preferred

**Use PolarColumnRenderableSeries📘 when:**

- You need data-driven gauges
- Multiple data points need to be displayed
- Dynamic updates are required
- You want to leverage series-level features like fillLinearGradient📘, paletteProviders📘 or animation📘

Both approaches can be combined in the same chart to create sophisticated gauge visualizations with multiple indicators, thresholds, and interactive elements.