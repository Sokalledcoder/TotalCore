---
source: https://www.scichart.com/documentation/js/v4/get-started/tutorials-js-npm-webpack/tutorial-05-zoom-and-pan-with-realtime-updates
scraped_at: 2025-11-28T18:25:02.289736
---

# https://www.scichart.com/documentation/js/v4/get-started/tutorials-js-npm-webpack/tutorial-05-zoom-and-pan-with-realtime-updates

# Tutorial 05 - Zoom and Pan with Realtime Updates

In Tutorial 04 - Adding Realtime Updates, we showed you how to dynamically update DataSeries to enable Real-time updates in SciChart.js. In this tutorial, were going to show you how to allow zooming and panning while scrolling data.

If you haven't read it already, also check out Tutorial 03 - Adding Zooming Panning Behavior as we will assume you have the knowledge to add zoom and pan behaviors to a SciChart.js JavaScript chart.

The source code for this tutorial can be found at SciChart.JS.Examples Github Repository

## Creating the Base Application

We're going to start off with the code we created in the previous Tutorial 04 - Adding Realtime Updates. If you haven't already started that tutorial, please run through it first so you can understand the concepts.

**Start with this code to begin with**. This will create a real-time chart with scrolling data, **but no zooming or panning yet.**

- index.js
- index.html

`import {`

SciChartSurface,

NumericAxis,

XyDataSeries,

FastLineRenderableSeries,

XyScatterRenderableSeries,

EllipsePointMarker,

NumberRange

} from "scichart";

async function initSciChart() {

// Create the SciChartSurface in the div 'scichart-root'

// The SciChartSurface, and webassembly context 'wasmContext' are paired. This wasmContext

// instance must be passed to other types that exist on the same surface.

const {sciChartSurface, wasmContext} = await SciChartSurface.create("scichart-root");

// Create an X,Y Axis and add to the chart

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

// Create a Scatter series, and Line series and add to chart

const scatterSeries = new XyScatterRenderableSeries(wasmContext, {

pointMarker: new EllipsePointMarker(wasmContext, { width: 7, height: 7, fill: "White", stroke: "SteelBlue" }),

});

const lineSeries = new FastLineRenderableSeries(wasmContext, { stroke: "#4083B7", strokeThickness: 2 });

sciChartSurface.renderableSeries.add(lineSeries, scatterSeries);

// Create and populate some XyDataSeries with static data

// Note: you can pass xValues, yValues arrays to constructors, and you can use appendRange for bigger datasets

const scatterData = new XyDataSeries(wasmContext, { dataSeriesName: "Cos(x)" });

const lineData = new XyDataSeries(wasmContext, { dataSeriesName: "Sin(x)" });

for(let i = 0; i < 1000; i++) {

lineData.append(i, Math.sin(i*0.1));

scatterData.append(i, Math.cos(i*0.1));

}

// Assign these dataseries to the line/scatter renderableseries

scatterSeries.dataSeries = scatterData;

lineSeries.dataSeries = lineData;

// SciChart will now redraw with static data

//

// #region ExampleA

// Scrolling the chart by appending and manipulating xAxis.visibleRange

const updateDataFunc = () => {

// Append another data-point to the chart. We use dataSeries.count()

// to determine the current length before appending

const i = lineData.count();

lineData.append(i, Math.sin(i * 0.1));

scatterData.append(i, Math.cos(i * 0.1));

// Apply scrolling to the chart by updating xAxis.visibleRange

// Also see dataSeries.fifoCapacity and dataSeries.fifoSweeping for more options

const xAxis = sciChartSurface.xAxes.get(0);

xAxis.visibleRange = new NumberRange(i-1000, i);

};

// Repeat at 60Hz

setInterval(updateDataFunc, 1000/60);

// #endregion

}

initSciChart();

`<html lang="en-us">`

<head>

<meta charset="utf-8" />

<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />

<link rel="icon" href="data:," />

<title>SciChart.js Tutorial 4 - Part 3, Realtime Scrolling</title>

<script async type="text/javascript" src="bundle.js"></script>

<style>

body {

font-family: "Arial";

}

</style>

</head>

<body>

<h1>Hello SciChart.js world!</h1>

<p>

In this example we explore real-time updates by scrolling data in

SciChart.js

</p>

<!-- the Div where the SciChartSurface will reside -->

<div id="scichart-root" style="width: 800px; height: 600px"></div>

</body>

</html>

## Adding Zooming Behavior

From Tutorial 03 - Adding Zooming, Panning Behavior, we learned that we can add ChartModifiers to the sciChartSurface.chartModifiers📘 collection to add specific zoom, or pan behaviors to the chart.

However, the code we added to scroll the chart on update is going to conflict with the user mouse-zooming behaviors. Take a look below:

- Zooming and Panning Step 1

` ...`

import {

RubberBandXyZoomModifier,

ZoomExtentsModifier,

} from "scichart";

async function initSciChart() {

// Add this code to enable zooming by mouse-drag and double-click to zoom extents

//

sciChartSurface.chartModifiers.add(new ZoomExtentsModifier({isAnimated: false}));

sciChartSurface.chartModifiers.add(new RubberBandXyZoomModifier());

...

const updateDataFunc = () => {

// Append another data-point to the chart. We use dataSeries.count()

// to determine the current length before appending

const i = lineData.count();

lineData.append(i, Math.sin(i * 0.1));

scatterData.append(i, Math.cos(i * 0.1));

// However, user-zoom will conflict with this code which scrolls the chart on update

xAxis.visibleRange = new NumberRange(i-1000, i);

};

// Repeat at 60Hz

setInterval(updateDataFunc, 1000 / 60);

...

}

initSciChart();

If we want to enable user-zoom, and also scroll the chart, we need to selectively implement that scroll. To do so we can use the sciChartSurface.zoomState📘 property.

## The sciChartSurface.zoomState Property

The sciChartSurface.zoomState📘 property allows us to detect if the chart has been zoomed or panned by the user, or if the chart is at extents of the data. You can take a look at the values of the EZoomState Enum here📘.

If we modified our code, we can selectively use this property to detect if the user is zooming and halt any automatic scrolling. For example, try modifying the updateDataFunc as follows:

- Part1/index.js

`// import {`

// ZoomExtentsModifier, RubberBandZoomModifier,

// } from "scichart";

// Add ZoomExtentsModifier and disable extents animation

sciChartSurface.chartModifiers.add(

new ZoomExtentsModifier({ isAnimated: false })

);

// Add RubberBandZoomModifier

sciChartSurface.chartModifiers.add(new RubberBandXyZoomModifier());

// Part 2: Appending data in realtime

//

const updateDataFunc = () => {

// Append another data-point to the chart. We use dataSeries.count()

// to determine the current length before appending

const i = lineData.count();

lineData.append(i, Math.sin(i * 0.1));

scatterData.append(i, Math.cos(i * 0.1));

// import { ZoomState } from "scichart";

//

// Using zoomState, we only scroll if the state is not userZooming

// This property is set internally whenever the user mouse-down drags on the chart or

// performs a zoom operation, and can be used to selectively enable or disable scrolling

if (sciChartSurface.zoomState !== EZoomState.UserZooming) {

xAxis.visibleRange = new NumberRange(i - 1000, i);

}

};

// Repeat at 60Hz

setInterval(updateDataFunc, 1000 / 60);

Now run the application again, click left mouse button and move it to select an area. After releasing the button the chart will be zoomed in. To resume realtime updates perform double click.

## Adding Panning Behavior to a Realtime Chart

In order to add ZoomPanModifier, update the code as follows. Don't forget to include the same ZoomState logic as we had before.

- Part2/index.js

`// import {`

// ZoomExtentsModifier, RubberBandZoomModifier,

// ZoomPanModifier, EExecuteOn, EModifierMouseArgKey

// } from "scichart";

// Add ZoomExtentsModifier and RubberBandZoomModifier

sciChartSurface.chartModifiers.add(

new ZoomExtentsModifier({ isAnimated: false })

);

sciChartSurface.chartModifiers.add(new RubberBandXyZoomModifier());

// Add ZoomPanModifier enabled on right-mouse button

sciChartSurface.chartModifiers.add(

new ZoomPanModifier({

executeCondition: { button: EExecuteOn.MouseRightButton, key: EModifierMouseArgKey.None }

})

);

// Part 2: Appending data in realtime

//

const updateDataFunc = () => {

// Append another data-point to the chart. We use dataSeries.count()

// to determine the current length before appending

const i = lineData.count();

lineData.append(i, Math.sin(i * 0.1));

scatterData.append(i, Math.cos(i * 0.1));

// Prevent changing visibleRange if user is zooming or panning

if (sciChartSurface.zoomState !== EZoomState.UserZooming) {

xAxis.visibleRange = new NumberRange(i - 1000, i);

}

};

You can use ChartModifierBase.executeCondition📘 to make it work with different mouse button or mouse button + Ctrl/Alt/Shift button. Like we did in the example above

`new ZoomPanModifier({`

executeCondition: { button: EExecuteOn.MouseRightButton, key: EModifierMouseArgKey.None }

});

Now run the application again, left click the chart and move the mouse. As a result the chart will moving with the mouse. To pan the chart, use the right mouse button. To resume realtime updates perform double click.

## Further Examples - the Realtime Ticking Stock Chart demo

In the SciChart.js Examples Suite - viewable at scichart.com/demo, we have an example of realtime updates with zooming & panning built into the chart. This is the JavaScript Realtime Ticking Stock Charts example.

In this example as new candle data is added, the chart advances by 1 to automatically keep the new candle in the same place in the viewport. However, if you scroll back in time so that the latest candle is out of the viewport, the advancing by 1 does not occur.

To achieve this, we use techniques similar to the above tutorial to selectively advance the chart by one candle **only if the latest data-point is inside the viewport**.

This allows you to create an intuitive user zooming, panning experience while advancing the chart or scrolling as new data comes in.

- TS

` // Is the latest candle in the viewport?`

if (xAxis.visibleRange.max > getLatestCandleDate) {

// If so, shift the xAxis by one candle

const dateDifference = priceBar.date / 1000 - getLatestCandleDate;

const shiftedRange = new NumberRange(

xAxis.visibleRange.min + dateDifference,

xAxis.visibleRange.max + dateDifference

);

xAxis.animateVisibleRange(shiftedRange, 250, easing.inOutQuad);

}

And the Source-code for how we achieved it at our Github repository, in file createCandlestickChart.ts, function **onNewTrade()**.