---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/data-series-api/deleting-memory
scraped_at: 2025-11-28T18:24:24.543539
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/data-series-api/deleting-memory

# Deleting DataSeries Memory

SciChart.js stores memory in WebAssembly. This allows us to achieve our incredible performance, and also provide a unfied experience across SciChart platforms (Windows, iOS, Android and JavaScript).

Unlike JavaScript which has built-in garbage collection, WebAssembly requires that you delete memory that you have allocated. Think of it as similar to closing a WebSocket connection if you want to close the connection and free memory.

See related articles: Memory Usage Best Practices which has some further info on optimising memory usage with SciChart.js, and Memory Leak Debugging which introduces our new tools to identify and fix memory leaks.

## Examples of how to use Delete()

Once you are finished with the DataSeries, don't forget to call IDeletable.delete()📘. This frees WebAssembly native memory and releases it back to the host.

Below are a few examples of best-practices when deleting dataSeries, renderableSeries and sciChartSurfaces.

### Example 1 - dataseries delete()

`// Create a DataSeries`

console.log(`Example A: Creating, clearing and deleting a dataseries`);

const xyDataSeries = new XyDataSeries(wasmContext, {

xValues,

yValues,

});

// Clear it - does not delete memory, just removes all data-points

xyDataSeries.clear();

console.log(`xyDataSeries is cleared but retains memory: ${xyDataSeries.getNativeXValues().capacity()} Datapoints`);

// Frees memory - the data-series cannot be re-used after this

xyDataSeries.delete();

console.log(`xyDataSeries is deleted: ${xyDataSeries.getIsDeleted()}`);

### Example 2 - reassign dataseries

`// When re-assigning a dataseries, make sure to delete the old series`

const oldSeries = lineSeries.dataSeries;

oldSeries.delete();

lineSeries.dataSeries = new XyDataSeries(wasmContext, {

xValues: [1, 2, 3, 4, 5, 6, 7, 8, 9],

yValues: [2.5, 3.5, 3.7, 4.0, 5.0, 5.5, 5.0, 4.0, 3.0]

});

console.log(`oldSeries is deleted: ${oldSeries.getIsDeleted()}`);

console.log(`lineSeries.dataSeries is deleted: ${lineSeries.dataSeries.getIsDeleted()}`);

### Example 3 - deleting renderableseries

`// Calling delete on a RenderableSeries will delete both the RenderableSeries and its DataSeries`

// The series is no longer usable

lineSeries.delete();

console.log(`lineSeries.dataSeries is now deleted`);

### Example 4 - deleting scichartsurface

`// Calling Delete on a SciChartSurface will delete and free memory on all elements in this chart`

// This chart is no longer usable

sciChartSurface.delete()

console.log(`sciChartSurface is deleted: ${sciChartSurface.isDeleted}`);

Failing to call IDeletable.delete()📘 on a DataSeries or it's parent SciChartSurface when it is no longer needed can result in a memory leak.

To simplify your code, if you do not change DataSeries instances, you can call delete on the parent SciChartSurface once. This will delete all child objects that hold native memory.