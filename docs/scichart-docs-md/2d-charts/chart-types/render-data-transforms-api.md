---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/render-data-transforms-api
scraped_at: 2025-11-28T18:24:42.647524
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/render-data-transforms-api

# RenderDataTransforms API

**RenderDataTransforms** allow you to transform your data immediately before it is drawn.

This allows you to change visual output performing transforms on chart series, while keeping your data unchanged - meaning tooltips, cursors and more are unchanged by this type of transform.

This API differs from the Data Filters API, which applies transforms to Data and can be used to create Moving Averages, or Linear Interpolation and more.

The RenderTransforms API keeps your data intact, but changes the visual output on the screen.

Some examples of uses of RenderDataTransforms are:

**Interpolating the data.**SciChart uses the RenderDataTransforms API internally to draw the spline series**Switching Styles**on a series, for example rendering data on the same series with different pointmarkers or line styles.**Splitting Line Segments**, adding points into the data to be able to draw a single line segment in multiple colors**Adding Gaps to series**by manipulating NaN values

## Where RenderDataTransforms Fit

In this documentation we are going to walk through some examples of RenderDataTransforms, but to understand them, we first need to understand some details of the SciChart render process and the difference between DataSeries and PointSeries.

The SciChart render function goes through roughly the following stages:

**Layout**. Here we calculate the size and position of the axes**AutoRange**. If required, we measure the data range and update the visibleRange of the axes**Prepare series data.**Here we convert from the DataSeries to a PointSeries. A PointSeries has arrays of vectors like a DataSeries, but not other functionality. The PointSeries may be just a wrapper (basePointSeriesWrapped📘) - pointing to the vectors in the dataSeries, or it may be the result of a resampling operation (basePointSeriesResampled📘), in which case it has completely separate sets of vectors. This, along with an indexRange which indicates what part of the data should be drawn, is put together into RenderPassData📘.**Draw series**. The renderPassData📘 is passed to the draw method of each drawingProvider📘 on the renderableSeries📘. Lines and pointMarkers have separate drawingProviders. This is where the renderDataTransform📘 can come into play. If the current drawingProvider is in the list on the transform, then the transform is run and the resulting renderPassData is given to the drawingProvider instead.

The point here is that the renderDataTransform📘 only applies to drawing. It does not change the dataSeries, and is not seen by hitTest or modifiers. It can however be used by AutoRange if required.

To make all this efficient, there is a base class for renderDataTransforms📘 which holds the result of the transform and only runs it if necessary.

## BaseRenderDataTransform

When creating renderDataTransforms, you should extend from BaseRenderDataTransform📘 or (since 3.4.662) one of the non-abstract derived classes eg XyBaseRenderDataTransform📘, XyyBaseRenderDataTransform📘, or OhlcBaseRenderDataTransform📘.

You should implement runTransformInternal📘, which returns a pointSeries📘, rather than RenderPassData📘. The base class takes care of calling runTransformInternal📘 only when necessary, and creating the RenderPassData from the pointSeries.

In order for this to work, and to avoid memory leaks, you should clear and push to the vectors on BaseRenderDataTransform.pointSeries📘. Do NOT create a new pointSeries in runTransformInternal📘.

If your transform depends on anything other than the dataSeries and the indexRange, then you need to set requiresTransform📘 to **true** of that dependency changes. There are examples of this below.

If your transform changes the yRange of your data and you want this accounted for in AutoRange, set useForYRange📘 true. The transform will be run and the result used for autoRange, and since the resulting pointSeries is held by the transform it will not need to run again at the point of drawing.

## Worked Example: Splitting Data to Multiple DrawingProviders

This is a simplified version of the Multi Style Series demo. Below is the transform which takes xy data and returns an xyyPointSeries📘 with the unselected points in the yValues and selected points in the y1Values.

- TYPEscript

`// Using XyyBaseRenderDataTransform here because you cannot extend the abstract BaseRenderDataTransform when using browser bundle`

class SplitBySelectedDataTransform extends XyyBaseRenderDataTransform {

protected runTransformInternal(renderPassData: RenderPassData): IPointSeries {

// Guard in case the incoming data is empty

// If you want to do nothing and draw the original data, you don't need to copy it, you can just return renderPassData.pointSeries

if (!renderPassData.pointSeries) {

return this.pointSeries;

}

// It is important to reuse this.pointSeries. Do NOT create a new pointSeries on each transform

const { xValues: oldX, yValues: oldY, indexes: oldI, resampled } = renderPassData.pointSeries;

const { xValues, yValues, y1Values, indexes } = this.pointSeries;

// Clear the target vectors

xValues.clear();

yValues.clear();

y1Values.clear();

indexes.clear();

// indexRange tells the drawing to only use a subset of the data. If data has been resampled, then always use all of it

const iStart = resampled ? 0 : renderPassData.indexRange.min;

const iEnd = resampled ? oldX.size() - 1 : renderPassData.indexRange?.max;

const ds = this.parentSeries.dataSeries as XyDataSeries;

for (let i = iStart; i <= iEnd; i++) {

// If data has been resampled, we need the original index in order to get the correct metadata

const index = resampled ? oldI.get(i) : i;

const md = ds.getMetadataAt(index);

xValues.push_back(oldX.get(i));

indexes.push_back(index);

// Push the y value to the desired target vector

if (md.isSelected) {

yValues.push_back(Number.NaN);

y1Values.push_back(oldY.get(i));

} else {

yValues.push_back(oldY.get(i));

y1Values.push_back(Number.NaN);

}

}

// Return the transformed pointSeries.

return this.pointSeries;

}

}

To use this, we set up a second drawingProvider which uses a different pointMarker and draws the y1Values of the pointSeries.

- TYPEscript

`const xValues = makeIncArray(50);`

const yValues = makeIncArray(50, 1, y => Math.sin(y * 0.2));

// Create metaData with some points selected

const metadata = xValues.map(x => ({ isSelected: x > 10 && x < 20 } as IPointMetadata));

const renderableSeries = new XyScatterRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues,

yValues,

metadata

//containsNaN: true,

}),

pointMarker: new TrianglePointMarker(wasmContext, {

width: 10,

height: 10,

stroke: "green",

fill: "green"

})

});

// Create a second PointMarkerDrawingProvider with a ySelector so that it uses y1Values

const selectedPointDrawingProvider = new PointMarkerDrawingProvider(

wasmContext,

renderableSeries,

ps => (ps as IXyyPointSeries).y1Values

);

// Create a different pointMarker

const squarePM = new SquarePointMarker(wasmContext, {

width: 10,

height: 10,

stroke: "red",

fill: "red"

});

// Tell the new drawingProvider to use the new pointmarker instead of the one from the series.

selectedPointDrawingProvider.getProperties = () => ({

pointMarker: squarePM as IPointMarker

});

// Add the new drawingProvider to the series

renderableSeries.drawingProviders.push(selectedPointDrawingProvider);

// Create the transform and add it to the series. Pass the drawingProviders array as this transform applies to all of them

renderableSeries.renderDataTransform = new SplitBySelectedDataTransform(

renderableSeries,

wasmContext,

renderableSeries.drawingProviders

);

sciChartSurface.renderableSeries.add(renderableSeries);

// Add Datapoint selection to allow updating the state on which the transform depends

sciChartSurface.chartModifiers.add(

new DataPointSelectionModifier({

allowClickSelect: true,

onSelectionChanged: args => {

// Since the transform depends on the selection state, we must tell the transform that it must run when the selection changes.

renderableSeries.renderDataTransform.requiresTransform = true;

}

})

);

The output looks like this

## Worked Example: Splitting lines for Threshold Coloring

The Coloring Series per-point using PaletteProvider demo shows a simple way to change the color of line segments if they are above or below a threshold. However, per point coloring applies to individual line segments. If you have less data or longer line segments and want the coloring to be split exactly on the threshold, then you need to add points into your data at the intersections. RenderDataTransforms allow you to do this without affecting the drawing of pointMarkers.

Here is a transform which does this for a set of y thresholds. The algorithm needs to handle the fact that a line could cross multiple thresholds, and that an intersection could be on an existing point. Note that we use an ObservableArray for the thresholds so we can set requiresTransform if the thresholds change.

This transform should only apply to line drawing, so we pass only the first drawingProvider from the renderableSeries to the transform.

- TYPEscript

`class ThresholdRenderDataTransform extends XyBaseRenderDataTransform {`

// Using XyBaseRenderDataTransform here as we are converting to XyPointSeries

public thresholds: ObservableArrayBase<number> = new ObservableArrayBase();

public constructor(parentSeries: BaseRenderableSeries, wasmContext: TSciChart, thresholds: number[]) {

// Apply to line drawing only

super(parentSeries, wasmContext, [parentSeries.drawingProviders[0]]);

this.thresholds.add(...thresholds);

this.onThresholdsChanged = this.onThresholdsChanged.bind(this);

this.thresholds.collectionChanged.subscribe(this.onThresholdsChanged);

}

private onThresholdsChanged(data: ObservableArrayChangedArgs) {

this.requiresTransform = true;

if (this.parentSeries.invalidateParentCallback) {

this.parentSeries.invalidateParentCallback();

}

}

public delete(): void {

this.thresholds.collectionChanged.unsubscribeAll();

super.delete();

}

protected runTransformInternal(renderPassData: RenderPassData): IPointSeries {

const numThresholds = this.thresholds.size();

if (numThresholds === 0) {

return renderPassData.pointSeries;

}

const { xValues: oldX, yValues: oldY, indexes: oldI, resampled } = renderPassData.pointSeries;

const { xValues, yValues, indexes } = this.pointSeries;

const iStart = resampled ? 0 : renderPassData.indexRange.min;

const iEnd = resampled ? oldX.size() - 1 : renderPassData.indexRange?.max;

xValues.clear();

yValues.clear();

indexes.clear();

// This is the index of the threshold we are currently under.

let level = 0;

let lastY = oldY.get(iStart);

// Find the starting level

for (let t = 0; t < numThresholds; t++) {

if (lastY > this.thresholds.get(t)) {

level++;

}

}

let lastX = oldX.get(iStart);

xValues.push_back(lastX);

yValues.push_back(lastY);

indexes.push_back(0);

let newI = 0;

for (let i = iStart + 1; i <= iEnd; i++) {

const y = oldY.get(i);

const x = oldX.get(i);

if (level > 0 && lastY > this.thresholds.get(level - 1)) {

if (y === this.thresholds.get(level - 1)) {

// decrease level but don't add a point

level--;

}

while (y < this.thresholds.get(level - 1)) {

// go down

const t = this.thresholds.get(level - 1);

// interpolate to find intersection

const f = (lastY - t) / (lastY - y);

const xNew = lastX + (x - lastX) * f;

newI++;

xValues.push_back(xNew);

yValues.push_back(t);

// use original data index so metadata works

indexes.push_back(i);

level--;

if (level === 0) break;

}

}

if (level < numThresholds && lastY <= this.thresholds.get(level)) {

if (y === this.thresholds.get(level)) {

// increase level but don't add a point

level++;

}

while (y > this.thresholds.get(level)) {

// go up

const t = this.thresholds.get(level);

const f = (t - lastY) / (y - lastY);

const xNew = lastX + (x - lastX) * f;

newI++;

xValues.push_back(xNew);

yValues.push_back(t);

indexes.push_back(i);

level++;

if (level === numThresholds) break;

}

}

lastY = y;

lastX = x;

newI++;

xValues.push_back(lastX);

yValues.push_back(lastY);

indexes.push_back(newI);

}

return this.pointSeries;

}

}

Next we need a paletteProvider which applies colours according to the thresholds. The stroke color at a point applies to the previous line segment ending at that point, so we have to track the previous y value to see if the line was approaching the threshold from above or below. Thanks to the transform, we know every line segment will be completely within one of the threshold ranges.

- TYPEscript

`const colorNames = ["green", "blue", "yellow", "red"];`

const colors = colorNames.map(c => parseColorToUIntArgb(c));

class ThresholdPaletteProvider extends DefaultPaletteProvider {

strokePaletteMode = EStrokePaletteMode.SOLID;

lastY: number;

public thresholds: number[];

public get isRangeIndependant() {

return true;

}

public constructor(thresholds: number[]) {

super();

this.thresholds = thresholds;

}

overrideStrokeArgb(

xValue: number,

yValue: number,

index: number,

opacity: number,

metadata: IPointMetadata

): number {

if (index == 0) {

this.lastY = yValue;

}

for (let i = 0; i < this.thresholds.length; i++) {

const threshold = this.thresholds[i];

if (yValue <= threshold && this.lastY <= threshold) {

this.lastY = yValue;

return colors[i];

}

}

this.lastY = yValue;

return colors[this.thresholds.length];

}

}

Now we can create a series and apply these to it

- TYPEscript

`// Create a series`

const lineSeries = new FastLineRenderableSeries(wasmContext, {

pointMarker: new EllipsePointMarker(wasmContext, {

stroke: "black",

strokeThickness: 0,

fill: "black",

width: 10,

height: 10

}),

dataSeries: new XyDataSeries(wasmContext, {

xValues: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],

yValues: [0, 1, 2, 3, 6, 4, 1, 1, 7, 5, 4]

}),

dataLabels: {

style: {

fontSize: 10

},

color: "white"

},

strokeThickness: 5

});

sciChartSurface.renderableSeries.add(lineSeries);

// Set initial thresholds

const thresholds = [1.5, 3, 5];

// Create and set the transform

const transform = new ThresholdRenderDataTransform(lineSeries, wasmContext, thresholds);

lineSeries.renderDataTransform = transform;

// Create and set the paletteProvider

const paletteProvider = new ThresholdPaletteProvider(thresholds);

lineSeries.paletteProvider = paletteProvider;

This is the final result. You can view the source of the embed below to see how the annotations are created and configured to update the thresholds.