---
source: https://www.scichart.com/documentation/js/v4/2d-charts/subcharts-api/example-resizable-multi-pane-charts-with-sub-charts
scraped_at: 2025-11-28T18:24:51.102313
---

# https://www.scichart.com/documentation/js/v4/2d-charts/subcharts-api/example-resizable-multi-pane-charts-with-sub-charts

# Worked Example: Resizable Multi Pane Charts with SubCharts

In the previous worked example, we showed you how to create Dynamic Multi-Panel Charts with the SubCharts API. By following this tutorial, we showed you how to have a single SciChartSurface📘 instance with 1...N Sub-Charts, each acting as a linked panel in a vertical chart group. All zooming, panning operations are linked, and you can dynamically add and remove chart panes programmatically, or by clicking a button.

In this worked example, we're going to extend the multi-panel subchart group by adding Grid-Splitters, allowing you to dynamically resize chart panes in the group. In addition, we will add a Close button and Maximise button to allow you to manipulate the chart group.

## Resizable Chart Panels with SubCharts

Let's extend the previous example to allow resizing of dynamic chart panes using the SubCharts API.

Here's the full working example below as an embedded CodePen.

**Click "Add Chart" or "Remove Chart"**in order to dynamically change the number of chart panes using the SubCharts API.- Resize the chart panes by
**dragging the grid splitter.** **Click the close button**once you've added some charts to remove a panel.

In the following sections, we will explain the code and how it works.

### Extending the Code to include Resizable Grid-Splitters

The HTML hasn't changed and is still quite simple. However we've added some new classes to the CSS.

Here they are below:

- HTML
- CSS

`<div class="header">`

<button id="addChartBtn">Add Chart</button>

<button id="removeChartBtn">Remove Chart</button>

<span class="header-label">Click Add/Remove Chart. Drag to pan all charts</span>

</div>

<div id="scichart-root"></div>

`body {`

margin: 0;

overflow: hidden;

font-family: Arial;

}

.header {

height: 40px;

display: flex;

align-items: center;

padding: 0 10px;

background-color: #f5f5f5;

border-bottom: 1px solid #ddd;

box-sizing: border-box;

gap: 10px;

}

.header-label {

color: #333;

font-weight: bold;

margin-left: 10px;

}

#scichart-root {

width: 100%;

height: calc(100vh - 40px);

position: relative;

}

.grid-splitter {

position: absolute;

width: 100%;

height: 6px;

background-color: #92a8c6ff;

cursor: row-resize;

z-index: 100;

box-sizing: border-box;

display: flex;

align-items: center;

justify-content: center;

}

.grid-splitter::before {

content: "⋮";

color: #333;

font-size: 16px;

font-weight: bold;

transform: rotate(90deg);

display: block;

line-height: 6px;

letter-spacing: 2px;

}

.chart-close-button {

position: absolute;

right: 10px;

width: 20px;

height: 20px;

background: SteelBlue;

color: white;

border: none;

border-radius: 3px;

cursor: pointer;

display: flex;

align-items: center;

justify-content: center;

font-size: 12px;

z-index: 1000;

}

.chart-close-button:hover {

background: LightSteelBlue;

}

### The Chart Initialization Code

The Chart Initialization code has been updated in order to add grid splitter and close button elements to the DOM. Have a look at the updated `createDynamicPanelChart()`

function below.

- createDynamicPanelChart()

`// Async function to create a dynamic panel chart with SubCharts`

// Each chart will occupy 100% width, and each successive chart will occupy 1/n height

async function createDynamicPanelChart(divElementId) {

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

// Initialize minimum panel size

updateMinPanelSize();

// Update minimum panel size when window resizes

window.addEventListener("resize", updateMinPanelSize);

// Create axis synchronizer with initial range

const axisSynchronizer = new AxisSynchroniser();

// Create initial chart with two sub charts, each occupying 50% height

addNewChart(sciChartSurface, wasmContext, axisSynchronizer);

addNewChart(sciChartSurface, wasmContext, axisSynchronizer);

// Wire up button handlers

document.getElementById("addChartBtn").onclick = () => addNewChart(sciChartSurface, wasmContext, axisSynchronizer);

document.getElementById("removeChartBtn").onclick = () => removeChart(sciChartSurface, axisSynchronizer);

// return the parent scichartsurface and add/remove chart functions

return {

sciChartSurface,

addChart: () => addNewChart(sciChartSurface, wasmContext, axisSynchronizer),

removeChart: index => removeSpecificChart(index, sciChartSurface, axisSynchronizer)

};

}

createDynamicPanelChart("scichart-root");

This works as before, creating a single parent SciChartSurface📘 to occupy the `<div>`

with `Id="scichart-root"`

. To populate the chart with two chart-panes, `addNewChart()`

is called twice. Functions to `addChart()`

and `removeChart()`

are returned from `createDynamicPanelChart()`

to allow you to further customize the chart group programmatically after creation.

### Updated addNewChart() Code

So how does `addNewChart()`

work? This function has been extended to handle creation and management of grid splitters and close buttons. You can find the code below:

- addNewChart()

`// Function for adding a new SubChart to an existing parent SciChartSurface.`

// All subcharts will be resized to occupy equal height on the parent surface.

function addNewChart(

parentSciChartSurface: SciChartSurface,

wasmContext: TSciChart,

axisSynchronizer: AxisSynchroniser

) {

const chartCount = parentSciChartSurface.subCharts?.length ?? 0;

// Calculate new panel size

if (panelSizes.length === 0) {

panelSizes.push(1); // First panel takes full height

} else {

// Resize existing panels and add new one

const newSize = 1 / (chartCount + 1);

panelSizes = panelSizes.map(size => size * (chartCount / (chartCount + 1)));

panelSizes.push(newSize);

}

// Add new chart

const newChart = SciChartSubSurface.createSubSurface(parentSciChartSurface, {

position: new Rect(0, 0, 1, panelSizes[chartCount]),

theme: new SciChartJsNavyTheme(),

title: `Chart ${chartCount + 1}`,

titleStyle: { fontSize: 14 }

});

// Add splitter if this isn't the first chart

if (chartCount > 0) {

// Calculate the correct position for the splitter by summing all panel sizes before it

const splitterPosition = panelSizes.slice(0, chartCount).reduce((a, b) => a + b, 0);

const splitter = createSplitter(chartCount - 1, splitterPosition);

document.getElementById("scichart-root").appendChild(splitter);

setupSplitterEvents(splitter, parentSciChartSurface, axisSynchronizer);

}

// Update all chart positions

updateChartPositions(parentSciChartSurface);

updateSplitterPositions(); // Ensure all splitters are correctly positioned

// Add axes and modifiers

const xAxis = new NumericAxis(wasmContext, {

axisTitle: "XAxis",

axisTitleStyle: { fontSize: 12 }

});

newChart.xAxes.add(xAxis);

newChart.yAxes.add(

new NumericAxis(wasmContext, {

axisTitle: "YAxis",

axisTitleStyle: { fontSize: 12 }

})

);

// Add modifiers

newChart.chartModifiers.add(new ZoomPanModifier());

newChart.chartModifiers.add(new MouseWheelZoomModifier());

newChart.chartModifiers.add(new ZoomExtentsModifier());

// Add random data series

const dataSeries = new XyDataSeries(wasmContext);

const { xValues, yValues } = generateRandomData();

dataSeries.appendRange(xValues, yValues);

const lineSeries = new FastLineRenderableSeries(wasmContext, {

stroke: getRandomColor(),

strokeThickness: 2,

dataSeries

});

newChart.renderableSeries.add(lineSeries);

// Synchronize the x-axis

axisSynchronizer.addAxis(xAxis);

// Update close buttons for all charts

updateCloseButtons(parentSciChartSurface, axisSynchronizer);

return {

sciChartSurface: newChart,

wasmContext

};

}

Similar to before, we call SciChartSubSurface.createSubSurface()📘 to add a SubChart to the parent surface. This needs to be added at a specific position, and later in `addNewChart()`

we call `updateChartPositions()`

and `updateSplitterPositions()`

to reposition everything.

The helper function `createSplitter()`

is called to add a grid splitter into the DOM. `setupSplitterEvents()`

subscribes to pointer-down, pointer-move and pointer-up so that you can capture drag events by the user.

### Updated removeChart() Code

`removeChart()`

has also been updated to allow removal of a specific chart at index. This is wired into the close button event handler so you can click to remove a specific chart.Here's the code below:

- removeChart()

`// Helper function to remove a specific Sub-chart pane from a parent SciChartSurface`

function removeSpecificChart(index, parentSciChartSurface, axisSynchronizer) {

const chartCount = parentSciChartSurface.subCharts?.length ?? 0;

if (chartCount <= 1) return; // Keep at least one chart

const chartToRemove = parentSciChartSurface.subCharts[index];

// Remove axis from synchronizer before removing chart

axisSynchronizer.removeAxis(chartToRemove.xAxes[0]);

// Remove chart and update panel sizes

parentSciChartSurface.removeSubChart(chartToRemove);

panelSizes.splice(index, 1);

// Remove corresponding splitter

const splitters = document.querySelectorAll(".grid-splitter");

if (index > 0) {

splitters[index - 1].remove();

} else if (splitters.length > 0) {

splitters[0].remove();

}

// Normalize remaining panel sizes

const totalSize = panelSizes.reduce((a, b) => a + b, 0);

panelSizes = panelSizes.map(size => size / totalSize);

// Update positions

updateChartPositions(parentSciChartSurface);

updateSplitterPositions();

updateCloseButtons(parentSciChartSurface, axisSynchronizer);

}

// Function to reomve the last chart from the SciChartSurface

function removeChart(parentSciChartSurface, axisSynchronizer) {

removeSpecificChart(parentSciChartSurface.subCharts.length - 1, parentSciChartSurface, axisSynchronizer);

}

## Conclusion

Using the SubCharts API it's possible to create a multi-pane synchronized chart group in SciChart. This places one or more child chart surfaces on a parent chart, which all share the same WebGL canvas, context and drawing loop. The single unified nature of drawing with SubCharts ensures high performance on all browsers, and allows you to create dynamic linked multi-chart applications such as financial apps, telemetry monitoring apps and more using SciChart.js.

You can see the full source-code for this example by clicking "Edit on CodePen" button in the embedded example at the top of the page.