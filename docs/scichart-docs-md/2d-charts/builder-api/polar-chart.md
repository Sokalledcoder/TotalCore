---
source: https://www.scichart.com/documentation/js/v4/2d-charts/builder-api/polar-chart
scraped_at: 2025-11-28T18:24:13.346648
---

# https://www.scichart.com/documentation/js/v4/2d-charts/builder-api/polar-chart

# Creating a Polar Chart

SciChart provides a powerful API for creating various types of charts, including **Polar Charts**.

The buildChart📘 function can be used to build both 2D Charts, Pie Charts, **2D Polar Charts** & 3D Charts, so the returned object type will differ depending on the chart type.

## Using buildChart📘 to create a Polar Chart

- TS

`const {`

chartBuilder,

ESciChartSurfaceType,

EThemeProviderType,

EAxisType,

EPolarAxisMode,

EChart2DModifierType,

ESeriesType,

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { sciChartSurface, wasmContext } = await chartBuilder.buildChart(divElementId, {

type: ESciChartSurfaceType.Polar2D,

options: {

surface: {

theme: { type: EThemeProviderType.Navy }

},

xAxes: [{

type: EAxisType.PolarNumericAxis,

options: {

polarAxisMode: EPolarAxisMode.Angular,

}

}],

yAxes: [{

type: EAxisType.PolarNumericAxis,

options: {

polarAxisMode: EPolarAxisMode.Radial,

labelPrecision: 0,

}

}],

series: [

{

type: ESeriesType.PolarColumnSeries,

xyData: {

xValues: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],

yValues: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

},

options: {

stroke: "rgba(255, 0, 0, 1)",

fill: "rgba(255, 0, 0, 0.3)",

dataPointWidth: 0.8

}

}

],

modifiers: [

{ type: EChart2DModifierType.PolarMouseWheelZoom },

{ type: EChart2DModifierType.PolarZoomExtents },

{ type: EChart2DModifierType.PolarCursor }

]

}

});

## Using build2DPolarChart📘 to explicitly create a Polar Chart:

- TS

`const {`

build2DPolarChart,

EThemeProviderType,

EAxisType,

EPolarAxisMode,

EChart2DModifierType,

ESeriesType,

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { sciChartSurface, wasmContext } = await build2DPolarChart(divElementId, {

surface: {

theme: { type: EThemeProviderType.Navy }

},

xAxes: [{

type: EAxisType.PolarNumericAxis,

options: {

polarAxisMode: EPolarAxisMode.Angular,

}

}],

yAxes: [{

type: EAxisType.PolarNumericAxis,

options: {

polarAxisMode: EPolarAxisMode.Radial,

labelPrecision: 0,

}

}],

series: [

{

type: ESeriesType.PolarColumnSeries,

xyData: {

xValues: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],

yValues: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

},

options: {

stroke: "rgba(255, 0, 0, 1)",

fill: "rgba(255, 0, 0, 0.3)",

dataPointWidth: 0.8

}

}

],

modifiers: [

{ type: EChart2DModifierType.PolarMouseWheelZoom },

{ type: EChart2DModifierType.PolarZoomExtents },

{ type: EChart2DModifierType.PolarCursor }

]

});

Both of these methods will result in this output:

note

The options that the polar chart builder accepts are the same as the 2D surface, and can be seen here ISciChart2DDefinition📘, but you must choose options with `Polar`

in their name.