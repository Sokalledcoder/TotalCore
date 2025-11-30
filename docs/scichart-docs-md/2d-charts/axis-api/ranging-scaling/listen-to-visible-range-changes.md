---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/ranging-scaling/listen-to-visible-range-changes
scraped_at: 2025-11-28T18:24:12.244763
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/ranging-scaling/listen-to-visible-range-changes

# Axis Ranging - How to Listen to VisibleRange Changes

## How to listen to VisibleRange changes

It is possible to subscribe to listening to the AxisCore.visibleRange📘 changes using the AxisCore.visibleRangeChanged📘 event.

- TS
- Builder API (JSON Config)

`// Create a chart with X,Y axis`

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

// Add a label showing the status

const textAnnotation = new TextAnnotation({

text: "Drag to pan the chart",

...options

});

sciChartSurface.annotations.add(textAnnotation);

// subscribe to visibleRangeChanged on yAxis

sciChartSurface.yAxes.get(0).visibleRangeChanged.subscribe(args => {

const message = `yAxis range: ${args.visibleRange.min.toFixed(2)}, ${args.visibleRange.max.toFixed(2)}`;

console.log(message);

textAnnotation.text = message;

});

`const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {`

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: {

type: EAxisType.NumericAxis,

options: {

axisTitle: "X Axis"

}

},

yAxes: {

type: EAxisType.NumericAxis,

options: {

axisTitle: "Y Axis"

}

},

modifiers: [{ type: EChart2DModifierType.ZoomPan }],

annotations: [

{

type: EAnnotationType.SVGTextAnnotation,

options: {

text: "Drag to pan the chart",

x1: 0.5,

y1: 0.5,

xCoordinateMode: ECoordinateMode.Relative,

yCoordinateMode: ECoordinateMode.Relative,

horizontalAnchorPoint: EHorizontalAnchorPoint.Center,

verticalAnchorPoint: EVerticalAnchorPoint.Top,

opacity: 0.77,

fontSize: 28,

fontWeight: "Bold",

textColor: "White"

}

}

]

});

const yAxis = sciChartSurface.yAxes.get(0);

const textAnnotation = /** @type {import("scichart").TextAnnotation} */ (sciChartSurface.annotations.get(0));

yAxis.visibleRangeChanged.subscribe(args => {

const message = `yAxis range: ${args.visibleRange.min.toFixed(2)}, ${args.visibleRange.max.toFixed(2)}`;

console.log(message);

textAnnotation.text = message;

});

This results in the following output:

The most typical use for this callback is to perform some kind of operation when the AxisCore.visibleRange📘 changes, such as updating UI.

It is also possible to use this callback to restrict the VisibleRange in some way, e.g set a bounded or clipped range onto AxisCore.visibleRange📘 when the range changes outside of a desired area.