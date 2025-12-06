---
source: https://tradingview.github.io/lightweight-charts/tutorials/how_to/panes
scraped_at: 2025-12-01T16:03:54.327807
---

# https://tradingview.github.io/lightweight-charts/tutorials/how_to/panes

# Panes

Lightweight Charts™ allows you to create multiple panes in a single chart.

Using multiple panes in a charting library can be incredibly useful for a variety of analytical and visualization scenarios, especially when dealing with complex datasets or requiring detailed comparative analysis across different data dimensions.

This example shows how to use panes in Lightweight Charts™. We will create a chart with two panes: the first one will display a stock's price over time and the second one will contain trading volume. The price and volume will be represented with candles and an area, respectively.

You can see a full working example below.

## How to add a pane

To introduce an additional pane into a chart, specify `paneIndex`

during series creation.

Alternatively, you can invoke the `moveToPane`

method on the series instance. Note that if the pane with specified index doesn't exist, it will be created.

`const volumeSeries = chart.addSeries(`

HistogramSeries,

{

priceFormat: {

type: 'volume',

},

},

1 // Pane index

);

// Moving the series to a different pane

volumeSeries.moveToPane(2);

If a series is moved out of a pane and no other series remain, the pane will be automatically removed.

### Customizations

Lightweight Charts™ provides options to customize the panes. You can adjust the pane separator color by specifying the `separatorColor`

property in the
`layout.panes`

chart options, and use `separatorHoverColor`

to change the separator color on hover.

`chart.applyOptions({`

layout: {

panes: {

separatorColor: '#ff0000',

separatorHoverColor: '#00ff00',

enableResize: false,

},

},

});

Lightweight Charts™ includes `PaneApi`

that allows you to control each pane. The API has methods to get information on the pane such as `getHeight()`

, `paneIndex()`

, and `getSeries()`

. It also contains methods to adjust the pane parameters, for example `setHeight(height)`

and `moveTo(paneIndex)`

.

To get a `PaneApi`

instance for each pane, you need to call the `panes`

method on the `ChartApi`

instance.
Let's say we want to set the height of the second pane to 300px and move it to the first position.

`const secondPane = chart.panes()[1];`

secondPane.setHeight(300);

secondPane.moveTo(0);

Note that the minimum pane height is 30px. Any values lower than 30px will be ignored.

To remove the pane, you can call the `removePane(paneIndex)`

method on the `ChartApi`

instance.

`chart.removePane(1);`

Note that removing a pane also removes any series contained within it.

## Full Example

## How to use the code sample

**Before you use the code sample below, you should do the following::**

- Import
`createChart`

. Refer to Getting Started for more information. - Add an HTML div element with the
`id`

of the`container`

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

panes: {

separatorColor: '#f22c3d',

separatorHoverColor: 'rgba(255, 0, 0, 0.1)',

// setting this to false will disable the resize of the panes by the user

enableResize: false,

},

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

const candlestickSeries = chart.addSeries(CandlestickSeries, {

upColor: '#26a69a', downColor: '#ef5350', borderVisible: false,

wickUpColor: '#26a69a', wickDownColor: '#ef5350',

// we are setting pane index 1 for this series

}, 1);

areaSeries.setData([

{ time: '2018-10-19', value: 52.89 },

]);

// setting the data for the volume series.

// note: we are defining each bars color as part of the data

candlestickSeries.setData([

{ time: '2018-10-19', open: 75.16, high: 82.84, low: 36.16, close: 45.72 },

]);

const candlesPane = chart.panes()[1];

candlesPane.moveTo(0);

candlesPane.setHeight(150);

chart.timeScale().fitContent();