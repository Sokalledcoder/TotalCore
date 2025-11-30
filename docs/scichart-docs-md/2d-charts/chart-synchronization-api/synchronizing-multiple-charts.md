---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-synchronization-api/synchronizing-multiple-charts
scraped_at: 2025-11-28T18:24:21.376402
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-synchronization-api/synchronizing-multiple-charts

# Synchronizing Multiple Charts

SciChart.js features a rich set of APIs to synchronize multiple charts. With these APIs you can create dynamic dashboards and chart groups, for example:

- Group charts together with linked behaviours
- Sync chart sizes and axis sizes across chart groups
- Sync tooltips, zooming or panning across chart groups
- Dynamically add or remove chart panes to groups

The JavaScript Sync Multi Chart Example can be found in the SciChart.Js Examples Suite on Github, or our live demo at scichart.com/demo

## How to create a Chart Group

We've created an example showing how create a synchonrized chart group below. First we will start off with the codepen, then share the code and walk through how it works.

Zoom and Pan the above chart to get a feel for how synchronized charts work in a group!

First of all some HTML is required to create two vertical charts. For simplicity this has been included with inline styles showing how to layout the two charts.

- HTML

`<div id="scichart-root">`

<div id="chart0Div" style="width: 100%; height: 50%"></div>

<div id="chart1Div" style="width: 100%; height: 50%"></div>

</div>

After that, some code to initialize the two charts can look like this:

- TS

`// Create two charts for Synchronization`

const { SciChartSurface, NumericAxis, FastLineRenderableSeries, XyDataSeries, SciChartJsNavyTheme } = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const createSciChartSurface = async (divId, isFirstChart) => {

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divId, {

theme: new SciChartJsNavyTheme()

});

// Create some deliberate differences between chart 0 and chart 1

sciChartSurface.background = isFirstChart ? "#22365B" : "#18304A";

sciChartSurface.canvasBorder = isFirstChart ? { borderBottom: 4, color: "#55698E" } : undefined;

sciChartSurface.xAxes.add(

new NumericAxis(wasmContext, {

axisTitle: isFirstChart ? "XAxis 0" : "XAxis 1"

})

);

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

// Create some deliberate differences between chart 0 and chart 1

labelPrecision: isFirstChart ? 2 : 4,

axisTitle: isFirstChart ? "YAxis 0" : "YAxis 1"

})

);

const xValues = [];

const yValues = [];

for (let i = 0; i < 100; i++) {

const coef = isFirstChart ? 1 : 0.5;

xValues.push(i);

yValues.push(0.2 * coef * Math.sin((i * 0.1) / coef) - Math.cos(i * 0.01));

}

sciChartSurface.renderableSeries.add(

new FastLineRenderableSeries(wasmContext, {

// Create some deliberate differences between chart 0 and chart 1

stroke: isFirstChart ? "#FF6600" : "#3377FF",

strokeThickness: 5,

dataSeries: new XyDataSeries(wasmContext, {

xValues,

yValues

})

})

);

return sciChartSurface;

};

// Create two SciChartSurfaces with separate <div> elements in the DOM

// Create the first chart, Expects a <div id="chart0Div"> in the DOM

const sciChartSurface0 = await createSciChartSurface("chart0Div", true);

// Create the second chart, Expects a <div id="chart1Div"> in the DOM

const sciChartSurface1 = await createSciChartSurface("chart1Div", false);

This code initializes a SciChartSurface, creates xAxis and yAxis and adds some data and a line series.

The function *createSciChartSurface* creates a single chart, so this is called twice passing in a different `<div>`

ID in order to create the two vertical charts.

## Synchronizing Zooming, Panning and Tooltips on two charts

To Synchronize the two charts, we have to carry out the following steps:

- Synchronize xAxis.visibleRange📘 on the two charts by using a AxisCore.visibleRangeChanged📘 callback
- Synchronize chart widths using a SciChartVerticalGroup📘
- Finally, optionally synchronize chart modifiers (Cursor, Tooltips) using a modifierGroup📘

- TS

`const { SciChartVerticalGroup, ZoomPanModifier, MouseWheelZoomModifier, RolloverModifier } = SciChart;`

// Step1: Synchronize the two chart visibleRanges

sciChartSurface0.xAxes.get(0).visibleRangeChanged.subscribe(data1 => {

sciChartSurface1.xAxes.get(0).visibleRange = data1.visibleRange;

});

sciChartSurface1.xAxes.get(0).visibleRangeChanged.subscribe(data1 => {

sciChartSurface0.xAxes.get(0).visibleRange = data1.visibleRange;

});

// Step 2: Synchronize the two chart axis sizes using SciChartVerticalGroup

// this is useful in case the Y-axis have different sizes due to differing visibleRange

// text formatting or size

const verticalGroup = new SciChartVerticalGroup();

verticalGroup.addSurfaceToGroup(sciChartSurface0);

verticalGroup.addSurfaceToGroup(sciChartSurface1);

// Step 3: Add some cursors, zooming behaviours and link them with a modifier group

// This ensures mouse events on one chart are sent to the other chart

const group0 = "modifierGroup0";

sciChartSurface0.chartModifiers.add(

new ZoomPanModifier({ modifierGroup: group0 }),

new MouseWheelZoomModifier({ modifierGroup: group0 }),

new RolloverModifier({ modifierGroup: group0 })

);

const group1 = "modifierGroup1";

sciChartSurface1.chartModifiers.add(

new ZoomPanModifier({ modifierGroup: group1 }),

new MouseWheelZoomModifier({ modifierGroup: group1 }),

new RolloverModifier({ modifierGroup: group1 })

);

## Some Notes on Chart Synchronization

Adding a modifierGroup📘 to specific chart modifiers will ensure that mouse events from one chart are passed to the other and vice versa. This will actually cause zooming, panning, mousewheel and tooltip/cursor behaviour to occur on all charts (when one chart is interacted with).

However, from an axis range point of view it is far more accurate to synchronize xAxis.visibleRange📘 on the two charts by using a AxisCore.visibleRangeChanged📘 callback. Mouse events are only accurate to a pixel and some inconsistencies can be built up with synchronized charts unless you also have the visibleRange synchronization.

Adding a SciChartVerticalGroup📘 ensures that the yAxis sizes on the two charts are exactly the same. This step is optional but in case of differing sizes of the axis it will give a more consistent look. For vertical chart groups you can use the SciChartHorizontalGroup📘 helper class.