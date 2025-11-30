---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/polar-modifiers/polar-series-selection-modifier
scraped_at: 2025-11-28T18:24:17.400977
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/polar-modifiers/polar-series-selection-modifier

# PolarSeriesSelectionModifier

The PolarSeriesSelectionModifier📘 is a modifier that allows users to select a series on a polar chart. It provides visual feedback when a series is selected or hovered, enhancing the user experience by allowing for interaction with the chart.

## Adding a PolarSeriesSelectionModifier to a Chart

- TS
- Builder API (JSON Config)

`const { `

PolarSeriesSelectionModifier,

PolarLineRenderableSeries,

XyDataSeries,

} = SciChart;

// or for npm: import { PolarSeriesSelectionModifier } from "scichart";

// const { sciChartSurface, wasmContext } = await SciChartPolarSurface.create(divElementId, {})

// ...

// Add 2 series

sciChartSurface.renderableSeries.add(

new PolarLineRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: Array.from({ length: 10 }, (_, i) => i),

yValues: Array.from({ length: 10 }, (_, i) => Math.sin(i * 0.1))

}),

stroke: "#FFAA00",

strokeThickness: 3,

onSelectedChanged: (sourceSeries) => {

sourceSeries.stroke = sourceSeries.isSelected ? "white" : "#FFAA00";

},

onHoveredChanged: (sourceSeries) => {

sourceSeries.stroke = sourceSeries.isHovered ? "gray" : "#FFAA00";

},

}),

new PolarLineRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: Array.from({ length: 10 }, (_, i) => i),

yValues: Array.from({ length: 10 }, (_, i) => Math.cos(i * 0.1))

}),

stroke: "#3388FF",

strokeThickness: 3,

onSelectedChanged: (sourceSeries) => {

sourceSeries.stroke = sourceSeries.isSelected ? "white" : "#3388FF";

},

onHoveredChanged: (sourceSeries) => {

sourceSeries.stroke = sourceSeries.isHovered ? "gray" : "#3388FF";

},

})

);

// Add PolarSeriesSelectionModifier behaviour to the chart

sciChartSurface.chartModifiers.add(

new PolarSeriesSelectionModifier(),

);

`// Demonstrates how to configure the PolarSeriesSelection in SciChart.js using the Builder API`

const {

chartBuilder,

EThemeProviderType,

EAxisType,

EChart2DModifierType,

ESeriesType,

EPolarAxisMode,

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

onSelectedChanged: (sourceSeries) => {

sourceSeries.stroke = sourceSeries.isSelected ? "white" : "#FFAA00";

},

onHoveredChanged: (sourceSeries) => {

sourceSeries.stroke = sourceSeries.isHovered ? "gray" : "#FFAA00";

}

}

},

{

type: ESeriesType.PolarLineSeries,

xyData: {

xValues: Array.from({ length: 10 }, (_, i) => i),

yValues: Array.from({ length: 10 }, (_, i) => Math.cos(i * 0.1))

},

options: {

stroke: "#3388FF",

strokeThickness: 3,

onSelectedChanged: (sourceSeries) => {

sourceSeries.stroke = sourceSeries.isSelected ? "white" : "#3388FF";

},

onHoveredChanged: (sourceSeries) => {

sourceSeries.stroke = sourceSeries.isHovered ? "gray" : "#3388FF";

}

}

},

],

modifiers: [

{

type: EChart2DModifierType.PolarSeriesSelection

}

]

});