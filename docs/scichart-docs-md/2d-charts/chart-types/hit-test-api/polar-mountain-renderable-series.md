---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/hit-test-api/polar-mountain-renderable-series
scraped_at: 2025-11-28T18:24:32.150451
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/hit-test-api/polar-mountain-renderable-series

# Hit-Test API for Polar Mountain Series

The IHitTestProvider.hitTest method on PolarMountainRenderableSeries📘 tests if the click was within the mountain body, and returns a HitTestInfo📘 object with the following properties:

## Hit-Test on a particular Polar Mountain Series

Calling the `hitTest`

method on one specific series can be done this way:

`const x = mouseEvent.offsetX * DpiHelper.PIXEL_RATIO;`

const y = mouseEvent.offsetY * DpiHelper.PIXEL_RATIO;

const hitTestInfo: HitTestInfo = polarMountainSeries.hitTestProvider.hitTest(x, y);

The algorithm is as follows:

- Finds two nearest points in x direction that the x-hit value falls between them.
- Tests if the click is within the triangle formed by two nearest points and the center of polar surface HitTestInfo.isHit📘 property.

## Hit-Test on multiple Polar Mountain Series

First, we add two renderable series we will hit-test on:

`// add a couple of polar mountains to the chart`

const polarMountain1 = new PolarMountainRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: [0, 1, 2, 3, 4, 5, 6, 7],

yValues: [2.5, 1.8, 3.0, 1.4, 2.0, 1.75, 2.4, 1.5],

dataSeriesName: "Red Mountain"

}),

stroke: "white",

fill: "#883333",

});

const polarMountain2 = new PolarMountainRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: [8, 9, 10, 11, 12, 13, 14, 15],

yValues: [4.5, 3.2, 5.1, 2.8, 4.0, 3.5, 4.8, 3.0],

dataSeriesName: "Blue Mountain"

}),

stroke: "black",

fill: "#3333AA",

pointMarker: new EllipsePointMarker(wasmContext, {

width: 10,

height: 10,

strokeThickness: 2,

stroke: "SteelBlue",

fill: "LightSteelBlue"

}),

});

sciChartSurface.renderableSeries.add(polarMountain1, polarMountain2);

Second, we add an event-listener on the "mousedown" event:

`// Add an event listener for mouse down events`

sciChartSurface.domCanvas2D.addEventListener("mousedown", (mouseEvent: MouseEvent) => {

// Use our DpiHelper class to multiply coordinates, else screens with non-100% scaling will not work very well

const x = mouseEvent.offsetX * DpiHelper.PIXEL_RATIO;

const y = mouseEvent.offsetY * DpiHelper.PIXEL_RATIO;

// optional - flag to stop checking for hit-test on other series once a hit is found

let wasTheHitSuccessfulAtLeastOnce = false;

[...sciChartSurface.renderableSeries.asArray()] // copy the renderable series to an array

.reverse() // reverse array -> The 2nd series will be drawn on top of the 1st series, users likely want to hit-test the topmost series first (valueable for overlapping series)

.forEach(rs => {

console.log(`Trying hit test on: ${rs.getDataSeriesName()}`);

if (rs.hitTestProvider && mouseEvent && !wasTheHitSuccessfulAtLeastOnce) {

const hitTestInfo = rs.hitTestProvider.hitTest(x, y, HIT_TEST_RADIUS);

dotAnnotation.x1 = hitTestInfo.hitTestPointValues.x;

dotAnnotation.y1 = hitTestInfo.hitTestPointValues.y;

dotAnnotation.isHidden = false;

if (hitTestInfo.isHit) {

// Successful Hit

dotAnnotation.svgString = SUCCESSFUL_HIT_SVG;

textAnnotation.text = `Hit (x: ${hitTestInfo.hitTestPointValues.x.toFixed(2)}, y: ${hitTestInfo.hitTestPointValues.y.toFixed(2)})\n`

+ `- series: "${hitTestInfo.associatedSeries.getDataSeriesName()}"\n`

+ `- mountain index: ${hitTestInfo.dataSeriesIndex}\n`

+ `- yValue: ${hitTestInfo.yValue}`;

wasTheHitSuccessfulAtLeastOnce = true;

} else {

// No Hit

dotAnnotation.svgString = NO_HIT_SVG;

textAnnotation.text = `No hit detected\n`;

}

}

});

});

Which results in the following example