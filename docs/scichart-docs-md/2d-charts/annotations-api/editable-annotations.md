---
source: https://www.scichart.com/documentation/js/v4/2d-charts/annotations-api/editable-annotations
scraped_at: 2025-11-28T18:24:01.154443
---

# https://www.scichart.com/documentation/js/v4/2d-charts/annotations-api/editable-annotations

# Editable Annotations

The annotations API allows you to mark any annotation as editable by setting isEditable true. Editable annotations can be selected and dragged, and some can be resized. This page describes how you can respond to a user's interaction with an annotation, and how to **customise the style of the selected view** of the annotation.

## Annotation Interactions

All annotations have the following properties and events which can be used to run code on user interaction:

AnnotationBase Property | Description |
|---|---|
| isEditable📘 | When true, an annotation is editable. It may be selected, dragged or resized. Individual behaviours can be controlled by the following properties. |
| isSelected📘 | Set true when an editable annotation is clicked. This causes the selection box and the drag points to be shown. These are known as the adorners. Setting this programatically is not advised |
| selectedChanged📘 | An event that is fired when isSelected changes. |
| dragStarted📘 / onDragStarted📘 | dragStarted is an event which fires on mouseDown of an editable annotation. This is fired by the call to onDragStarted which is overridden in various annotations to determine which dragging point is being used, setting the adornerDraggingPoint📘 property. If this is not set, dragging will not be performed. You can pass a callback for the event via the onDragStarted📘 property of the IAnnotationsBase options object when constructing. |
| dragDelta📘 / onDragAdorner📘 | dragDelta is the event which fires during dragging. This is fired by the call to onDragAdorner which translates the mouse point to xy coordinates and calls calcDragDistance📘, which is where the coordinates of the annotation are updated. You can pass a callback for the event via the onDrag📘 property of the IAnnotationsBase options object when constructing. |
| dragEnded📘 / onDragEnded📘 | dragEnded is an event which fires on mouseUp when dragging has finished. This is fired by the call to onDragEnded. You can pass a callback for the event via the onDragEnded📘 property of the IAnnotationsBase options object when constructing. |
| resizeDirections📘 | Controls which direction an annotation may be resized in, e.g. X, Y or Xy |

## Enabling and Subscribing to Drag Events in Annotations

Below is an example of how to enable editing (dragging) on a TextAnnotation📘, as well as how to get a callback on when the annotation is updated.

- TS

`// A TextAnnotation which can be dragged and updates its value on drag`

const textAnnotation = new TextAnnotation({

x1: 1,

y1: 3,

fontSize: 24,

fontFamily: "Default",

text: "{{ DRAG ME! }}",

isEditable: true

});

textAnnotation.dragDelta.subscribe(args => {

textAnnotation.text = `I was dragged to ${textAnnotation.x1.toFixed(2)}, ${textAnnotation.y1.toFixed(2)}`;

});

sciChartSurface.annotations.add(textAnnotation);

Try it out below by dragging the annotation.

## Dragging to discrete values

Sometimes you want an annotation to snap to particular values as you drag. The way to do this is to override onDragAdorner📘 and convert to discete points there, then pass these to calcDragDistance📘. Here is an example of an AxisMarkerAnnotation📘 that can only take discrete values, from our Rich Interactions Demo.

- TS

`class DiscreteAxisMarker extends AxisMarkerAnnotation {`

stepSize = 1;

minValue = 0;

maxValue = 10;

constructor(options) {

super(options);

}

onDragAdorner(args) {

super.onDragAdorner(args);

const xyValues = this.getValuesFromCoordinates(args.mousePoint, true);

if (xyValues) {

let { x, y } = xyValues;

if (this.x1 !== undefined) {

x = Math.floor(x / this.stepSize) * this.stepSize;

} else if (this.y1 !== undefined) {

y = Math.floor(y / this.stepSize) * this.stepSize;

}

this.calcDragDistance(new Point(x, y));

if (this.x1 !== undefined) {

this.x1 = Math.min(Math.max(this.x1, this.minValue), this.maxValue);

} else if (this.y1 !== undefined) {

this.y1 = Math.min(Math.max(this.y1, this.minValue), this.maxValue);

}

}

this.dragDelta.raiseEvent(new AnnotationDragDeltaEventArgs());

}

}

// Now add to the SciChartSurface:

// sciChartSurface.annotations.add(new DiscreteAxisMarker({ y1: 5, formattedValue: "Drag Me!" }));

Try it out below by dragging the axis marker:

## Limiting Resize to Specific Directions (x,y)

Another property of interactable annotation is the dimension where it can be moved or resized. By default it is possible to move a BoxAnnotation📘 towards each side of the chart. In the next example we will demonstrate a usage of the AnnotationBase.resizeDirections📘 property. We will limit the annotation to resize and move only along the X Axis.

It is also possible to restrict the drag direction of the box annotation by subscribing to the dragDelta📘 event callback. Find an example below.

- TS
- Builder API (JSON Config)

`// A box annotation which can only be dragged in the X-direction`

const boxAnnotation = new BoxAnnotation({

x1: 3,

x2: 7,

y1: 3,

y2: 7,

isEditable: true,

isSelected: true,

// Restricts resize direction in the X-direction only

resizeDirections: EXyDirection.XDirection

});

// Restricts drag direction in the X-direction only

boxAnnotation.dragDelta.subscribe(arg => {

boxAnnotation.y1 = 3;

boxAnnotation.y2 = 7;

});

sciChartSurface.annotations.add(boxAnnotation);

`const { chartBuilder, EAnnotationType } = SciChart;`

// or for npm import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

annotations: [

{

type: EAnnotationType.RenderContextBoxAnnotation,

options: {

x1: 3,

x2: 7,

y1: 3,

y2: 7,

isEditable: true,

isSelected: true,

// custom resize direction

resizeDirections: EXyDirection.XDirection

}

}

]

});