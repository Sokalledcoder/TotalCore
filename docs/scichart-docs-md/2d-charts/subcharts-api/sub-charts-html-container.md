---
source: https://www.scichart.com/documentation/js/v4/2d-charts/subcharts-api/sub-charts-html-container
scraped_at: 2025-11-28T18:24:52.008725
---

# https://www.scichart.com/documentation/js/v4/2d-charts/subcharts-api/sub-charts-html-container

# SubCharts Html Container

Another feature of the SubCharts API is an ability to add custom HTML content around a sub-chart.

When adding a Sub Chart to a SciChartSurface with the SciChartSubSurface.createSubSurface()📘 function, you can place extra optional HTML elements into the DOM. By specifying their IDs and classes to the SubChart, they can be positioned on top of, and around the SciChartSubSurface📘.

This is achieved by composing following required HTML elements:

- the element used to create the main surface.**scichart-root-element**- the element which will be displayed at the sub-surface position. It will have the sub-surface and custom html inside; more sub-chart containers could be added if there are many sub-charts.**sub-chart-container**- the element which will hold the actual custom HTML content; sections are placed to the sides of a sub-surface accordingly to their class names: left-section, right-section, top-section, bottom-section.**chart-html-section**

Here is the setup required for the example: We will start from adding HTML markup which corresponds to the descriptions above. CSS is also added to give the HTML elements size and note that each have `position: absolute`

.

- HTML
- CSS

`<!-- the Div where the SciChartSurface will reside -->`

<div id="scichart-root"></div>

<!-- the div where a custom HTML elements could reside, its size and position will be managed by SciChartSurface -->

<div id="sub-chart-container-id-1" class="sub-chart-container">

<div class="chart-html-section left-section">A left section of the sub-chart</div>

<div class="chart-html-section right-section">Right Section</div>

<div class="chart-html-section top-section">Top Section</div>

<div class="chart-html-section bottom-section">Bottom Section</div>

</div>

`body {`

margin: 0;

}

#scichart-root {

width: 100%;

height: 100vh;

}

.sub-chart-container {

position: absolute;

border: 1px solid red;

}

.chart-html-section {

pointer-events: all;

position: absolute;

}

.left-section {

width: 100px;

height: 100%;

background-color: rgba(212, 245, 66, 0.5);

}

.right-section {

top: 0;

right: 0;

width: 100px;

height: 100%;

background-color: rgba(226, 78, 14, 0.5);

}

.top-section {

top: 0;

width: calc(100% - 200px);

height: 50px;

position: absolute;

left: 100px;

background-color: rgba(236, 66, 245, 0.5);

}

.bottom-section {

bottom: 0;

width: calc(100% - 200px);

height: 50px;

position: absolute;

left: 100px;

background-color: rgba(66, 245, 224, 0.5);

}

In the JavaScript, we create a SubChart as normal by calling SciChartSubSurface.createSubSurface()📘, however we also specify I2DSubSurfaceOptions.subChartContainerId📘. This property accepts both string (Id) or `HtmlDivElement`

. We also specify class names that will identify sections of the container.

- TS
- Builder API (JSON Config)

`// Add a Sub-Charts to the main surface. This will display a rectangle showing the current zoomed in area on the parent chart`

const subChart1 = SciChartSubSurface.createSubSurface(sciChartSurface, {

position: new Rect(0.1, 0.1, 0.6, 0.4),

isTransparent: false,

isVisible: true,

coordinateMode: ESubSurfacePositionCoordinateMode.Relative,

title: "SubChart with HTML Elements",

titleStyle: { fontSize: 16, color: "#eeeeee77" },

// Specify the subChartContainer for extra HTML elements

// These will be positioned by SciChartSubSurface

// This property accepts a string or an HTMLDivElement

subChartContainerId: "sub-chart-container-id-1"

});

// specify class names of section elements within the sub-chart container

subChart1.topSectionClass = "top-section";

subChart1.leftSectionClass = "left-section";

subChart1.bottomSectionClass = "bottom-section";

subChart1.rightSectionClass = "right-section";

`const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {`

surface: { theme: { type: EThemeProviderType.Dark } },

// Main chart definition is here

xAxes: { type: EAxisType.NumericAxis },

yAxes: { type: EAxisType.NumericAxis },

// Subchart definition is here

subCharts: [

{

surface: {

position: new Rect(0.1, 0.1, 0.6, 0.4),

isTransparent: false,

isVisible: true,

coordinateMode: ESubSurfacePositionCoordinateMode.Relative,

title: "SubChart with HTML Elements",

titleStyle: { fontSize: 16, color: "#eeeeee77" },

// Specify the subChartContainer for extra HTML elements

// These will be positioned by SciChartSubSurface

// This property accepts a string or an HTMLDivElement

subChartContainerId: "sub-chart-container-id-1"

},

// Define the x,y axis on Subchart

xAxes: { type: EAxisType.NumericAxis },

yAxes: { type: EAxisType.NumericAxis },

// Define the series on Subchart

series: [

{

type: ESeriesType.LineSeries,

xyData: {

xValues,

yValues: yValues

},

options: {

stroke: "#0066FF",

strokeThickness: 5

}

}

]

}

]

});

As a result the container will be drawn with the position and sizes specified when creating the sub-surface, while the sub-surface itself will shrink accordingly to the space occupied by the custom content sections.

**Note** left-section, right-section, top-section, bottom-section are the default values used for the class names of sections.

The HTML Elements and CSS styles can also be added programmatically, that way extra elements around Sub-Charts can also be fully dynamic. We'll show you how in the next section.

## Creating a Draggable Header on SubCharts

Let's create a concrete example of using HTML Containers with SubCharts. In this updated example we will create some HTML elements and place them dynamically using JavaScript. This will give the effect of creating a draggable SubChart on a SciChartSurface.

First let's create a function to create a Sub-Chart with container HTML.

- createSubChartContainer()

`function createSubChartContainer(sciChartSurface: SciChartSurface, subChartOptions: I2DSubSurfaceOptions) {`

// Create the subChartContainer HTML and add to the DOM

const container = document.createElement("div");

container.id = generateGuid(); // generateGuid imported from SciChart

container.style.position = "absolute";

container.style.border = "1px solid #4682b4";

document.body.appendChild(container);

const { title, ...subChartOptionsNoTitle } = subChartOptions;

// Create a top bar header HTML element for the subchart

const topBar = document.createElement("div");

topBar.style.pointerEvents = "all";

topBar.style.position = "absolute";

topBar.style.top = "0";

topBar.style.width = "100%";

topBar.style.height = "30px";

topBar.style.backgroundColor = "#4682b4";

// className is required to specify that this is a top-section bar, to be positioned outside the chart

// even if this class isn't used or specified in the DOM.

// Default available options are "top-section", "bottom-section", "left-section", "right-section"

topBar.className = "top-section";

container.appendChild(topBar);

const containerTitle = document.createElement("span");

containerTitle.style.userSelect = "none";

containerTitle.style.color = "#eee";

containerTitle.style.fontFamily = "Arial";

containerTitle.style.fontWeight = "Bold";

containerTitle.style.left = "10px";

containerTitle.style.top = "5px";

containerTitle.style.position = "relative";

containerTitle.innerText = title as string;

topBar.appendChild(containerTitle);

// Add a Sub-Charts to the main surface. This will display a rectangle showing the current zoomed in area on the parent chart

const subChart = SciChartSubSurface.createSubSurface(sciChartSurface, {

...subChartOptionsNoTitle,

theme: sciChartSurface.themeProvider,

// Specify the subChartContainer

subChartContainerId: container

});

// Track dragging state

let isDragging = false;

let startX = 0;

let startY = 0;

let startRect;

// Handle pointer down to start drag

container.onpointerdown = e => {

isDragging = true;

startX = e.clientX;

startY = e.clientY;

startRect = subChart.subPosition;

// Capture pointer to receive events outside container

container.setPointerCapture(e.pointerId);

};

// Handle pointer move to update position

container.onpointermove = e => {

if (!isDragging) return;

// Calculate delta movement in pixels

const deltaX = e.clientX - startX;

const deltaY = e.clientY - startY;

// Convert pixel movement to relative coordinates (0..1)

const parentWidth = sciChartSurface.domChartRoot.clientWidth;

const parentHeight = sciChartSurface.domChartRoot.clientHeight;

const relativeX = deltaX / parentWidth;

const relativeY = deltaY / parentHeight;

// Update subchart position

subChart.subPosition = new Rect(

startRect.x + relativeX,

startRect.y + relativeY,

startRect.width,

startRect.height

);

};

// Handle pointer up to end drag

container.onpointerup = e => {

isDragging = false;

container.releasePointerCapture(e.pointerId);

};

return subChart;

}

This function creates a container `<div>`

element with a unique Id and adds it to the DOM. It creates a topBar `<div>`

and adds that to the container. CSS styles are applied to ensure `position: absolute`

and the `className = "top-section"`

is applied to the topBar, which helps SciChart position the element around the SubChart. We destructure the options so that the title can be set on the topBar and create the SubChart speciying the `subChartContainerId`

as an HTMLElement (also supports string Id).

Next, by subscribing to `container.onpointerdown`

, `onpointermove`

and `onpointerup`

we can reposition the SubChart by calling `SciChartSubSurface.subPosition`

. Note that this accepts a `Rect`

with relative coordinates, so we have to calculate that based on the parent `sciChartSurface.domChartRoot`

width & height.

Note that the use of `position: absolute`

and applying applying `className = "top-section"`

helps SciChart position the top section above the SubChart.

The SubChart can now be added to a parent SciChartSurface as follows:

- Add SubChart

`const subChart = createSubChartContainer(sciChartSurface, {`

position: new Rect(0.1, 0.1, 0.4, 0.4),

isTransparent: false,

isVisible: true,

coordinateMode: ESubSurfacePositionCoordinateMode.Relative,

title: "Draggable Sub-Chart Window"

});

// Add x,y axis to the subchart

subChart.xAxes.add(new NumericAxis(wasmContext));

subChart.yAxes.add(new NumericAxis(wasmContext));

// Add a series to the subchart

subChart.renderableSeries.add(

new FastLineRenderableSeries(wasmContext, {

stroke: "#47bde6",

strokeThickness: 5,

dataSeries: new XyDataSeries(wasmContext, {

xValues,

yValues

})

})

);

This declares a SubChart with initial position, and adds some x,y axis and series.

Here's the result. You can now have a draggable SubChart window in a SciChartSurface!