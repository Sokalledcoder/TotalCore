---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/non-uniform-heatmap-renderable-series
scraped_at: 2025-11-28T18:24:34.648933
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/non-uniform-heatmap-renderable-series

# The Non-Uniform Heatmap Chart Type

A complementary type to the Uniform Heatmap is the Non-Uniform Heatmap, new to SciChart.js v2.3.

Non-Uniform Heatmaps can be created using the NonUniformHeatmapRenderableSeries📘 type.

The JavaScript Non-Uniform Heatmap Chart Example can be found in the SciChart.Js Examples Suite > Non-Uniform Heatmap Chart on Github

## Create a Non-Uniform Heatmap

Non-Uniform heatmaps are a variation on Uniform heatmaps, where you can specify independent sizes for heatmap rows and columns.

The cell sizes are specified either by an array of X,Y cell coordinates or a mapping function passed to the constructor options of NonUniformHeatmapDataSeries📘.

For example, you can create a Non-uniform Heatmap with the following code:

- TS
- Builder API (JSON Config)

`// Demonstrates how to create a uniform heatmap chart with SciChart.js`

const {

SciChartSurface,

NumericAxis,

HeatmapColorMap,

NonUniformHeatmapRenderableSeries,

NonUniformHeatmapDataSeries,

SciChartJsNavyTheme

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

// Create a SciChartSurface with X & Y Axis

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

// The data for the heatmap is a 2d Array of zValues [height][width]

// for example:

// const zValues = [

// [0, 2, 3.4],

// [5, 3, 4],

// [3, 1.5, -1],

// ];

const zValues = generateHeatmapData();

// Create the non-uniform heatmap series

const heatmapSeries = new NonUniformHeatmapRenderableSeries(wasmContext, {

// Pass in the 2d zValues array and x/yCellOffsets to give x,y positions

dataSeries: new NonUniformHeatmapDataSeries(wasmContext, {

zValues,

// arrays with the cell offsets

xCellOffsets: [0, 10, 20, 26, 36, 60, 72, 84],

yCellOffsets: [100, 250, 390, 410, 600]

}),

// zValues mapped to colours using the colorMap.

// zValue[y][x] when compared to HeatmapColorMap.maximum corresponds to gradientstop offset=1

// zValue[y][x] when compared to HeatmapColorMap.minimum corresponds to gradientstop offset=0

colorMap: new HeatmapColorMap({

minimum: 0,

maximum: 100,

gradientStops: [

{ offset: 0, color: "#14233C" },

{ offset: 0.2, color: "#264B93" },

{ offset: 0.3, color: "#50C7E0" },

{ offset: 0.5, color: "#67BDAF" },

{ offset: 0.7, color: "#DC7969" },

{ offset: 0.9, color: "#F48420" },

{ offset: 1, color: "#EC0F6C" }

]

}),

// optional settings

opacity: 0.77,

// values outside of the colorMap.min/max will be filled with the colours at edge of the colormap

fillValuesOutOfRange: true,

// Optional datalabels may be placed in cell

dataLabels: {

style: {

fontFamily: "Default",

fontSize: 16

},

color: "white"

}

});

sciChartSurface.renderableSeries.add(heatmapSeries);

`// Demonstrates how to create a line chart with SciChart.js using the Builder API`

const { chartBuilder, ESeriesType, HeatmapColorMap, EThemeProviderType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

series: {

type: ESeriesType.NonUniformHeatmapSeries,

options: {

colorMap: new HeatmapColorMap({

minimum: 0,

maximum: 100,

gradientStops: [

{ offset: 0, color: "#14233C" },

{ offset: 0.2, color: "#264B93" },

{ offset: 0.3, color: "#50C7E0" },

{ offset: 0.5, color: "#67BDAF" },

{ offset: 0.7, color: "#DC7969" },

{ offset: 0.9, color: "#F48420" },

{ offset: 1, color: "#EC0F6C" }

]

}),

dataLabels: {

style: { fontFamily: "Default", fontSize: 16 },

color: "White"

}

},

heatmapData: {

zValues: generateHeatmapData(),

xCellOffsets: [0, 10, 20, 26, 36, 60, 72, 84],

yCellOffsets: [100, 250, 390, 410, 600]

}

}

});

This results in the following output:

**Above:** The Non-Uniform Heatmap allows you to have uneven sizes for columns & rows in a javascript heatmap. In the case where you have equal cell sizes, use the Uniform Heatmap for faster performance.

In the code above:

- We create a 2D array (type
`number[][]`

). This is filled with heat values of the heatmap. - A NonUniformHeatmapDataSeries📘 instance is created with
`xCellOffsets = []`

and`yCellOffsets = []`

. This defines the position of the heatmap in X,Y space as well as the position of each column/row. - We set the Colormap, which maps colors to heat values in the dataseries.
- NonUniformHeatmapRenderableSeries📘 instance is created with INonUniformHeatmapRenderableSeriesOptions.dataSeries📘 and INonUniformHeatmapRenderableSeriesOptions.colorMap📘 options and added to the sciChartSurface.renderableSeries📘 collection.
- Alternatively we can assign a NonUniformHeatmapRenderableSeries.dataSeries📘 property separately.

### Updating Heatmap Values

The Uniform Heatmap documentation - Updating Heatmaps shows how you can update a heatmap dynamically, by using the setZValues()📘 function. The mechanism for the Non-uniform heatmap is the same.

### Heatmap Color Maps

The Uniform Heatmap documentation - ColorMaps and Legends shows how you can modify a heatmaps color mapping, which maps zValues to cell colors, by using the colorMap📘 property. The mechanism for the Non-uniform heatmap is the same.

### Adding Text in Cell to a Non-Uniform Heatmap

The Uniform Heatmap documentation shows how you can add text-in cell to a heatmap via the dataLabelProvider📘 property. The mechanism for the Non-uniform heatmap is the same.

### Adding a Heatmap Legend to a Non-Uniform Heatmap

The Uniform Heatmap documentation - ColorMaps and Legends shows how you can a HeatmapLegend📘 with colorMap to the heatmap chart. The mechanism for the Non-uniform heatmap is the same.

## Defining the x,y cell positions

As well as passing an array of x/yCellOffsets as a mapping function, it is possible to pass just arrays via INonUniformHeatmapSeriesOptions.xCellOffsets📘 and INonUniformHeatmapSeriesOptions.yCellOffsets📘.

The function should generate cell offsets based on the index. This feature is useful when dataSeries are updated dynamically with NonUniformHeatmapDataSeries.setZValues📘, which will trigger recalculation of the offsets.

### Both the following two code examples are valid:

`// Passing just cell Offset Arrays`

const xRangeOffsetsSource = [0, 10, 20, 26, 36, 60, 72, 84];

const yRangeOffsetsSource = [100, 250, 390, 410, 600];

const dataSeries = new NonUniformHeatmapDataSeries(wasmContext, {

zValues,

xCellOffsets: xRangeOffsetsSource,

yCellOffsets: yRangeOffsetsSource

});

as well as this:

`// Passing just cell Offset Arrays`

const xRangeOffsetsSource = [0, 10, 20, 26, 36, 60, 72, 84];

const yRangeOffsetsSource = [100, 250, 390, 410, 600];

const dataSeries = new NonUniformHeatmapDataSeries(wasmContext, {

zValues,

xCellOffsets: i => xRangeOffsetsSource[i],

yCellOffsets: i => yRangeOffsetsSource[i]

});