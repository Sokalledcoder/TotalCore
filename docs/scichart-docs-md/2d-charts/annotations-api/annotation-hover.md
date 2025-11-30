---
source: https://www.scichart.com/documentation/js/v4/2d-charts/annotations-api/annotation-hover
scraped_at: 2025-11-28T18:24:00.378953
---

# https://www.scichart.com/documentation/js/v4/2d-charts/annotations-api/annotation-hover

# Annotation Hover

Annotations Hover API is an opt-in functionality that allows detecting hover events on chart annotations and adding event handlers.

The JavaScript Hoverable Trade Markers Example can be found in the SciChart.Js Examples Suite on Github, or our live demo at scichart.com/demo

## Using AnnotationHoverModifier

To enable the hover detection we need to add the AnnotationHoverModifier📘.

- TS
- Builder API (JSON Config)

`// Add an annotation with hover behaviour`

const boxAnnotation = new BoxAnnotation({

xCoordinateMode: ECoordinateMode.Relative,

yCoordinateMode: ECoordinateMode.Relative,

fill: "#3d34eb",

strokeThickness: 1,

x1: 0.1,

x2: 0.4,

y1: 0.4,

y2: 0.6,

onHover: args => {

const { sender, mouseArgs, isHovered } = args;

if (mouseArgs && isHovered) {

const relativeCoordinates = args.getRelativeCoordinates();

console.log("The annotation is hovered at", relativeCoordinates);

}

}

});

sciChartSurface.annotations.add(boxAnnotation);

// Add AnnotationHoverModifier to enable hover behaviour

const annotationHoverModifier = new AnnotationHoverModifier({

enableHover: true,

targets: [boxAnnotation],

hoverMode: EHoverMode.AbsoluteTopmost,

notifyOutEvent: true,

notifyPositionUpdate: true,

onHover: args => {

const { mouseArgs, includedEntities, hoveredEntities, unhoveredEntities } = args;

const hoveredAnnotations = hoveredEntities as BoxAnnotation[];

const unhoveredAnnotations = unhoveredEntities as BoxAnnotation[];

hoveredAnnotations.forEach(annotation => {

annotation.fill = "#34eb8c";

annotation.strokeThickness = 3;

});

unhoveredAnnotations.forEach(annotation => {

annotation.fill = "#3d34eb";

annotation.strokeThickness = 1;

});

}

});

sciChartSurface.chartModifiers.add(annotationHoverModifier);

`const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {`

surface: {

theme: new SciChartJsNavyTheme()

},

// Add an annotation with hover behaviour

annotations: [

{

type: EAnnotationType.RenderContextBoxAnnotation,

options: {

id: "boxAnnotation",

xCoordinateMode: ECoordinateMode.Relative,

yCoordinateMode: ECoordinateMode.Relative,

fill: "#3d34eb",

strokeThickness: 1,

x1: 0.1,

x2: 0.4,

y1: 0.4,

y2: 0.6,

onHover: args => {

const { sender, mouseArgs, isHovered } = args;

if (mouseArgs && isHovered) {

const relativeCoordinates = args.getRelativeCoordinates();

console.log("The annotation is hovered at", relativeCoordinates);

}

}

}

}

],

// Add AnnotationHoverModifier to enable hover behaviour

modifiers: [

{

type: EChart2DModifierType.AnnotationHover,

options: {

enableHover: true,

targets: ["boxAnnotation"],

hoverMode: EHoverMode.AbsoluteTopmost,

notifyOutEvent: true,

notifyPositionUpdate: true,

onHover: args => {

const { mouseArgs, includedEntities, hoveredEntities, unhoveredEntities } = args;

const hoveredAnnotations = hoveredEntities as BoxAnnotation[];

const unhoveredAnnotations = unhoveredEntities as BoxAnnotation[];

hoveredAnnotations.forEach(annotation => {

annotation.fill = "#34eb8c";

annotation.strokeThickness = 3;

});

unhoveredAnnotations.forEach(annotation => {

annotation.fill = "#3d34eb";

annotation.strokeThickness = 1;

});

}

}

}

]

});

## Adding Hover Event Handlers

There are several different options for adding a callback for the hover event.

- By passing onHover📘 via an annotation constructor options📘, or subscribing to the annotation.hovered📘 event handler on an AnnotationBase📘 derived type. This allows you to have different hover behaviour for each annotation, and the args has a method which allows you to find out where on the annotation the over occurred.

- By passing onHover📘 via the constructor of the AnnotationHoverModifier📘 or subscribing to the annotationHoverModifier.hoverChanged📘 event handler on an instance of AnnotationHoverModifier📘. This gives you a single callback with access to both the hovered and unhovered annotations, allowing you to define common hover behaviour in one place, and enabling you to update other annotations when one is hovered.

- Hover on modifier

`// onHover in constructor. Internally this just subcribes to the hovered event using the function you pass in.`

const annotationHoverModifier = new AnnotationHoverModifier({

onHover: (args: IHoverCallbackArgs<IAnnotation>) => {

const { mouseArgs, includedEntities, hoveredEntities, unhoveredEntities } = args;

// ...

}

});

// subscribe to hovered event directly

annotationHoverModifier.hoverChanged.subscribe((args: IHoverCallbackArgs<IAnnotation>) => {

// ...

});

These approaches could be used simultaneously.

## Hover Detection Options

The hover detection functionality is managed by the AnnotationHoverModifier📘. By default, the modifier checks every annotation within SciChartSurface.annotations📘 that is visible upon mouse move. Then if the mouse position is over any of the annotations, only the one that is above all others is considered to be hovered. An event will be raised if the hovered state of annotation has changed (e.g. it became hovered or unhovered).

These behaviors can be modified via the IAnnotationHoverModifierOptions📘.

### Hover Detection Mode

The hover detection rules are defined by the hoverMode📘 property accepting values from EHoverMode📘 enum.

- AbsoluteTopmost📘 (default) - selects only one annotation that is not overlayed by any other annotation at the mouse position; the mode checks both included and ignored targets, but can select only an included one.
- TopmostIncluded📘 - selects only one annotation that is not overlayed by any other annotation at the mouse position; the mode checks and selects only included targets.
- Multi📘 - selects multiple included annotations at the mouse position.

### Types of actions that trigger event

To modify the hover change condition when an event should be raised use notifyOutEvent📘 and notifyPositionUpdate📘 flags.

- notifyOutEvent📘 - defines whether an event should be raised when any of the annotations has become unhovered. For example, if set to false an event won't be raised when all of the annotations are unhovered. Defaults to true.
- notifyPositionUpdate📘 - defines whether an event should be raised when the list of hovered and unhovered annotations haven't changed. E.g. the mouse position changed within the bounds of an already hovered annotation. Defaults to false.

## Hover Targets

To check only a specific set of annotations use the targets📘 property. It can accept either

- an array of annotations
- and array of annotation ids
- a function returning an array of annotations
- the name of a function registered with the Builder API

- Target Selector

`const targetsSelector = modifier => hoverableAnnotations;`

const annotationHoverModifier = new AnnotationHoverModifier({

targets: targetsSelector,

hoverMode: EHoverMode.Multi

});

Here is a simple example using the methods described above: