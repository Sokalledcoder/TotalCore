---
source: https://www.scichart.com/documentation/js/v4/2d-charts/miscellaneous-apis/render-events
scraped_at: 2025-11-28T18:24:47.116998
---

# https://www.scichart.com/documentation/js/v4/2d-charts/miscellaneous-apis/render-events

# Render Events

A surface instance exposes several EventHandlers📘 corresponding to different stages of the chart rendering cycle.

Before comparing render events, it's important to understand the following:

- There are two types of charts:

- with a
**shared WASM context**– Multiple charts share the same WebGL context. They render on a single WebGL canvas and are then copied sequentially to separate 2D canvases. - with an
**individual WASM context**– Each chart has its own WebGL canvas and renders independently.

- The
**SubCharts API**enables rendering multiple smaller charts simultaneously on a single canvas.

For more details, check out these pages:

## Lifecycle EventHandlers List

Below is the list of render process event handlers, in the order they occur:

-
**redrawRequested**📘 Triggered on the main surface when an initial invalidate call occurs. Subsequent invalidate calls will not trigger this event until the chart has been rendered. This event is**only**fired on the main surface and does**not**apply to sub-charts. -
**preRenderAll**📘 Triggered on the main surface before the render loop begins. Use it to apply custom configurations such as styling or changes to the visible range. This event is**only**fired on the main surface and does**not**apply to sub-charts. It is also currently**not**applicable to 3D charts. -
**preRender**📘 Triggered on a surface or sub-surface before rendering. Use it to apply logic for layout adjustments, such as modifying the visible range aspect ratio or`PointMarker`

size. -
**layoutMeasured**📘 Triggered during rendering when the visible range, size, and axis positions are measured. Use this event to hook into the rendering process when your logic depends on coordinates or offsets. -
**rendered**📘 Triggered after the render logic has executed on a surface or sub-surface. -
**renderedToWebGL**📘 Triggered on the main surface after rendering completes. Use this to add custom drawing on the WebGL canvas. -
**renderedToDestination**📘 Triggered on the main surface after rendering completes and the image is transferred to the target canvas. Use this to add custom drawing on the 2D canvas. -
**painted**📘 Triggered on the main surface after the frame has been committed by the client environment. This event is useful for confirming that the chart was drawn, for example, before exporting it as an image.

Use `preRenderAll`

and `renderedToDestination`

to measure chart render performance.
See Performance Measurement.

## Helper Functions

The library provides a helper function receiveNextEvent📘 to promisify a single event occurrence.

Additionally, a surface exposes a nextStateRender📘 method,
which works similarly to `receiveNextEvent`

, but subscribes only to `renderedToDestination`

and allows passing options to control the Suspend Updates API.

## Usage Examples

### Ensuring the frame was drawn

When exporting images or performing visual tests, you often need to ensure that the chart has rendered and any animations have completed.

The following example demonstrates how to guarantee that any logic invalidating the chart during the render loop has finished and the chart is stable (i.e., not requested to redraw).

- TS

`const { xValues, yValues } = generateData(10, 1);`

const dataSeries = new XyDataSeries(wasmContext, { xValues, yValues, capacity: 1000 });

const lineSeries = new FastLineRenderableSeries(wasmContext, {

stroke: "olive",

strokeThickness: 2,

dataSeries,

animation: new WaveAnimation({ duration: 3000 })

});

sciChartSurface.renderableSeries.add(lineSeries);

while (await receiveNextEvent(sciChartSurface.painted)) {}

console.log("animation completed");

### Performance Measurement

Lifecycle events can be used to measure chart performance.
To measure frame render time, use `preRenderAll`

and `renderedToDestination`

.
Other events may also be useful.

It’s recommended to initialize a chart with `createSuspended: true`

to ensure rendering doesn’t start before the `create`

function completes.

Here is an example demonstrating how to set up rendering performance measurement. It outputs results to the console.

For thorough performance analysis, consider measuring other operations (such as data append/update times). You can also check out Performance and Memory Usage test suites.

- TS
- JS

`const initStartTimeStamp = performance.now();`

const { sciChartSurface, wasmContext } = await SciChartSurface.createSingle(rootElement, {

createSuspended: true

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

// The fist frame is usually the slowest, so we perform and measure it separately.

// Also in this example we include it into the initialization time.

// #region_C_start

await sciChartSurface.nextStateRender({

resumeBefore: true,

invalidateOnResume: true,

suspendAfter: false

});

// #region_C_end

const firstFrameRenderedTimeStamp = performance.now();

const renderStartTimeStamps: DOMHighResTimeStamp[] = [];

const renderEndTimeStamps: DOMHighResTimeStamp[] = [];

const framePaintedTimeStamps: DOMHighResTimeStamp[] = [];

sciChartSurface.preRenderAll.subscribe(() => {

renderStartTimeStamps.push(performance.now());

});

sciChartSurface.renderedToDestination.subscribe(() => {

renderEndTimeStamps.push(performance.now());

});

sciChartSurface.painted.subscribe(() => {

framePaintedTimeStamps.push(performance.now());

});

const outputPerformanceMeasurements = () => {

if (

renderEndTimeStamps.length !== renderStartTimeStamps.length ||

renderEndTimeStamps.length !== framePaintedTimeStamps.length

) {

// this will mean that the setup is wrong, probably due to the missing "createSuspended" flag during the initialization

console.warn(

"There are differences in timestamps number!",

renderStartTimeStamps,

renderEndTimeStamps,

framePaintedTimeStamps

);

}

const aggregatedResults = renderEndTimeStamps.map((end, index) => {

const start = renderStartTimeStamps[index];

return { start, end, renderDuration: end - start, frameDuration: framePaintedTimeStamps[index] - start };

});

console.log("Performance Measurement Results");

console.log("Initial Frame time", firstFrameRenderedTimeStamp - initStartTimeStamp);

console.table(aggregatedResults);

// cleanup the results to output only new ones the next time

renderStartTimeStamps.length = 0;

renderEndTimeStamps.length = 0;

framePaintedTimeStamps.length = 0;

};

// render one more time and show results

sciChartSurface.invalidateElement();

await receiveNextEvent(sciChartSurface.painted);

outputPerformanceMeasurements();

`const initStartTimeStamp = performance.now();`

const { sciChartSurface, wasmContext } = await SciChartSurface.createSingle(rootElement, {

createSuspended: true

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

// The fist frame is usually the slowest, so we perform and measure it separately.

// Also in this example we include it into the initialization time.

// #region_C_start

await sciChartSurface.nextStateRender({

resumeBefore: true,

invalidateOnResume: true,

suspendAfter: false

});

// #region_C_end

const firstFrameRenderedTimeStamp = performance.now();

const renderStartTimeStamps = [];

const renderEndTimeStamps = [];

const framePaintedTimeStamps = [];

sciChartSurface.preRenderAll.subscribe(() => {

renderStartTimeStamps.push(performance.now());

});

sciChartSurface.renderedToDestination.subscribe(() => {

renderEndTimeStamps.push(performance.now());

});

sciChartSurface.painted.subscribe(() => {

framePaintedTimeStamps.push(performance.now());

});

const outputPerformanceMeasurements = () => {

if (renderEndTimeStamps.length !== renderStartTimeStamps.length ||

renderEndTimeStamps.length !== framePaintedTimeStamps.length) {

// this will mean that the setup is wrong, probably due to the missing "createSuspended" flag during the initialization

console.warn("There are differences in timestamps number!", renderStartTimeStamps, renderEndTimeStamps, framePaintedTimeStamps);

}

const aggregatedResults = renderEndTimeStamps.map((end, index) => {

const start = renderStartTimeStamps[index];

return { start, end, renderDuration: end - start, frameDuration: framePaintedTimeStamps[index] - start };

});

console.log("Performance Measurement Results");

console.log("Initial Frame time", firstFrameRenderedTimeStamp - initStartTimeStamp);

console.table(aggregatedResults);

// cleanup the results to output only new ones the next time

renderStartTimeStamps.length = 0;

renderEndTimeStamps.length = 0;

framePaintedTimeStamps.length = 0;

};

// render one more time and show results

sciChartSurface.invalidateElement();

await receiveNextEvent(sciChartSurface.painted);

outputPerformanceMeasurements();

Additionally, this example shows an annotation displaying some rendering performance results.

The implementation:

- TS
- JS

`/**`

* An annotation displaying render performance stats of the surface.

* It extends the NativeTextAnnotation so its position and styles could be easily updated.

*

* @remarks Since the annotation is rendered on the same surface, the annotation displays stats from the previous frame.

* So, basically it is always a frame behind the last drawn frame...

*/

class PerformanceStatsAnnotation extends NativeTextAnnotation {

constructor(options?: INativeTextAnnotationOptions) {

super(options);

this.processResults = this.processResults.bind(this);

this.x1 = 0;

this.y1 = 0;

this.xCoordinateMode = ECoordinateMode.Relative;

this.yCoordinateMode = ECoordinateMode.Relative;

this.multiLineAlignment = EMultiLineAlignment.Left;

this.backgroundProperty = options?.background ?? "black";

}

public onAttach(scs: SciChartSurface): void {

super.onAttach(scs);

if (scs.isSubSurface) {

scs.hasInvalidState = true;

throw new Error(

`PerformanceStatsAnnotation is only supposed to be attached to a regular surface, not a sub-chart!`

);

}

subscribeToPerformanceMeasurements(scs, this.processResults);

}

protected processResults(result: TPerformanceMeasurementResults) {

const {

invalidatedTimeStamp,

renderStartTimeStamp,

renderToWebGlEndTimeStamp,

renderEndTimeStamp,

paintEndTimeStamp,

lastPaintEndTimeStamp

} = result;

const renderTime = renderEndTimeStamp - renderStartTimeStamp;

const renderToWebGlTime = renderToWebGlEndTimeStamp - renderStartTimeStamp;

const copyToCanvasTime = renderTime - renderToWebGlTime;

const timeToRenderStart = renderStartTimeStamp - invalidatedTimeStamp;

const timeBetweenPaints = paintEndTimeStamp - lastPaintEndTimeStamp;

const timeFromRequestToPaint = paintEndTimeStamp - invalidatedTimeStamp;

// updating the underlying property instead of the setter to prevent invalidation,

// alternatively Suspend API could be used

this.textProperty = [

`FPS: ${(1000 / timeBetweenPaints).toFixed(3).padStart(3, "0")}`,

`Render: ${renderTime.toFixed(2).padStart(2, "0")}ms`,

renderToWebGlTime === renderToWebGlTime

? `Copy to Canvas: ${copyToCanvasTime.toFixed(2).padStart(2, "0")}ms`

: "",

`Since Last Paint: ${timeBetweenPaints.toFixed(2).padStart(2, "0")}ms`

].join("\n");

}

}

/**

* Collected performance timestamps

*/

type TPerformanceMeasurementResults = {

invalidatedTimeStamp: DOMHighResTimeStamp;

renderStartTimeStamp: DOMHighResTimeStamp;

renderToWebGlEndTimeStamp: DOMHighResTimeStamp;

renderEndTimeStamp: DOMHighResTimeStamp;

paintEndTimeStamp: DOMHighResTimeStamp;

lastPaintEndTimeStamp: DOMHighResTimeStamp;

};

function subscribeToPerformanceMeasurements(

surface: SciChartSurface,

callback: (result: TPerformanceMeasurementResults) => void

) {

let invalidatedTimeStamp: DOMHighResTimeStamp;

let renderStartTimeStamp: DOMHighResTimeStamp;

let renderToWebGlEndTimeStamp: DOMHighResTimeStamp;

let renderEndTimeStamp: DOMHighResTimeStamp;

let paintEndTimeStamp: DOMHighResTimeStamp;

let lastPaintEndTimeStamp: DOMHighResTimeStamp;

surface.redrawRequested.subscribe(isInvalidated => {

invalidatedTimeStamp = performance.now();

});

surface.preRenderAll.subscribe(() => {

renderStartTimeStamp = performance.now();

});

if (surface.isCopyCanvasSurface) {

surface.renderedToWebGl.subscribe(() => {

renderToWebGlEndTimeStamp = performance.now();

});

}

surface.renderedToDestination.subscribe(() => {

renderEndTimeStamp = performance.now();

});

surface.painted.subscribe(() => {

lastPaintEndTimeStamp = paintEndTimeStamp;

paintEndTimeStamp = performance.now();

callback({

invalidatedTimeStamp,

renderStartTimeStamp,

renderToWebGlEndTimeStamp,

renderEndTimeStamp,

paintEndTimeStamp,

lastPaintEndTimeStamp

});

});

}

`/**`

* An annotation displaying render performance stats of the surface.

* It extends the NativeTextAnnotation so its position and styles could be easily updated.

*

* @remarks Since the annotation is rendered on the same surface, the annotation displays stats from the previous frame.

* So, basically it is always a frame behind the last drawn frame...

*/

class PerformanceStatsAnnotation extends NativeTextAnnotation {

constructor(options) {

super(options);

this.processResults = this.processResults.bind(this);

this.x1 = 0;

this.y1 = 0;

this.xCoordinateMode = ECoordinateMode.Relative;

this.yCoordinateMode = ECoordinateMode.Relative;

this.multiLineAlignment = EMultiLineAlignment.Left;

this.backgroundProperty = options?.background ?? "black";

}

onAttach(scs) {

super.onAttach(scs);

if (scs.isSubSurface) {

scs.hasInvalidState = true;

throw new Error(`PerformanceStatsAnnotation is only supposed to be attached to a regular surface, not a sub-chart!`);

}

subscribeToPerformanceMeasurements(scs, this.processResults);

}

processResults(result) {

const { invalidatedTimeStamp, renderStartTimeStamp, renderToWebGlEndTimeStamp, renderEndTimeStamp, paintEndTimeStamp, lastPaintEndTimeStamp } = result;

const renderTime = renderEndTimeStamp - renderStartTimeStamp;

const renderToWebGlTime = renderToWebGlEndTimeStamp - renderStartTimeStamp;

const copyToCanvasTime = renderTime - renderToWebGlTime;

const timeToRenderStart = renderStartTimeStamp - invalidatedTimeStamp;

const timeBetweenPaints = paintEndTimeStamp - lastPaintEndTimeStamp;

const timeFromRequestToPaint = paintEndTimeStamp - invalidatedTimeStamp;

// updating the underlying property instead of the setter to prevent invalidation,

// alternatively Suspend API could be used

this.textProperty = [

`FPS: ${(1000 / timeBetweenPaints).toFixed(3).padStart(3, "0")}`,

`Render: ${renderTime.toFixed(2).padStart(2, "0")}ms`,

renderToWebGlTime === renderToWebGlTime

? `Copy to Canvas: ${copyToCanvasTime.toFixed(2).padStart(2, "0")}ms`

: "",

`Since Last Paint: ${timeBetweenPaints.toFixed(2).padStart(2, "0")}ms`

].join("\n");

}

}

function subscribeToPerformanceMeasurements(surface, callback) {

let invalidatedTimeStamp;

let renderStartTimeStamp;

let renderToWebGlEndTimeStamp;

let renderEndTimeStamp;

let paintEndTimeStamp;

let lastPaintEndTimeStamp;

surface.redrawRequested.subscribe(isInvalidated => {

invalidatedTimeStamp = performance.now();

});

surface.preRenderAll.subscribe(() => {

renderStartTimeStamp = performance.now();

});

if (surface.isCopyCanvasSurface) {

surface.renderedToWebGl.subscribe(() => {

renderToWebGlEndTimeStamp = performance.now();

});

}

surface.renderedToDestination.subscribe(() => {

renderEndTimeStamp = performance.now();

});

surface.painted.subscribe(() => {

lastPaintEndTimeStamp = paintEndTimeStamp;

paintEndTimeStamp = performance.now();

callback({

invalidatedTimeStamp,

renderStartTimeStamp,

renderToWebGlEndTimeStamp,

renderEndTimeStamp,

paintEndTimeStamp,

lastPaintEndTimeStamp

});

});

}