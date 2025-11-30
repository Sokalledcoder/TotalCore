---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/data-series-api/data-series-api-overview
scraped_at: 2025-11-28T18:24:24.385238
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/data-series-api/data-series-api-overview

# DataSeries API Overview

## What can you do with the DataSeries in SciChart?

Most chart libraries are geared towards loading a chart with static data and never modifying it.

With SciChart.js, you can:

- Create a chart initially with X, Y data and optional metadata (objects) per-point
- Store values in floating-point 64 bit numbers
- modify the data: appending new data, removing, inserting
- Update values
- Animate changes of data or new values
- Replace all values - like in a spectrum analyzer
- Scroll values - real-time monitoring scenarios
- Sweep values - wrap around as data reaches the right edge of the viewport.

DataSeries allow you to have fine-grained control over the chart data & enable dynamic updates.

## DataSeries Types

The following DataSeries types exist in SciChart.js. All DataSeries types store memory in WebAssembly and implement the IDeletable📘 interface. You must call IDeletable.delete()📘 when discarding a DataSeries to free memory.

Internally the DataSeries wrap the JavaScript number type, which is a double-precision 64-bit floating-point number and expect numeric values. You can also store Dates and render strings on chart axis, more on that below.

Here's the content formatted as a two-column Markdown table with headers:

## Creating, Assigning a DataSeries

A DataSeries can be created with a single line of code, once you have a wasmContext (WebAssembly Context). The WebAssembly Context is created when you call the SciChartSurface.create()📘 function, and the context should be used for elements on that chart only.

- TS
- Builder API (JSON Config)

`// import { SciChartSurface, XyDataSeries, FastLineRenderableSeries ... } from "scichart"`

const xValues = [];

const yValues = [];

for (let i = 0; i < 100; i++) {

xValues.push(i);

yValues.push(0.2 * Math.sin(i * 0.1) - Math.cos(i * 0.01));

}

// Create a DataSeries

const xyDataSeries = new XyDataSeries(wasmContext, {

// Optional: pass X,Y values to DataSeries constructor for fast initialization

// each are Arrays of numbers or Float64Array (typed array for best performance)

xValues,

yValues

});

// Create a renderableSeries and assign the dataSeries

const lineSeries = new FastLineRenderableSeries(wasmContext, {

dataSeries: xyDataSeries

});

// add to the chart

sciChartSurface.renderableSeries.add(lineSeries);

`// Demonstrates how to create and assign a dataSeries with SciChart.js using the Builder API`

const { chartBuilder, ESeriesType, EThemeProviderType, XyDataSeries } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const xValues = [0, 1, 2, 3, 4, 5, 6, 7, 8];

const yValues = [2.5, 3.5, 3.7, 4.0, 5.0, 5.5, 5.0, 4.0, 3.0];

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

series: [

{

type: ESeriesType.LineSeries,

// This section creates a DataSeries with X,Y values

xyData: {

xValues,

yValues

},

options: {

stroke: "#FF6600",

strokeThickness: 2

}

}

]

});

// However this is also valid (either xyData, or new XyDataSeries)

// sciChartSurface.renderableSeries.get(0).dataSeries = new XyDataSeries(wasmContext, { xValues, yValues });

Once the DataSeries has been created, it can be assigned to a RenderableSeries by setting the BaseRenderableSeries.dataSeries📘 property. This is true for both the classic JavaScript API or the Builder API. More info on this in the section on RenderableSeries.

Once you are finished with the DataSeries, don't forget to call IDeletable.delete()📘. This frees WebAssembly native memory and releases it back to the operating system. For more info see the related article Best Practices when Deleting DataSeries.

## Setting Data Distribution Flags

For optimal drawing and correct operation, SciChart.js needs to know the distribution of your data, whether sorted in the x-direction and whether the data contains NaN (Not a Number). These flags will be computed automatically, but can be specified for improved performance.

- TS
- Builder API (JSON Config)

`const xyDataSeries = new XyDataSeries(wasmContext, {`

xValues,

yValues,

// Data distribution flags are calculated automatically as you update data.

// Providing them in advance can improve performance for big-data

// Note: undefined behaviour will occur if these flags are set incorrectly

dataIsSortedInX: true,

dataEvenlySpacedInX: true,

containsNaN: false

});

`const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {`

surface: { theme: { type: EThemeProviderType.Dark } },

series: [

{

type: ESeriesType.LineSeries,

// This section creates a DataSeries with X,Y values

// IDataSeriesOptions are valid here

xyData: {

xValues: [0, 1, 2, 3, 4, 5, 6, 7, 8],

yValues: [2.5, 3.5, 3.7, 4.0, 5.0, 5.5, 5.0, 4.0, 3.0],

dataIsSortedInX: true,

dataEvenlySpacedInX: true,

containsNaN: false

},

options: {

stroke: "#FF6600",

strokeThickness: 2

}

}

]

});

// However this is also valid (either xyData, or onew XyDataSeries)

// sciChartSurface.renderableSeries.get(0).dataSeries = new XyDataSeries(wasmContext, { xValues, yValues });

When you don't specify Data Distribution Flags, SciChart.js will compute them automatically as data is updated. This adds a small performance overhead, only noticeable with very big data.

If you specify flags manually, make sure they are correct, and update them as your data updates. If you don't, undefined behaviour can occur.

## Getting the DataSeries XRange and YRange

All DataSeries types expose the XRange📘 and YRange (via getWindowedYRange📘) of the underlying series. If you need to know the min and max of the DataSeries in the X or Y direction, then call one of these properties:

Example Title

- TS

`const xyDataSeries = new XyDataSeries(webAssemblyContext);`

xyDataSeries.appendRange([1, 2, 3], [10, 20, 30]);

// XRange will choose the first/last value if isSorted=true, else it will iterate over all values

const xRange = xyDataSeries.xRange; // Type NumberRange

console.log(`XRange: ${xRange.toString()}`);

// yRange requires a window of x-values. To get the entire yRange, pass in xRange

const yRange = xyDataSeries.getWindowedYRange(xRange, true, false);

console.log(`YRange: ${yRange.toString()}`);

// Outputs to console

// XRange: NumberRange (1, 3)

// YRange: NumberRange (10, 30)

## Storing Date & String values in DataSeries

All DataSeries store 64-bit double precision numeric values. However, if you want to display a date or a string on an axis, you need to do a small conversion first.

### Storing Dates on DataSeries in SciChart

DataSeries don't support dates, but you can store values as a unix timestamp and render them as a date on the axis. The process is:

- Store Dates as Unix timestamps in the DataSeries.
- Format the Date using our built-in LabelProvider, or create your own

Examples can be found in the SciChart.js examples suite, or in our documentation on the Label Formatting page.

### Storing Strings in DataSeries in SciChart

Similarly, DataSeries don't support strings, but if you want to render strings, then it's advisable to use X values as sequential integers e.g. 0,1,2,3... and use the LabelProvider feature to format labels as strings.