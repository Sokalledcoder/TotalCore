---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/data-point-labels/data-label-coloring
scraped_at: 2025-11-28T18:24:22.956242
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/data-point-labels/data-label-coloring

# Data Label Coloring

DataLabels allow per data-point text labels to be drawn on series, or arbitrary text labels at x,y positions on the chart.

You can see several datalabel examples on the SciChart.js demo:

- The Line Chart example
- The Column Chart example
- The PaletteProvider example
- The DataLabels demo
- The Stacked Column Chart demo
- The Population Pyramid demo

Explore these for some rich examples of how to use this API.

## Label Colouring

The color property on the dataLabels option sets the color for all labels, but you can do per-label coloring by overriding the getColor()📘 function on the dataLabelProvider📘.

This function hsa to return the integer color codes used by SciChart's engine, so you need to use parseColorToUIntArgb📘 helper function to convert from html colors. It is a good idea to pre-calculate integer colour codes, rather than compute them each time labels are drawn, as in the example below.

- TS
- JS

`// Create a column series and add dataLabels`

const columnSeries = new FastColumnRenderableSeries(wasmContext, {

stroke: "SteelBlue",

fill: "LightSteelBlue",

strokeThickness: 1,

dataSeries: new XyDataSeries(wasmContext, {

xValues: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],

yValues: [-3, -4, 0, 2, 6.3, 3, 4, 8, 7, 5, 6, 8]

}),

dataLabels: {

positionMode: EColumnDataLabelPosition.Outside,

style: {

fontFamily: "Default",

fontSize: 18,

padding: new Thickness(3, 0, 3, 0)

},

color: "#EEE"

}

});

sciChartSurface.renderableSeries.add(columnSeries);

// Override the colouring using dataLabelProvider.getColor

// import { parseColorToUIntArgb } from "scichart";

const red = parseColorToUIntArgb("red");

const yellow = parseColorToUIntArgb("yellow");

const green = parseColorToUIntArgb("green");

(columnSeries.dataLabelProvider as ColumnSeriesDataLabelProvider).getColor = (dataLabelState, text) => {

const y = dataLabelState.yVal();

if (y <= 0) return red;

if (y <= 5) return yellow;

return green;

};

`// Create a column series and add dataLabels`

const columnSeries = new FastColumnRenderableSeries(wasmContext, {

stroke: "SteelBlue",

fill: "LightSteelBlue",

strokeThickness: 1,

dataSeries: new XyDataSeries(wasmContext, {

xValues: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],

yValues: [-3, -4, 0, 2, 6.3, 3, 4, 8, 7, 5, 6, 8]

}),

dataLabels: {

positionMode: EColumnDataLabelPosition.Outside,

style: {

fontFamily: "Default",

fontSize: 18,

padding: new Thickness(3, 0, 3, 0)

},

color: "#EEE"

}

});

sciChartSurface.renderableSeries.add(columnSeries);

// Override the colouring using dataLabelProvider.getColor

// import { parseColorToUIntArgb } from "scichart";

const red = parseColorToUIntArgb("red");

const yellow = parseColorToUIntArgb("yellow");

const green = parseColorToUIntArgb("green");

columnSeries.dataLabelProvider.getColor = (dataLabelState, text) => {

const y = dataLabelState.yVal();

if (y <= 0)

return red;

if (y <= 5)

return yellow;

return green;

};

This results in the following output: