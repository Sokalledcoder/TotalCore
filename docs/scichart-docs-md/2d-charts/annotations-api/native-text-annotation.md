---
source: https://www.scichart.com/documentation/js/v4/2d-charts/annotations-api/native-text-annotation
scraped_at: 2025-11-28T18:24:02.673899
---

# https://www.scichart.com/documentation/js/v4/2d-charts/annotations-api/native-text-annotation

# NativeTextAnnotation

NativeTextAnnotation📘 works almost exactly like the normal TextAnnotation📘 but instead of using SVG, it draws using the native text api that is new in SciChart.JS v3 or greater. This allows for some significant benefits:

**Performance:**you can draw hundreds or even thousands of text labels without significant slowdown.**Multi-line text is much easier**. Separate lines with the newline (/n) character, and adjust lineSpacing📘 and multiLineAlignment📘 if needed.**Rotated text is much easier:**If you try and rotate SVG text, you will often find it gets clipped by its own viewbox. NativeText does not. You can control the angle via NativeTextAnnotation.rotation📘. You can control center of rotation by overriding getRotationCenter📘 if need be.**Text wrapping is much easier:**NativeTextAnnotation📘 can wrap to the chart area, or to the width you set for it. If you make the annotation editable you can see the wrapping change as you resize.**Allows Text Scaling:**Using the NativeTextAnnotation.scale📘 property text can be drawn at different sizes without creating a new font.

warning

There are also some limitations compared to svg text:

- Font style and font weight are not supported. Fonts other than Arial must be
`ttf`

and either be hosted on your server or registered if coming from the internet. See Native Text Font Loading

## Creating many variants of NativeTextAnnotation📘:

- TS
- Builder API (JSON Config)

async function addAnnotationToChart(divElementId) {

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

// Add a selection of NativeTextAnnotations to the chart

sciChartSurface.annotations.add(

new NativeTextAnnotation({

x1: 1,

y1: 9,

text: "The default font is Arial, which does not need to be hosted or registered",

fontSize: 18

})

);

// Loading a NativeTextAnnotation with a custom font

const result = await sciChartSurface.registerFont(

"MyCustomFont",

"https://fonts.gstatic.com/s/opensans/v29/mem8YaGs126MiZpBA-U1UpcaXcl0Aw.ttf"

);

console.log("Native font was loaded? " + result);

sciChartSurface.annotations.add(

new NativeTextAnnotation({

x1: 3,

y1: 7,

text: "This text uses a custom font",

fontFamily: "MyCustomFont",

fontSize: 24

})

);

// Rotating a NativeTextAnnotation with multline text

sciChartSurface.annotations.add(

new NativeTextAnnotation({

x1: 1,

y1: 5,

text: "Native text supports\nmultiline and rotation",

fontFamily: "Default",

fontSize: 24,

rotation: 30,

textColor: "orange"

})

);

// Word Wrapping a NativeTextAnnotation

sciChartSurface.annotations.add(

new NativeTextAnnotation({

x1: 5,

y1: 5,

text: "Native text can automatically wrap to the chart area or the annotation width. ",

fontFamily: "Default",

fontSize: 24,

isEditable: true,

wrapTo: EWrapTo.ViewRect

})

);

// Scaling a native text annotation

const scaledText = new NativeTextAnnotation({

x1: 5,

y1: 3,

text: "Native text can be scaled\nwithout changing the font size",

fontFamily: "Default",

fontSize: 16,

scale: 1

});

sciChartSurface.annotations.add(scaledText);

const scaleAnimation = new GenericAnimation({

from: 0,

to: 1,

duration: 2000,

onAnimate: (from, to, progress) => {

if (progress < 0.5) {

scaledText.scale = 1 + progress;

} else {

scaledText.scale = 1 + (1 - progress);

}

},

onCompleted: () => {

scaleAnimation.reset();

}

});

sciChartSurface.addAnimation(scaleAnimation);

}

addAnnotationToChart("scichart-root");

`const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {`

annotations: [

{

type: EAnnotationType.RenderContextNativeTextAnnotation,

options: {

x1: 1,

y1: 9,

text: "The default font is Arial, which does not need to be hosted or registered",

fontSize: 18

}

},

{

type: EAnnotationType.RenderContextNativeTextAnnotation,

options: {

x1: 1,

y1: 5,

text: "Native text supports\nmultiline and rotation",

fontFamily: "Default",

fontSize: 24,

rotation: 30,

textColor: "orange"

}

},

{

type: EAnnotationType.RenderContextNativeTextAnnotation,

options: {

x1: 3,

y1: 7,

text: "This text uses a font from the internet",

fontFamily: "MyCustomFont",

fontSize: 24

}

},

{

type: EAnnotationType.RenderContextNativeTextAnnotation,

options: {

x1: 5,

y1: 5,

text: "Native text can automatically wrap to the chart area or the annotation width. ",

fontFamily: "Default",

fontSize: 24,

isEditable: true,

wrapTo: EWrapTo.ViewRect

}

},

{

type: EAnnotationType.RenderContextNativeTextAnnotation,

options: {

id: "scaleAnnotation",

x1: 5,

y1: 3,

text: "Native text can be scaled\nwithout changing the font size",

fontFamily: "Default",

fontSize: 16

}

}

]

});

// Registering the custom font

const result = await sciChartSurface.registerFont(

"MyCustomFont",

"https://fonts.gstatic.com/s/opensans/v29/mem8YaGs126MiZpBA-U1UpcaXcl0Aw.ttf"

);

console.log("Native font was loaded? " + result);

// Scaling the last NativeTextAnnotation

const scaleAnnotation = sciChartSurface.annotations.getById("scaleAnnotation") as NativeTextAnnotation;

const scaleAnimation = new GenericAnimation({

from: 0,

to: 1,

duration: 2000,

onAnimate: (from, to, progress) => {

if (progress < 0.5) {

scaleAnnotation.scale = 1 + progress;

} else {

scaleAnnotation.scale = 1 + (1 - progress);

}

},

onCompleted: () => {

scaleAnimation.reset();

}

});

sciChartSurface.addAnimation(scaleAnimation);

This results in the following output:

## Polar Charts with NativeTextAnnotation

To add a NativeTextAnnotation📘 to a Polar chart, use the same exact code, just change the surface and axes types. The NativeTextAnnotation will be positioned in polar coordinates.

- TS
- Builder API (JSON Config)

`const {`

NativeTextAnnotation,

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

new NativeTextAnnotation({

text: "Polar Native\nText Annotations",

horizontalAnchorPoint: EHorizontalAnchorPoint.Center,

verticalAnchorPoint: EVerticalAnchorPoint.Center,

x1: 2.5, // at 12 o'clock (if range is 0 ot 10, since startAngle is at 9 o'clock)

y1: 2,

fontSize: 56,

lineSpacing: 15,

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

type: EAnnotationType.RenderContextNativeTextAnnotation,

options: {

text: "Polar Native\nText Annotations",

horizontalAnchorPoint: EHorizontalAnchorPoint.Center,

verticalAnchorPoint: EVerticalAnchorPoint.Center,

x1: 2.5, // at 12 o'clock (if range is 0 ot 10, since startAngle is at 9 o'clock)

y1: 2,

fontSize: 56,

lineSpacing: 15,

textColor: "#FFFFFF22",

xCoordinateMode: ECoordinateMode.DataValue,

yCoordinateMode: ECoordinateMode.DataValue,

annotationLayer: EAnnotationLayer.BelowChart

}

}

]

});

This results in the following: