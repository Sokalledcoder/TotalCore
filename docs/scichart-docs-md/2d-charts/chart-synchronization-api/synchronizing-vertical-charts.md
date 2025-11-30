---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-synchronization-api/synchronizing-vertical-charts
scraped_at: 2025-11-28T18:24:21.297326
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-synchronization-api/synchronizing-vertical-charts

# Synchronizing Vertical Charts

In SciChart.js v3.4, you can now synchronize Vertical Charts, enabling grouped zooming, panning, cursors and tooltips as well as synchronized axis sizes when charts are arranged vertically.

Before reading this topic, it's worth to familiarize yourself with What is a Vertical Chart as well as the topic on Synchronizing Multiple Charts

### Recap on Vertical Charts

Vertical Charts are when a 2D cartesian chart is rotated 90 degrees, or transposed, so that series render from top to bottom as opposed to left to right.

In SciChart, vertical charts are implemented by setting the axis.axisAlignment, e.g.

`xAxis.axisAlignment = EAxisAlignment.Top; // or Bottom`

yAxis.axisAlignment = EAxisAlignemnt.Left; // or Right

This transposes the entire chart including series rendering, tooltips and annotations and resulting in a vertical chart which renders top to bottom.

Read more about creating Vertical Charts here.

### Recap on Synchronizing Multiple Charts

In SciChart.js, multiple charts may be synchronized to ensure that zooming/panning operations, tooltips or cursors and even axis sizes are synchronized. This allows you to create multi chart pane applications, or complex dashboards which zoom and pan or allow tooltips/cursors in unison.

The method to synchronize multiple charts involves several steps, which are laid out in the page Synchronizing Multiple Charts

## Creating a pair of Vertical Charts

We've created an example showing how to sync vertical charts below. First we will start off with the codepen, then share the code and walk through how it works.

Zoom and Pan the above chart to get a feel for how synchronized vertical charts work in a group!

First of all some HTML is required to create two vertical charts. For simplicity this has been included with inline styles showing how to arrange the two divs vertically.

- html

`<div id="scichart-root" style="display: flex">`

<div id="chart0Div" style="width: 50%; height: 100%; flex: 1"></div>

<div id="chart1Div" style="width: 50%; height: 100%; flex: 1"></div>

</div>

After that, some code to initialize the two charts can look like this:

- TS

`// Create Vertical Charts for synchronization`

const {

SciChartSurface,

NumericAxis,

FastLineRenderableSeries,

XyDataSeries,

SciChartJsNavyTheme,

EAxisAlignment

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const createSciChartSurface = async (divId, isFirstChart) => {

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divId, {

theme: new SciChartJsNavyTheme()

});

// Create some deliberate differences between chart 0 and chart 1

sciChartSurface.background = isFirstChart ? "#22365B" : "#18304A";

sciChartSurface.canvasBorder = isFirstChart ? { borderRight: 4, color: "#55698E" } : undefined;

sciChartSurface.xAxes.add(

new NumericAxis(wasmContext, {

axisTitle: isFirstChart ? "XAxis 0" : "XAxis 1",

axisAlignment: EAxisAlignment.Right

})

);

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

// Create some deliberate differences between chart 0 and chart 1

labelPrecision: isFirstChart ? 1 : 4,

axisTitle: isFirstChart ? "YAxis 0" : "YAxis 1",

axisAlignment: EAxisAlignment.Top,

rotation: -90,

axisBorder: { borderBottom: 3, color: "#55698E" }

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

This code initializes a SciChartSurface, creates xAxis and yAxis in the configuration to allow a vertical chart, and adds some data and a line series.

The function `createSciChartSurface`

creates a single chart, so this is called twice passing in a different `<div>`

ID in order to create the two vertical charts.

## Synchronizing Zooming, Panning and Tooltips on Vertical Charts

To synchronize the two charts, we have to carry out the following steps:

- Synchronize xAxis.visibleRange📘 on the two charts by using a AxisCore.visibleRangeChanged📘 callback
- Synchronize chart axis heights using a SciChartHorizontalGroup📘
- Finally, optionally synchronize chart modifiers (Cursor, Tooltips) using a modifierGroup📘

- Synchronizing Vertical Charts

`const { SciChartHorizontalGroup, ZoomPanModifier, MouseWheelZoomModifier, RolloverModifier } = SciChart;`

// or, for npm, import { SciChartHorizontalGroup, ... } from "scichart"

// Step 1: Synchronize the two chart visibleRanges

sciChartSurface0.xAxes.get(0).visibleRangeChanged.subscribe(data1 => {

sciChartSurface1.xAxes.get(0).visibleRange = data1.visibleRange;

});

sciChartSurface1.xAxes.get(0).visibleRangeChanged.subscribe(data1 => {

sciChartSurface0.xAxes.get(0).visibleRange = data1.visibleRange;

});

// Step 2: Synchronize the two chart axis sizes using SciChartHorizontalGroup

// this is useful in case the Y-axis have different sizes (heights) due to text formatting

// or visibleRange differences

const horizontalGroup = new SciChartHorizontalGroup();

horizontalGroup.addSurfaceToGroup(sciChartSurface0);

horizontalGroup.addSurfaceToGroup(sciChartSurface1);

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

## Some Notes on Chart Synchronization with Vertical Charts

Adding a modifierGroup📘 to specific chart modifiers will ensure that mouse events from one chart are passed to the other and vice versa. This will actually cause zooming, panning, mousewheel and tooltip/cursor behaviour to occur on all charts (when one chart is interacted with).

However, from an axis range point of view it is far more accurate to synchronize xAxis.visibleRange📘 on the two charts by using a AxisCore.visibleRangeChanged📘 callback. Mouse events are only accurate to a pixel and some inconsistencies can be built up with synchronized charts unless you also have the visibleRange synchronization.

Adding a SciChartHorizontalGroup📘 ensures that the yAxis sizes on the two charts are exactly the same. This step is optional but in case of differing sizes of the axis it will give a more consistent look. For horizontal chart groups you can use the SciChartVerticalGroup📘 helper class.