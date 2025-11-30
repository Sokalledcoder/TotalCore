---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/data-point-labels/data-labels-api-overview
scraped_at: 2025-11-28T18:24:23.692521
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/data-point-labels/data-labels-api-overview

# DataLabels API Overview

DataLabels allow per data-point text labels to be drawn on series, or arbitrary text labels at x,y positions on the chart.

You can see several datalabel examples on the SciChart.js demo:

- The Line Chart example
- The Column Chart example
- The PaletteProvider example
- The DataLabels demo
- The Stacked Column Chart demo
- The Population Pyramid demo

Explore these for some rich examples of how to use this API.

## The DataLabels API

Each RenderableSeries as a dataLabelProvider📘 property. Many also accept Data Label configuration via constructor options📘.

This defines whether text labels are rendered for data-points, and the style and positioning of these text labels.

## Adding Data Labels

You an configure data labels for almost any series by setting a valid style on the dataLabels property📘 in the series options:

- TS
- Builder API (JSON Config)

`// Demonstrates how to add DataLabels to a chart with SciChart.js`

const {

SciChartSurface,

NumericAxis,

FastLineRenderableSeries,

EllipsePointMarker,

XyDataSeries,

SciChartJsNavyTheme

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

// Create a chart with X, Y axis

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

// Create a Line series with a pointmarker & some data

// We add dataLabels by setting the dataLabels constructor option

sciChartSurface.renderableSeries.add(

new FastLineRenderableSeries(wasmContext, {

stroke: "SteelBlue",

strokeThickness: 3,

pointMarker: new EllipsePointMarker(wasmContext, {

width: 10,

height: 10,

strokeThickness: 2,

stroke: "SteelBlue",

fill: "LightSteelBlue"

}),

dataSeries: new XyDataSeries(wasmContext, {

xValues: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],

yValues: [4.3, 5.3, 6, 6.3, 6, 5.2, 4.5, 4.6, 5, 6, 7, 8]

}),

// Data labels are enabled here. Simply set style, color

dataLabels: {

style: {

fontFamily: "Default",

fontSize: 16

},

color: "#EEE"

}

})

);

`// Demonstrates how to add DataLabels to a chart with SciChart.js using the Builder API`

const { chartBuilder, ESeriesType, EThemeProviderType, EPointMarkerType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

series: [

{

type: ESeriesType.LineSeries,

xyData: {

xValues: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],

yValues: [4.3, 5.3, 6, 6.3, 6, 5.2, 4.5, 4.6, 5, 6, 7, 8]

},

options: {

stroke: "#0066FF",

strokeThickness: 5,

pointMarker: {

type: EPointMarkerType.Ellipse,

options: {

width: 10,

height: 10,

strokeThickness: 2,

stroke: "SteelBlue",

fill: "LightSteelBlue"

}

},

// Data labels are enabled here. Simply set style, color

dataLabels: {

style: {

fontFamily: "Default",

fontSize: 16

},

color: "#EEE"

}

}

}

]

});

This results in the following output:

## Standard Label Formatting

Datalabels supports the same numeric format and precision options as axis labels. By default the Y-value is printed to the label. The numericFormat option is one of the ENumericFormat📘 values.

- TS
- Builder API (JSON Config)

`sciChartSurface.renderableSeries.add(`

new FastLineRenderableSeries(wasmContext, {

stroke: "SteelBlue",

strokeThickness: 3,

pointMarker,

dataSeries,

// Configure datalabel formatting using similar

// numericFormat and precision options to the axis label formatting

dataLabels: {

numericFormat: ENumericFormat.Decimal,

precision: 4,

style: {

fontFamily: "Default",

fontSize: 16

},

color: "#EEE"

}

})

);

`const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {`

surface: { theme: { type: EThemeProviderType.Dark } },

series: [

{

type: ESeriesType.LineSeries,

xyData: {

xValues: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],

yValues: [4.3, 5.3, 6, 6.3, 6, 5.2, 4.5, 4.6, 5, 6, 7, 8]

},

options: {

stroke: "#0066FF",

strokeThickness: 5,

pointMarker,

// ...

// Configure datalabel formatting using similar

// numericFormat and precision options to the axis label formatting

dataLabels: {

numericFormat: ENumericFormat.Decimal,

precision: 4,

style: {

fontFamily: "Default",

fontSize: 16

},

color: "#EEE"

}

}

}

]

});

The precision is now increased to 4 decimal places

Data Labels formatting uses similar code to the LabelProvider for axis labels. This means that labels can be formatted as dates, exponents or scientific notation.