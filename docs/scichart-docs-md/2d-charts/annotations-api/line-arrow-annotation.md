---
source: https://www.scichart.com/documentation/js/v4/2d-charts/annotations-api/line-arrow-annotation
scraped_at: 2025-11-28T18:24:02.829271
---

# https://www.scichart.com/documentation/js/v4/2d-charts/annotations-api/line-arrow-annotation

# LineArrowAnnotation

The LineArrowAnnotation📘 class extends LineAnnotation📘 and adds an optional arrowhead at each line endpoint. Use it to annotate charts with directional indicators.

## Create a Line Arrow Annotation

The following code will declare 2 LineArrowAnnotation📘s and add them to the chart.

- TS
- Builder API (JSON Config)

`const {`

SciChartSurface,

SciChartJsNavyTheme,

LineArrowAnnotation,

NumericAxis,

EArrowHeadPosition,

EDraggingGripPoint,

} = SciChart;

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme(),

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

const arrow1 = new LineArrowAnnotation({

x1: 1,

x2: 6,

y1: 2,

y2: 9,

isArrowHeadScalable: true, // the arrow head will scale with the visibleRange

arrowStyle: {

headLength: 40,

headWidth: 45,

headDepth: 0.8,

fill: "#113388",

stroke: "#3399FF",

strokeThickness: 3

},

stroke: "#3399FF",

strokeThickness: 3,

isEditable: true,

isSelected: true,

arrowHeadPosition: EArrowHeadPosition.End, // only show arrow head at the end

dragPoints: [ EDraggingGripPoint.x2y2 ], // only allow dragging by the end point

});

const arrow2 = new LineArrowAnnotation({

x1: 4,

x2: 9,

y1: 2,

y2: 9,

isArrowHeadScalable: false,

arrowStyle: {

headLength: 25,

headWidth: 25,

headDepth: 1,

fill: "#883300",

stroke: "#FF6600",

strokeThickness: 3

},

stroke: "#FF6600",

strokeThickness: 3,

arrowHeadPosition: EArrowHeadPosition.StartEnd, // show arrow heads on both ends

isEditable: true,

dragPoints: [

EDraggingGripPoint.x1y1,

EDraggingGripPoint.x2y2

], // allow dragging by both end points

});

// append the annotations to the surface

sciChartSurface.annotations.add(arrow1, arrow2);

`const { `

chartBuilder,

EAnnotationType,

EArrowHeadPosition,

EDraggingGripPoint,

} = SciChart;

// or for npm import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: {

theme: { type: "Navy" },

},

annotations: [

{

type: EAnnotationType.RenderContextLineArrowAnnotation,

options: {

stroke: "#3399FF",

strokeThickness: 3,

x1: 1,

y1: 2, // start point (1, 2)

x2: 6,

y2: 9, // end point (6, 9)

arrowHeadPosition: EArrowHeadPosition.End, // show arrow head at the end

isArrowHeadScalable: true, // the arrow head will scale with the visibleRange

isEditable: true,

dragPoints: [ EDraggingGripPoint.x2y2 ], // allow drag editing by the end point

arrowStyle: {

headLength: 40,

headWidth: 45,

headDepth: 0.8,

fill: "#113388",

stroke: "#3399FF",

strokeThickness: 3

}

}

},

{

type: EAnnotationType.RenderContextLineArrowAnnotation,

options: {

stroke: "#FF6600",

strokeThickness: 3,

x1: 4,

y1: 1, // start point (4, 1)

x2: 9,

y2: 8, // end point (9, 8)

arrowHeadPosition: EArrowHeadPosition.StartEnd, // show arrow heads on both ends

isArrowHeadScalable: false,

isEditable: true,

dragPoints: [

EDraggingGripPoint.x1y1,

EDraggingGripPoint.x2y2

], // allow drag editing by both end points

arrowStyle: {

headLength: 40,

headWidth: 45,

headDepth: 0.8,

fill: "#883300",

stroke: "#FF6600",

strokeThickness: 3

}

}

},

],

});

Resulting in the following output:

In the code above:

- We create 2 instances of LineArrowAnnotation📘 with different arrowhead styles.
- The first annotation has an arrowhead at the end, while the second has 2 arrowheads, 1 at both ends.
- Also, the first annotation's arrowhead will scale with the zooming, while the second will not.
- In case you want to use editable annotations using isEditable📘:
`true`

, you can use the dragPoints📘 property to pass an array of valid drag points. See EDraggingGripPoint📘 for more details.

### Unique Properties

| Property | Type | Default | Description |
|---|---|---|---|
| arrowHeadPosition | EArrowHeadPosition📘 | End | Where to place the arrowhead(s) -> Start, End, Start&End |
| isArrowHeadScalable | boolean | false | Whether to scale the arrowhead size with zooming. |
| arrowStyle | IArrowStyle📘 | - | Arrowhead style options. |
| onArrowHeadSizeChanged | TArrowheadSizeChangedCallback📘 | undefined | Callback to modify arrowhead size based on angle. |

All other properties are inherited from LineAnnotation📘 & AnnotationBase📘 and work as expected.

tip

Use `headDepth: 0`

for simple line arrows without filled heads.

tip

Set `isArrowHeadScalable: true`

for annotations that maintain relative size during zooming.