---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/hit-test-api/fast-line-renderable-series
scraped_at: 2025-11-28T18:24:31.136408
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/hit-test-api/fast-line-renderable-series

# Hit-Test API for Line Series

## The hitTest method on Line Series

The **IHitTestProvider.hitTest** method on FastLineRenderableSeries tests if the click was within the **hitTestRadius** from the line. The algorithm differs for sorted and unsorted data.

`// hitTest method on LineSeries`

const hitTestInfo = lineSeries.hitTestProvider.hitTest(premultipliedX, premultipliedY, HIT_TEST_RADIUS);

For **sorted data** the algorithm is as follows:

- Find the nearest point in X direction.
- Take the second adjacent point which is on the other side from the hit-test point.
- Calculate the distance from the hit-test point to the line formed by two points above and update HitTestInfo.isHit property.

For **unsorted data**:

- Iterate over each of the line segments and find the index with minimal distance to the hit-test point.
- Compare this distance with the
**hitTestRadius**and update**HitTestInfo.isHit**property.

## The hitTestDataPoint method on Line Series

The **IHitTestProvider.hitTestDataPoint** method on FastLineRenderableSeries tests if the click was within the **hitTestRadius** from a data point.

`// hitTestDataPoint method on Line Series`

const hitTestInfo = lineSeries.hitTestProvider.hitTestDataPoint(premultipliedX, premultipliedY, HIT_TEST_RADIUS);

The algorithm is as follows:

-
Iterate over each of the points to find the nearest one on the XY plane.

-
Compare distance to the nearest point with the

**hitTestRadius**and update**HitTestInfo.isHit**property.

This is an example of the **hitTestDataPoint** method usage.

- JS
- TS

`import {SciChartSurface, NumericAxis, FastLineRenderableSeries, XyDataSeries, NumberRange, DpiHelper, CustomAnnotation, EHorizontalAnchorPoint, EVerticalAnchorPoint } from "scichart";`

export async function hitTestTs(divId) {

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divId);

const HIT_TEST_RADIUS = 10 * DpiHelper.PIXEL_RATIO;

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { growBy: new NumberRange(0.05, 0.05) }));

const xLineValues = [0, 1, 2, 3, 4, 5, 6, 7, 8];

const yLineValues = [0, 0.5, 1.3, 2.4, 3, 2.5, 2.2, 1.9, 1.2];

const lineSeries = new FastLineRenderableSeries(wasmContext, {

strokeThickness: 3,

dataSeries: new XyDataSeries(wasmContext, { xValues: xLineValues, yValues: yLineValues })

});

sciChartSurface.renderableSeries.add(lineSeries);

// Add an SVG annotation to display the mouse click

const svgAnnotation = new CustomAnnotation({

svgString: `<svg width="8" height="8"><circle cx="50%" cy="50%" r="4" fill="#FF0000"/></svg>`,

isHidden: true,

horizontalAnchorPoint: EHorizontalAnchorPoint.Center,

verticalAnchorPoint: EVerticalAnchorPoint.Center

});

sciChartSurface.annotations.add(svgAnnotation);

sciChartSurface.domCanvas2D.addEventListener('mousedown', (mouseEvent) => {

const mouseClickX = mouseEvent.offsetX;

const mouseClickY = mouseEvent.offsetY;

console.log("mouseClickX", mouseClickX, "mouseClickY", mouseClickY);

const premultipliedX = mouseEvent.offsetX * DpiHelper.PIXEL_RATIO;

const premultipliedY = mouseEvent.offsetY * DpiHelper.PIXEL_RATIO;

console.log('premultipliedX', premultipliedX, 'premultipliedY', premultipliedY);

// IHitTestProvider.hitTestDataPoint

const hitTestInfo = lineSeries.hitTestProvider.hitTestDataPoint(premultipliedX, premultipliedY, HIT_TEST_RADIUS);

svgAnnotation.x1 = hitTestInfo.hitTestPointValues.x;

svgAnnotation.y1 = hitTestInfo.hitTestPointValues.y;

svgAnnotation.isHidden = false;

const resultDiv = document.getElementById("result");

resultDiv.innerText = `isHit = ${hitTestInfo.isHit}`;

console.log('hitTestInfo', hitTestInfo);

});

}

`import {SciChartSurface, NumericAxis, FastLineRenderableSeries, XyDataSeries, NumberRange, DpiHelper, CustomAnnotation, EHorizontalAnchorPoint, EVerticalAnchorPoint } from "scichart";`

export async function hitTestTs(divId: string) {

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divId);

const HIT_TEST_RADIUS = 10 * DpiHelper.PIXEL_RATIO;

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { growBy: new NumberRange(0.05, 0.05) }));

const xLineValues = [0, 1, 2, 3, 4, 5, 6, 7, 8];

const yLineValues = [0, 0.5, 1.3, 2.4, 3, 2.5, 2.2, 1.9, 1.2];

const lineSeries = new FastLineRenderableSeries(wasmContext, {

strokeThickness: 3,

dataSeries: new XyDataSeries(wasmContext, { xValues: xLineValues, yValues: yLineValues })

});

sciChartSurface.renderableSeries.add(lineSeries);

// Add an SVG annotation to display the mouse click

const svgAnnotation = new CustomAnnotation({

svgString: `<svg width="8" height="8"><circle cx="50%" cy="50%" r="4" fill="#FF0000"/></svg>`,

isHidden: true,

horizontalAnchorPoint: EHorizontalAnchorPoint.Center,

verticalAnchorPoint: EVerticalAnchorPoint.Center

});

sciChartSurface.annotations.add(svgAnnotation);

sciChartSurface.domCanvas2D.addEventListener('mousedown', (mouseEvent: MouseEvent) => {

const mouseClickX = mouseEvent.offsetX;

const mouseClickY = mouseEvent.offsetY;

console.log("mouseClickX", mouseClickX, "mouseClickY", mouseClickY);

const premultipliedX = mouseEvent.offsetX * DpiHelper.PIXEL_RATIO;

const premultipliedY = mouseEvent.offsetY * DpiHelper.PIXEL_RATIO;

console.log('premultipliedX', premultipliedX, 'premultipliedY', premultipliedY);

// IHitTestProvider.hitTestDataPoint

const hitTestInfo = lineSeries.hitTestProvider.hitTestDataPoint(premultipliedX, premultipliedY, HIT_TEST_RADIUS);

svgAnnotation.x1 = hitTestInfo.hitTestPointValues.x;

svgAnnotation.y1 = hitTestInfo.hitTestPointValues.y;

svgAnnotation.isHidden = false;

const resultDiv = document.getElementById("result");

resultDiv.innerText = `isHit = ${hitTestInfo.isHit}`;

console.log('hitTestInfo', hitTestInfo);

});

}

If we run the example we get this chart.

Clicking near a data point results is **isHit=true**. In the browser console you will find output for the **HitTestInfo** object.

## The hitTestXSlice method on Line Series

The **IHitTestProvider.hitTestXSlice** method is used for CursorModifier and RolloverModifier to get information about the nearest point.

`// hitTestXSlice method on Line Series`

const hitTestInfo = lineSeries.hitTestProvider.hitTestXSlice(premultipliedX, premultipliedY);

The way it works:

- Finds the nearest point in X direction.
- Sets
**HitTestInfo.isHit**property to True if the mouse click was within the data bounds.