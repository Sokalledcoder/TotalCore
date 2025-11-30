---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/hit-test-api/fast-mountain-renderable-series
scraped_at: 2025-11-28T18:24:31.257437
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/hit-test-api/fast-mountain-renderable-series

# Hit-Test API for Mountain Series

## The hitTest method on Mountain Series

The **IHitTestProvider.hitTest** method on FastMountainRenderableSeries tests if the click was within the mountain body.

`// hitTest method on Mountain Series`

const hitTestInfo = mountainSeries.hitTestProvider.hitTest(premultipliedX, premultipliedY);

The algorithm is as follows:

- Find the nearest data point in X direction.
- Test if the click was within the mountain body and update
**HitTestInfo.isHit**property.

This is the full example of the **hitTest** method on Mountain Series.

- JS
- TS

`import { SciChartSurface, NumericAxis, NumberRange, DpiHelper, CustomAnnotation, EHorizontalAnchorPoint, EVerticalAnchorPoint, XyDataSeries, FastMountainRenderableSeries } from "scichart";`

export async function hitTestMountainTs(divId) {

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divId);

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { growBy: new NumberRange(0.05, 0.05) }));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { growBy: new NumberRange(0.05, 0.05) }));

// Column series

const xValues = [0, 1, 2, 3, 4, 5, 6, 7, 8];

const yValues = [0, 0.2, 1, 2.0, 2.5, 1.9, 1.9, 1.5, 1.2];

const mountainSeries = new FastMountainRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: xValues,

yValues: yValues

})

});

sciChartSurface.renderableSeries.add(mountainSeries);

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

console.log('mouseClickX', mouseClickX, 'mouseClickY', mouseClickY);

const premultipliedX = mouseEvent.offsetX * DpiHelper.PIXEL_RATIO;

const premultipliedY = mouseEvent.offsetY * DpiHelper.PIXEL_RATIO;

console.log('premultipliedX', premultipliedX, 'premultipliedY', premultipliedY);

// IHitTestProvider.hitTest

const hitTestInfo = mountainSeries.hitTestProvider.hitTest(premultipliedX, premultipliedY);

svgAnnotation.x1 = hitTestInfo.hitTestPointValues.x;

svgAnnotation.y1 = hitTestInfo.hitTestPointValues.y;

svgAnnotation.isHidden = false;

const resultDiv = document.getElementById('result');

resultDiv.innerText = `isHit = ${hitTestInfo.isHit}`;

console.log('hitTestInfo', hitTestInfo);

});

}

`import { SciChartSurface, NumericAxis, NumberRange, DpiHelper, CustomAnnotation, EHorizontalAnchorPoint, EVerticalAnchorPoint, XyDataSeries, FastMountainRenderableSeries } from "scichart";`

export async function hitTestMountainTs(divId: string) {

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divId);

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { growBy: new NumberRange(0.05, 0.05) }));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { growBy: new NumberRange(0.05, 0.05) }));

// Column series

const xValues = [0, 1, 2, 3, 4, 5, 6, 7, 8];

const yValues = [0, 0.2, 1, 2.0, 2.5, 1.9, 1.9, 1.5, 1.2];

const mountainSeries = new FastMountainRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: xValues,

yValues: yValues

})

});

sciChartSurface.renderableSeries.add(mountainSeries);

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

console.log('mouseClickX', mouseClickX, 'mouseClickY', mouseClickY);

const premultipliedX = mouseEvent.offsetX * DpiHelper.PIXEL_RATIO;

const premultipliedY = mouseEvent.offsetY * DpiHelper.PIXEL_RATIO;

console.log('premultipliedX', premultipliedX, 'premultipliedY', premultipliedY);

// IHitTestProvider.hitTest

const hitTestInfo = mountainSeries.hitTestProvider.hitTest(premultipliedX, premultipliedY);

svgAnnotation.x1 = hitTestInfo.hitTestPointValues.x;

svgAnnotation.y1 = hitTestInfo.hitTestPointValues.y;

svgAnnotation.isHidden = false;

const resultDiv = document.getElementById('result');

resultDiv.innerText = `isHit = ${hitTestInfo.isHit}`;

console.log('hitTestInfo', hitTestInfo);

});

}

This gives us the chart below.

If to click inside the mountain it will be hit. In the browser console you will find output for the **HitTestInfo** object.

## The hitTestDataPoint method on Mountain Series

The **IHitTestProvider.hitTestDataPoint** method on FastMountainRenderableSeries tests if the click was within the **hitTestRadius** from a data point.

`// hitTestDataPoint method on Mountain Series`

const hitTestInfo = mountainSeries.hitTestProvider.hitTestDataPoint(premultipliedX, premultipliedY, HIT\_TEST\_RADIUS);

The algorithm is as follows:

- Iterate over each of the points to find the nearest one on the XY plane.
- Compare distance to the point with the
**hitTestRadius**and update**HitTestInfo.isHit**property.

## The hitTestXSlice method on Mountain Series

The **IHitTestProvider.hitTestXSlice** method is used for CursorModifier and RolloverModifier to get information about the nearest point.

`// hitTestXSlice method on Mountain Series`

const hitTestInfo = mountainSeries.hitTestProvider.hitTestXSlice(premultipliedX, premultipliedY);

The way it works:

- Finds the nearest point in X direction.
- Sets
**HitTestInfo.isHit**property to**True**if the mouse click was within the data bounds.