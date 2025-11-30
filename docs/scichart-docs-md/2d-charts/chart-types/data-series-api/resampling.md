---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/data-series-api/resampling
scraped_at: 2025-11-28T18:24:25.224853
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/data-series-api/resampling

# DataSeries Resampling

**New to SciChart.js v2.1!** Resampling in SciChart.js enables *tens of millions of data-points* to be displayed in a JavaScript chart, or insane levels of high performance such as ten million candlesticks, enough for the entire history of Bitcoin to be displayed in a 1-minute chart.

By default, SciChart.js uses resampling of data to ensure the minimum viable data-set is displayed on the screen. SciChart.js resampling algorithms are sophisticated time-series simplification algorithms which result in **visually imperceptible changes to the chart**, but hugely improved performance. They improve performance by allowing you to draw datasets with millions, or tens of millions of points in a JavaScript Chart.

## Effect of Resampling on Visual Output

Resampling algorithms in SciChart are designed to preserve information about the dataset and not affect the visual output. Specifically, peaks and trough information is preserved as are all major turning points of a time-series. **Resampling algorithms in SciChart are not decimation, and information is not lost.** However, the number of points on screen are reduced so you may end up with a "thinner" or less dense looking dataset. The changes should be visually imperceptible and can be tuned if required (see more on resamplingPrecision below).

Here are some before/after images with resampling applied to show the effect on the visual output with resampling applied / not applied.

**Above**: Random walk data with and without resampling applied. All peak/trough information is preserved when resampling applied.

**Above**: Sinewave data with random spikes with and without resampling applied. All peak/trough information is preserved when resampling applied.

**Above**: Noisy sinewave data with and without resampling applied. All peak/trough information is preserved when resampling applied.

## Properties which affect Resampling

The following properties affect resampling mode and precision. Defaults are included in the table below.

Property | Default | Comment |
|---|---|---|
| BaseRenderableSeries.resamplingMode📘 | Auto📘 | Locally sets resampling mode for this series. Values of Auto📘 or None📘 are the most useful. |
| BaseRenderableSeries.resamplingPrecision📘 | 0 | Locally sets resampling precision for this series. Default = 0. Value of 1.0 means double precision, increasing density of output series but at an approx ~20% performance decrease. Value of 2.0 means quad precision etc... |
| SciChartDefaults.debugDisableResampling📘 | false | NOT RECOMMENDED UNLESS IN DEBUG MODE: Turn on/off adaptive, visually lossless resampling algorithms globally for the entire application. |

In addition, the distribution of data (which can be auto-detected or specified) or the series type will dictate which resampling mode is chosen automatically - in order to maximise performance without affecting visual output.

## Globally enabling or Disabling Resampling

It is possible to globally enable or disable resampling for all series by setting the SciChartDefaults.debugDisableResampling📘 property.

We recommend not disabling resampling unless debugging visual output of the chart. This will massively impact performance and is not necessary, as SciChart automatically chooses the correct algorithm and strategy to maintain visual output while hugely improving performance.

`// Globally disabling resampling`

import { SciChartDefaults } from "scichart";

// Prior to version 3.5 this was called SciChartDefaults.enableResampling = false

// in v3.5 and above you can set debugDisableResampling = true

SciChartDefaults.debugDisableResampling = true;

## Disabling Resampling or Setting Mode per-series

By default EResamplingMode.Auto📘 is applied to DataSeries. you can also disable resampling on a per-series basis by setting BaseRenderableSeries.resamplingMode📘 = EResamplingMode.None📘.

`// Setting ResamplingModes`

import { FastLineRenderableSeries, EResamplingMode } from "scichart";

// By default, EResamplingMode.Auto enables resampling (where available)

const lineSeries = new FastLineRenderableSeries(wasmContext, {

resamplingMode: EResamplingMode.Auto,

resamplingPrecision: 1 // See the TypeDoc on resamplingPrecision for more details

} );

// Setting the property to none disables resampling for this series

const lineSeries = new FastLineRenderableSeries(wasmContext, {

resamplingMode: EResamplingMode.None

} );

Other resampling modes are also available in the EResamplingMode📘 enumeration. We suggest leaving these to Auto or None unless directed to by SciChart.js support.

We recommend leaving resamplingMode as Auto unless debugging the visual output of the chart. This will massively impact performance and is not necessary, as SciChart automatically chooses the correct algorithm and strategy to maintain visual output while hugely improving performance.

## Data Distribution

Resampling algorithms make assumptions about the data in order to produce a valid output. SciChart.js provides variety of the resampling modes internally, and auto detects the most suitable one depending on your series-type, dataset size and data distribution.

For correct resampling, the data distribution matters. For example. SciChart.js uses different drawing algorithms if the data is evenly spaced in X vs not evenly spaced, for unsorted vs. sorted data and for when the yValues contain NaN (not a number) or not. All this is to balance optimal performance while maintaining visual accuracy.

By default, SciChart.js will calculate:

- If your data is sorted in the X-direction or not (aka a Time-series)
- If your data is uniformly spaced in the X-direction or not
- If your data contains NaN (Not a Number - used to render gaps) in the Y-values or not

When specified, SciChart.js will not calculate these flags. This improves performance on data append/update/insert/remove operations.

`// Specify Data and Flags when constructing`

import { SciChartSurface, XyDataSeries } from "scichart";

const { sciChartSurface, wasmContext } = await SciChartSurface.create("scichart-div-id");

const dataSeries = new XyDataSeries(wasmContext, {

// Optional: pass data distribution properties (this improves performance)

// else SciChart.js will auto-detect these properties as you update data

dataIsSortedInX: true,

dataEvenlySpacedInX: true,

containsNaN: false,

});

// These properties may also be set after the dataseries has been created

dataSeries.isSorted = true;

dataSeries.containsNaN = true;

When specified in the constructor options of a DataSeries, SciChart.js will not calculate **dataIsSortedInX** and **containsNaN**. This improves performance on data append/update/insert/remove operations by a factor of 5.

## What is ResamplingPrecision?

The BaseRenderableSeries.resamplingPrecision📘 property may be tuned to affect the output result. In some cases where the dataset is very noisy, a higher resampling precision may provide a more visually appealing result.

Here is an example of a very noisy dataset (random values between 0-1) with varying `resamplingPrecision`

.

**Above**: Random Noise (0..1) with Resampling Enabled vs. Disabled and XOR Difference (`resamplingPrecision = 0`

)

**Above**: Random Noise (0..1) with Resampling Enabled vs. Disabled and XOR Difference (`resamplingPrecision = 1`

)

In most cases the default `resamplingPrecision`

value of 0 is sufficient. In some cases where the visual output is not appealing, simply increasing `resamplingPrecision`

from 0 to 1 results in 2x the output points and a better result. This will incur an approx 20% performance hit for very large datasets.

## Resampling effect on Performance

For smaller datasets Resampling will have no effect on performance. SciChart.js is already very highly optimised for datasets up to 1 million datapoints.

For larger datasets, Resampling has a linear trade-off by dynamically reducing the data to the minimum viable set for visually identical drawing on the fly. You will start to see performance improvements from around 100,000 datapoints or more.

With SciChart.js resampling, we were able to render 10,000,000 (ten million) data-points in under 25 milliseconds:

We were also able to achieve 10,000,000 (10 million) candles in a Candlestick Chart, enough to draw the entire history of Bitcoin BTC/USD in a 1-minute chart!

Read further info on how to get the best performance from SciChart.js on our performance tips & tricks page.