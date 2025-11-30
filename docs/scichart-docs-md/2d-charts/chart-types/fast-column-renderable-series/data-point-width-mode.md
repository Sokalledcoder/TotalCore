---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/fast-column-renderable-series/data-point-width-mode
scraped_at: 2025-11-28T18:24:27.098057
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/fast-column-renderable-series/data-point-width-mode

# Column Series Data Point Width Mode

### Overview

Not just applicable to Column Series, but also Error Bars Series, Candlestick, Rectangle Series and OHLC Series, the dataPointWidth📘 and dataPointWidthMode📘 properties allow controlling of spacing of bars on a 2D JavaScript Chart.

In previous articles we've shown how dataPointWidth📘 can be used to change the width of bar-style series, for example Columns, Error Bars and Candlesticks/OHLC.

By default, dataPointWidth📘 sets the width of columns/bars as a fraction of available space, with valid values from 0.0 - 1.0.

New to SciChart.js v3.4 and above, a new property dataPointWidthMode📘 has been added. This has values of **Absolute**, **Range** and **Relative**. These define how the dataPointWidth📘 is interpreted on these series types:

### EDataPointWidthMode.Absolute📘

Interprets Data Point Width as an absolute pixel value

### EDataPointWidthMode.Range📘

Interprets Data Point Width as the x data range per column. This is useful if you are plotting sparse columns on a NumericAxis

### EDataPointWidthMode.Relative📘

Interprets Data Point Width as a relative to the full width which is axis length / number of columns. This assumes that there are no gaps in the data. If you are plotting sparse columns on a NumericAxis, consider Range mode

### Example

Here's an example of their use below. They can be very useful to change how sparsely populated column series behave.

Given a dataset with sparse values like this:

- TS

`// Create some data with gaps`

const xValues = [0, 10, 30, 70, 80, 90, 110, 120, 150, 180, 190];

const yValues = [0.2, 0.4, 0.8, 1.5, 2.4, 8.1, 13.7, 6.4, 3.5, 1.4, 0.4];

const dataSeries = new XyDataSeries(wasmContext, { xValues, yValues });

And 3 column series with different dataPointWidthModes:

- TS

`// Create and add three column series to demonstrate the different EDataPointWidthModes`

const columnSeries0 = new FastColumnRenderableSeries(wasmContext, {

dataSeries,

fill: "#50C7E077",

stroke: "#50C7E0",

strokeThickness: 2,

yAxisId: "Absolute",

dataPointWidthMode: EDataPointWidthMode.Absolute,

// When dataPointWidthMode=Absolute, this is the width of each column in pixels

dataPointWidth: 8,

});

const columnSeries1 = new FastColumnRenderableSeries(wasmContext, {

dataSeries,

fill: "#EC0F6C77",

stroke: "#EC0F6C",

strokeThickness: 2,

yAxisId: "Range",

dataPointWidthMode: EDataPointWidthMode.Range,

// When dataPointWidthMode=Range, this is the width of each column in range units

dataPointWidth: 8,

});

const columnSeries2 = new FastColumnRenderableSeries(wasmContext, {

dataSeries,

fill: "#30BC9A77",

stroke: "#30BC9A",

strokeThickness: 2,

yAxisId: "Relative",

dataPointWidthMode: EDataPointWidthMode.Relative,

// When dataPointWidthMode=Range, this is the width of each column in relative units of available space

dataPointWidth: 0.8,

});

sciChartSurface.renderableSeries.add(columnSeries0, columnSeries1, columnSeries2);

The result is the following output:

### Breakdown:

**EDataPointWidthMode.Relative**📘 was the previous default (and only) value prior to v3.4. This would calculate the available space for a column and render each bar as a fraction of that availble space (from 0.0 - 1.0). The problem with this mode was that when x-values were unevenly spaced or the dataset was sparse, then

**EDataPointWidthMode.Absolute**📘 has been added post v3.4 which renders each bar as a pixel width. This is perfect for handling sparse datasets, except the bar will not scale as the chart is zoomed in or out.

**EDataPointWidthMode.Relative**📘 has also been added post v3.4. This mode renders each bar as a x-Range, so if the xAxis has a range of 0-200 and you specify a value of 8, then a bar will occupy exactly 8 data units. Using this mode, bars or columns will never overlap.