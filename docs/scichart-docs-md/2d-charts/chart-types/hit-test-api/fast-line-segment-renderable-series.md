---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/hit-test-api/fast-line-segment-renderable-series
scraped_at: 2025-11-28T18:24:31.038002
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/hit-test-api/fast-line-segment-renderable-series

# Hit-Test API for Line Segment Series

The IHitTestProvider.hitTest method on FastLineSegmentRenderableSeries📘 tests if the click was within the Line's bounds and returns a HitTestInfo📘 object with the following properties:

### HitTest on 1 particular Line Segment Series:

The algorithm is as follows:

- Find the nearest line in X direction.
- Test if the click was within line bounds and update HitTestInfo.isHit📘 property.

First, you need to add at least 1 renderable series you plan to hit-test on:

`// add a couple of line segments to the chart`

const lineSegment1 = new FastLineSegmentRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: [0.5, 1, 2, 3, 5, 4, 6, 7, 8, 9],

yValues: [4.5, 3.2, 5.1, 2.8, 4.0, 3.5, 4.8, 3.0, 2.3, 7.1],

dataSeriesName: "Teal&Orange Segments"

}),

strokeThickness: 5,

paletteProvider: new LineSegmentPaletteProvider(),

});

sciChartSurface.renderableSeries.add(lineSegment1);

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

x1: 1,

y1: 9,

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

+ `- Series index: ${hitTestInfo.dataSeriesIndex}\n`

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