---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/polar-modifiers/polar-legend-modifier
scraped_at: 2025-11-28T18:24:16.641690
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/polar-modifiers/polar-legend-modifier

# PolarLegendModifier

The PolarLegendModifier📘 is a modifier that displays a legend for the series in a polar chart. It provides information about the series, such as their names and colors, enhancing the user experience by allowing for easy identification of data series.

- TS
- Builder API (JSON Config)

`const { PolarLegendModifier } = SciChart;`

// or for npm: import { PolarLegendModifier } from "scichart";

// Add PolarLegendModifier behaviour to the chart

sciChartSurface.chartModifiers.add(

new PolarLegendModifier({

showCheckboxes: true,

showSeriesMarkers: true

})

);

`// Demonstrates how to configure the PolarLegendModifier in SciChart.js using the Builder API`

const {

chartBuilder,

EAxisType,

EChart2DModifierType,

EPolarAxisMode,

ESeriesType

} = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DPolarChart(divElementId, {

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

type: ESeriesType.PolarColumnSeries,

options: {

fill: "#55aaff44",

stroke: "#55aaff",

dataPointWidth: 0.6,

strokeThickness: 2

},

xyData: {

xValues: Array.from({ length: 10 }, (_, i) => i),

yValues: Array.from({ length: 10 }, (_, i) => Math.sin(i * 0.1)),

dataSeriesName: "Sine"

},

},

{

type: ESeriesType.PolarLineSeries,

options: {

stroke: "#ff8800",

strokeThickness: 4

},

xyData: {

xValues: Array.from({ length: 10 }, (_, i) => i),

yValues: Array.from({ length: 10 }, (_, i) => Math.cos(i * 0.1)),

dataSeriesName: "Cosine"

},

}

],

modifiers: [

{

type: EChart2DModifierType.PolarLegend,

options: {

showCheckboxes: true,

showSeriesMarkers: true

}

}

]

});

This results in the following behavior: