---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/hit-test-api/fast-column-renderable-series
scraped_at: 2025-11-28T18:24:29.881777
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/hit-test-api/fast-column-renderable-series

# Hit-Test API for Column Series

## The hitTest method on Column Series

The **IHitTestProvider.hitTest** method on FastColumnRenderableSeries tests if the click was within the Column.

`// hitTest method on Column Series`

const hitTestInfo = columnSeries.hitTestProvider.hitTest(premultipliedX, premultipliedY);

The algorithm is as follows:

- Find the nearest column in X direction.
- Test if the click was within column body and update
**HitTestInfo.isHit**property.

This is the full example of the **hitTest** method on Column Series.

- JS
- TS

`import {SciChartSurface, NumericAxis, NumberRange, DpiHelper, CustomAnnotation, EHorizontalAnchorPoint, XyDataSeries, FastColumnRenderableSeries} from "scichart";`

export async function hitTestColumnTs(divId) {

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divId);

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { growBy: new NumberRange(0.05, 0.05) }));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { growBy: new NumberRange(0.05, 0.05) }));

// Column series

const xColumnValues = [0, 1, 2, 3, 4, 5, 6, 7, 8];

const yColumnValues = [0, 0.2, 1, 2.0, 2.5, 1.9, 1.9, 1.5, 1.2];

const columnSeries = new FastColumnRenderableSeries(wasmContext, {

fill: 'rgba(255,255,255,0.9)',

dataPointWidth: 0.5,

dataSeries: new XyDataSeries(wasmContext, {

xValues: xColumnValues,

yValues: yColumnValues

})

});

sciChartSurface.renderableSeries.add(columnSeries);

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

const hitTestInfo = columnSeries.hitTestProvider.hitTest(premultipliedX, premultipliedY);

svgAnnotation.x1 = hitTestInfo.hitTestPointValues.x;

svgAnnotation.y1 = hitTestInfo.hitTestPointValues.y;

svgAnnotation.isHidden = false;

const resultDiv = document.getElementById('result');

resultDiv.innerText = `isHit = ${hitTestInfo.isHit}`;

console.log('hitTestInfo', hitTestInfo);

});

}

`import {SciChartSurface, NumericAxis, NumberRange, DpiHelper, CustomAnnotation, EHorizontalAnchorPoint, XyDataSeries, FastColumnRenderableSeries} from "scichart";`

export async function hitTestColumnTs(divId: string) {

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divId);

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { growBy: new NumberRange(0.05, 0.05) }));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { growBy: new NumberRange(0.05, 0.05) }));

// Column series

const xColumnValues = [0, 1, 2, 3, 4, 5, 6, 7, 8];

const yColumnValues = [0, 0.2, 1, 2.0, 2.5, 1.9, 1.9, 1.5, 1.2];

const columnSeries = new FastColumnRenderableSeries(wasmContext, {

fill: 'rgba(255,255,255,0.9)',

dataPointWidth: 0.5,

dataSeries: new XyDataSeries(wasmContext, {

xValues: xColumnValues,

yValues: yColumnValues

})

});

sciChartSurface.renderableSeries.add(columnSeries);

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

const hitTestInfo = columnSeries.hitTestProvider.hitTest(premultipliedX, premultipliedY);

svgAnnotation.x1 = hitTestInfo.hitTestPointValues.x;

svgAnnotation.y1 = hitTestInfo.hitTestPointValues.y;

svgAnnotation.isHidden = false;

const resultDiv = document.getElementById('result');

resultDiv.innerText = `isHit = ${hitTestInfo.isHit}`;

console.log('hitTestInfo', hitTestInfo);

});

}

This gives us the chart below.

If to click inside the column it will be hit. In the browser console you will find output for the **HitTestInfo** object.

## The hitTestDataPoint method on Column Series

The **IHitTestProvider.hitTestDataPoint** method on FastColumnRenderableSeries tests if the click was within the **hitTestRadius** from a data point.

`// hitTestDataPoint method on Column Series`

const hitTestInfo = columnSeries.hitTestProvider.hitTestDataPoint(premultipliedX, premultipliedY, HIT_TEST_RADIUS);

The algorithm is as follows:

- Iterate over each of the points to find the nearest one on the XY plane.
- Compare distance to the point with the
**hitTestRadius**and update**HitTestInfo.isHit**property accordingly.

## The hitTestXSlice method on Column Series

The **IHitTestProvider.hitTestXSlice** method is used for CursorModifier and RolloverModifier to get information about the nearest point.

`// hitTestXSlice method on Column Series`

const hitTestInfo = columnSeries.hitTestProvider.hitTestXSlice(premultipliedX, premultipliedY);

The way it works:

- Finds the nearest point in X direction.
- Sets
**HitTestInfo.isHit**property to**True**if the mouse click was within the data bounds.