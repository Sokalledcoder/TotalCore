---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/polar-modifiers/polar-cursor-modifier
scraped_at: 2025-11-28T18:24:16.430265
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/polar-modifiers/polar-cursor-modifier

# PolarCursorModifier

The PolarCursorModifier📘 is a modifier that provides a crosshair cursor on a polar chart. It allows users to hover over data points and see their values, enhancing the interactivity of the chart.

## Adding a PolarCursorModifier to a Chart

Similarly to the CursorModifier for a Cartesian 2D chart, a PolarCursorModifier📘 can be added to the `sciChartSurface.chartModifiers`

collection of a SciChartPolarSurface📘 to enable crosshair behavior. For example:

- TS
- Builder API (JSON Config)

`const { PolarCursorModifier, EAngularAxisLabelPlacement, ERadialAxisLabelPlacement } = SciChart;`

// or for npm: import { PolarCursorModifier, ... } from "scichart";

// const { sciChartSurface, wasmContext } = await SciChartPolarSurface.create(divElementId, {})

// ...

// Add PolarCursorModifier behaviour to the chart

sciChartSurface.chartModifiers.add(

new PolarCursorModifier({

lineColor: "#55aaff",

lineThickness: 2,

axisLabelFill: "#55aaff",

angularAxisLabelPlacement: EAngularAxisLabelPlacement.Center,

radialAxisLabelPlacement: ERadialAxisLabelPlacement.Center,

showRadialLine: true,

showCircularLine: true

})

);

`// Demonstrates how to configure the PolarCursorModifier in SciChart.js using the Builder API`

const {

chartBuilder,

EAxisType,

EChart2DModifierType,

EPolarAxisMode,

EAngularAxisLabelPlacement,

ERadialAxisLabelPlacement,

ESeriesType

} = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DPolarChart(divElementId, {

xAxes: {

type: EAxisType.PolarNumericAxis,

options: { polarAxisMode: EPolarAxisMode.Angular }

},

yAxes: {

type: EAxisType.PolarNumericAxis,

options: { polarAxisMode: EPolarAxisMode.Radial }

},

series: [

{

type: ESeriesType.PolarLineSeries,

options: {

stroke: "#50C7E0",

strokeThickness: 5,

},

xyData: {

xValues: Array.from({ length: 10 }, (_, i) => i),

yValues: Array.from({ length: 10 }, (_, i) => Math.sin(i * 0.1))

}

}

],

modifiers: [

{

type: EChart2DModifierType.PolarCursor,

options: {

lineColor: "#55aaff",

lineThickness: 3,

axisLabelFill: "#55aaff",

angularAxisLabelPlacement: EAngularAxisLabelPlacement.Center,

radialAxisLabelPlacement: ERadialAxisLabelPlacement.Top,

showRadialLine: true,

showCircularLine: true

}

}

]

});

This results in the following behavior: