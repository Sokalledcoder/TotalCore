---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/hit-test-api/uniform-heatmap-renderable-series
scraped_at: 2025-11-28T18:24:33.819050
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/hit-test-api/uniform-heatmap-renderable-series

# Hit-Test API for Heatmap Series

## The hitTest method on Heatmap Series

The **IHitTestProvider.hitTest** method on UniformHeatmapRenderableSeries tests if the click was within the Heatmap.

`// hitTest method on Heatmap Series`

const hitTestInfo = heatmapSeries.hitTestProvider.hitTest(premultipliedX, premultipliedY);

The algorithm is as follows:

- Find X and Y index of the tile being clicked.
- Test if the click was within the Heatmap surface and update
**HitTestInfo.isHit**property.

This is the full example of the **hitTest** method on Heatmap Series.

- JS
- TS

`import {SciChartSurface, NumericAxis, DpiHelper, CustomAnnotation, EHorizontalAnchorPoint, EVerticalAnchorPoint, EAxisAlignment, HeatmapColorMap, HeatmapColorMap, UniformHeatmapDataSeries, UniformHeatmapRenderableSeries, NumberRange } from "scichart";`

export async function hitTestHeatmapTs(divId) {

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divId);

sciChartSurface.xAxes.add(

new NumericAxis(wasmContext, { axisTitle: 'Heatmap X', growBy: new NumberRange(0.05, 0.05) })

);

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

axisTitle: 'Heatmap Y',

axisAlignment: EAxisAlignment.Left,

growBy: new NumberRange(0.05, 0.05)

})

);

const gradientStops = [

{ offset: 0, color: 'yellow' },

{ offset: 1, color: 'red' }

];

const colorMap = new HeatmapColorMap({

minimum: 0,

maximum: 3,

gradientStops

});

const initialZValues = [

[3, 0, 1, 2],

[0, 1, 2, 3]

];

const dataSeries = new UniformHeatmapDataSeries(wasmContext, {

xStart: 0,

xStep: 1,

yStart: 3,

yStep: 1,

zValues: initialZValues

});

dataSeries.hasNaNs = true;

const heatmapSeries = new UniformHeatmapRenderableSeries(wasmContext, {

opacity: 0.5,

dataSeries,

colorMap

});

sciChartSurface.renderableSeries.add(heatmapSeries);

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

const hitTestInfo = heatmapSeries.hitTestProvider.hitTest(premultipliedX, premultipliedY);

svgAnnotation.x1 = hitTestInfo.hitTestPointValues.x;

svgAnnotation.y1 = hitTestInfo.hitTestPointValues.y;

svgAnnotation.isHidden = false;

const resultDiv = document.getElementById('result');

resultDiv.innerText = `isHit = ${hitTestInfo.isHit}`;

console.log('hitTestInfo', hitTestInfo);

});

}

`import {SciChartSurface, NumericAxis, DpiHelper, CustomAnnotation, EHorizontalAnchorPoint, EVerticalAnchorPoint, EAxisAlignment, HeatmapColorMap, HeatmapColorMap, UniformHeatmapDataSeries, UniformHeatmapRenderableSeries, NumberRange } from "scichart";`

export async function hitTestHeatmapTs(divId: string) {

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divId);

sciChartSurface.xAxes.add(

new NumericAxis(wasmContext, { axisTitle: 'Heatmap X', growBy: new NumberRange(0.05, 0.05) })

);

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

axisTitle: 'Heatmap Y',

axisAlignment: EAxisAlignment.Left,

growBy: new NumberRange(0.05, 0.05)

})

);

const gradientStops = [

{ offset: 0, color: 'yellow' },

{ offset: 1, color: 'red' }

];

const colorMap = new HeatmapColorMap({

minimum: 0,

maximum: 3,

gradientStops

});

const initialZValues = [

[3, 0, 1, 2],

[0, 1, 2, 3]

];

const dataSeries = new UniformHeatmapDataSeries(wasmContext, {

xStart: 0,

xStep: 1,

yStart: 3,

yStep: 1,

zValues: initialZValues

});

dataSeries.hasNaNs = true;

const heatmapSeries = new UniformHeatmapRenderableSeries(wasmContext, {

opacity: 0.5,

dataSeries,

colorMap

});

sciChartSurface.renderableSeries.add(heatmapSeries);

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

const hitTestInfo = heatmapSeries.hitTestProvider.hitTest(premultipliedX, premultipliedY);

svgAnnotation.x1 = hitTestInfo.hitTestPointValues.x;

svgAnnotation.y1 = hitTestInfo.hitTestPointValues.y;

svgAnnotation.isHidden = false;

const resultDiv = document.getElementById('result');

resultDiv.innerText = `isHit = ${hitTestInfo.isHit}`;

console.log('hitTestInfo', hitTestInfo);

});

}

If to click inside the Heatmap surface it will be hit. In the browser console you will find output for the **HitTestInfo** object containing **heatmapValue**, **heatmapXIndex** and **heatmapYIndex** properties which are only for the UniformHeatmapDataSeries📘.

## The hitTestDataPoint method on Heatmap Series

The **IHitTestProvider.hitTestDataPoint** method is not supported for UniformHeatmapRenderableSeries.

## The hitTestXSlice method on Heatmap Series

The **IHitTestProvider.hitTestXSlice** method works identically as the **IHitTestProvider.hitTest**.