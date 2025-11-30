---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-styling/visibility-of-axis-elements
scraped_at: 2025-11-28T18:24:06.978911
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-styling/visibility-of-axis-elements

# Visibility of Axis Elements

In SciChart.js all the elements of an axis may be hidden or shown invidually, with the following code:

- TS
- Builder API (JSON Config)

`// Demonstrates how to show/hide axis parts SciChart.js`

const {

SciChartSurface,

NumericAxis,

SciChartJSLightTheme,

TextAnnotation,

ECoordinateMode,

EHorizontalAnchorPoint,

EVerticalAnchorPoint

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

// Choose a light theme to make this obvious

theme: new SciChartJSLightTheme()

});

// Create a X-Axis hiding elements

sciChartSurface.xAxes.add(

new NumericAxis(wasmContext, {

axisTitle: "X Axis (Hiding elements)",

// Show or hide individual elements of the axis

drawMajorBands: true,

drawLabels: false,

drawMinorGridLines: false,

drawMajorGridLines: true,

drawMinorTickLines: true,

drawMajorTickLines: false

})

);

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

// Hide the entire axis

isVisible: false

})

);

`// Demonstrates how to show/hide axis parts SciChart.js`

const { chartBuilder, EThemeProviderType, EAxisType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: {

type: EAxisType.NumericAxis,

options: {

axisTitle: "X Axis (Hiding elements)",

// Show or hide individual elements of the axis

drawMajorBands: true,

drawLabels: false,

drawMinorGridLines: false,

drawMajorGridLines: true,

drawMinorTickLines: true,

drawMajorTickLines: false

}

},

yAxes: {

type: EAxisType.NumericAxis,

options: {

// Hide the entire axis

isVisible: false

}

}

});

This results in the following output:

A hidden axis still behaves like an axis with all the scaling that comes with it, just without the visual elements like labels and gridlines.

## Using Hidden Axis to Scale a Series to Viewport

Other than styling, a hidden axis is very useful to scale a series to a viewport.

Say you had a chart with two series on the same Y-Axis, and with different amplitudes. You want to click a button to maximise a series to the viewport. You can do this with a hidden axis.

Here's a code sample below:

- TS

`// Create a SciChartSurface`

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

// Add some Series to the chart

sciChartSurface.renderableSeries.add(

new FastLineRenderableSeries(wasmContext, {

xAxisId: "xAxis",

yAxisId: "yAxis",

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues, dataSeriesName: "Series A" }),

stroke: "#50C7E0",

strokeThickness: 3

})

);

sciChartSurface.renderableSeries.add(

new FastLineRenderableSeries(wasmContext, {

xAxisId: "xAxis",

yAxisId: "yAxis",

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues1, dataSeriesName: "Series B" }),

stroke: "#F48420",

strokeThickness: 3

})

);

sciChartSurface.renderableSeries.add(

new FastLineRenderableSeries(wasmContext, {

xAxisId: "xAxis",

yAxisId: "yAxis",

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues2, dataSeriesName: "Series C" }),

stroke: "#EC0F6C",

strokeThickness: 3

})

);

// Default X-Axis

sciChartSurface.xAxes.add(

new NumericAxis(wasmContext, {

id: "xAxis",

axisTitle: "X Axis"

})

);

// Default YAxis

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

id: "yAxis",

axisTitle: "Y Axis",

growBy: new NumberRange(0.1, 0.1)

})

);

// Hidden YAxis with ID=HiddenYAxis

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

id: "HiddenYAxis",

isVisible: false,

autoRange: EAutoRange.Always

})

);

// Get the checboxes in the DOM (see index.html)

const checkboxes = Array.from(document.getElementsByClassName("checkbox"));

// Function invoked when a checkbox is checked/unchecked

const onCheckedChanged = e => {

// find a renderableSeries by dataSeriesName matching checkbox id

const series = sciChartSurface.renderableSeries

.asArray()

.find(rs => rs.dataSeries.dataSeriesName === e.target.id);

if (!series) return;

if (e.target.checked) {

// If the series is checked, show it on the hidden YAxis with AutoRange.Always

console.log("Maximising " + series.dataSeries.dataSeriesName);

series.yAxisId = "HiddenYAxis";

} else {

// Else, put it back on the default axis / default scaling

series.yAxisId = "yAxis";

console.log("Setting " + series.dataSeries.dataSeriesName + " to default axis");

}

};

// get checkboxes by class name and add event listener to change event

checkboxes.forEach(element => {

element.addEventListener("change", e => {

onCheckedChanged(e);

// @ts-ignore

if (e.target.checked) {

// uncheck other checkboxes

// @ts-ignore

checkboxes.filter(cb => cb.id !== e.target.id)

.forEach(cb => {

// @ts-ignore

cb.checked = false;

onCheckedChanged({ target: cb });

});

}

});

});

This results in the following output: