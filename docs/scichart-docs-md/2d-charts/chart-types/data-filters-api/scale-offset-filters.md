---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/data-filters-api/scale-offset-filters
scraped_at: 2025-11-28T18:24:22.894060
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/data-filters-api/scale-offset-filters

# Scale Offset Filters

The ScaleOffsetFilter Applies a scale (multiplier) and an offset (addition) to each field value in a Data Series. There is a specific filter for each type of dataseries:

**XyScaleOffsetFilter****XyyScaleOffsetFilter****XyzScaleOffsetFilter****OhlcScaleOffsetFilter**

## Applying Scale & Offset to Chart Data

To create an **XyScaleOffsetFilter** and apply it to your chart, use the following code:

- TS

`import {`

SciChartSurface,

NumericAxis,

XyDataSeries,

FastLineRenderableSeries,

NumberRange,

XyScaleOffsetFilter

} from "scichart";

...

const { sciChartSurface, wasmContext } = await SciChartSurface.create('scichart-div-id');

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { growBy: new NumberRange(0.1, 0.1) }));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { growBy: new NumberRange(0.1, 0.1) }));

// Original Data

const dataSeries = new XyDataSeries(wasmContext, {

xValues: [1, 2, 3, 4],

yValues: [1, 2, 3, 4],

});

const originalLine = new FastLineRenderableSeries(wasmContext, { dataSeries, stroke: "#5555ff" });

// Create the filter, passing in the original series

const scaleOffsetFilter = new XyScaleOffsetFilter(dataSeries, { scale: 2, offset: -3 });

const filteredLine = new FastLineRenderableSeries(wasmContext, { dataSeries: scaleOffsetFilter, stroke: "#cc6600" });

sciChartSurface.renderableSeries.add(originalLine, filteredLine);

This produces the following chart where the orange filtered data is twice as steep, and shifted down by 3.

With the Filters API in SciChart.js, if you update the original data, or any of the parameters of the filter, the chart will automatically redraw.

Note that ScaleOffsetFilter only changes data in the Y direction. If you want to shift data in X, create a Complex Custom Filter. The other ScaleOffsetFilters apply the same transformation to every non-x field. If you want to apply different filters to different fields, create a Complex Custom Filter.

## Specifying the Input Field

An Xy filter will produce an XyDataSeries, but it can accept any series type as input. The options includes a **field** property of type **EDataSeriesField**, which determines which field on the original series will be the input. For Xyy filters there are yField and y1Field, and for Xyz filters there are yField and zField options.

## Percentage Change

You can use a ScaleOffset filter to show the percentage change in a series, which is useful for comparing data at different scales. For a running example of this with code see our Percentage Change demo