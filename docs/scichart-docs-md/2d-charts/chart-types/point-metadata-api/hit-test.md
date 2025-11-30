---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/point-metadata-api/hit-test
scraped_at: 2025-11-28T18:24:38.591281
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/point-metadata-api/hit-test

# Metadata and HitTest

The Hi-Test API is a low level API used to extract information about chart series under the mouse. Our own in-house RolloverModifier and CursorModifier are based on this API. You can use it too to create Drill-downs and custom data-inspections.

This article purpose is to keep it brief and show you how to store and retrieve Metadata from datapoints during a Hit-Test operation. Further reading about these APIs can be found below.

Background reading:

- If you haven't already, read the article DataSeries PointMetadata API which will show you how to setup a DataSeries with point metadata (javascript objects).
- Also take a look at the Hit-Test API docs to describe how to perform chart hit-testing (inspection on click, hover)

## Example: Metadata + HitTest

Here's a code sample showing how to extract metadata from a HitTest result. This is as simple as getting HitTestInfo.metadata

- JS

`// Create metadata with initial values. Metadata can be any JS object`

const dataSeries = new XyDataSeries(wasmContext, {

xValues: [1, 2, 3, 4, 5],

yValues: [4.3, 5.3, 6, 6.3, 6.4],

metadata: [

{ stringValue: "Here's", customValue: 7 },

{ stringValue: "Some", customValue: 7 },

{ stringValue: "Metadata" },

{ stringValue: "With", customValue: 99 },

{ stringValue: "Hit-Test" }

]

});

// Add a line series with the metadata

sciChartSurface.renderableSeries.add(

new FastLineRenderableSeries(wasmContext, {

dataSeries,

pointMarker: new EllipsePointMarker(wasmContext, {

width: 11,

height: 11,

fill: "#364BA0",

stroke: "#50C7E0",

strokeThickness: 2

})

})

);

// Perform a hit-test operation using mousedown event on the SciChartSurface <div>

sciChartSurface.domCanvas2D.addEventListener("mousedown", mouseEvent => {

const mouseClickX = mouseEvent.offsetX;

const mouseClickY = mouseEvent.offsetY;

console.log("mouseClickX", mouseClickX, "mouseClickY", mouseClickY);

// DpiHelper is a helper class in SciChart.js which allows you to adjust screen coordinates for browser zoom, retina and high-dpi screens

const premultipliedX = mouseEvent.offsetX * DpiHelper.PIXEL_RATIO;

const premultipliedY = mouseEvent.offsetY * DpiHelper.PIXEL_RATIO;

console.log("premultipliedX", premultipliedX, "premultipliedY", premultipliedY);

const HIT_TEST_RADIUS = 10;

// Perform a hit-test. Find out the members of HitTestInfo at https://www.scichart.com/documentation/js/v4/typedoc/classes/hittestinfo.html

const hitTestInfo = sciChartSurface.renderableSeries

.get(0)

.hitTestProvider.hitTest(premultipliedX, premultipliedY, HIT_TEST_RADIUS);

const resultDiv = document.getElementById("debug-hittest");

resultDiv.innerHTML =

`<p>Hit-test at x,y = ${mouseClickX}, ${mouseClickY}</p>` + `<p>isHit = ${hitTestInfo.isHit}</p>`;

if (hitTestInfo.isHit) {

resultDiv.innerHTML +=

`<p>index = ${hitTestInfo.dataSeriesIndex}</p>` +

`<p>xValue = ${hitTestInfo.xValue}</p>` +

`<p>yValue = ${hitTestInfo.yValue}</p>` +

`<p>Metadata.stringValue = ${hitTestInfo.metadata?.stringValue ?? "null"}</p>` +

`<p>Metadata.customValue = ${hitTestInfo.metadata?.customValue ?? "null"}</p>`;

}

console.log("hitTestInfo", hitTestInfo);

});

Click on the data-points in the example below to see the Hit-Test result.