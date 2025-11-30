---
source: https://www.scichart.com/documentation/js/v4/2d-charts/annotations-api/vertical-line-annotation
scraped_at: 2025-11-28T18:24:04.321330
---

# https://www.scichart.com/documentation/js/v4/2d-charts/annotations-api/vertical-line-annotation

# VerticalLineAnnotation

The VerticalLineAnnotation📘 allows to draw a **vertical line** between Y1, Y2 coordinates at X1.

## Declaring a VerticalLineAnnotation in code

The following code will declare a VerticalLineAnnotation📘 and add it to the chart.

- TS
- Builder API (JSON Config)

`const { VerticalLineAnnotation, NumericAxis, SciChartSurface, ELabelPlacement, SciChartJsNavyTheme } = SciChart;`

// or for npm import { SciChartSurface, ... } from "scichart"

async function addAnnotationToChart(divElementId) {

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

// Add a selection of annotations to the chart

sciChartSurface.annotations.add(

// Vertically line stretched across the viewport, showing label value = X (9)

new VerticalLineAnnotation({

labelPlacement: ELabelPlacement.Axis,

showLabel: true,

stroke: "#FF6600",

strokeThickness: 2,

x1: 9,

axisLabelFill: "#FF6600",

axisLabelStroke: "#333",

axisFontSize: 20

}),

// Vertically line with a custom label value

new VerticalLineAnnotation({

labelPlacement: ELabelPlacement.Axis,

showLabel: true,

stroke: "#3388FF",

strokeThickness: 2,

strokeDashArray: [5, 5],

x1: 4,

axisLabelFill: "#3388FF",

labelValue: "Custom Label",

axisLabelStroke: "White",

axisFontSize: 20

})

);

}

addAnnotationToChart("scichart-root");

`const { chartBuilder, EAnnotationType } = SciChart;`

// or for npm import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

annotations: [

{

type: EAnnotationType.RenderContextVerticalLineAnnotation,

options: {

labelPlacement: ELabelPlacement.Axis,

showLabel: true,

stroke: "#FF6600",

strokeThickness: 2,

x1: 9,

axisLabelFill: "#FF6600",

axisLabelStroke: "#333",

axisFontSize: 20

}

},

{

type: EAnnotationType.RenderContextVerticalLineAnnotation,

options: {

labelPlacement: ELabelPlacement.Axis,

showLabel: true,

stroke: "#3388FF",

strokeThickness: 2,

strokeDashArray: [5, 5],

x1: 4,

axisLabelFill: "#3388FF",

labelValue: "Custom Label",

axisLabelStroke: "White",

axisFontSize: 20

}

}

]

});

This results in the following output:

## Changing Label Position or Label Value

The label may be placed on the line, or on the axis. Placemement of the label is controlled by the VerticalLineAnnotation.labelPlacement📘 property, which expects an ELabelPlacement📘 enum.

Valid settings are `Axis`

, `Bottom`

, `BottomLeft`

, `BottomRight`

, `Top`

, `TopLeft`

, `TopRight`

, `Left`

and `Right`

.

For example, setting **labelPlacement** to `ELabelPlacement.TopRight`

:

- TS
- Builder API (JSON Config)

`// Add a selection of annotations to the chart`

sciChartSurface.annotations.add(

// Vertically line stretched across the viewport, showing label value = X (9)

new VerticalLineAnnotation({

labelPlacement: ELabelPlacement.TopRight,

showLabel: true,

stroke: "#FF6600",

strokeThickness: 2,

x1: 9,

axisLabelFill: "#FF6600",

axisLabelStroke: "#333",

axisFontSize: 20

}),

// Vertically line with a custom label value

new VerticalLineAnnotation({

labelPlacement: ELabelPlacement.TopLeft,

showLabel: true,

stroke: "#3388FF",

strokeThickness: 2,

strokeDashArray: [5, 5],

x1: 4,

axisLabelFill: "#3388FF",

labelValue: "Custom Label",

axisLabelStroke: "White",

axisFontSize: 20

})

);

`const { chartBuilder, EAnnotationType } = SciChart;`

// or for npm import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

annotations: [

{

type: EAnnotationType.RenderContextVerticalLineAnnotation,

options: {

labelPlacement: ELabelPlacement.TopRight,

showLabel: true,

stroke: "#FF6600",

strokeThickness: 2,

x1: 9,

axisLabelFill: "#FF6600",

axisLabelStroke: "#333",

axisFontSize: 20

}

},

{

type: EAnnotationType.RenderContextVerticalLineAnnotation,

options: {

labelPlacement: ELabelPlacement.TopLeft,

showLabel: true,

stroke: "#3388FF",

strokeThickness: 2,

strokeDashArray: [5, 5],

x1: 4,

axisLabelFill: "#3388FF",

labelValue: "Custom Label",

axisLabelStroke: "White",

axisFontSize: 20

}

}

]

});

Results in the label being placed on the top right of the line.

Labels on VerticalLineAnnotations may be placed on the `Axis`

, or at `Bottom`

, `BottomLeft`

, `BottomRight`

, `Top`

, `TopLeft`

, `TopRight`

, `Left`

or `Right`

of the line.

## VerticalAlignment Stretch and Partially Drawn Lines

VerticalLineAnnotations📘 may be drawn to stretch vertically across the viewport, or to a specific Y-value. To truncate a VerticalLineAnnotation simply specify a y1 coordinate.

For example, the two options are shown below in code:

- TS
- Builder API (JSON Config)

`const { VerticalLineAnnotation, NumericAxis, SciChartSurface, ELabelPlacement, SciChartJsNavyTheme } = SciChart;`

// or for npm import { SciChartSurface, ... } from "scichart"

async function addAnnotationToChart(divElementId) {

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

// Add a selection of annotations to the chart

sciChartSurface.annotations.add(

// Vertically line stretched across the viewport, showing label value = X (9)

new VerticalLineAnnotation({

labelPlacement: ELabelPlacement.Axis,

showLabel: true,

stroke: "SteelBlue",

strokeThickness: 2,

x1: 9,

axisLabelFill: "SteelBlue",

axisFontSize: 20

}),

// Vertically line with a custom label value

new VerticalLineAnnotation({

showLabel: true,

stroke: "Orange",

strokeThickness: 2,

x1: 6,

y1: 4, // only draw up to Y=4

axisLabelFill: "Orange",

axisFontSize: 20

})

);

}

addAnnotationToChart("scichart-root");

`const { chartBuilder, EAnnotationType } = SciChart;`

// or for npm import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

annotations: [

{

type: EAnnotationType.RenderContextVerticalLineAnnotation,

options: {

labelPlacement: ELabelPlacement.Axis,

showLabel: true,

stroke: "SteelBlue",

strokeThickness: 2,

x1: 9,

axisLabelFill: "SteelBlue",

axisFontSize: 20

}

},

{

type: EAnnotationType.RenderContextVerticalLineAnnotation,

options: {

showLabel: true,

stroke: "Orange",

strokeThickness: 2,

x1: 6,

y1: 4, // only draw up to Y=4

axisLabelFill: "Orange",

axisFontSize: 20

}

}

]

});

Result in this output:

## Styling the VerticalLineAnnotation

The following properties can be set to style the VerticalLineAnnotation�📘:

Property | Description |
|---|---|
| labelPlacement📘 | An enumeration defining where the vertical line label is placed. Default is on axis. |
| labelValue📘 | The label value. By default this will equal the x1 value with text formatting applied by the axis. However it can be overridden to any string |
| showLabel📘 | When true, a label is shown |
| stroke📘 | The stroke color of the vertical line |
| strokeDashArray📘 | Gets or sets the strokeDashArray for the LineAnnotation |
| strokeThickness📘 | The stroke thickness of the vertical line |
| axisLabelFill📘 | The box fill color for the axis label |
| axisLabelStroke📘 | The text-color for the axis label |
| axisFontFamily📘 | The font family for the axis label text |
| axisFontSize📘 | The font size for the axis label text |