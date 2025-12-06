---
source: https://tradingview.github.io/lightweight-charts/tutorials/how_to/series-markers
scraped_at: 2025-12-01T16:03:58.667955
---

# https://tradingview.github.io/lightweight-charts/tutorials/how_to/series-markers

# Add Series Markers

A series marker is an annotation which can be drawn on the chart at a specific point. It can be used to draw attention to specific events within the data set. This example shows how to add series markers to your chart.

## Short answer

You can add markers to a series by passing an array of `seriesMarker`

objects to the `createSeriesMarkers`

method on
an `ISeriesApi`

instance.

`const markers = [`

{

time: { year: 2018, month: 12, day: 23 },

position: 'aboveBar',

color: '#f68410',

shape: 'circle',

text: 'A',

},

];

createSeriesMarkers(series, markers);

You can see a full working example below.

## Further information

A series marker is an annotation which can be attached to a specific data point within a series.
We don't need to specify a vertical price value but rather only the `time`

property since the
marker will determine it's vertical position from the data points values (such as `high`

and
`low`

in the case of candlestick data) and the specified `position`

property (SeriesMarkerPosition).

## Resources

You can view the related APIs here:

- SeriesMarker - Series Marker interface.
- SeriesMarkerPosition - Positions that can be set for the marker.
- SeriesMarkerShape - Shapes that can be set for the marker.
- createSeriesMarkers - Method for adding markers to a series.
- Time Types - Different time formats available to use.

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

`// Lightweight Charts™ Example: Series Markers`

// https://tradingview.github.io/lightweight-charts/tutorials/how_to/series-markers

const chartOptions = {

layout: {

textColor: 'black',

background: { type: 'solid', color: 'white' },

},

};

/** @type {import('lightweight-charts').IChartApi} */

const chart = createChart(document.getElementById('container'), chartOptions);

const series = chart.addSeries(CandlestickSeries, {

upColor: '#26a69a', downColor: '#ef5350', borderVisible: false,

wickUpColor: '#26a69a', wickDownColor: '#ef5350',

});

const data = [

{

time: { year: 2018, month: 9, day: 22 },

open: 29.630237296336794,

high: 35.36950035097501,

low: 26.21522501353531,

close: 30.734997177569916,

},

];

series.setData(data);

// determining the dates for the 'buy' and 'sell' markers added below.

const datesForMarkers = [data[data.length - 39], data[data.length - 19]];

let indexOfMinPrice = 0;

for (let i = 1; i < datesForMarkers.length; i++) {

if (datesForMarkers[i].high < datesForMarkers[indexOfMinPrice].high) {

indexOfMinPrice = i;

}

}

const markers = [

{

time: data[data.length - 48].time,

position: 'aboveBar',

color: '#f68410',

shape: 'circle',

text: 'D',

},

];

for (let i = 0; i < datesForMarkers.length; i++) {

if (i !== indexOfMinPrice) {

markers.push({

time: datesForMarkers[i].time,

position: 'aboveBar',

color: '#e91e63',

shape: 'arrowDown',

text: 'Sell @ ' + Math.floor(datesForMarkers[i].high + 2),

});

} else {

markers.push({

time: datesForMarkers[i].time,

position: 'belowBar',

color: '#2196F3',

shape: 'arrowUp',

text: 'Buy @ ' + Math.floor(datesForMarkers[i].low - 2),

});

}

}

/** @type {import('lightweight-charts').createSeriesMarkers} */

createSeriesMarkers(series, markers);

chart.timeScale().fitContent();