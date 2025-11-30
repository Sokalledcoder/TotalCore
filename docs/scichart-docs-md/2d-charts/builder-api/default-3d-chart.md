---
source: https://www.scichart.com/documentation/js/v4/2d-charts/builder-api/default-3d-chart
scraped_at: 2025-11-28T18:24:12.980164
---

# https://www.scichart.com/documentation/js/v4/2d-charts/builder-api/default-3d-chart

# Creating a 3D Chart

SciChart provides a powerful API for creating various types of charts, including **3D Charts**.

The buildChart📘 function can be used to build both 2D Charts, Pie Charts, 2D Polar Charts & **3D Charts**, so the returned object type will differ depending on the chart type.

## Using buildChart📘 to create a Pie Chart

- TS

`// Demonstrates how to create a basic 3D chart using the Builder API in SciChart.js`

const {

chartBuilder,

EThemeProviderType,

ESciChartSurfaceType,

EAxisType,

ESeriesType3D,

EChart3DModifierType,

EPointMarker3DType,

Vector3

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { sciChart3DSurface, wasmContext } = await chartBuilder.buildChart(divElementId, {

type: ESciChartSurfaceType.Default3D,

options: {

surface: {

theme: { type: EThemeProviderType.Navy },

cameraOptions: {

position: new Vector3(300, 300, 300),

}

},

zAxis: {

type: EAxisType.NumericAxis3D,

options: {

axisTitle: "Z Axis",

labelPrecision: 0

}

},

series: [

{

type: ESeriesType3D.ScatterRenderableSeries3D,

xyzData: {

xValues: Array.from({ length: 10 }, (_, i) => Math.round(Math.random() * 10)),

yValues: Array.from({ length: 10 }, (_, i) => Math.round(Math.random() * 10)),

zValues: Array.from({ length: 10 }, (_, i) => Math.round(Math.random() * 10)),

},

options: {

pointMarker: {

type: EPointMarker3DType.Sphere,

options: {

size: 20,

fill: "#3388FF",

}

}

}

}

],

modifiers: [

{ type: EChart3DModifierType.MouseWheelZoom },

{ type: EChart3DModifierType.Orbit },

{ type: EChart3DModifierType.ZoomExtents }

]

}

});

## Using build3DChart📘 to explicitly create a 3D Chart.

- TS

`// Demonstrates how to create a basic 3D chart using the Builder API in SciChart.js`

const {

build3DChart,

EThemeProviderType,

EAxisType,

ESeriesType3D,

EChart3DModifierType,

EPointMarker3DType,

Vector3

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { sciChart3DSurface, wasmContext } = await build3DChart(divElementId, {

// no need to specify `type` here, as build3DChart always returns a 3D surface

surface: {

theme: { type: EThemeProviderType.Navy },

cameraOptions: {

position: new Vector3(300, 300, 300),

}

},

zAxis: {

type: EAxisType.NumericAxis3D,

options: {

axisTitle: "Z Axis",

labelPrecision: 0

}

},

series: [

{

type: ESeriesType3D.ScatterRenderableSeries3D,

xyzData: {

xValues: Array.from({ length: 10 }, (_, i) => Math.round(Math.random() * 10)),

yValues: Array.from({ length: 10 }, (_, i) => Math.round(Math.random() * 10)),

zValues: Array.from({ length: 10 }, (_, i) => Math.round(Math.random() * 10)),

},

options: {

pointMarker: {

type: EPointMarker3DType.Sphere,

options: {

size: 20,

fill: "#3388FF",

}

}

}

}

],

modifiers: [

{ type: EChart3DModifierType.MouseWheelZoom },

{ type: EChart3DModifierType.Orbit },

{ type: EChart3DModifierType.ZoomExtents }

]

});

Both of these methods will result in this output: