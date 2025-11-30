---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/data-series-api/append-insert-update-remove
scraped_at: 2025-11-28T18:24:24.195796
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/data-series-api/append-insert-update-remove

# Append, Insert, Update, Remove

SciChart.js is designed to be a highly dynamic chart library for frequently updating data. Once you have created a chart with a RenderableSeries / DataSeries pair, you can manipulate the data in any way and the chart will redraw / update.

Data Updates are handled in a reactive way and are 'debounced' so that the chart only draws 1/60th of a second regardless of how many changes to data you make.

## The DataSeries Append, Update, Insert, Remove functions

Here's an table from the TypeDoc for XyDataSeries📘 showing functions available for updating the data.

All chart series updates are done via the DataSeries API using the append()📘, insert()📘, update()📘, remove()📘 functions. There are also variations such as appendRange()📘, insertRange()📘 etc... which accept an array of data.

Note that different dataSeries such as XyDataSeries📘, XyzDataSeries📘, XyyDataSeries📘 and OhlcDataSeries📘 have slightly different function signatures for append/update functions. Click the links above to the Typedoc for more info.

Here are some common operations:

`// Append, Update, Insert, Remove`

const xyDataSeries = new XyDataSeries(wasmContext);

xyDataSeries.append(1, 10); // Appends X=1, Y=10

xyDataSeries.append(2, 20); // Appends X=2, Y=20

xyDataSeries.appendRange([3, 4, 5], [30, 40, 50]); // Appends X=3,4,5 and Y=30,40,50

xyDataSeries.removeAt(0); // removes the 0th xy point

xyDataSeries.removeRange(0, 2); // Removes 2 points from index 0 onwards

xyDataSeries.insert(0, 100, 200); // Inserts X=100, Y=200 at index 0

//xyDataSeries.insertRange(...)

xyDataSeries.update(0, 22); // Updates the Y-value at index 0

xyDataSeries.clear(); // Clears the dataseries. NOTE: Does not free memory

xyDataSeries.delete(); // Deletes WebAssembly memory. The series is no longer usable.

**For the best possible performance, when modifying large datasets**, use the appendRange📘, insertRange📘, removeRange📘 functions. These accept an array of values and are considerably faster than appending point-by-point.

Failing to call IDeletable.delete()📘 on a DataSeries when it is no longer needed can result in a memory leak.

To simplify your code, if you do not change DataSeries instances, you can call delete on the parent SciChartSurface once. This will delete all child objects that hold native memory.

## Examples of Dynamic Updates

There are a number of worked examples of how to apply dynamic updates to the chart over at the page DataSeries Realtime Updates.