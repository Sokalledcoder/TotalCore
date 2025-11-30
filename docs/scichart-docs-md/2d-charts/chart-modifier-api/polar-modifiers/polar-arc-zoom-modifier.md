---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/polar-modifiers/polar-arc-zoom-modifier
scraped_at: 2025-11-28T18:24:16.212271
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/polar-modifiers/polar-arc-zoom-modifier

# PolarArcZoomModifier

The PolarArcZoomModifier📘 is a modifier that allows users to zoom in on a specific arc of a polar chart. It provides a visual feedback mechanism for selecting the area to zoom in on, enhancing the user experience by allowing for focused analysis of specific data ranges.

## Adding a PolarArcZoomModifier to a Chart

A PolarArcZoomModifier📘 can be added to the `sciChartSurface.chartModifiers`

collection to enable zoom to fit behavior using a user-drawn arc selection. It is the polar counterpart of the XyRubberBandZoomModifier - used on the Cartesian 2D charts.

For example:

- TS
- Builder API (JSON Config)

`const { PolarArcZoomModifier, easing } = SciChart;`

// or for npm: import { PolarArcZoomModifier, easing } from "scichart";

// const { sciChartSurface, wasmContext } = await SciChartPolarSurface.create(divElementId, {})

// ...

// Add PolarArcZoomModifier behaviour to the chart

sciChartSurface.chartModifiers.add(

new PolarArcZoomModifier({

isAnimated: true,

fill: "#50C7E022",

strokeThickness: 5,

stroke: "white",

animationDuration: 2000,

easingFunction: easing.outCubic,

}),

);

`// Demonstrates how to configure the PolarArcZoomModifier in SciChart.js using the Builder API`

const {

chartBuilder,

EThemeProviderType,

EAxisType,

EChart2DModifierType,

easing,

EPolarAxisMode,

ESeriesType

} = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DPolarChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: {

type: EAxisType.PolarNumericAxis,

options: {

polarAxisMode: EPolarAxisMode.Angular

}

},

yAxes: {

type: EAxisType.PolarNumericAxis,

options: {

polarAxisMode: EPolarAxisMode.Radial

}

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

type: EChart2DModifierType.PolarArcZoom,

options: {

isAnimated: true,

fill: "#00ffff33",

strokeThickness: 5,

stroke: "red",

animationDuration: 2000,

easingFunction: easing.outCubic

}

}

]

});

This results in the following behavior: