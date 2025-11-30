---
source: https://www.scichart.com/documentation/js/v4/2d-charts/miscellaneous-apis/batching-updates-or-temporary-suspending-drawing
scraped_at: 2025-11-28T18:24:46.467226
---

# https://www.scichart.com/documentation/js/v4/2d-charts/miscellaneous-apis/batching-updates-or-temporary-suspending-drawing

# Batching Updates or Temporary Suspending Drawing

In SciChart.js, every update you make to the chart can potentially trigger a redraw. For example:

- Calling
`DataSeries.append()`

- Setting
`Axis.visibleRange`

- Adding a new series to the
`sciChartSurface.renderableSeries`

collection

All of these operations may trigger a redraw of the `SciChartSurface`

. This might not be desirable in all cases, so there is an API that allows you to temporarily suspend or pause drawing while making multiple updates.

## The Suspend Updates API

The Suspend Updates API should be used when you want to temporarily stop drawing on a `SciChartSurface`

.

This can be useful in certain scenarios:

- It helps improve performance and reduce visual artifacts when making many changes at once (see Data Updates Batching example).
- It can be used in combination with Render Events to apply custom layout calculations.
- It allows control over rendering and timing. For example, by setting up your own render loop.

## SciChart's Redraw-on-Update Behavior Overview

By default, a chart instance redraws only if its state has changed. This includes modifications to properties, data, chart entities, font loading, resizing, pixel ratio changes, visibility changes, and more.

When a modification occurs, it issues an internal "invalidate" request.

This signals the chart to rerender on the next animation frame.

The Suspend Updates API allows the chart to ignore these invalidation requests.

The default behavior of the SciChart Engine relies on render operations being scheduled via `requestAnimationFrame`

.

Some invalidation requests should not be ignored, as doing so may lead to unexpected results.

For example, chart resizing, pixel ratio changes, or tab visibility changes call the `invalidateElement`

method with the `force: true`

option. This triggers a redraw regardless of the suspend state.

You can override the `invalidateElement`

and `notifyPropertyChanged`

methods for more granular control over which updates trigger a redraw.

## Usage

The main logic for suspending updates is handled by an UpdateSuspender📘 instance, accessible via the sciChartSurface.suspender📘 property.

There are two mechanisms to toggle update suspension:

- suspender.suspend📘/suspender.resume📘 - a counter based mechanisms;
- suspender.lock📘/
**unlock**- a token based mechanisms. Both can be used together and are applied in some areas of the SciChart rendering logic implicitly.

You can also check the current state with the `suspender.isSuspended`

📘 flag, which reflects the cumulative suspend state based on both counter and token-based controls.

The surface also exposes convenience methods for accessing the API.

### Basic

Two primary methods of this API are `sciChartSurface.suspendUpdates`

📘 and `sciChartSurface.resumeUpdates`

📘, which internally call suspender.suspend📘 and suspender.resume📘 respectively.

The surface also exposes the `isSuspended`

📘 property.

A few important things to note:

- Calling
`suspendUpdates`

multiple times requires you to call`resumeUpdates`

the same number of times to fully resume updates. - Alternatively,
`resumeUpdates`

accepts a`force`

flag in the options, which resets the counter regardless of how many times it was suspended. - Another option is
`invalidateOnResume`

, which triggers a redraw immediately after resuming.

#### Data Updates Batching Example Using Suspend/Resume

- TS
- JS

`// In this setup data is updated approximately each 10ms,`

// but the redraw is requested only when a batch of data points has been accumulated up to the specified size (`maxBatchSize`)

let batchCounter = 0;

const maxBatchSize = 1000;

let timer: NodeJS.Timeout;

const toggleUpdates = () => {

if (timer) {

clearInterval(timer);

timer = null;

return;

}

timer = setInterval(() => {

// here we create arrays of additional 10 data points

const { xValues, yValues } = generateData(10, 1, dataSeries.count());

// Pause chart rerender requests before updating the data.

sciChartSurface.suspendUpdates();

// appending data points here won't trigger the chart redraw

dataSeries.appendRange(xValues, yValues);

console.log("Data updated. Number of points in the current batch: ", batchCounter);

// unpause the chart

sciChartSurface.resumeUpdates({ invalidateOnResume: false, force: false });

// but if the accumulated data points reached the desired batch size,

// we request a redraw explicitly

batchCounter += xValues.length;

if (batchCounter === maxBatchSize) {

// reset counter

batchCounter = 0;

// request a redraw

sciChartSurface.invalidateElement();

}

}, 10);

};

// bind the timer cleanup to the surface lifecycle

sciChartSurface.addDeletable({

delete: () => {

clearInterval(timer);

}

});

toggleUpdates();

`// In this setup data is updated approximately each 10ms,`

// but the redraw is requested only when a batch of data points has been accumulated up to the specified size (`maxBatchSize`)

let batchCounter = 0;

const maxBatchSize = 1000;

let timer;

const toggleUpdates = () => {

if (timer) {

clearInterval(timer);

timer = null;

return;

}

timer = setInterval(() => {

// here we create arrays of additional 10 data points

const { xValues, yValues } = generateData(10, 1, dataSeries.count());

// Pause chart rerender requests before updating the data.

sciChartSurface.suspendUpdates();

// appending data points here won't trigger the chart redraw

dataSeries.appendRange(xValues, yValues);

console.log("Data updated. Number of points in the current batch: ", batchCounter);

// unpause the chart

sciChartSurface.resumeUpdates({ invalidateOnResume: false, force: false });

// but if the accumulated data points reached the desired batch size,

// we request a redraw explicitly

batchCounter += xValues.length;

if (batchCounter === maxBatchSize) {

// reset counter

batchCounter = 0;

// request a redraw

sciChartSurface.invalidateElement();

}

}, 10);

};

// bind the timer cleanup to the surface lifecycle

sciChartSurface.addDeletable({

delete: () => {

clearInterval(timer);

}

});

toggleUpdates();

### Alternative Lock/Unlock Methods

Another way to suspend updates is via `suspender.lock`

📘, which returns an `unlock`

function that must be called to resume updates.

These methods provide a stricter suspension mechanism.

Since `suspender.isSuspended`

can be affected by both `suspend`

/`resume`

and `lock`

/`unlock`

,

the `lock`

/`unlock`

pair ensures that suspension is lifted only by its corresponding `unlock`

call - it cannot be bypassed or force-resumed by other means.

#### Data Updates Batching Example Using Lock/Unlock

- TS
- JS

`// In this setup data is updated approximately each 10ms,`

// but the redraw is requested only when a batch of data points has been accumulated up to the specified size (`maxBatchSize`)

let batchCounter = 0;

const maxBatchSize = 1000;

let timer: NodeJS.Timeout;

const toggleUpdates = () => {

if (timer) {

clearInterval(timer);

timer = null;

return;

}

timer = setInterval(() => {

// Pause chart rerender requests before updating the data.

const unlock = sciChartSurface.suspender.lock();

// here we create arrays of additional 10 data points

const { xValues, yValues } = generateData(10, 1, dataSeries.count());

// appending data points here won't trigger the chart redraw

dataSeries.appendRange(xValues, yValues);

batchCounter += xValues.length;

console.log("Data updated. Number of points in the current batch: ", batchCounter);

// unpause the chart

unlock();

// but if the accumulated data points reached the desired batch size,

// we request a redraw explicitly

if (batchCounter === maxBatchSize) {

// reset counter

batchCounter = 0;

// request a redraw

sciChartSurface.invalidateElement();

}

}, 10);

};

// bind the timer cleanup to the surface lifecycle

sciChartSurface.addDeletable({

delete: () => {

clearInterval(timer);

}

});

toggleUpdates();

`// In this setup data is updated approximately each 10ms,`

// but the redraw is requested only when a batch of data points has been accumulated up to the specified size (`maxBatchSize`)

let batchCounter = 0;

const maxBatchSize = 1000;

let timer;

const toggleUpdates = () => {

if (timer) {

clearInterval(timer);

timer = null;

return;

}

timer = setInterval(() => {

// Pause chart rerender requests before updating the data.

const unlock = sciChartSurface.suspender.lock();

// here we create arrays of additional 10 data points

const { xValues, yValues } = generateData(10, 1, dataSeries.count());

// appending data points here won't trigger the chart redraw

dataSeries.appendRange(xValues, yValues);

batchCounter += xValues.length;

console.log("Data updated. Number of points in the current batch: ", batchCounter);

// unpause the chart

unlock();

// but if the accumulated data points reached the desired batch size,

// we request a redraw explicitly

if (batchCounter === maxBatchSize) {

// reset counter

batchCounter = 0;

// request a redraw

sciChartSurface.invalidateElement();

}

}, 10);

};

// bind the timer cleanup to the surface lifecycle

sciChartSurface.addDeletable({

delete: () => {

clearInterval(timer);

}

});

toggleUpdates();

### Suspend Chart on Initialization

To prevent the chart from rendering immediately upon initialization, use the `createSuspended`

📘 option when creating the surface.

- TS
- JS

`const { sciChartSurface, wasmContext } = await SciChartSurface.create(rootElement, {`

createSuspended: true

});

`const { sciChartSurface, wasmContext } = await SciChartSurface.create(rootElement, {`

createSuspended: true

});

### onResumed Event Handler

The `suspender.onResumed`

📘 handler lets you subscribe to an event when a surface becomes unsuspended.

- TS
- JS

`sciChartSurface.suspender.onResumed.subscribe(() => {`

console.log("Updates resumed.");

});

`sciChartSurface.suspender.onResumed.subscribe(() => {`

console.log("Updates resumed.");

});

### Freeze Drawing for Charts Out of View

This feature also uses the Suspend API internally.

It helps optimize performance by suspending charts that are out of view on the page.

Check out the Freeze Drawing for Charts section for more details.

## Troubleshooting

If your chart appears frozen after using this API, it may be because you forgot to call `resume`

or `unlock`

.

Ensure the suspender is resumed—once active again, the chart should respond to mouse input and reflect data or property changes.