---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/multi-axis-and-layout/polar-chart-layout
scraped_at: 2025-11-28T18:24:11.490492
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/multi-axis-and-layout/polar-chart-layout

# Polar Chart Layout

Polar charts - charts created with SciChartPolarSurface.create()📘, have a different axis layout compared to Cartesian charts. In polar charts, the axes are arranged in a circular manner, which allows for `radial`

and `angular`

measurements.

The easiest way of thinking about polar axes is this:

**Radial Axis**: Measures distance from the center of the chart up until the border of it,**like a radius**, and is typically used in the same logic an`Y Axis`

is used in 2D Cartesian charts.**Angular Axis**: Measures the angle around the center of the chart,**like a circle**, and is typically used in the same logic an`X Axis`

is used in 2D Cartesian charts.

This is just a suggestion, and in the same way you can have Vertical Charts on Cartesian surfaces, (where the traditional X and Y axes are interchanged).

### Regular vs Vertical Polar Charts

Notice the following 2 examples, where the first one is a regular, horizontal polar chart, using the `Angular`

axis as an x-axis, representing the separate columns of the chart and the `Radial`

axis as a y-axis representing the height of each column in the chart, while the second chart is a vertical polar chart, where the roles are reversed.

### Creating the 2 axes of a Polar surface in SciChart.js can be done like so:

- Creating the Radial and Angular Axes

`const { sciChartSurface, wasmContext } = await SciChartPolarSurface.create(divElementId, {`

theme: new SciChartJsNavyTheme(),

title: "Polar Chart Layout Example"

});

// Add polar axes

const angularXAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Angular,

visibleRange: new NumberRange(0, 360) // 0 to 360 degrees

});

sciChartSurface.xAxes.add(angularXAxis);

const radialYAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Radial,

visibleRange: new NumberRange(0, 10) // 0 to 10 units of height

});

sciChartSurface.yAxes.add(radialYAxis);

This will result in the following layout:

### Advanced Polar Chart Layout

For the Polar Axes, we have created a special label provider, available out of the box, called RadianLabelProvider📘, which formats the labels in radians. Make sure to read the TSDoc indications📘 before using it, and observe how the errorTolerance📘 and maxDenominator📘 pair with AxisBase.autoTicks📘 and AxisBase.majorDelta📘 to determine the label values.

- Advanced Polar Chart Layout

`const {`

SciChartPolarSurface,

PolarNumericAxis,

NumberRange,

RadianLabelProvider,

SciChartJsNavyTheme,

EPolarAxisMode,

} = SciChart;

// Create a SciChartPolarSurface

const { wasmContext, sciChartSurface } = await SciChartPolarSurface.create(divElementId, {

theme: new SciChartJsNavyTheme(),

});

// Add polar axes

const angularXAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Angular,

visibleRange: new NumberRange(0, Math.PI * 2), // 0 to 2π radians

labelProvider: new RadianLabelProvider({

maxDenominator: 6, // 6 is the maximum denominator for fractions, e.g. π/6, 2π/3, but NOT 5π/12

errorTolerance: 0.1, // since PI divisions are not exact, we allow a small error tolerance

}),

autoTicks: false, // take control over tick distance

majorDelta: Math.PI / 6, // 30 degrees in radians

totalAngle: Math.PI * 2, // this is the default value, but can be set to a different value if needed (e.g. Math.PI for a half-circle chart)

startAngle: 0, // this is the default value, but can be set to a different value if needed (e.g. Math.PI / 2 to start at 12 o'clock)

isInnerAxis: false, // whether to draw labels inside or outside of the polar chart

flippedCoordinates: false,// whether to go clockwise or counter-clockwise (default is counter-clockwise)

})

sciChartSurface.xAxes.add(angularXAxis);

const radialYAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Radial,

visibleRange: new NumberRange(0, 10),

innerRadius: 0.2, // donut hole in the middle

labelPrecision: 0,

drawMinorGridLines: false,

})

sciChartSurface.yAxes.add(radialYAxis);

And this is how it looks like:

### Partial Polar Chart Layout

By changing the totalAngle📘 property on your angular axis, you can control the sweeping angle of your polar surface, e.g. you can have half-circles, quarter-circles, etc.
It expects values in between `0`

and `Math.PI * 2`

There is also a totalAngleDegrees📘 property available for convenience, with values in between `0`

and `360`

- Partial Polar Layout

`const {`

SciChartPolarSurface,

PolarNumericAxis,

NumberRange,

RadianLabelProvider,

SciChartJsNavyTheme,

EPolarAxisMode,

} = SciChart;

// Create a SciChartPolarSurface

const { wasmContext, sciChartSurface } = await SciChartPolarSurface.create(divElementId, {

theme: new SciChartJsNavyTheme(),

});

// Add polar axes

const angularXAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Angular,

visibleRange: new NumberRange(0, Math.PI * 1.5), // 0 to 1.5π radians

labelProvider: new RadianLabelProvider({

maxDenominator: 3, // 3 is the maximum denominator for fractions, e.g. 2π/3, but NOT π/6

errorTolerance: 0.001, // since PI divisions are not exact, we allow a small error tolerance

}),

autoTicks: false, // take control over tick distance

majorDelta: Math.PI / 4, // 45 degrees in radians

totalAngle: Math.PI * 1.5,

// totalAngleDegrees: 270, // same thing as Math.PI * 1.5 radians, but in degrees

startAngle: -Math.PI / 4, // this is the default value, but can be set to a different value if needed (e.g. Math.PI / 2 to start at 12 o'clock)

// startAngleDegrees: -45, // same thing as -Math.PI/4 radians, but in degrees

isInnerAxis: false, // whether to draw labels inside or outside of the polar chart

flippedCoordinates: false, // whether to go clockwise or counter-clockwise (default is counter-clockwise)

})

sciChartSurface.xAxes.add(angularXAxis);

const radialYAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Radial,

visibleRange: new NumberRange(0, 10),

labelPrecision: 0,

drawMinorGridLines: false,

startAngle: -Math.PI / 4, // also match the radial labels to the start of the angular axis

})

sciChartSurface.yAxes.add(radialYAxis);

// optionally add some polar arcs to showcase the functionality of startAngle and totalAngle

const arcThresholds = [1.8, 2.9, Math.PI * 1.5];

const innerRadius = 7.5;

const outerRadius = 9.5;

sciChartSurface.annotations.add(

new SciChart.PolarArcAnnotation({

isEditable: true,

x1: 0,

x2: arcThresholds[0],

y1: outerRadius,

y2: innerRadius,

fill: "rgba(213, 76, 96, 0.5)",

stroke: "rgba(213, 76, 96, 1)",

strokeThickness: 3,

}),

new SciChart.PolarArcAnnotation({

isEditable: true,

x1: arcThresholds[0],

x2: arcThresholds[1],

y1: outerRadius,

y2: innerRadius,

fill: "rgba(250, 252, 90, 0.5)",

stroke: "rgba(250, 252, 90, 1)",

strokeThickness: 3,

}),

new SciChart.PolarArcAnnotation({

isEditable: true,

x1: arcThresholds[1],

x2: arcThresholds[2],

y1: outerRadius,

y2: innerRadius,

fill: "rgba(136, 242, 136, 0.5)",

stroke: "rgba(136, 242, 136, 1)",

strokeThickness: 3,

})

);

Resulting in the following layout:

### More Tips:

If using PolarZoomExtentsModifier📘 on a polar chart, you will likely want to set zoomExtentsToInitialRange📘 to `true`

, so that the zoom extents modifier will not try and squash the first and last data points together.

If the gridlines are too often for your liking, you can either:

- Set drawMinorGridLines📘:
`false`

on any axis - Or set minorsPerMajor📘 to something lower than
`5`

(the default). Use`2`

for a minimal look.

- You can also customize the
`color`

,`thickness`

and`strokeDashArray`

of both major and minor gridlines via MajorGridLineStyle📘 and MinorGridLineStyle📘, both having the TGridLineStyle📘 type.