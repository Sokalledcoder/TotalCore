---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-types/polar-numeric-axis
scraped_at: 2025-11-28T18:24:08.795551
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-types/polar-numeric-axis

# The Polar Numeric Axis

The PolarNumericAxis📘 is a specialized axis type for polar charts (radar, spider, and polar area plots) in SciChart.js.

Polar axes map values either around a circle (**Angular**, or "theta") or outward from the center (**Radial**, or "r"). Their unique properties make them essential for any circular, gauge, or radar visualization.

## What Makes Polar Axes Special?

**Dual Modes using the PolarNumericAxis.polarAxisMode📘 to either:**- EPolarAxisMode.Angular📘: The axis is mapped to sweeps (angles) around the circle. Typically the
**xAxis**. - EPolarAxisMode.Radial📘: The axis is mapped from the center outward. Typically the
**yAxis**.

- EPolarAxisMode.Angular📘: The axis is mapped to sweeps (angles) around the circle. Typically the
**Fully Customizable Sweep:**- Start point using startAngle📘
- Sweep size on the
**Angular**axis via totalAngle📘. - Direction (clockwise/counterclockwise) - manipulated by flippedCoordinates📘 set to
**true**/**false**. By default, the angular axis starts at 3 o'clock (0 radians) and goes counterclockwise. For a 12 o'clock and clockwise increment set up, use these properties:`const angularAxis = new PolarNumericAxis(wasmContext, {`

...

flippedCoordinates: true, // increment clockwise

startAngle: -Math.PI / 2, // start at 12 o'clock

// or `startAngleDegrees: -90 degrees`, the minus is there since we flip the coordinate calculator

})

**Multiple Angular Gridline Styles using gridlineMode📘:**- Choose between EGridLineMode.Circles📘 - which is the default, or EGridLineMode.Polygons📘 (spider/radar/cobweb).

**Support for Donut Charts:**- Use innerRadius📘 to hollow out the center—great for gauges and donuts. Takes in values between
`0`

and`1`

.

- Use innerRadius📘 to hollow out the center—great for gauges and donuts. Takes in values between
**Multiple axis label appearances using polarLabelMode📘:**- Options for angular label orientation: Horizontal📘, Perpendicular📘, Parallel📘

## PolarNumericAxis in Action

Here is how to configure both **angular** and **radial** axes in a polar chart:

`const {`

SciChartPolarSurface,

SciChartJsNavyTheme,

PolarNumericAxis,

PolarLineRenderableSeries,

XyDataSeries,

EPolarAxisMode,

NumberRange,

EAxisAlignment,

EPolarLabelMode

} = SciChart;

const { sciChartSurface, wasmContext } = await SciChartPolarSurface.create(rootElement, {

theme: new SciChartJsNavyTheme()

});

// Angular axis: goes around the circle, from 0 to 360 degrees

const angularAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Angular, // Lines around the center

axisAlignment: EAxisAlignment.Top,

polarLabelMode: EPolarLabelMode.Perpendicular,

visibleRange: new NumberRange(0, 270),

startAngleDegrees: 90, // Start at 12 o'clock

totalAngleDegrees: 270, // Sweep 270 degrees (3/4 circle)

flippedCoordinates: true, // Clockwise

labelPrecision: 0,

autoTicks: false, // Take control over tick management

majorDelta: 30, // set Major ticks at every 30 units (degrees)

majorGridLineStyle: {

strokeThickness: 1,

},

minorGridLineStyle: {

strokeThickness: 1,

color: "rgba(50, 100, 255, 0.2)",

strokeDashArray: [5, 3]

}

});

sciChartSurface.xAxes.add(angularAxis);

// Radial axis: from center outward, with circular gridlines

const radialAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Radial,

axisAlignment: EAxisAlignment.Right,

gridlineMode: SciChart.EPolarGridlineMode.Circles, // Or Polygons for spider/radar

innerRadius: 0.1, // 10% donut hole

visibleRange: new NumberRange(0, 5),

drawLabels: true,

drawMinorGridLines: false,

});

sciChartSurface.yAxes.add(radialAxis);

sciChartSurface.renderableSeries.add(

new PolarLineRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: Array.from({ length: 28 }, (_, i) => i * 10), // 0, 10, ..., 270

yValues: Array.from({ length: 28 }, (_, i) => 1 + 3 * Math.abs(Math.sin((i * 10 * Math.PI) / 180)))

}),

stroke: "#FF6600",

strokeThickness: 3,

})

);

## Tips

Always pair an **Angular** and **Radial**. You can have multiple axes in a polar chart, but make sure you have one of each first.

For a **vertical polar chart**, set the yAxis's polarAxisMode📘 to Angular📘 and the xAxis's to Radial📘

## Best Practices

-
Use innerRadius📘 for donut/ring charts, or gridlineMode📘: Polygons📘 for radar/spider style.

-
Customize tick intervals by setting autoTicks📘 to

`false`

and playing with majorDelta📘 and minorDelta📘 -
Use xCenterOffset📘 and yCenterOffset📘 for fine layout control, great for dashboards and overlays.

-
The labelPostfix📘 is often set to

`°`

, along with labelPrecision📘 =`0`

to indicate degrees. -
For smaller polar charts, setting drawMinorGridLines📘 to

`false`

can help improve readability by only keeping the major grid lines. -
By default, labelPrecision📘 is set to

`1`

, but if you work with degrees or just larger datasets, you may want to set it to`0`

and format the label as`270°`

instead of`270.0°`

.