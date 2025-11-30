---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/polar-modifiers/polar-data-point-selection-modifier
scraped_at: 2025-11-28T18:24:16.709086
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/polar-modifiers/polar-data-point-selection-modifier

# PolarDataPointSelectionModifier

The PolarDataPointSelectionModifier📘 is a modifier that allows users to select data points on a polar chart. It provides visual feedback when a data point is selected, enhancing the user experience by allowing for interaction with the chart.

## Adding a PolarDataPointSelectionModifier to a Chart

- TS
- Builder API (JSON Config)

`const { `

PolarDataPointSelectionModifier,

DataPointSelectionPaletteProvider,

PolarLineRenderableSeries,

XyDataSeries,

EllipsePointMarker,

} = SciChart;

// or for npm: import { PolarDataPointSelectionModifier } from "scichart";

// const { sciChartSurface, wasmContext } = await SciChartPolarSurface.create(divElementId, {})

// ...

// Add a series with point markers & a DataPointSelectionPaletteProvider to see the selection effect

sciChartSurface.renderableSeries.add(

new PolarLineRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: Array.from({ length: 10 }, (_, i) => i),

yValues: Array.from({ length: 10 }, (_, i) => Math.sin(i * 0.1))

}),

stroke: "#FFAA00",

strokeThickness: 3,

pointMarker: new EllipsePointMarker(wasmContext, {

width: 12,

height: 12,

fill: "#000000",

stroke: "#FFAA00",

strokeThickness: 2,

}),

paletteProvider: new DataPointSelectionPaletteProvider({

fill: "#FFFFFF",

stroke: "#FFAA00", // keep the same

})

})

);

// Add PolarDataPointSelectionModifier behaviour to the chart

sciChartSurface.chartModifiers.add(

new PolarDataPointSelectionModifier({

allowDragSelect: true,

allowClickSelect: true,

selectionStroke: "#3388FF",

selectionFill: "#3388FF44",

onSelectionChanged: (args) => {

console.log("seriesSelectionModifier onSelectionChanged", args);

},

}),

);

`// Demonstrates how to configure the PolarDataPointSelection in SciChart.js using the Builder API`

const {

chartBuilder,

EThemeProviderType,

EAxisType,

EChart2DModifierType,

ESeriesType,

EPolarAxisMode,

DataPointSelectionPaletteProvider

} = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DPolarChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: {

type: EAxisType.PolarNumericAxis,

options: { polarAxisMode: EPolarAxisMode.Angular }

},

yAxes: {

type: EAxisType.PolarNumericAxis,

options: { polarAxisMode: EPolarAxisMode.Angular }

},

series: [

{

type: ESeriesType.PolarLineSeries,

xyData: {

xValues: Array.from({ length: 10 }, (_, i) => i),

yValues: Array.from({ length: 10 }, (_, i) => Math.sin(i * 0.1))

},

options: {

stroke: "#FFAA00",

strokeThickness: 3,

pointMarker: {

type: SciChart.EPointMarkerType.Triangle,

options: {

width: 12,

height: 12,

fill: "#000000",

stroke: "#FFAA00",

strokeThickness: 2

}

},

paletteProvider: new DataPointSelectionPaletteProvider({

fill: "#FFFFFF",

stroke: "#FFAA00", // keep the same

})

}

}

],

modifiers: [

{

type: EChart2DModifierType.PolarDataPointSelection

}

]

});