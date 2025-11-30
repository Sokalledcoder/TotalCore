---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/hit-test-api/stacked-mountain-renderable-series
scraped_at: 2025-11-28T18:24:33.711840
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/hit-test-api/stacked-mountain-renderable-series

# Hit-Test API for Stacked Mountain Series

## The hitTest method on Stacked Mountain Series

The **IHitTestProvider.hitTest** method on **StackedMountainRenderableSeries** tests if the click was within the band for this stacked mountain series.

`// hitTest method on Stacked Mountain Series`

const hitTestInfo = stackedMountainRS.hitTestProvider.hitTest(premultipliedX, premultipliedY);

The algorithm is as follows:

- Find the nearest data point in X direction.
- Test if the click was within the band for this stacked mountain series and update
**HitTestInfo.isHit**property.

This is the full example of the **hitTest** method on Stacked Mountain Series.

`import { SciChartSurface, NumericAxis, DpiHelper, CustomAnnotation, EHorizontalAnchorPoint, EVerticalAnchorPoint, NumberRange, XyDataSeries, HitTestInfo, StackedMountainRenderableSeries, StackedMountainCollection} from "scichart";`

export async function hitTestStackedMountainTs(divId) {

const xValues = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18];

const y1Values = [4, 7, 5.2, 9.4, 3.8, 5.1, 7.5, 12.4, 14.6, 8.1, 11.7, 14.4, 16, 3.7, 5.1, 6.4, 3.5, 2.5];

const y2Values = [15, 10.1, 10.2, 10.4, 10.8, 1.1, 11.5, 3.4, 4.6, 0.1, 1.7, 14.4, 6, 13.7, 10.1, 8.4, 8.5, 12.5];

const y3Values = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 3, 3, 2, 2, 2];

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divId);

const xAxis = new NumericAxis(wasmContext);

sciChartSurface.xAxes.add(xAxis);

const yAxis = new NumericAxis(wasmContext);

yAxis.growBy = new NumberRange(0, 0.1);

sciChartSurface.yAxes.add(yAxis);

const dataSeries1 = new XyDataSeries(wasmContext, { xValues, yValues: y1Values });

const dataSeries2 = new XyDataSeries(wasmContext, { xValues, yValues: y2Values });

const dataSeries3 = new XyDataSeries(wasmContext, { xValues, yValues: y3Values });

const rendSeries1 = new StackedMountainRenderableSeries(wasmContext);

rendSeries1.dataSeries = dataSeries1;

rendSeries1.fill = '#939899';

rendSeries1.rolloverModifierProps.markerColor = '#7b7e80';

rendSeries1.rolloverModifierProps.tooltipColor = 'rgba(147,152,153,0.7)';

rendSeries1.rolloverModifierProps.tooltipTextColor = '#000';

rendSeries1.isDigitalLine = false;

const rendSeries2 = new StackedMountainRenderableSeries(wasmContext);

rendSeries2.dataSeries = dataSeries2;

rendSeries2.fill = '#66838d';

rendSeries2.rolloverModifierProps.markerColor = '#495d65';

rendSeries2.rolloverModifierProps.tooltipColor = 'rgba(102,131,141,0.7)';

rendSeries2.rolloverModifierProps.tooltipTextColor = '#000';

rendSeries2.isDigitalLine = false;

const rendSeries3 = new StackedMountainRenderableSeries(wasmContext);

rendSeries3.dataSeries = dataSeries3;

rendSeries3.fill = '#368BC1';

rendSeries3.rolloverModifierProps.markerColor = '#2d739e';

rendSeries3.rolloverModifierProps.tooltipColor = 'rgba(54,139,193,0.7)';

rendSeries3.rolloverModifierProps.tooltipTextColor = '#000';

rendSeries3.isDigitalLine = false;

const verticallyStackedMountainCollection = new StackedMountainCollection(wasmContext);

verticallyStackedMountainCollection.add(rendSeries1, rendSeries2, rendSeries3);

sciChartSurface.renderableSeries.add(verticallyStackedMountainCollection);

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

const hitTestResults: HitTestInfo[] = verticallyStackedMountainCollection

.asArray()

.reduce((acc, stackedMountainRS) => {

const hitTestInfo = stackedMountainRS.hitTestProvider.hitTest(premultipliedX, premultipliedY);

acc.push(hitTestInfo);

return acc;

}, []);

svgAnnotation.x1 = hitTestResults[0].hitTestPointValues.x;

svgAnnotation.y1 = hitTestResults[0].hitTestPointValues.y;

svgAnnotation.isHidden = false;

const resultDiv = document.getElementById('result');

resultDiv.innerText = JSON.stringify(

hitTestResults.map((hitTestInfo, index) => `${index} isHit = ${hitTestInfo.isHit}; `)

);

console.log('hitTestResults', hitTestResults);

});

}

The StackedMountainCollection in this example has three StackedMountainRenderableSeries. Therefore, we use **reduce** function to iterate over each renderable series and to accumulate the result.

This gives us this chart.

If we click inside the gray band it will be hit for the StackedMountainRenderableSeries with index 1. In the browser console you will find output with an array of **HitTestInfo** results.

## The hitTestDataPoint method on Stacked Mountain Series

The **IHitTestProvider.hitTestDataPoint** method is not supported for StackedMountainRenderableSeries.

## The hitTestXSlice method on Stacked Mountain Series

The **IHitTestProvider.hitTestXSlice** method is used for CursorModifier and RolloverModifier to get information about the nearest point.

`// hitTestXSlice on Stacked Mountain Series`

const hitTestInfo = stackedMountainRS.hitTestProvider.hitTestXSlice(premultipliedX, premultipliedY);

The way it works:

- Finds the nearest point in X direction.
- Sets
**HitTestInfo.isHit**property to**True**if the mouse click was within the data bounds.