---
source: https://tradingview.github.io/lightweight-charts/tutorials/demos/compare-multiple-series
scraped_at: 2025-12-01T16:03:53.017351
---

# https://tradingview.github.io/lightweight-charts/tutorials/demos/compare-multiple-series

# Compare multiple series

This Multi-Series Comparison Example illustrates how an assortment of data
series can be integrated into a single chart for comparisons. Simply use the
charting API `addSeries`

to create multiple series.

If you would like an unique price scales for each individual series, particularly when dealing with data series with divergent value ranges, then take a look at the Two Price Scales Example.

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

tip

Some code may be hidden to improve readability. Toggle the checkbox above the code block to reveal all the code.

`// Lightweight Charts™ Example: Compare multiple series`

// https://tradingview.github.io/lightweight-charts/tutorials/how_to/compare-multiple-series

const chartOptions = {

layout: {

textColor: 'black',

background: { type: 'solid', color: 'white' },

},

};

/** @type {import('lightweight-charts').IChartApi} */

const chart = createChart(document.getElementById('container'), chartOptions);

const lineSeriesOne = chart.addSeries(LineSeries, { color: '#2962FF' });

const lineSeriesTwo = chart.addSeries(LineSeries, { color: 'rgb(225, 87, 90)' });

const lineSeriesThree = chart.addSeries(LineSeries, { color: 'rgb(242, 142, 44)' });

const lineSeriesOneData = generateLineData();

const lineSeriesTwoData = generateLineData();

const lineSeriesThreeData = generateLineData();

lineSeriesOne.setData(lineSeriesOneData);

lineSeriesTwo.setData(lineSeriesTwoData);

lineSeriesThree.setData(lineSeriesThreeData);

chart.timeScale().fitContent();