---
source: https://www.scichart.com/documentation/js/v4/2d-charts/subcharts-api/example-using-sub-charts-to-create-large-dashboard
scraped_at: 2025-11-28T18:24:51.229140
---

# https://www.scichart.com/documentation/js/v4/2d-charts/subcharts-api/example-using-sub-charts-to-create-large-dashboard

# Worked Example: Using SubCharts to create a Large Dashboard

SubCharts API gives an ability to create multiple charts while providing a great rendering performance. All the charts on a SubChart use a single, shared WebGL context. This means 100s of charts can be placed on screen and update very fast.

SciChart supports unlimited charts on a page at different locations in the HTML DOM via our innovative, Shared WebGL context technology. See the section on SciChartSurface.create() vs. createSingle() for more background information about WebGL context limits.

The following SubCharts method provides a higher-performance way of creating large grids of charts in similar locations.

In this section we will show how to generate a 10x10 grid of sub-charts to demonstrate the abilities of the SubCharts API.

- TS
- Builder API (JSON Config)

// demonstrates how to create a massive 10x10 panel of charts using SubCharts API

async function create10x10PanelChart(divElementId) {

// Create a parent (regular) SciChartSurface which will contain the sub-chart

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

// Add a Sub-Charts to the main surface. This will display a rectangle showing the current zoomed in area on the parent chart

for (let subChartIndex = 0; subChartIndex < subChartsNumber; ++subChartIndex) {

const { rowIndex, columnIndex } = getSubChartPositionIndexes(subChartIndex, columnsNumber);

const width = 1 / columnsNumber;

const height = 1 / rowsNumber;

const position = new Rect(columnIndex * width, rowIndex * height, width, height);

const subChartOptions = {

subChartPadding: Thickness.fromNumber(5),

id: `subChart-${subChartIndex}`,

position

};

const subSurface = SciChartSubSurface.createSubSurface(sciChartSurface, subChartOptions);

subSurface.xAxes.add(

new NumericAxis(wasmContext, {

isVisible: false,

autoRange: EAutoRange.Always

})

);

subSurface.yAxes.add(new NumericAxis(wasmContext, { isVisible: false }));

// Add random data series

subSurface.renderableSeries.add(

new FastLineRenderableSeries(wasmContext, {

stroke: getRandomColor(),

strokeThickness: 2,

dataSeries: new XyDataSeries(wasmContext, {

fifoCapacity: dataCount * 20

})

})

);

// Add an annotation to the sub-chart showing the index

subSurface.annotations.add(

new TextAnnotation({

x1: 0,

y1: 0,

text: `${subChartIndex + 1}`,

xCoordinateMode: ECoordinateMode.Relative,

yCoordinateMode: ECoordinateMode.Relative,

horizontalAnchorPoint: EHorizontalAnchorPoint.Left,

verticalAnchorPoint: EVerticalAnchorPoint.Top,

fontSize: 16,

fontWeight: "bold",

textColor: "#FFFFFF",

background: "#00000077"

})

);

}

// If you return the parent chart to the caller

// you can access sciChartSurface.subCharts to configure the child chars (add series, data)

return {

sciChartSurface

};

}

`// Demonstrates how to create a 1x2 panel of charts using SubCharts and the Builder API`

async function builderExample(divElementId) {

// Demonstrates how to create a line chart with SciChart.js using the Builder API

const subCharts = [];

for (let subChartIndex = 0; subChartIndex < subChartsNumber; ++subChartIndex) {

const { rowIndex, columnIndex } = getSubChartPositionIndexes(subChartIndex, columnsNumber);

const width = 1 / columnsNumber;

const height = 1 / rowsNumber;

const position = new Rect(columnIndex * width, rowIndex * height, width, height);

subCharts.push({

surface: {

id: `subChart-${subChartIndex}`,

subChartPadding: Thickness.fromNumber(5),

position

},

xAxes: {

type: EAxisType.NumericAxis,

options: { isVisible: false }

},

yAxes: {

type: EAxisType.NumericAxis,

options: { isVisible: false }

},

series: {

type: ESeriesType.LineSeries,

xyData: {

fifoCapacity: dataCount,

xValues: generateRandomData(0).xValues,

yValues: generateRandomData(0).yValues

},

options: { stroke: "#44C8F1", strokeThickness: 3 }

}

});

}

const { sciChartSurface, wasmContext } = await chartBuilder.build2DChart(divElementId, {

surface: { padding: Thickness.fromNumber(0) },

subCharts

});

return {

sciChartSurface

};

}

Where `getSubChartPositionIndexes()`

, `getRandomColor()`

and `generateRandomData()`

are helper functions.

`getSubChartPositionIndexes()`

is used to calculate where a sub-chart should be placed on the grid`getRandomColor()`

- returns random color.`getRandomData()`

- to generate X and Y values.

For example, in this case:

- helper functions

`const subChartsNumber = 100;`

let columnsNumber = 10;

let rowsNumber = 10;

let colorIndex = 0;

function getRandomColor() {

return ["#274b92", "#47bde6", "#ae418d", "#e97064", "#68bcae", "#634e96"][colorIndex++ % 6];

}

let dataCount = 10;

const xValuesBuffer = new Float64Array(dataCount);

const yValuesBuffer = new Float64Array(dataCount);

function generateRandomData(xStart = 0) {

for (let i = 0; i < dataCount; i++) {

xValuesBuffer[i] = i + xStart;

yValuesBuffer[i] = Math.random();

}

return { xValues: xValuesBuffer, yValues: yValuesBuffer };

}

function getSubChartPositionIndexes(chartIndex, columnNumber) {

const rowIndex = Math.floor(chartIndex / columnNumber);

const columnIndex = chartIndex % columnNumber;

return { rowIndex, columnIndex };

}