---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/uniform-heatmap-renderable-series/updating-realtime
scraped_at: 2025-11-28T18:24:45.945647
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/uniform-heatmap-renderable-series/updating-realtime

# Updating (Realtime) Heatmaps

The heatmap is supposed to be fully dynamic, enabling real-time graphics. The UniformHeatmapRenderableSeries📘 however does not support append, insert, update, remove functions like other DataSeries do.

You can however update the data and force a refresh simply by updating the data passed in by calling heatmapDataSeries.setZValues()📘 with a new 2-dimensional array, or by modifying part of the existing the 2d array and calling heatmapDataSeries.notifyDataChanged()📘.

Update part of a heatmap:

- TS

`// Create an empty 2D array of size height & width`

const initialZValues = zeroArray2D([height, width]);

// Create a Heatmap Data-series. Pass the heatValues as a number[][] to the UniformHeatmapDataSeries

const heatmapDataSeries = new UniformHeatmapDataSeries(wasmContext, {

xStart: 100,

xStep: 1,

yStart: 100,

yStep: 1,

zValues: initialZValues

});

// ...

// Later, update the data

initialZValues[5][6] = 123.4;

heatmapDataSeries.notifyDataChanged(); // Tell SciChart the data has changed

// You can also load an entirely new array with the function UniformHeatmapDataSeries.setZValues

const newZValues // type number[][]

heatmapDataSeries.setZValues(newZValues);

Here's a full working example below:

The full source-code for that example can be found below:

- TS

`// Demonstrates how to create and update a uniform heatmap chart with SciChart.js`

const {

SciChartSurface,

NumericAxis,

HeatmapColorMap,

UniformHeatmapDataSeries,

UniformHeatmapRenderableSeries,

SciChartJsNavyTheme

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

// Create a SciChartSurface with X & Y Axis

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

const WIDTH = 100;

const HEIGHT = 75;

const MAX_SERIES = 200;

let index = 20;

// This function generates data for the heatmap series example

function generateExampleData(width, height, cpMax, index, maxIndex) {

const { zeroArray2D } = SciChart;

// or, import { zeroArray2D } from "SciChart";

// Returns a 2-dimensional javascript array [height (y)] [width (x)] size

const zValues = zeroArray2D([height, width]);

const angle = (Math.PI * 2 * index) / maxIndex;

// When appending data to a 2D Array for the heatmap, the order of appending (X,Y) does not matter

// but when accessing the zValues[][] array, we set data [y] then [x]

for (let y = 0; y < height; y++) {

for (let x = 0; x < width; x++) {

const v =

(1 + Math.sin(x * 0.02 + angle)) * 50 +

(1 + Math.sin(y * 0.05 + angle)) * 50 * (1 + Math.sin(angle * 2));

const cx = width / 2;

const cy = height / 2;

const r = Math.sqrt((x - cx) * (x - cx) + (y - cy) * (y - cy));

const exp = Math.max(0, 1 - r * 0.008);

const zValue = v * exp + Math.random() * 10;

zValues[y][x] = zValue > cpMax ? cpMax : zValue;

}

}

return zValues;

}

// Create a Heatmap Data-series. Pass heatValues as a number[][] to the UniformHeatmapDataSeries

// Open the Codepen below to see the definition of this function

const heatmapDataSeries = new UniformHeatmapDataSeries(wasmContext, {

xStart: 0,

xStep: 1,

yStart: 0,

yStep: 1,

zValues: generateExampleData(WIDTH, HEIGHT, 200, index, MAX_SERIES)

});

// Create a Heatmap RenderableSeries with the color map. ColorMap.minimum/maximum defines the values in

// HeatmapDataSeries which correspond to gradient stops at 0..1

const heatmapSeries = new UniformHeatmapRenderableSeries(wasmContext, {

dataSeries: heatmapDataSeries,

useLinearTextureFiltering: false,

colorMap: new HeatmapColorMap({

minimum: 0,

maximum: 200,

gradientStops: [

{ offset: 1, color: "#EC0F6C" },

{ offset: 0.9, color: "#F48420" },

{ offset: 0.7, color: "#DC7969" },

{ offset: 0.5, color: "#67BDAF" },

{ offset: 0.3, color: "#50C7E0" },

{ offset: 0.2, color: "#264B93" },

{ offset: 0, color: "#14233C" }

]

})

});

sciChartSurface.renderableSeries.add(heatmapSeries);

const updateChart = () => {

// Cycle through generating data on timer tick. In reality this can be any [][] 2d array

const newZValues = generateExampleData(WIDTH, HEIGHT, 200, index++, MAX_SERIES);

// Update the heatmap z-values

heatmapDataSeries.setZValues(newZValues);

if (index >= MAX_SERIES) {

index = 0;

}

setTimeout(updateChart, 20);

};

updateChart();

### Updating the XStep, XStart, YStep, YStart or changing the size of heatmap

At the time of writing we have no way to update the xStep, xStart, yStep, yStart properties of a UniformHeatmapDataSeries once it has been created, but a workaround was posted at the SciChart Forum.