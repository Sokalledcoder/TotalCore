---
source: https://tradingview.github.io/lightweight-charts/tutorials/how_to/legends
scraped_at: 2025-12-01T16:03:57.461509
---

# https://tradingview.github.io/lightweight-charts/tutorials/how_to/legends

# Legends

Lightweight Charts™ doesn't include a built-in legend feature, however it is something which can be added to your chart by following the examples presented below.

## How to

In order to add a legend to the chart we need to create and position an `html`

into the desired position above
the chart. We can then subscribe to the crosshairMove events (subscribeCrosshairMove) provided by the `IChartApi`

instance, and manually
update the content within our `html`

legend element.

`chart.subscribeCrosshairMove(param => {`

let priceFormatted = '';

if (param.time) {

const dataPoint = param.seriesData.get(areaSeries);

const price = data.value !== undefined ? data.value : data.close;

priceFormatted = price.toFixed(2);

}

// legend is a html element which has already been created

legend.innerHTML = `${symbolName} <strong>${priceFormatted}</strong>`;

});

The process of creating the legend html element and positioning can be seen within the examples below.
Essentially, we create a new div element within the container div (holding the chart) and then position
and style it using `css`

.

You can see full working examples below.

## Resources

Below are a few external resources related to creating and styling html elements:

## Examples

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

### Simple Legend Example

`// Lightweight Charts™ Example: Legend`

// https://tradingview.github.io/lightweight-charts/tutorials/how_to/legends

const chartOptions = {

layout: {

textColor: 'black',

background: { type: 'solid', color: 'white' },

},

};

/** @type {import('lightweight-charts').IChartApi} */

const chart = createChart(document.getElementById('container'), chartOptions);

chart.applyOptions({

rightPriceScale: {

scaleMargins: {

top: 0.3, // leave some space for the legend

bottom: 0.25,

},

},

crosshair: {

// hide the horizontal crosshair line

horzLine: {

visible: false,

labelVisible: false,

},

},

// hide the grid lines

grid: {

vertLines: {

visible: false,

},

horzLines: {

visible: false,

},

},

});

const areaSeries = chart.addSeries(AreaSeries, {

topColor: '#2962FF',

bottomColor: 'rgba(41, 98, 255, 0.28)',

lineColor: '#2962FF',

lineWidth: 2,

crossHairMarkerVisible: false,

});

areaSeries.setData([

{ time: '2018-10-19', value: 26.19 },

]);

const symbolName = 'ETC USD 7D VWAP';

const container = document.getElementById('container');

const legend = document.createElement('div');

legend.style = `position: absolute; left: 12px; top: 12px; z-index: 1; font-size: 14px; font-family: sans-serif; line-height: 18px; font-weight: 300;`;

container.appendChild(legend);

const firstRow = document.createElement('div');

firstRow.innerHTML = symbolName;

firstRow.style.color = 'black';

legend.appendChild(firstRow);

chart.subscribeCrosshairMove(param => {

let priceFormatted = '';

if (param.time) {

const data = param.seriesData.get(areaSeries);

const price = data.value !== undefined ? data.value : data.close;

priceFormatted = price.toFixed(2);

}

firstRow.innerHTML = `${symbolName} <strong>${priceFormatted}</strong>`;

});

chart.timeScale().fitContent();

### 3 Line Legend Example

`// Lightweight Charts™ Example: Legend 3 Lines`

// https://tradingview.github.io/lightweight-charts/tutorials/how_to/legends

const chartOptions = {

layout: {

textColor: 'black',

background: { type: 'solid', color: 'white' },

},

};

/** @type {import('lightweight-charts').IChartApi} */

const chart = createChart(document.getElementById('container'), chartOptions);

chart.applyOptions({

rightPriceScale: {

scaleMargins: {

top: 0.4, // leave some space for the legend

bottom: 0.15,

},

},

crosshair: {

// hide the horizontal crosshair line

horzLine: {

visible: false,

labelVisible: false,

},

},

// hide the grid lines

grid: {

vertLines: {

visible: false,

},

horzLines: {

visible: false,

},

},

});

const areaSeries = chart.addSeries(AreaSeries, {

topColor: '#2962FF',

bottomColor: 'rgba(41, 98, 255, 0.28)',

lineColor: '#2962FF',

lineWidth: 2,

crossHairMarkerVisible: false,

});

const data = [

{ time: '2018-10-19', value: 26.19 },

];

areaSeries.setData(data);

const symbolName = 'AEROSPACE';

const container = document.getElementById('container');

const legend = document.createElement('div');

legend.style = `position: absolute; left: 12px; top: 12px; z-index: 1; font-size: 14px; font-family: sans-serif; line-height: 18px; font-weight: 300;`;

legend.style.color = 'black';

container.appendChild(legend);

const getLastBar = series => {

const lastIndex = series.dataByIndex(Number.MAX_SAFE_INTEGER, -1);

return series.dataByIndex(lastIndex);

};

const formatPrice = price => (Math.round(price * 100) / 100).toFixed(2);

const setTooltipHtml = (name, date, price) => {

legend.innerHTML = `<div style="font-size: 24px; margin: 4px 0px;">${name}</div><div style="font-size: 22px; margin: 4px 0px;">${price}</div><div>${date}</div>`;

};

const updateLegend = param => {

const validCrosshairPoint = !(

param === undefined || param.time === undefined || param.point.x < 0 || param.point.y < 0

);

const bar = validCrosshairPoint ? param.seriesData.get(areaSeries) : getLastBar(areaSeries);

// time is in the same format that you supplied to the setData method,

// which in this case is YYYY-MM-DD

const time = bar.time;

const price = bar.value !== undefined ? bar.value : bar.close;

const formattedPrice = formatPrice(price);

setTooltipHtml(symbolName, time, formattedPrice);

};

chart.subscribeCrosshairMove(updateLegend);

updateLegend(undefined);

chart.timeScale().fitContent();