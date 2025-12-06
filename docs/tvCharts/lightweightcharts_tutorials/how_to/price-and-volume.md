---
source: https://tradingview.github.io/lightweight-charts/tutorials/how_to/price-and-volume
scraped_at: 2025-12-01T16:04:00.975171
---

# https://tradingview.github.io/lightweight-charts/tutorials/how_to/price-and-volume

# Price and volume on a single chart

This example shows how to include a volume study on your chart.

## How to add a volume histogram

An additional series can be added to a chart as an 'overlay' by setting the series'
`priceScaleId`

to `''`

.
An overlay doesn't make use of either the left or right price scale, and it's positioning
is controlled by setting the `scaleMargins`

property on the price scale options associated with the series.

`const volumeSeries = chart.addSeries(HistogramSeries, {`

priceFormat: {

type: 'volume',

},

priceScaleId: '', // set as an overlay by setting a blank priceScaleId

});

volumeSeries.priceScale().applyOptions({

// set the positioning of the volume series

scaleMargins: {

top: 0.7, // highest point of the series will be 70% away from the top

bottom: 0,

},

});

We are using the Histogram series type to draw the volume bars.
We can set the `priceFormat`

option to `'volume'`

to have the values display correctly within
the crosshair line label.

We adjust the position of the overlay series to the bottom 30% of the chart by
setting the `scaleMargins`

properties as follows:

`volumeSeries.priceScale().applyOptions({`

scaleMargins: {

top: 0.7, // highest point of the series will be 70% away from the top

bottom: 0, // lowest point will be at the very bottom.

},

});

Similarly, we can set the position of the main series using the same approach. By setting
the `bottom`

margin value to `0.4`

we can ensure that the two series don't overlap each other.

`mainSeries.priceScale().applyOptions({`

scaleMargins: {

top: 0.1, // highest point of the series will be 10% away from the top

bottom: 0.4, // lowest point will be 40% away from the bottom

},

});

We can control the color of the histogram bars by directly specifying color inside the data set.

`histogramSeries.setData([`

{ time: '2018-10-19', value: 19103293.0, color: 'green' },

{ time: '2018-10-20', value: 20345000.0, color: 'red' },

]);

You can see a full working example below.

## Resources

## Full example

## How to use the code sample

**The code presented below requires:**

- That
`createChart`

has already been imported. See Getting Started for more information, - and that there is an html div element on the page with an
`id`

of`container`

.

Here is an example skeleton setup: Code Sandbox.
You can paste the provided code below the `// REPLACE EVERYTHING BELOW HERE`

comment.

Some code may be hidden to improve readability. Toggle the checkbox above the code block to reveal all the code.

`// Lightweight Charts™ Example: Price and Volume`

// https://tradingview.github.io/lightweight-charts/tutorials/how_to/price-and-volume

const chartOptions = {

layout: {

textColor: 'black',

background: { type: 'solid', color: 'white' },

},

rightPriceScale: {

borderVisible: false,

},

};

/** @type {import('lightweight-charts').IChartApi} */

const chart = createChart(document.getElementById('container'), chartOptions);

const areaSeries = chart.addSeries(AreaSeries, {

topColor: '#2962FF',

bottomColor: 'rgba(41, 98, 255, 0.28)',

lineColor: '#2962FF',

lineWidth: 2,

});

areaSeries.priceScale().applyOptions({

scaleMargins: {

// positioning the price scale for the area series

top: 0.1,

bottom: 0.4,

},

});

const volumeSeries = chart.addSeries(HistogramSeries, {

color: '#26a69a',

priceFormat: {

type: 'volume',

},

priceScaleId: '', // set as an overlay by setting a blank priceScaleId

// set the positioning of the volume series

scaleMargins: {

top: 0.7, // highest point of the series will be 70% away from the top

bottom: 0,

},

});

volumeSeries.priceScale().applyOptions({

scaleMargins: {

top: 0.7, // highest point of the series will be 70% away from the top

bottom: 0,

},

});

areaSeries.setData([

{ time: '2018-10-19', value: 54.90 },

]);

// setting the data for the volume series.

// note: we are defining each bars color as part of the data

volumeSeries.setData([

{ time: '2018-10-19', value: 19103293.00, color: '#26a69a' },

]);

chart.timeScale().fitContent();