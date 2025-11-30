---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/data-point-labels/custom-data-label-formatting
scraped_at: 2025-11-28T18:24:23.162847
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/data-point-labels/custom-data-label-formatting

# Custom DataLabel Formatting with getText()

DataLabels allow per data-point text labels to be drawn on series, or arbitrary text labels at x,y positions on the chart.

You can see several datalabel examples on the SciChart.js demo:

- The Line Chart example
- The Column Chart example
- The PaletteProvider example
- The DataLabels demo
- The Stacked Column Chart demo
- The Population Pyramid demo

Explore these for some rich examples of how to use this API.

In the article DataLabels API Overview we showed you how to apply simple formatting rules to change the number of decimal places on Data Labels. What if you needed more complex Data Label formatting rules? Enter custom label formatting.

## Custom Label Formatting

To take full control of the label text, override the dataLabelProvider.getText()📘 function on the series renderableSeries.dataLabelProvider📘.

getText📘 has a single parameter of type DataLabelState📘. This has a number of helper functions that allow you to get the x and y values and coordinates without having to worry about which way the axes run or if you are using a vertical chart.

This example outputs both X and Y Values. DataLabels are rendered using the new native text system, so they support multiline using \n for newlines. The dataLabels style option has **multiLineAlignment** and **lineSpacing** properties for controlling multiline text.

- TS
- Builder API (JSON Config)

`// Create a line series with dataLabels`

const lineSeries = new FastLineRenderableSeries(wasmContext, {

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

// dataLabels style must be specified to show labels

dataLabels: {

style: {

fontFamily: "Arial",

fontSize: 16,

lineSpacing: 4,

multiLineAlignment: EMultiLineAlignment.Left

},

color: "#EEE"

}

});

// Override default dataLabelProvider.getText() function

// See type DataLabelState for available data

(lineSeries.dataLabelProvider as DataLabelProvider).getText = dataLabelState => {

return `Point index ${dataLabelState.index}\n[x: ${dataLabelState.xVal()}, y: ${dataLabelState.yVal()}]`;

};

`// Demonstrates how to add DataLabels to a chart with SciChart.js using the Builder API`

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

fontFamily: "Arial",

fontSize: 16

},

color: "#EEE"

}

}

}

]

});

// Note you can access dataLabelProvider from a constructed chart as follows

(sciChartSurface.renderableSeries.get(0).dataLabelProvider as DataLabelProvider).getText = dataLabelState => {

return `Point index ${dataLabelState.index}\n[x: ${dataLabelState.xVal()}, y: ${dataLabelState.yVal()}]`;

};

See the DataLabelState📘 type for what data is passed into the getText()📘 function for each label