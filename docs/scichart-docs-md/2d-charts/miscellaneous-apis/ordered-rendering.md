---
source: https://www.scichart.com/documentation/js/v4/2d-charts/miscellaneous-apis/ordered-rendering
scraped_at: 2025-11-28T18:24:47.324604
---

# https://www.scichart.com/documentation/js/v4/2d-charts/miscellaneous-apis/ordered-rendering

# Ordered Rendering

The render order of an element on a 2D chart defines how it will be displayed while overlapping other chart elements. It is analogous to the definition of "z-index".

## Render Order of chart elements

Here we will describe some details on how series, annotations, labels, grid lines, sub-charts are handling render order. This topic may require familiarity with the following points:

- SciChart has different target canvases where the elements are rendered.
- SubCharts API allows putting multiple surfaces on a chart
- Native Text API vs
**Texture Text Rendering**

### Default behavior

The normal order of layering is

`background > grid lines and bands > series > annotations > text labels`

Thus, text labels usually are above other types of entities.

By default, elements of the same type are rendered in the insertion order.

The default layers are defined in EDefaultRenderLayer📘.

The order may differ depending on some configuration specifics.

#### Series Render Order

Series render order depends on the insertion order into renderableSeries📘 collection. While it also may change when series are hovered or selected (this feature can be enabled with SeriesSelectionModifier📘).

#### Annotations Render Order

Annotations expose annotationLayer📘 property, which allows them to be placed behind grid-lines/series or above them. (Refer to EAnnotationLayer📘)

Dom Annotations have limited support of the layering options due to their rendering specifics.

#### Native Text Render Order

Native Text rendering could be batched for performance optimization. However to make sure the text is rendered at the correct layer you may need to use immediate Native Text rendering. Some contexts where you can force the immediate rendering are:

- renderNativeAxisLabelsImmediately📘 for axis labels
- drawImmediate📘 on NativeTextAnnotation📘

Also, native text can be used in other contexts such as annotations, data labels, titles, etc...

#### SubCharts Render Order

Sub-charts conform to insertion order when rendering, and the main (parent) surface is processed first by default. This also means that the elements attached to the main surface are rendered before the entities on sub-charts.

#### Background rendering

A chart background📘 is rendered on a root `div`

element domChartRoot📘,
while a sub-chart background is rendered with WebGl on the Render Context Canvas.
Thus, a parent surface background is always rendered below everything else;
And a sub-chart can use only a plain color as a background.

Both parent surfaces and sub-charts support transparent backgrounds. Example of chart background styling📘 Example of isTransparent property on sub-charts📘

## Custom Order

SciChart allows changing the render order of some elements.

First of all, it is possible by setting the order of items within collections on a surface such as `renderableSeries`

, `annotations`

, `subCharts`

.
To do this dynamically, Use and `add`

and `remove`

methods on a collection.

Then, some elements (currently series and annotations) have methods for advanced control of the render order. The API is defined in IOrderedRenderable📘

### Ordered Renderables

SciChart allows setting a custom render order on instances that implement `IOrderedRenderable`

.

#### Absolute order

The order can be set as a value via the renderOrder📘 constructor option (or dynamically via setRenderOrder📘).

For example, in the following setup, we change the order of the first annotation so it is rendered on top of the second one, which is the opposite of the default behaviour.

`const textAnnotation1 = new NativeTextAnnotation({`

xCoordinateMode: ECoordinateMode.Pixel,

yCoordinateMode: ECoordinateMode.Pixel,

x1: 200,

y1: 200,

padding: Thickness.fromNumber(8),

isEditable: true,

fontSize: 32,

background: "blue",

text: "textAnnotation1",

renderOrder: 3

});

const textAnnotation2 = new NativeTextAnnotation({

xCoordinateMode: ECoordinateMode.Pixel,

yCoordinateMode: ECoordinateMode.Pixel,

x1: 220,

y1: 220,

padding: Thickness.fromNumber(8),

isEditable: true,

fontSize: 32,

background: "red",

text: "textAnnotation2"

});

sciChartSurface.annotations.add(textAnnotation1, textAnnotation2);

#### Relative Order

Alternatively, an order could be set as an offset from another Ordered Renderable instance.

In this example, we demonstrate how to place an annotation on a layer between renderable series via renderNextTo📘 option (or setRenderNextTo📘 method).

- TS
- JS

`const lineSeries1 = new SplineLineRenderableSeries(wasmContext, {`

dataSeries: dataSeries1,

stroke: "royalblue",

strokeThickness: 5

});

const lineSeries2 = new SplineLineRenderableSeries(wasmContext, {

dataSeries: dataSeries2,

stroke: "orangered",

strokeThickness: 5

});

sciChartSurface.renderableSeries.add(lineSeries1, lineSeries2);

const boxAnnotation = new BoxAnnotation({

renderNextTo: { renderable: lineSeries1.id, offset: 0 },

fill: "mediumseagreen",

xCoordinateMode: ECoordinateMode.DataValue,

yCoordinateMode: ECoordinateMode.Relative,

x1: 8,

y1: 0,

x2: 12,

y2: 1

});

sciChartSurface.annotations.add(boxAnnotation);

`const lineSeries1 = new SplineLineRenderableSeries(wasmContext, {`

dataSeries: dataSeries1,

stroke: "royalblue",

strokeThickness: 5

});

const lineSeries2 = new SplineLineRenderableSeries(wasmContext, {

dataSeries: dataSeries2,

stroke: "orangered",

strokeThickness: 5

});

sciChartSurface.renderableSeries.add(lineSeries1, lineSeries2);

const boxAnnotation = new BoxAnnotation({

renderNextTo: { renderable: lineSeries1.id, offset: 0 },

fill: "mediumseagreen",

xCoordinateMode: ECoordinateMode.DataValue,

yCoordinateMode: ECoordinateMode.Relative,

x1: 8,

y1: 0,

x2: 12,

y2: 1

});

sciChartSurface.annotations.add(boxAnnotation);

#### Customizing Render Layer

Setting a custom render layer allows to place an entity at a layer of different entity kinds, as well.

Here we will demonstrate how to place series at the background layer, so that grid lines are rendered above them. For that we can use renderLayer📘 or setRenderLayer📘

`const lineSeries1 = new SplineMountainRenderableSeries(wasmContext, {`

renderLayer: EDefaultRenderLayer.Background,

dataSeries: dataSeries1,

stroke: "royalblue",

strokeThickness: 5

});

sciChartSurface.renderableSeries.add(lineSeries1);

#### Surface Render Order

It is also possible to change the render order of an element to appear as if it was rendered on another sub-chart, or to change the render order of a whole sub-chart

Let's consider the following setup:

- TS
- JS

`const [subSurface1, subSurface2] = buildSubCharts(`

[

{

xAxes: {

type: EAxisType.NumericAxis,

options: { autoRange: EAutoRange.Once }

},

surface: {

position: { x: 100, y: 100, width: 200, height: 200 },

coordinateMode: ESubSurfacePositionCoordinateMode.Pixel,

isTransparent: true

},

series: [

{

type: ESeriesType.SplineMountainSeries,

xyData: {

xValues: Array.from({ length: 20 }, (_, i) => i),

yValues: [12, 9, 10, 6, 7, 11, 13, 8, 9, 10, 14, 7, 5, 9, 8, 13, 6, 10, 11, 12]

},

options: {

stroke: "FireBrick",

fill: "Tomato",

strokeThickness: 5

}

}

]

},

{

surface: {

position: { x: 150, y: 150, width: 200, height: 200 },

coordinateMode: ESubSurfacePositionCoordinateMode.Pixel,

isTransparent: true

},

series: [

{

type: ESeriesType.SplineMountainSeries,

xyData: {

xValues: Array.from({ length: 20 }, (_, i) => i),

yValues: [6, 8, 5, 9, 3, 10, 7, 6, 4, 12, 8, 9, 10, 5, 11, 7, 3, 8, 9, 6]

},

options: {

stroke: "Navy",

fill: "DodgerBlue",

strokeThickness: 5

}

}

]

}

],

sciChartSurface

) as SciChartSubSurface[];

`const [subSurface1, subSurface2] = buildSubCharts([`

{

xAxes: {

type: EAxisType.NumericAxis,

options: { autoRange: EAutoRange.Once }

},

surface: {

position: { x: 100, y: 100, width: 200, height: 200 },

coordinateMode: ESubSurfacePositionCoordinateMode.Pixel,

isTransparent: true

},

series: [

{

type: ESeriesType.SplineMountainSeries,

xyData: {

xValues: Array.from({ length: 20 }, (_, i) => i),

yValues: [12, 9, 10, 6, 7, 11, 13, 8, 9, 10, 14, 7, 5, 9, 8, 13, 6, 10, 11, 12]

},

options: {

stroke: "FireBrick",

fill: "Tomato",

strokeThickness: 5

}

}

]

},

{

surface: {

position: { x: 150, y: 150, width: 200, height: 200 },

coordinateMode: ESubSurfacePositionCoordinateMode.Pixel,

isTransparent: true

},

series: [

{

type: ESeriesType.SplineMountainSeries,

xyData: {

xValues: Array.from({ length: 20 }, (_, i) => i),

yValues: [6, 8, 5, 9, 3, 10, 7, 6, 4, 12, 8, 9, 10, 5, 11, 7, 3, 8, 9, 6]

},

options: {

stroke: "Navy",

fill: "DodgerBlue",

strokeThickness: 5

}

}

]

}

], sciChartSurface);

Then, to reorder the sub-charts, we can apply the setSurfaceRenderOrder📘 method on a surface:

`subSurface1.setSurfaceRenderOrder(3);`

Result:

Or to modify the render order only of the series from the first chart we can apply the setSurfaceRenderOrder📘 method on them:

- TS
- JS

`const firstSubSurface = sciChartSurface.subCharts[0] as SciChartSubSurface;`

const firstSeries = firstSubSurface.renderableSeries.get(0) as SplineMountainRenderableSeries;

firstSeries.setSurfaceRenderOrder(3);

`const firstSubSurface = sciChartSurface.subCharts[0];`

const firstSeries = firstSubSurface.renderableSeries.get(0);

firstSeries.setSurfaceRenderOrder(3);

Result: