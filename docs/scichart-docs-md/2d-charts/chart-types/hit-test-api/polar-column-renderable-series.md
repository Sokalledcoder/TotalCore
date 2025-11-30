---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/hit-test-api/polar-column-renderable-series
scraped_at: 2025-11-28T18:24:32.590315
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/hit-test-api/polar-column-renderable-series

# Hit-Test API for Polar Column Series

The IHitTestProvider.hitTest method on PolarColumnRenderableSeries📘 tests if the click was within the Column's body and returns a HitTestInfo📘 object with the following properties:

### HitTest on 1 particular Polar Column Series:

Calling the `hitTest`

method on one specific series is very easy and can be done this way:

`const x = mouseEvent.offsetX * DpiHelper.PIXEL_RATIO;`

const y = mouseEvent.offsetY * DpiHelper.PIXEL_RATIO;

const colHitTestInfo: HitTestInfo = colSeries1.hitTestProvider.hitTest(x, y);

The algorithm is as follows:

- Find the nearest column in X direction.
- Test if the click was within column body and update HitTestInfo.isHit📘 property.

### Here is how you would implement it on multiple Polar Column Series:

First, you need to add the renderable series you plan to hit-test on:

`// add a couple of polar columns to the chart`

const polarColumn1 = new PolarColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],

yValues: [2.5, 1.8, 3.0, 1.4, 2.0, 1.75, 2.4, 1.5, 3.0, 4.5, 2],

dataSeriesName: "Red Columns"

}),

stroke: "white",

fill: "#883333",

dataPointWidth: 0.6

});

const polarColumn2 = new PolarColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: [9, 10, 11, 12, 13, 14, 15, 16],

yValues: [4.5, 3.2, 3.9, 2.8, 4.0, 3.5, 4.8, 3.0],

dataSeriesName: "Blue Columns"

}),

stroke: "black",

fill: "#3333AA99",

dataPointWidth: 0.8

});

sciChartSurface.renderableSeries.add(polarColumn1, polarColumn2);

And then, add an event-listener, likely on the "mousedown" event:

`// Add an event listener for mouse down events`

sciChartSurface.domCanvas2D.addEventListener("mousedown", (mouseEvent: MouseEvent) => {

// Use our DpiHelper class to multiply coordinates, else screens with non-100% scaling will not work very well

const x = mouseEvent.offsetX * DpiHelper.PIXEL_RATIO;

const y = mouseEvent.offsetY * DpiHelper.PIXEL_RATIO;

// optional - flag to stop checking for hit-test on other series once a hit is found

let wasTheHitSuccessfulAtLeastOnce = false;

[...sciChartSurface.renderableSeries.asArray()] // copy the renderable series to an anonymous array to not modify the original collection

.reverse() // The default layering of series is from bottom to top in the array, so we reverse it to check from top to bottom

.forEach(rs => {

console.log(`Trying hit test on: ${rs.getDataSeriesName()}`);

if (rs.hitTestProvider && mouseEvent && !wasTheHitSuccessfulAtLeastOnce) {

const hitTestInfo = rs.hitTestProvider.hitTestDataPoint(x, y, HIT_TEST_RADIUS);

dotAnnotation.x1 = hitTestInfo.hitTestPointValues.x;

dotAnnotation.y1 = hitTestInfo.hitTestPointValues.y;

dotAnnotation.isHidden = false;

if (hitTestInfo.isHit) {

// Successful Hit

dotAnnotation.svgString = SUCCESSFUL_HIT_SVG;

textAnnotation.text = `Hit (x: ${hitTestInfo.hitTestPointValues.x.toFixed(2)}, y: ${hitTestInfo.hitTestPointValues.y.toFixed(2)})\n`

+ `- series: "${hitTestInfo.associatedSeries.getDataSeriesName()}"\n`

+ `- column index: ${hitTestInfo.dataSeriesIndex}\n`

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

Which results in this following functionality: