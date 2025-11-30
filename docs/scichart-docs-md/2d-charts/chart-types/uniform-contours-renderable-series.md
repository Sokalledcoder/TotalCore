---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/uniform-contours-renderable-series
scraped_at: 2025-11-28T18:24:45.341634
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/uniform-contours-renderable-series

# The Contours Series Type

Contour maps or Contour-plots can be created using the UniformContoursRenderableSeries📘 type.

The JavaScript Heatmap Chart Example can be found in the SciChart.Js Examples Suite > Contours Chart on Github, or our live demo at scichart.com/demo.

## Create a Contours Plot

SciChart's Contour series is an extremely fast, lightweight chart types for rendering two dimensional data as a contour plot. The UniformContoursRenderableSeries📘 type should be used in conjunction with a UniformHeatmapDataSeries📘 when you simply want to specify a Step in the X,Y direction (each cell is the same size).

To create a Javascript Contours Chart with SciChart.js, use the following code:

- TS
- Builder API (JSON Config)

`// Demonstrates how to create a contour plot with SciChart.js`

const {

SciChartSurface,

NumericAxis,

HeatmapColorMap,

UniformHeatmapDataSeries,

UniformHeatmapRenderableSeries,

UniformContoursRenderableSeries,

SciChartJsNavyTheme

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

// Create a SciChartSurface with X & Y Axis

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

const WIDTH = 300;

const HEIGHT = 200;

const colorPaletteMax = 200;

// Create a Heatmap Data-series. zValues are heatValues as a 2D Array (number[][])

// Open the Codepen below to see the definition of this function

const zValues = generateExampleData(3, WIDTH, HEIGHT, colorPaletteMax);

// Create the uniform heatmap data series. Pass heatValues as number[][]

const heatmapDataSeries = new UniformHeatmapDataSeries(wasmContext, {

// 2d zValues array. Dimensions [height][width]

zValues,

// xStart, xStep, yStart, yStep defines the x,y position

xStart: 0,

xStep: 1,

yStart: 0,

yStep: 1

});

// Create a Contours RenderableSeries with the same data

const contourSeries = new UniformContoursRenderableSeries(wasmContext, {

dataSeries: heatmapDataSeries,

zMin: 20,

zMax: colorPaletteMax,

zStep: 20

});

// Add it to the scichartsurface

sciChartSurface.renderableSeries.add(contourSeries);

// Create a background heatmap series with the same data and add to the chart

const heatmapSeries = new UniformHeatmapRenderableSeries(wasmContext, {

dataSeries: heatmapDataSeries,

opacity: 0.5,

useLinearTextureFiltering: false,

// See heatmap documentation for description of how colormaps work

colorMap: new HeatmapColorMap({

minimum: 0,

maximum: colorPaletteMax,

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

// Add to the SciChartSurface

sciChartSurface.renderableSeries.add(heatmapSeries);

`// Demonstrates how to create a line chart with SciChart.js using the Builder API`

const { chartBuilder, ESeriesType, HeatmapColorMap, EThemeProviderType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const WIDTH = 300;

const HEIGHT = 200;

const colorPaletteMax = 200;

// Create a Heatmap Data-series. zValues are heatValues as a 2D Array (number[][])

// Open the Codepen below to see the definition of this function

const zValues = generateExampleData(3, WIDTH, HEIGHT, colorPaletteMax);

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

series: [

{

type: ESeriesType.UniformContoursSeries,

options: {

zMin: 20,

zMax: colorPaletteMax,

zStep: 20

},

heatmapData: {

zValues,

xStart: 0,

xStep: 1,

yStart: 0,

yStep: 1

}

},

{

type: ESeriesType.UniformHeatmapSeries,

options: {

colorMap: new HeatmapColorMap({

minimum: 0,

maximum: colorPaletteMax,

gradientStops: [

{ offset: 1, color: "#EC0F6C" },

{ offset: 0.9, color: "#F48420" },

{ offset: 0.7, color: "#DC7969" },

{ offset: 0.5, color: "#67BDAF" },

{ offset: 0.3, color: "#50C7E0" },

{ offset: 0.2, color: "#264B93" },

{ offset: 0, color: "#14233C" }

]

}),

opacity: 0.5

},

heatmapData: {

zValues,

xStart: 0,

xStep: 1,

yStart: 0,

yStep: 1

}

}

]

});

In the code above:

- We create an empty 2D array
`number[][]`

using the helper function`zeroArray2D`

. This is filled with values in the generateData function - A UniformHeatmapDataSeries📘 instance is created with
`xStart`

,`xStep`

,`yStart`

,`yStep`

values =`0`

,`1`

,`0`

,`1`

. This means the heatmap starts at`(X, Y)`

=`(0, 0)`

and each cell is`1`

on the axis. - We set the contour
`stroke`

and`strokeThickness`

. - A UniformContoursRenderableSeries📘 instance is created and added to the sciChartSurface.renderableSeries📘 collection.

This results in the following output:

## Updating Data in a Contour map

The contour map is supposed to be fully dynamic, enabling real-time graphics. The Contours Series📘 however does not support append, insert, update, remove functions like other DataSeries do. You can however update the data and force a refresh simply by updating the data passed in. To do this, use the following code:

`import { UniformHeatmapDataSeries, zeroArray2D } from "scichart";`

const height = 10; // Set the height of the heatmap

const width = 20; // Set the width of the heatmap

// Create an empty 2D array of size height & width

const initialZValues: number[][] = zeroArray2D([height, width]);

// Create a Heatmap Data-series. Pass the heatValues as a number[][] to the UniformHeatmapDataSeries

const heatmapDataSeries = new UniformHeatmapDataSeries({

xStart: 0,

xStep: 1,

yStart: 0,

yStep: 1,

zValues: initialZValues

});

// ...

// Later, update the data

initialZValues[5][6] = 123.4;

heatmapDataSeries.notifyDataChanged() // Notify SciChart that the data has changed

// You can also load an entirely new array with the function UniformHeatmapDataSeries.setZValues

const newZValues; // type number[][]

heatmapDataSeries.setZValues(newZValues);

For more details, including a live example of how to update 2D array data for heatmaps and contours, see the Uniform Heatmap documentation - Updating Heatmaps documentation page. The mechanism for contour plots is the same.