---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/hit-test-api/fast-triangle-renderable-series
scraped_at: 2025-11-28T18:24:31.332454
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/hit-test-api/fast-triangle-renderable-series

# Hit-Test API for Triangle Series

The IHitTestProvider.hitTest method on FastTriangleRenderableSeries📘 tests if the click was within the Triangle's bounds and returns a HitTestInfo📘 object with the following properties:

### HitTest on 1 particular Triangle Series:

The algorithm is as follows:

- Find the nearest triangle in X direction.
- Test if the click was within triangle bounds and update HitTestInfo.isHit📘 property.

First, you need to add at least 1 renderable series you plan to hit-test on:

`const sXValues = [`

329, 300, 264, 234, 195, 174, 134, 136, 87, 106, 61, 103, 74, 115,

92, 129, 116, 164, 156, 193, 208, 247, 242, 286, 273, 321, 286, 327,

283, 321, 282, 308, 262, 280, 239, 213, 175, 144, 111, 82, 64

];

const sYValues = [

426, 411, 446, 415, 446, 417, 446, 414, 426, 396, 385, 370, 338, 341,

309, 313, 275, 295, 255, 284, 232, 264, 225, 248, 209, 212, 190, 174,

159, 136, 134, 102, 104, 75, 99, 68, 103, 76, 111, 83, 127

];

const sSeries = new FastTriangleRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: sXValues,

yValues: sYValues

}),

paletteProvider: new SPaletteProvider(),

drawMode: ETriangleSeriesDrawMode.Strip,

isDigitalLine: false,

fill: "green",

});

sciChartSurface.renderableSeries.add(sSeries);

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

y1: 470,

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