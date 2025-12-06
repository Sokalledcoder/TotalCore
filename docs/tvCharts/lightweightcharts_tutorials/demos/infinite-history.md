---
source: https://tradingview.github.io/lightweight-charts/tutorials/demos/infinite-history
scraped_at: 2025-12-01T16:03:49.544955
---

# https://tradingview.github.io/lightweight-charts/tutorials/demos/infinite-history

# Infinite history

This sample showcases the capability of Lightweight Charts™ to manage and display an ever-expanding dataset, resembling a live feed that loads older data when the user scrolls back in time. The example depicts a chart that initially loads a limited amount of data, but later fetches additional data as required.

Key to this functionality is the
`subscribeVisibleLogicalRangeChange`

method. This function is triggered when the visible data range changes, in this
case, when the user scrolls beyond the initially loaded data.

By checking if the amount of unseen data on the left of the screen falls below a
certain threshold (in this example, 10 units), it's determined whether
additional data needs to be loaded. New data is appended through a simulated
delay using `setTimeout`

.

This kind of infinite history functionality is typical of financial charts which frequently handle large and continuously expanding datasets.

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

`// Lightweight Charts™ Example: Infinite history`

// https://tradingview.github.io/lightweight-charts/tutorials/demos/infinite-history

const container = document.getElementById('container');

/** @type {import('lightweight-charts').IChartApi} */

const chart = createChart(container, chartOptions);

const series = chart.addSeries(CandlestickSeries, {

upColor: '#26a69a',

downColor: '#ef5350',

borderVisible: false,

wickUpColor: '#26a69a',

wickDownColor: '#ef5350',

});

const datafeed = new Datafeed();

series.setData(datafeed.getBars(200));

chart.timeScale().subscribeVisibleLogicalRangeChange(logicalRange => {

if (logicalRange.from < 10) {

// load more data

const numberBarsToLoad = 50 - logicalRange.from;

const data = datafeed.getBars(numberBarsToLoad);

setTimeout(() => {

series.setData(data);

}, 250); // add a loading delay

}

});