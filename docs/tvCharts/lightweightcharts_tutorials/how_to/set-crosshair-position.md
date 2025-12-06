---
source: https://tradingview.github.io/lightweight-charts/tutorials/how_to/set-crosshair-position
scraped_at: 2025-12-01T16:04:00.308466
---

# https://tradingview.github.io/lightweight-charts/tutorials/how_to/set-crosshair-position

# Set crosshair position

Lightweight Charts™ allows the crosshair position to be set programatically using the `setCrosshairPosition`

, and cleared using `clearCrosshairPosition`

.

Usually the crosshair position is set automatically by the user's actions. However in some cases you may want to set it explicitly. For example if you want to synchronise the crosshairs of two separate charts.

## Syncing two charts

`// Lightweight Charts™ Example: Crosshair syncing`

// https://tradingview.github.io/lightweight-charts/tutorials/how_to/set-crosshair-position

chart1.timeScale().subscribeVisibleLogicalRangeChange(timeRange => {

chart2.timeScale().setVisibleLogicalRange(timeRange);

});

chart2.timeScale().subscribeVisibleLogicalRangeChange(timeRange => {

chart1.timeScale().setVisibleLogicalRange(timeRange);

});

function getCrosshairDataPoint(series, param) {

if (!param.time) {

return null;

}

const dataPoint = param.seriesData.get(series);

return dataPoint || null;

}

function syncCrosshair(chart, series, dataPoint) {

if (dataPoint) {

chart.setCrosshairPosition(dataPoint.value, dataPoint.time, series);

return;

}

chart.clearCrosshairPosition();

}

chart1.subscribeCrosshairMove(param => {

const dataPoint = getCrosshairDataPoint(mainSeries1, param);

syncCrosshair(chart2, mainSeries2, dataPoint);

});

chart2.subscribeCrosshairMove(param => {

const dataPoint = getCrosshairDataPoint(mainSeries2, param);

syncCrosshair(chart1, mainSeries1, dataPoint);

});

## Tracking without long-press (on mobile)

If scrolling and scaling is disabled, then the API can be used to enable a kind of tracking mode without the user having to long-press the screen.

`// Lightweight Charts™ Example: Crosshair syncing`

// https://tradingview.github.io/lightweight-charts/tutorials/how_to/set-crosshair-position

document.getElementById('container').addEventListener('touchmove', e => {

const bcr = document.getElementById('container').getBoundingClientRect();

const x = bcr.left + e.touches[0].clientX;

const y = bcr.top + e.touches[0].clientY;

const price = mainSeries.coordinateToPrice(y);

const time = chart.timeScale().coordinateToTime(x);

if (!Number.isFinite(price) || !Number.isFinite(time)) {

return;

}

chart.setCrosshairPosition(price, time, mainSeries);

});

document.getElementById('container').addEventListener('touchend', () => {

chart.clearCrosshairPosition();

});