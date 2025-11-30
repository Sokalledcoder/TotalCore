---
source: https://www.scichart.com/documentation/js/v4/2d-charts/annotations-api/text-annotation
scraped_at: 2025-11-28T18:24:03.765735
---

# https://www.scichart.com/documentation/js/v4/2d-charts/annotations-api/text-annotation

# TextAnnotation

The TextAnnotation📘 type draws a text label at the x1,y1 location where coordinates are data-values. The TextAnnotation supports text📘, fontSize📘, fontWeight📘, fontFamily📘 and textColor📘 properties.

Coordinates may be relative, absolute or data-value based, to both xCoordinateMode📘, yCoordinateMode📘 properties as values of ECoordinateMode📘 enum.

## Declaring a TextAnnotation in code

The following code will declare a number of TextAnnotations📘 and add them to the chart.

- TS
- Builder API (JSON Config)

`const {`

TextAnnotation,

NumericAxis,

SciChartSurface,

EHorizontalAnchorPoint,

EVerticalAnchorPoint,

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

// Add TextAnnotations in the top left of the chart

new TextAnnotation({

text: "Annotations are Easy!",

fontSize: 24,

x1: 0.3,

y1: 9.7

}),

new TextAnnotation({

text: "You can create text",

fontSize: 18,

x1: 1,

y1: 9

}),

// Add TextAnnotations with anchor points

new TextAnnotation({

text: "Anchor Center (X1, Y1)",

horizontalAnchorPoint: EHorizontalAnchorPoint.Center,

verticalAnchorPoint: EVerticalAnchorPoint.Bottom,

x1: 2,

y1: 8

}),

new TextAnnotation({

text: "Anchor Right",

horizontalAnchorPoint: EHorizontalAnchorPoint.Right,

verticalAnchorPoint: EVerticalAnchorPoint.Top,

x1: 2,

y1: 8

}),

new TextAnnotation({

text: "or Anchor Left",

horizontalAnchorPoint: EHorizontalAnchorPoint.Left,

verticalAnchorPoint: EVerticalAnchorPoint.Top,

x1: 2,

y1: 8

})

);

}

addAnnotationToChart("scichart-root");

`const { chartBuilder, EAnnotationType } = SciChart;`

// or for npm import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

annotations: [

{

type: EAnnotationType.SVGTextAnnotation,

options: {

text: "Annotations are Easy!",

fontSize: 24,

x1: 0.3,

y1: 9.7

}

},

{

type: EAnnotationType.SVGTextAnnotation,

options: {

text: "You can create text",

fontSize: 18,

x1: 1,

y1: 9

}

},

{

type: EAnnotationType.SVGTextAnnotation,

options: {

text: "Anchor Center (X1, Y1)",

horizontalAnchorPoint: EHorizontalAnchorPoint.Center,

verticalAnchorPoint: EVerticalAnchorPoint.Bottom,

x1: 2,

y1: 8

}

},

{

type: EAnnotationType.SVGTextAnnotation,

options: {

text: "Anchor Right",

horizontalAnchorPoint: EHorizontalAnchorPoint.Right,

verticalAnchorPoint: EVerticalAnchorPoint.Top,

x1: 2,

y1: 8

}

},

{

type: EAnnotationType.SVGTextAnnotation,

options: {

text: "or Anchor Left",

horizontalAnchorPoint: EHorizontalAnchorPoint.Left,

verticalAnchorPoint: EVerticalAnchorPoint.Top,

x1: 2,

y1: 8

}

}

]

});

This results in the following output:

## Positioning a TextAnnotation with horizontal/vertical Anchor Points

A TextAnnotation📘 only requires coordinates x1,y1 to be set. The alignment of the text around this coordinate is controlled by the horizontalAnchorPoint📘, verticalAnchorPoint📘 properties.

Above: Set the horizontalAnchorPoint📘, and verticalAnchorPoint📘 property to determine which anchor point (horizontal: **left**, **center**, **right** or **vertical**: **top**, **center**, **bottom**) the x1, y1 coordinate is bound to.

## Aligning a LineAnnotation with x/yCoordinateModes

Like other annotation types, the TextAnnotation📘 can be positioned relatively or absolute using xCoordinateMode📘, yCoordinateMode📘 properties.

For example, to create a watermark in the centre of the chart, use this code:

- TS
- Builder API (JSON Config)

`// Add a TextAnnotation using CoordinateMode Relative and Horizontal/Vertical Anchor Point`

// to create a watermark in a fixed position in the middle of the chart

sciChartSurface.annotations.add(

// Watermark with CoordinateMode Relative

new TextAnnotation({

text: "Create a Watermark",

horizontalAnchorPoint: EHorizontalAnchorPoint.Center,

verticalAnchorPoint: EVerticalAnchorPoint.Center,

x1: 0.5,

y1: 0.5,

fontSize: 56,

fontWeight: "Bold",

textColor: "#FFFFFF22",

xCoordinateMode: ECoordinateMode.Relative,

yCoordinateMode: ECoordinateMode.Relative,

annotationLayer: EAnnotationLayer.BelowChart

})

);

`const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {`

annotations: [

{

type: EAnnotationType.SVGTextAnnotation,

options: {

text: "Create a Watermark",

horizontalAnchorPoint: EHorizontalAnchorPoint.Center,

verticalAnchorPoint: EVerticalAnchorPoint.Center,

x1: 0.5,

y1: 0.5,

fontSize: 56,

fontWeight: "Bold",

textColor: "#FFFFFF22",

xCoordinateMode: ECoordinateMode.Relative,

yCoordinateMode: ECoordinateMode.Relative,

annotationLayer: EAnnotationLayer.BelowChart

}

}

]

});

This results in the following output:

## Polar Charts with TextAnnotation

To add a TextAnnotation📘 to a Polar chart, use the same exact code, just change the surface and axes types. The TextAnnotation will be positioned in polar coordinates.

- TS
- Builder API (JSON Config)

`const {`

LineAnnotation,

TextAnnotation,

PolarNumericAxis,

SciChartPolarSurface,

SciChartJsNavyTheme,

EPolarAxisMode,

EHorizontalAnchorPoint,

EVerticalAnchorPoint,

ECoordinateMode,

EAnnotationLayer

} = SciChart;

// or for npm import { SciChartPolarSurface, ... } from "scichart"

async function addAnnotationToChart(divElementId) {

const { wasmContext, sciChartSurface } = await SciChartPolarSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

const angularAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Angular,

});

sciChartSurface.xAxes.add(angularAxis);

const radialAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Radial,

});

sciChartSurface.yAxes.add(radialAxis);

sciChartSurface.annotations.add(

new TextAnnotation({

text: "Polar Text Annotations",

horizontalAnchorPoint: EHorizontalAnchorPoint.Center,

verticalAnchorPoint: EVerticalAnchorPoint.Center,

x1: 2.5, // at 12 o'clock (if range is 0 ot 10, since startAngle is at 9 o'clock)

y1: 2,

fontSize: 56,

fontWeight: "Bold",

textColor: "#FFFFFF22",

xCoordinateMode: ECoordinateMode.DataValue,

yCoordinateMode: ECoordinateMode.DataValue,

annotationLayer: EAnnotationLayer.BelowChart

})

);

}

addAnnotationToChart("scichart-root");

`const { `

chartBuilder,

EAnnotationType,

EHorizontalAnchorPoint,

EVerticalAnchorPoint,

ECoordinateMode,

EAnnotationLayer

} = SciChart;

// or for npm import { chartBuilder , ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DPolarChart(divElementId, {

annotations: [

{

type: EAnnotationType.SVGTextAnnotation,

options: {

text: "Polar Text Annotations",

horizontalAnchorPoint: EHorizontalAnchorPoint.Center,

verticalAnchorPoint: EVerticalAnchorPoint.Center,

x1: 2.5, // at 12 o'clock (if range is 0 ot 10, since startAngle is at 9 o'clock)

y1: 2,

fontSize: 56,

fontWeight: "Bold",

textColor: "#FFFFFF22",

xCoordinateMode: ECoordinateMode.DataValue,

yCoordinateMode: ECoordinateMode.DataValue,

annotationLayer: EAnnotationLayer.BelowChart

}

}

]

});

This results in the following: