---
source: https://www.scichart.com/documentation/js/v4/2d-charts/subcharts-api/exampe-dynamic-multi-panel-charts-with-sub-charts
scraped_at: 2025-11-28T18:24:50.381408
---

# https://www.scichart.com/documentation/js/v4/2d-charts/subcharts-api/exampe-dynamic-multi-panel-charts-with-sub-charts

# Worked Example: Dynamic Multi-panel charts with SubCharts

Sub-Charts allows you to create re-usable multi-chart components that are managed by a single SciChartSurface📘 instance.

For example, in telemetry monitoring applications, you might need to create a group of charts which are arranged vertically, and dynamically add/remove chart panes to the group. This can be done in several ways, for example we have tutorials how to do this in JavaScript (Linking Multiple Charts). This tutorial use SciChartSurface.create(), which creates a single SciChartSurface📘 in a `<div>`

, allowing you to add series, data, axis, modifiers and annotations to the chart.

However, in some browsers like Mozilla Firefox, creating multiple charts using SciChartSurface.create() results in slower performance when rendering/drawing. This is because Mozilla (and even safari) are not optimised for high performance when copying WebGL content to multiple canvases.

As a solution, SubCharts can allow you to create a single shared SciChartSurface📘 and place multiple child charts on it (nested charts within charts).

## Dynamic Multi-Pane Charts with SubCharts Example

Let's create an example to add/remove chart panes dynamically with SubCharts, synchronizing the X-Axis so that zooming, panning operations occur across all charts.

Here's the full working example below as an embedded codepen. **Click "Add Chart" or "Remove Chart" in order to dynamically change the number of chart panes using the SubCharts API.**

In the following sections, we will explain the code and how it works.

### Creating the Code for a Multi-Panel Chart Group with SubCharts

#### HTML/CSS

Let's start by creating our HTML.

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

}

The provided **HTML structure** creates a simple **user interface for managing dynamic charts** using SciChart. It consists of two main elements: a `.header`

div and a `#scichart-root`

div. The `.header`

contains two buttons, **"Add Chart"** and **"Remove Chart"**, which allow users to dynamically modify the number of charts. Additionally, a `<span>`

element (`.header-label`

) provides instructions, informing users that they can add/remove charts and use drag gestures for panning. Below the header, the `#scichart-root`

div acts as the container where the SciChart surfaces and sub-charts will be rendered.

The `#scichart-root`

container is configured to **occupy the entire remaining viewport height** (`calc(100vh - 40px)`

), ensuring the chart fully utilizes the available space without overflowing.

#### Chart Initialization Code

Next, let's create the JavaScript:

- createDynamicPanelChart()

`// Async function to create a dynamic panel chart with SubCharts`

// Each chart will occupy 100% width, and each successive chart will occupy 1/n height

async function createDynamicPanelChart(divElementId) {

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

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

removeLastChart: () => removeChart(sciChartSurface, axisSynchronizer)

};

}

createDynamicPanelChart("scichart-root");

The `createDynamicPanelChart`

function initializes a **dynamic multi-panel chart** using SciChart's `SubCharts`

API, where each chart is stacked vertically and resizes automatically as new charts are added. It begins by creating a **parent** `SciChartSurface`

inside the provided `divElementId`

. An `AxisSynchroniser`

is also initialized to ensure that all charts share the same X-axis range. The function then calls `addNewChart`

, which creates the **first sub-chart occupying the full height** of the container. As more charts are added, each will dynamically resize to maintain equal height distribution across the available space.

The function also wires up **event handlers** for buttons (`addChartBtn`

and `removeChartBtn`

) that allow users to add or remove sub-charts interactively. Clicking the "Add Chart" button calls `addNewChart`

, which resizes existing charts and inserts a new one at the bottom, while clicking "Remove Chart" triggers `removeChart`

, which deletes the last sub-chart and resizes the remaining ones. Finally, `createDynamicPanelChart`

returns an object containing the `sciChartSurface`

and functions for adding or removing charts, making it easy to manipulate the chart layout programmatically. The function is immediately invoked with `"scichart-root"`

as the container, ensuring that the chart initializes when the script runs.

#### Adding and Removing Chart Panes from the SubChart Group

- addNewChart()

`// Function for adding a new SubChart to an existing parent SciChartSurface.`

// All subcharts will be resized to occupy equal height on the parent surface.

function addNewChart(

parentSciChartSurface: SciChartSurface,

wasmContext: TSciChart,

axisSynchronizer: AxisSynchroniser

) {

const chartCount = parentSciChartSurface.subCharts?.length ?? 0;

const newChartHeight = 1.0 / (chartCount + 1);

console.log(`Adding new chart. Chart count: ${chartCount}, New chart height: ${newChartHeight}`);

// Resize existing charts

for (let i = 0; i < chartCount; i++) {

const chart = parentSciChartSurface.subCharts[i];

chart.subPosition = new Rect(0, i * newChartHeight, 1, newChartHeight);

}

// Add new chart

const newChart = SciChartSubSurface.createSubSurface(parentSciChartSurface, {

position: new Rect(0, chartCount * newChartHeight, 1, newChartHeight),

theme: new SciChartJsNavyTheme(),

title: `Chart ${chartCount + 1}`,

titleStyle: { fontSize: 14 }

});

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

return {

sciChartSurface: newChart,

wasmContext

};

}

The `addNewChart()`

function calls SciChartSubSurface.createSubSurface()📘 to dynamically add a **new sub-chart** to an existing `SciChartSurface`

while ensuring that all sub-charts within the parent surface are resized to **equal heights**.

The function then **adds numeric X and Y axes** to the new chart, with the X-axis being **synchronized** across all charts using `axisSynchronizer`

. Several interactive modifiers—`ZoomPanModifier`

, `MouseWheelZoomModifier`

, and `ZoomExtentsModifier`

—are attached, enabling **zooming, panning, and scaling** for better usability.

Finally, the function returns the newly created sub-chart (`sciChartSurface`

) along with `wasmContext`

, allowing the caller to further customize the chart or add data series. This approach makes it easy to **dynamically expand a multi-chart layout**, ensuring a consistent and interactive user experience.

- removeChart()

`// Helper function to remove a Sub-chart pane from a parent SciChartSurface`

function removeChart(parentSciChartSurface, axisSynchronizer) {

const chartCount = parentSciChartSurface.subCharts?.length ?? 0;

if (chartCount <= 1) return; // Keep at least one chart

const chartToRemove = parentSciChartSurface.subCharts[chartCount - 1];

// Remove axis from synchronizer before removing chart

axisSynchronizer.removeAxis(chartToRemove.xAxes[0]);

// Remove chart

parentSciChartSurface.removeSubChart(chartToRemove);

// Resize remaining charts

const newChartHeight = 1.0 / (chartCount - 1);

for (let i = 0; i < chartCount - 1; i++) {

const chart = parentSciChartSurface.subCharts[i];

chart.subPosition = new Rect(0, i * newChartHeight, 1, newChartHeight);

}

}

The `removeChart`

function is responsible for dynamically **removing the last sub-chart** from a parent `SciChartSurface`

, ensuring that at least one chart remains visible. It first determines the current number of sub-charts via SciChartSurface.subCharts.length📘 and exits early if there is only one left.

If multiple charts exist, the function selects the last sub-chart and **removes its X-axis from the** `axisSynchronizer`

to prevent synchronization issues. This ensures that when the chart is deleted, its axis does not affect the remaining ones. Once the axis is removed, the function **removes the sub-chart** from the `SciChartSurface`

by calling SciChartSurface.removeSubChart()📘, reducing the number of displayed charts by one.

After removing the chart, the function **resizes and repositions the remaining sub-charts** by calling SciChatSubSurface.subPosition📘 to maintain an equal height distribution. It calculates the new height for each chart and updates their positions by calling . This ensures a consistent layout, where the remaining charts automatically expand to fill the available space.

Note that subPosition📘 is updated with a Rect which contains relative sizing (for more info see SubCharts Positioning)

#### Synchronizing Zooming, Panning across the SubCharts

- AxisSynchroniser

`// Helper class to synchronize the visible range of multiple axes in multi-chart examples`

class AxisSynchroniser {

visibleRange: NumberRange = new NumberRange(0, 10);

axes: NumericAxis[] = [];

visibleRangeChanged: EventHandler<any>;

constructor(initialRange?: NumberRange, axes?: NumericAxis[]) {

this.visibleRange = initialRange ?? this.visibleRange;

this.visibleRangeChanged = new EventHandler();

this.publishChange = this.publishChange.bind(this);

if (axes) {

axes.forEach(a => this.addAxis(a));

}

}

publishChange(data) {

this.visibleRange = data.visibleRange;

this.axes.forEach(a => (a.visibleRange = this.visibleRange));

this.visibleRangeChanged.raiseEvent(data);

}

addAxis(axis) {

if (!this.axes.includes(axis)) {

this.axes.push(axis);

axis.visibleRange = this.visibleRange;

axis.visibleRangeChanged.subscribe(this.publishChange);

}

}

removeAxis(axis) {

const index = this.axes.findIndex(a => a === axis);

if (index >= 0) {

this.axes.splice(index, 1);

axis.visibleRangeChanged.unsubscribe(this.publishChange);

}

}

}

The `AxisSynchroniser`

class ensures that multiple **axes in different sub-charts stay synchronized** by maintaining a shared `visibleRange`

. It initializes with an optional `initialRange`

and a list of axes, subscribing them to a `visibleRangeChanged`

event. The `publishChange`

method updates the stored `visibleRange`

and propagates the change to all registered axes, keeping them in sync. The `addAxis`

method registers a new axis, ensuring it adopts the shared `visibleRange`

and subscribes to changes, while `removeAxis`

removes an axis and unsubscribes it from updates. This class is essential for multi-chart setups where zooming or panning in one chart should update all others.

You can see the full source-code for this example by clicking "Edit on CodePen" button in the embedded example at the top of the page.