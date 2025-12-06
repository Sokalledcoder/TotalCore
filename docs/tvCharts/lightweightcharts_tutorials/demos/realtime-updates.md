---
source: https://tradingview.github.io/lightweight-charts/tutorials/demos/realtime-updates
scraped_at: 2025-12-01T16:03:54.469480
---

# https://tradingview.github.io/lightweight-charts/tutorials/demos/realtime-updates

# Realtime updates

This sample demonstrates how to mimic real-time updates on a candlestick chart
with Lightweight Charts™. The chart initially populates with some historical
data. By using `setInterval`

function, the chart then begins to receive
simulated real-time updates with the usage of `series.update(...)`

.

Each real-time update represents a new data point or modifies the latest point,
providing the illusion of a live, updating chart. If you scroll the chart and
wish to return to the latest data points then you can use the "Go to realtime"
button provided which calls the
`scrollToRealtime`

method
on the timescale.

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

`// Lightweight Charts™ Example: Realtime updates`

// https://tradingview.github.io/lightweight-charts/tutorials/demos/realtime-updates

const container = document.getElementById('container');

/** @type {import('lightweight-charts').IChartApi} */

const chart = createChart(container, chartOptions);

// Only needed within demo page

// eslint-disable-next-line no-undef

window.addEventListener('resize', () => {

chart.applyOptions({ height: 200 });

});

const series = chart.addSeries(CandlestickSeries, {

upColor: '#26a69a',

downColor: '#ef5350',

borderVisible: false,

wickUpColor: '#26a69a',

wickDownColor: '#ef5350',

});

const data = generateData(2500, 20, 1000);

series.setData(data.initialData);

chart.timeScale().fitContent();

chart.timeScale().scrollToPosition(5);

// simulate real-time data

function* getNextRealtimeUpdate(realtimeData) {

for (const dataPoint of realtimeData) {

yield dataPoint;

}

return null;

}

const streamingDataProvider = getNextRealtimeUpdate(data.realtimeUpdates);

const intervalID = setInterval(() => {

const update = streamingDataProvider.next();

if (update.done) {

clearInterval(intervalID);

return;

}

series.update(update.value);

}, 100);

const button = document.createElement('button');

button.innerText = 'Go to realtime';

button.addEventListener('click', () => chart.timeScale().scrollToRealTime());

buttonsContainer.appendChild(button);

container.appendChild(buttonsContainer);