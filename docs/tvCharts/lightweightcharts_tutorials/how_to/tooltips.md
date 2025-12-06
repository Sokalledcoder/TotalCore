---
source: https://tradingview.github.io/lightweight-charts/tutorials/how_to/tooltips
scraped_at: 2025-12-01T16:04:02.455847
---

# https://tradingview.github.io/lightweight-charts/tutorials/how_to/tooltips

# Tooltips

Lightweight Charts™ doesn't include a built-in tooltip feature, however it is something which can be added to your chart by following the examples presented below.

## How to

In order to add a tooltip to the chart we need to create and position an `html`

into the desired position above
the chart. We can then subscribe to the crosshairMove events (subscribeCrosshairMove) provided by the `IChartApi`

instance, and manually
update the content within our `html`

tooltip element and change it's position.

`chart.subscribeCrosshairMove(param => {`

if (

param.point === undefined ||

!param.time ||

param.point.x < 0 ||

param.point.y < 0

) {

toolTip.style.display = 'none';

} else {

const dateStr = dateToString(param.time);

toolTip.style.display = 'block';

const data = param.seriesData.get(series);

const price = data.value !== undefined ? data.value : data.close;

toolTip.innerHTML = `<div>${price.toFixed(2)}</div>`;

// Position tooltip according to mouse cursor position

toolTip.style.left = param.point.x + 'px';

toolTip.style.top = param.point.y + 'px';

}

});

The process of creating the tooltip html element and positioning can be seen within the examples below.
Essentially, we create a new div element within the container div (holding the chart) and then position
and style it using `css`

.

You can see full working examples below.

### Getting the mouse cursors position

The parameter object (MouseEventParams Interface) passed to the crosshairMove handler function (MouseEventhandler) contains a point property which gives the current mouse cursor position relative to the top left corner of the chart.

### Getting the data points position

It is possible to convert a price value into it's current vertical position on the chart by using
the priceToCoordinate method on the series' instance.
This along with the `param.point.x`

can be used to determine the position of the data point.

`chart.subscribeCrosshairMove(param => {`

const x = param.point.x;

const data = param.seriesData.get(series);

const price = data.value !== undefined ? data.value : data.close;

const y = series.priceToCoordinate(price);

console.log(`The data point is at position: ${x}, ${y}`);

});

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

### Floating Tooltip

The floating tooltip in this example will position itself next to the current datapoint.

`// Lightweight Charts™ Example: Floating Tooltip`

// https://tradingview.github.io/lightweight-charts/tutorials/how_to/tooltips

const chartOptions = {

layout: {

textColor: 'black',

background: { type: 'solid', color: 'white' },

},

};

/** @type {import('lightweight-charts').IChartApi} */

const chart = createChart(document.getElementById('container'), chartOptions);

chart.applyOptions({

crosshair: {

// hide the horizontal crosshair line

horzLine: {

visible: false,

labelVisible: false,

},

// hide the vertical crosshair label

vertLine: {

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

const series = chart.addSeries(AreaSeries, {

topColor: '#2962FF',

bottomColor: 'rgba(41, 98, 255, 0.28)',

lineColor: '#2962FF',

lineWidth: 2,

crossHairMarkerVisible: false,

});

series.priceScale().applyOptions({

scaleMargins: {

top: 0.3, // leave some space for the legend

bottom: 0.25,

},

});

series.setData([

{ time: '2018-10-19', value: 26.19 },

]);

const container = document.getElementById('container');

const toolTipWidth = 80;

const toolTipHeight = 80;

const toolTipMargin = 15;

// Create and style the tooltip html element

const toolTip = document.createElement('div');

toolTip.style = `width: 96px; height: 80px; position: absolute; display: none; padding: 8px; box-sizing: border-box; font-size: 12px; text-align: left; z-index: 1000; top: 12px; left: 12px; pointer-events: none; border: 1px solid; border-radius: 2px;font-family: -apple-system, BlinkMacSystemFont, 'Trebuchet MS', Roboto, Ubuntu, sans-serif; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale;`;

toolTip.style.background = 'white';

toolTip.style.color = 'black';

toolTip.style.borderColor = '#2962FF';

container.appendChild(toolTip);

// update tooltip

chart.subscribeCrosshairMove(param => {

if (

param.point === undefined ||

!param.time ||

param.point.x < 0 ||

param.point.x > container.clientWidth ||

param.point.y < 0 ||

param.point.y > container.clientHeight

) {

toolTip.style.display = 'none';

} else {

// time will be in the same format that we supplied to setData.

// thus it will be YYYY-MM-DD

const dateStr = param.time;

toolTip.style.display = 'block';

const data = param.seriesData.get(series);

const price = data.value !== undefined ? data.value : data.close;

toolTip.innerHTML = `<div style="color: ${'#2962FF'}">Apple Inc.</div><div style="font-size: 24px; margin: 4px 0px; color: ${'black'}">

${Math.round(100 * price) / 100}

</div><div style="color: ${'black'}">

${dateStr}

</div>`;

const coordinate = series.priceToCoordinate(price);

let shiftedCoordinate = param.point.x - 50;

if (coordinate === null) {

return;

}

shiftedCoordinate = Math.max(

0,

Math.min(container.clientWidth - toolTipWidth, shiftedCoordinate)

);

const coordinateY =

coordinate - toolTipHeight - toolTipMargin > 0

? coordinate - toolTipHeight - toolTipMargin

: Math.max(

0,

Math.min(

container.clientHeight - toolTipHeight - toolTipMargin,

coordinate + toolTipMargin

)

);

toolTip.style.left = shiftedCoordinate + 'px';

toolTip.style.top = coordinateY + 'px';

}

});

chart.timeScale().fitContent();

### Tracking Tooltip

The tracking tooltip will position itself next to the user's cursor.

`// Lightweight Charts™ Example: Tracking Tooltip`

// https://tradingview.github.io/lightweight-charts/tutorials/how_to/tooltips

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

// hide the vertical crosshair label

vertLine: {

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

const series = chart.addSeries(AreaSeries, {

topColor: 'rgba( 38, 166, 154, 0.28)',

bottomColor: 'rgba( 38, 166, 154, 0.05)',

lineColor: 'rgba( 38, 166, 154, 1)',

lineWidth: 2,

crossHairMarkerVisible: false,

});

series.setData([

{ time: '2016-07-18', value: 98.66 },

]);

const container = document.getElementById('container');

const toolTipWidth = 80;

const toolTipHeight = 80;

const toolTipMargin = 15;

// Create and style the tooltip html element

const toolTip = document.createElement('div');

toolTip.style = `width: 96px; height: 80px; position: absolute; display: none; padding: 8px; box-sizing: border-box; font-size: 12px; text-align: left; z-index: 1000; top: 12px; left: 12px; pointer-events: none; border: 1px solid; border-radius: 2px;font-family: -apple-system, BlinkMacSystemFont, 'Trebuchet MS', Roboto, Ubuntu, sans-serif; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale;`;

toolTip.style.background = 'white';

toolTip.style.color = 'black';

toolTip.style.borderColor = 'rgba( 38, 166, 154, 1)';

container.appendChild(toolTip);

// update tooltip

chart.subscribeCrosshairMove(param => {

if (

param.point === undefined ||

!param.time ||

param.point.x < 0 ||

param.point.x > container.clientWidth ||

param.point.y < 0 ||

param.point.y > container.clientHeight

) {

toolTip.style.display = 'none';

} else {

// time will be in the same format that we supplied to setData.

// thus it will be YYYY-MM-DD

const dateStr = param.time;

toolTip.style.display = 'block';

const data = param.seriesData.get(series);

const price = data.value !== undefined ? data.value : data.close;

toolTip.innerHTML = `<div style="color: ${'rgba( 38, 166, 154, 1)'}">ABC Inc.</div><div style="font-size: 24px; margin: 4px 0px; color: ${'black'}">

${Math.round(100 * price) / 100}

</div><div style="color: ${'black'}">

${dateStr}

</div>`;

const y = param.point.y;

let left = param.point.x + toolTipMargin;

if (left > container.clientWidth - toolTipWidth) {

left = param.point.x - toolTipMargin - toolTipWidth;

}

let top = y + toolTipMargin;

if (top > container.clientHeight - toolTipHeight) {

top = y - toolTipHeight - toolTipMargin;

}

toolTip.style.left = left + 'px';

toolTip.style.top = top + 'px';

}

});

chart.timeScale().fitContent();

### Magnifier Tooltip

The magnifier tooltip will position itself along the top edge of the chart while following the user's cursor along the horizontal time axis.

`// Lightweight Charts™ Example: Magnifier Tooltip`

// https://tradingview.github.io/lightweight-charts/tutorials/how_to/tooltips

const chartOptions = {

layout: {

textColor: 'black',

background: { type: 'solid', color: 'white' },

},

};

/** @type {import('lightweight-charts').IChartApi} */

const chart = createChart(document.getElementById('container'), chartOptions);

chart.applyOptions({

leftPriceScale: {

visible: true,

borderVisible: false,

},

rightPriceScale: {

visible: false,

},

timeScale: {

borderVisible: false,

},

crosshair: {

horzLine: {

visible: false,

labelVisible: false,

},

vertLine: {

visible: true,

style: 0,

width: 2,

color: 'rgba(32, 38, 46, 0.1)',

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

const series = chart.addSeries(AreaSeries, {

topColor: 'rgba( 239, 83, 80, 0.05)',

bottomColor: 'rgba( 239, 83, 80, 0.28)',

lineColor: 'rgba( 239, 83, 80, 1)',

lineWidth: 2,

crossHairMarkerVisible: false,

priceLineVisible: false,

lastValueVisible: false,

});

series.priceScale().applyOptions({

scaleMargins: {

top: 0.3, // leave some space for the legend

bottom: 0.25,

},

});

series.setData([

{ time: '2018-03-28', value: 154 },

]);

const container = document.getElementById('container');

const toolTipWidth = 96;

// Create and style the tooltip html element

const toolTip = document.createElement('div');

toolTip.style = `width: ${toolTipWidth}px; height: 300px; position: absolute; display: none; padding: 8px; box-sizing: border-box; font-size: 12px; text-align: left; z-index: 1000; top: 12px; left: 12px; pointer-events: none; border-radius: 4px 4px 0px 0px; border-bottom: none; box-shadow: 0 2px 5px 0 rgba(117, 134, 150, 0.45);font-family: -apple-system, BlinkMacSystemFont, 'Trebuchet MS', Roboto, Ubuntu, sans-serif; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale;`;

toolTip.style.background = `rgba(${'255, 255, 255'}, 0.25)`;

toolTip.style.color = 'black';

toolTip.style.borderColor = 'rgba( 239, 83, 80, 1)';

container.appendChild(toolTip);

// update tooltip

chart.subscribeCrosshairMove(param => {

if (

param.point === undefined ||

!param.time ||

param.point.x < 0 ||

param.point.x > container.clientWidth ||

param.point.y < 0 ||

param.point.y > container.clientHeight

) {

toolTip.style.display = 'none';

} else {

// time will be in the same format that we supplied to setData.

// thus it will be YYYY-MM-DD

const dateStr = param.time;

toolTip.style.display = 'block';

const data = param.seriesData.get(series);

const price = data.value !== undefined ? data.value : data.close;

toolTip.innerHTML = `<div style="color: ${'rgba( 239, 83, 80, 1)'}">⬤ ABC Inc.</div><div style="font-size: 24px; margin: 4px 0px; color: ${'black'}">

${Math.round(100 * price) / 100}

</div><div style="color: ${'black'}">

${dateStr}

</div>`;

let left = param.point.x; // relative to timeScale

const timeScaleWidth = chart.timeScale().width();

const priceScaleWidth = chart.priceScale('left').width();

const halfTooltipWidth = toolTipWidth / 2;

left += priceScaleWidth - halfTooltipWidth;

left = Math.min(left, priceScaleWidth + timeScaleWidth - toolTipWidth);

left = Math.max(left, priceScaleWidth);

toolTip.style.left = left + 'px';

toolTip.style.top = 0 + 'px';

}

});

chart.timeScale().fitContent();