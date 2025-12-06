---
source: https://tradingview.github.io/lightweight-charts/tutorials/demos/yield-curve-with-update-markers
scraped_at: 2025-12-01T16:03:55.204066
---

# https://tradingview.github.io/lightweight-charts/tutorials/demos/yield-curve-with-update-markers

# Yield Curve Chart with Update Markers

This sample demonstrates how to create a yield curve chart with real-time updates using Lightweight Charts™. The chart displays two yield curves and utilizes the UpDownMarkersPrimitive plugin to show price change markers for updates.

The chart is initialized with historical yield curve data for two series. By
using the `setInterval`

function, we simulate real-time updates to the first
curve. These updates are applied using the `update`

method provided by the
UpDownMarkersPrimitive, which automatically handles the creation and display of
markers for price changes.

Key features of this demo:

- Yield curve chart configuration with custom time range settings.
- Two line series representing different yield curves.
- Usage of the UpDownMarkersPrimitive plugin for displaying update markers.
- Simulated real-time updates to demonstrate dynamic data handling.

The UpDownMarkersPrimitive is attached to the first series when created using
`priceChangeMarkers = createUpDownMarkers(series1)`

. We then use
`priceChangeMarkers.setData(curve1)`

to initialize the data and
`priceChangeMarkers.update(...)`

for subsequent updates. This approach allows
the primitive to manage both the series data and the markers, providing a
seamless way to visualize price changes.

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

`// Lightweight Charts™ Example: Yield Curve Chart with Update Markers`

// https://tradingview.github.io/lightweight-charts/tutorials/demos/yield-curve-with-update-markers

const chartOptions = {

autoSize: true,

layout: {

textColor: 'black',

background: { type: 'solid', color: 'white' },

},

yieldCurve: {

baseResolution: 12,

minimumTimeRange: 10,

startTimeRange: 3,

},

handleScroll: false,

handleScale: false,

grid: {

vertLines: {

visible: false,

},

horzLines: {

visible: false,

},

},

timeScale: {

minBarSpacing: 3,

},

};

const container = document.getElementById('container');

const chart = createYieldCurveChart(container, chartOptions);

const series1 = chart.addSeries(LineSeries, {

lineType: 2,

color: '#26c6da',

pointMarkersVisible: true,

lineWidth: 2,

});

const priceChangeMarkers = createUpDownMarkers(series1);

priceChangeMarkers.setData(curve1);

const series2 = chart.addSeries(LineSeries, {

lineType: 2,

color: 'rgb(164, 89, 209)',

pointMarkersVisible: true,

lineWidth: 1,

});

series2.setData(curve2);

chart.timeScale().fitContent();

chart.timeScale().subscribeSizeChange(() => {

chart.timeScale().fitContent();

});

setInterval(() => {

curve1

.filter(() => Math.random() < 0.1)

.forEach(data => {

const shift = (Math.random() > 0.5 ? -1 : 1) * Math.random() * 0.01 * data.value;

priceChangeMarkers.update(

{

...data,

value: data.value + shift,

},

true

);

});

}, 5000);