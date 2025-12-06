---
source: https://tradingview.github.io/lightweight-charts/tutorials/demos/moving-average
scraped_at: 2025-12-01T16:03:50.580204
---

# https://tradingview.github.io/lightweight-charts/tutorials/demos/moving-average

# Moving average indicator

This example demonstrates the implementation of a moving average (MA) indicator using Lightweight Charts™. It effectively shows how to overlay a line series representing the moving average on a candlestick series.

Initial rendering involves the creation of a candlestick series using randomly
generated data. The `calculateMovingAverageSeriesData`

function subsequently
computes the 20-period MA data from the candlestick data. For each point, if
less than 20 data points precede it, the function creates a whitespace data
point. If 20 or more data points precede it, it calculates the MA for that
period.

The MA data set forms a line series, which is placed underneath the candlestick series (by creating the line series first). As a result, users can view the underlying price data (via the candlestick series) in conjunction with the moving average trend line which provides valuable analytical insight.

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

`// Lightweight Charts™ Example: Moving average indicator`

// https://tradingview.github.io/lightweight-charts/tutorials/demos/moving-average

/** @type {import('lightweight-charts').IChartApi} */

const chart = createChart(document.getElementById('container'), chartOptions);

const barData = generateCandleData(500);

function calculateMovingAverageSeriesData(candleData, maLength) {

const maData = [];

for (let i = 0; i < candleData.length; i++) {

if (i < maLength) {

// Provide whitespace data points until the MA can be calculated

maData.push({ time: candleData[i].time });

} else {

// Calculate the moving average, slow but simple way

let sum = 0;

for (let j = 0; j < maLength; j++) {

sum += candleData[i - j].close;

}

const maValue = sum / maLength;

maData.push({ time: candleData[i].time, value: maValue });

}

}

return maData;

}

const maData = calculateMovingAverageSeriesData(barData, 20);

const maSeries = chart.addSeries(LineSeries, { color: '#2962FF', lineWidth: 1 });

maSeries.setData(maData);

const candlestickSeries = chart.addSeries(CandlestickSeries, {

upColor: '#26a69a',

downColor: '#ef5350',

borderVisible: false,

wickUpColor: '#26a69a',

wickDownColor: '#ef5350',

});

candlestickSeries.setData(barData);