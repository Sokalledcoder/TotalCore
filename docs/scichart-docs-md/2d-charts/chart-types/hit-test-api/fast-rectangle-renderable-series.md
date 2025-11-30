---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/hit-test-api/fast-rectangle-renderable-series
scraped_at: 2025-11-28T18:24:31.395323
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/hit-test-api/fast-rectangle-renderable-series

# Hit-Test API for Rectangle Series

The IHitTestProvider.hitTest method on FastRectangleRenderableSeries📘 tests if the click was within the Rectangle's bounds and returns a HitTestInfo📘 object with the following properties:

### HitTest on 1 particular Rectangle Series:

The algorithm is as follows:

- Find the nearest rectangle in X direction.
- Test if the click was within rectangle bounds and update HitTestInfo.isHit📘 property.

First, you need to add at least 1 renderable series you plan to hit-test on:

`const xValues = [0, 6, 10, 17];`

const yValues = [0, 6, 2, 5];

const x1Values = [5, 9, 15, 25];

const y1Values = [5, 9, 8, 10];

const rectangleSeries = new FastRectangleRenderableSeries(wasmContext, {

dataSeries: new XyxyDataSeries(wasmContext, {

xValues,

yValues,

x1Values,

y1Values

}),

columnXMode: EColumnMode.StartEnd, // x, x1

columnYMode: EColumnYMode.TopBottom, // y, y1

fill: "cornflowerblue",

stroke: "black",

strokeThickness: 1,

opacity: 0.5

});

And then, add an event-listener, likely on the

`mousedown`

event:

`const SUCCESSFUL_HIT_SVG = `<svg width="8" height="8"><circle cx="50%" cy="50%" r="4" fill="#33AA33" stroke="#000000" stroke-width="0.7"/></svg>`;`

const NO_HIT_SVG = `<svg width="4" height="4"><circle cx="50%" cy="50%" r="2" fill="#FF0000"/></svg>`;

const HIT_TEST_RADIUS = 10; // Radius for hit testing

// --- Minimal HitTest and SVG Annotation ---

const dotAnnotation = new CustomAnnotation({

svgString: NO_HIT_SVG,

isHidden: true, // initially hidden

horizontalAnchorPoint: EHorizontalAnchorPoint.Center,

verticalAnchorPoint: EVerticalAnchorPoint.Center,

xCoordinateMode: ECoordinateMode.DataValue,

yCoordinateMode: ECoordinateMode.DataValue

});

const textAnnotation = new NativeTextAnnotation({

text: "",

fontSize: 20,

x1: 0,

y1: 10,

lineSpacing: 10,

multiLineAlignment: EMultiLineAlignment.Left,

xCoordinateMode: ECoordinateMode.DataValue,

yCoordinateMode: ECoordinateMode.DataValue,

});

sciChartSurface.annotations.add(dotAnnotation, textAnnotation);

// Add an event listener for mouse down events

sciChartSurface.domCanvas2D.addEventListener("mousedown", (mouseEvent: MouseEvent) => {

// Use our DpiHelper class to multiply coordinates, else screens with non-100% scaling will not work very well

const x = mouseEvent.offsetX * DpiHelper.PIXEL_RATIO;

const y = mouseEvent.offsetY * DpiHelper.PIXEL_RATIO;

const rs = sciChartSurface.renderableSeries.get(0); // Get the renderable series

if (rs.hitTestProvider && mouseEvent) {

const hitTestInfo = rs.hitTestProvider.hitTest(x, y, HIT_TEST_RADIUS);

dotAnnotation.x1 = hitTestInfo.hitTestPointValues.x;

dotAnnotation.y1 = hitTestInfo.hitTestPointValues.y;

dotAnnotation.isHidden = false;

if (hitTestInfo.isHit) {

// Successful Hit

dotAnnotation.svgString = SUCCESSFUL_HIT_SVG;

textAnnotation.text = `Hit (x: ${hitTestInfo.hitTestPointValues.x.toFixed(2)}, y: ${hitTestInfo.hitTestPointValues.y.toFixed(2)})\n`

+ `- Rectangle index: ${hitTestInfo.dataSeriesIndex}\n`

+ `- yValue: ${hitTestInfo.yValue}\n`

+ `- xValue: ${hitTestInfo.xValue}`;

} else {

// No Hit

dotAnnotation.svgString = NO_HIT_SVG;

textAnnotation.text = `No hit detected\n`;

}

}

});

Which results in this following functionality: