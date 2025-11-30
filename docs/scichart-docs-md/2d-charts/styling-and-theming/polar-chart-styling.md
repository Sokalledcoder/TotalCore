---
source: https://www.scichart.com/documentation/js/v4/2d-charts/styling-and-theming/polar-chart-styling
scraped_at: 2025-11-28T18:24:49.919245
---

# https://www.scichart.com/documentation/js/v4/2d-charts/styling-and-theming/polar-chart-styling

# Polar Chart Styling

Polar charts in SciChart.js are specialized charts designed for polar data visualization, which are circular in nature. They can be used to create various types of charts, such as radial bar, windrose, line, band, mountain, spider, scatter, heatmaps and more.

There is also the labelStyle📘 property, which acts the same way as the AxisBase.labelStyle📘 property, allowing you to set the font, color, and other styles of the labels based on the TLabelStyle📘 type.

### Grid mode for Radial Gridlines

The grid mode for radial gridlines can be controlled via the gridlineMode📘 property. This property determines how the radial gridlines are drawn.

For a Spider/Radar chart look you can set this property to EPolarGridLineMode.Polygon📘, which will draw the gridlines as concentric polygons, or you can stick to the default EPolarGridLineMode.Circles📘 which draws radial gridlines as arcs.

## Other Styling Properties

### Major Gridlines

aligned with labels having majorGridLineStyle📘 and drawMajorGridLines📘 properties.

### Minor Gridlines

between labels with minorGridLineStyle📘 and drawMinorGridLines📘 properties.

Both Major and Minor gridlines **style** objects have the TGridLineStyle📘 type, which allows you to set the `color`

, `thickness`

, and `strokeDashArray`

of the gridlines.

Also, the drawMajorGridLines📘 and drawMinorGridLines📘 properties are `boolean`

values that control whether the gridlines are drawn or not.

### Major Ticks

small marks, outside the axis, aligned with labels with majorTickLineStyle📘 and drawMajorTicks📘 properties.

### Minor Ticks

small marks, outside the axis, between labels with minorTickLineStyle📘 and drawMinorTicks📘 properties.

Both Major and Minor ticks **style** objects have the TTickLineStyle📘 type, which allows you to set the `color`

, `tickSize`

, and `strokeThickess`

of the ticks.

## Polar Axis Styling Example

Read the code comments carefully

- TS

`const {`

SciChartPolarSurface,

PolarNumericAxis,

NumberRange,

SciChartJsNavyTheme,

EPolarAxisMode,

EPolarGridlineMode,

PolarCategoryAxis,

EPolarLabelMode

} = SciChart;

// Create a SciChartPolarSurface

const { wasmContext, sciChartSurface } = await SciChartPolarSurface.create(divElementId, {

theme: new SciChartJsNavyTheme(),

});

// Add polar axes

const TOTAL_ANGLE = Math.PI * 1.5; // 270 degrees in radians (3 quarters of a circle)

sciChartSurface.xAxes.add(

new PolarCategoryAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Angular,

visibleRange: new NumberRange(0, 9),

totalAngle: TOTAL_ANGLE, // in radians

// totalAngleDegrees: 270, // if you want to work in degrees

flippedCoordinates: true, // increment clockwise

startAngle: (Math.PI - TOTAL_ANGLE) / 2, // formula to center incomplete polar surfaces like gauges ("with the missing slice at the bottom")

autoTicks: false, // take control over tick distance

majorDelta: 1, // draw tick every 1 unit

// minor gridlines turned off look better when radial axis gridlineMode is set to `Polygons`

drawMinorGridLines: false,

majorTickLineStyle: { // optionally style major ticks

color: "#FFFFFF",

tickSize: 2,

strokeThickness: 2,

},

majorGridLineStyle: { // optionally style major grid lines

color: "rgba(12,17,53,1)",

strokeThickness: 1,

strokeDashArray: [5, 2], // dashed lines

},

labels: ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth"],

labelStyle: {

color: "#FFFFFF",

},

polarLabelMode: EPolarLabelMode.Parallel // can also be "Perpendicular", or (the default) "Horizontal"

})

);

sciChartSurface.yAxes.add(

new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Radial,

visibleRange: new NumberRange(0, 10),

gridlineMode: EPolarGridlineMode.Polygons, // results in a radar chart look (straight radial lines in between grid lines)

startAngle: (Math.PI - TOTAL_ANGLE) / 2, // match the radial labels to the start of the angular axis

labelPrecision: 0,

majorGridLineStyle: { // optionally style major grid lines

color: "rgba(12,17,53,1)",

strokeThickness: 1,

strokeDashArray: [5, 2], // dashed lines

},

})

);

This results in the following output: