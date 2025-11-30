---
source: https://www.scichart.com/documentation/js/v4/2d-charts/annotations-api/annotations-api-overview
scraped_at: 2025-11-28T18:23:59.865977
---

# https://www.scichart.com/documentation/js/v4/2d-charts/annotations-api/annotations-api-overview

# Annotations API Overview

SciChart.js features a rich Annotations API, that allows you to place annotations (boxes, markers, text labels and custom shapes) over a chart:

Annotations can provide **interactive** event/news bullets, horizontal/vertical lines (thresholds), text/callouts as well as measurements such as Peak-to-peak or cycle duration. Annotations can be edited by click & drag, added by touching a screen, or, simply created programmatically. SciChart provides a number of built-in annotations, but you can also create your own.

## Annotation Types

The following annotation types are available out of the box in SciChart:

| Type | Description | Supported Chart Types |
|---|---|---|
| BoxAnnotation | Draws a rectangle at specific X1, X2, Y1, Y2 coordinates. | Cartesian |
| LineAnnotation | Draws a line between X1, Y1 and X2, Y2 positions. | Cartesian and Polar |
| TextAnnotation | Allows to place a piece of text at a specific location on a chart. | Cartesian and Polar |
| CustomAnnotation | Allows to place any SVG Content at a specific location on a chart. | Cartesian and Polar |
| VerticalLineAnnotation | Draws a vertical line at a given x position, with various labelling options | Cartesian |
| HorizontalLineAnnotation | Draws a horizontal line at a given y position, with various labelling options | Cartesian |
| LineArrowAnnotation | Allows to place line arrows at a specific location on a chart | Cartesian and Polar |
| AxisMarkerAnnotation | Allows to place a marker at a specific location on an axis | Cartesian |
| CustomAxisMarkerAnnotation | Uses an image instead of text for an axis marker | Cartesian |
| NativeTextAnnotation | Draws text natively rather than using svg, supporting rotation, multiline, wordwrap and scaling | Cartesian and Polar |
| HtmlCustomAnnotation | Allows to render arbitrary HTML content within a chart | Cartesian |
| HtmlTextAnnotation | Allows to place HTML text at a specific location on a chart | Cartesian |
| ArcAnnotation | Allows to place arc element at a specific location on a cartesian chart. | Cartesian |
| PolarArcAnnotation | Allows to place arc element at a specific location on a polar chart. | Polar |
| PolarPointerAnnotation | Allows to place a pointer on a polar chart. Is used for gauge charts | Polar |

Annotations have surfaceTypes📘 property, which defines list of compatible surface types. ESurfaceType.SciChartSurfaceType📘 stands for regular (Cartesian) chart and ESurfaceType.SciChartPolarSurfaceType📘 stands for Polar chart.

If an annotation is only compatible with Polar surfaces it has prefix "Polar" in the name. For example, PolarArcAnnotation works only with Polar surfaces. Annotations without the "Polar" prefix can be compatible with both surface types or only with Cartesian surfaces. For example, LineAnnotation is compatible with both surface types and BoxAnnotation is compatible only with Cartesian.

To learn more about any annotation type, please refer to the corresponding article.

## Adding an Annotation to a Chart

The SciChartSurface📘 stores all its annotations in the SciChartSurface.annotations📘 collection. The following code can be used to add an annotation to a chart:

- TS
- Builder API (JSON Config)

`const {`

BoxAnnotation,

TextAnnotation,

LineAnnotation,

NumericAxis,

SciChartSurface,

NumberRange,

EHorizontalAnchorPoint,

EVerticalAnchorPoint,

ECoordinateMode,

SciChartJsNavyTheme

} = SciChart;

// or for npm import { SciChartSurface, ... } from "scichart"

async function addAnnotationToChart(divElementId) {

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

// Add a selection of annotations to the chart

sciChartSurface.annotations.add(

new LineAnnotation({

stroke: "#FF6600",

strokeThickness: 3,

x1: 2.0,

x2: 8.0,

y1: 3.0,

y2: 7.0

}),

new BoxAnnotation({

stroke: "#FF3333",

strokeThickness: 1,

fill: "rgba(255,50,50,0.3)",

x1: 2.0,

x2: 8.0,

y1: 3.0,

y2: 7.0

}),

new BoxAnnotation({

stroke: "#33FF33",

strokeThickness: 1,

fill: "rgba(50, 255, 50, 0.3)",

x1: 3.0,

x2: 9.0,

y1: 4.0,

y2: 8.0

}),

new TextAnnotation({

x1: 100,

y1: 0.5,

xCoordinateMode: ECoordinateMode.Pixel,

yCoordinateMode: ECoordinateMode.Relative,

horizontalAnchorPoint: EHorizontalAnchorPoint.Left,

verticalAnchorPoint: EVerticalAnchorPoint.Center,

textColor: "yellow",

fontSize: 26,

fontFamily: "Default",

text: "TEXT ANNOTATION"

})

);

}

addAnnotationToChart("scichart-root");

`const { chartBuilder, EAnnotationType, ECoordinateMode, EVerticalAnchorPoint, EHorizontalAnchorPoint } = SciChart;`

// or for npm import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

annotations: [

{

type: EAnnotationType.RenderContextBoxAnnotation,

options: {

stroke: "#FF3333",

strokeThickness: 1,

fill: "rgba(255,50,50,0.3)",

x1: 2.0,

x2: 8.0,

y1: 3.0,

y2: 7.0

}

},

{

type: EAnnotationType.RenderContextBoxAnnotation,

options: {

stroke: "#33FF33",

strokeThickness: 1,

fill: "rgba(50,255,50,0.3)",

x1: 3.0,

x2: 9.0,

y1: 4.0,

y2: 8.0

}

},

{

type: EAnnotationType.SVGTextAnnotation,

options: {

x1: 100,

y1: 0.5,

xCoordinateMode: ECoordinateMode.Pixel,

yCoordinateMode: ECoordinateMode.Relative,

horizontalAnchorPoint: EHorizontalAnchorPoint.Left,

verticalAnchorPoint: EVerticalAnchorPoint.Center,

textColor: "yellow",

fontSize: 26,

fontFamily: "Times New Roman",

text: "TEXT ANNOTATION"

}

}

]

});

This results in the following output:

Individual Annotation features are discussed in greater detail in the following pages:

- The BoxAnnotation Type
- The LineAnnotation Type
- The TextAnnotation Type
- The CustomAnnotation Type

## Common Annotation Properties

All annotations in SciChart.js are derived from the AnnotationBase📘 **type. Individual Annotations have additional properties however the following common properties of the AnnotationBase📘 class listed below can be used to control all annotation types.**

| Property | Description |
|---|---|
annotationLayer📘 | Determines which canvas the annotation should be placed on. The default is EAnnotationLayer.AboveChart📘, where annotations are displayed above the chart series. Setting this property to EAnnotationLayer.BelowChart📘 places an annotation below series but above gridlines, axis bands and axis labels. Note that this method doesn't work with SVG based annotations such as TextAnnotation📘 and CustomAnnotation📘. Setting the property to EAnnotationLayer.Background📘 places an annotation below all elements on the chart (series, axis bands, gridlines, axis labels). This method works with all annotation types including SVG, and is useful for placing watermarks on the chart. |
xCoordinateMode📘, yCoordinateMode📘 | Determines how coordinates x1,y2,x2,y2 are used when placing the annotation. The default is ECoordinateMode.DataValue📘 where coordinates correspond to Data-values. ECoordinateMode.Relative📘 means coordinates are relative to the viewport. ECoordinateMode.Pixel📘 means coordinates are pixel values relative to the top-left of the viewport. |
horizontalAnchorPoint📘, verticalAnchorPoint📘 | Used to adjust the alignment of certain annotations. Above: HorizontalAnchorPoint, VerticalAnchorPoint when applied to a TextAnnotation |
isHidden📘 | Can be set to show or hide an annotation. |
hovered📘, isHovered📘, selectedChanged📘, isSelected📘 | Annotations can be made interactive with selection and hover callbacks. See Annotation Hover for details. |
resizeDirections📘 | Allows you to specify which direction (X, Y, Xy) an annotation may be resized in. |
dragStarted📘, dragDelta📘, dragEnded📘 | Callbacks may be registered when an annotation is dragged by the user. |
x1📘, x2📘, y1📘, y2📘 | Define the position of the annotation on the parent chart. Note that annotation position is also defined by the xCoordinateMode, yCoordinateMode properties. |
xAxisId📘, yAxisId📘 | In a multiple-axis scenario, used to bind the annotation to a specific X or Y-Axis. NOTE: If the value is not supplied it will use the first axis. |
isEditable📘 | If true, this annotation can be selected and dragged/resized. See Editable Annotations for more details. |
clicked📘 / onClick📘 | Event fired when the annotation is clicked. Works for both editable and non-editable annotations. The event arguments contain a point which gives the coordinates of where on the annotation it was clicked, relative to the top left corner. NOTE: If an editable annotation is already selected, clicking on it will fire dragStarted, but not clicked. |

More annotation properties and the inheritence hierachy may be viewed at the AnnotationBase Typedoc page📘.