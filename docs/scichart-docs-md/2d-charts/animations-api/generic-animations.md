---
source: https://www.scichart.com/documentation/js/v4/2d-charts/animations-api/generic-animations
scraped_at: 2025-11-28T18:23:59.317791
---

# https://www.scichart.com/documentation/js/v4/2d-charts/animations-api/generic-animations

# Generic Animations

SciChart.js v2.x and above features a new GenericAnimation API which allows you to animate almost everything in the chart and even things outside of the chart, because you have complete control of the onAnimate function. Normally, Generic Animations run at the same time, and for the duration you specify, but by using the onComplete function, you can make one animation start when another ends or create repeating loops.

The onAnimate function is passed the from and to values, and a progress value, which is between 0 and 1. This is calculated based on the elapsed time and the easing function. You can use this to interpolate between from and to, or ignore it and do something different!

Here you will find some simple examples what can be done with the Generic Animations API.

### Animating Annotations

All SciChart annotations can be animated with Generic Animations API. This example demonstrates moving a line annotation from one set of coords to another. Any editable property of the annotation can be updated. The key is the use of the arrow function to specify onAnimate, which captures the local context and allows us to update the annotation created earlier.

- JS
- TS

`import { SciChartSurface, NumericAxis, NumberRange, SciChartJSLightTheme, LineAnnotation, GenericAnimation, easing, DoubleAnimator } from "scichart";`

async function drawAnnotationAnimationsChart(divId) {

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divId, {

theme: new SciChartJSLightTheme()

});

// Setup axes

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { visibleRange: new NumberRange(0, 5) }));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { visibleRange: new NumberRange(0, 5) }));

// Setup annotations

const lineAnnotation = new LineAnnotation({ stroke: "#FF6600", strokeThickness: 3, x1: 0.0, x2: 0.5, y1: 0.5, y2: 0.0 });

sciChartSurface.annotations.add(lineAnnotation);

// Setup animations

const lineAnimation = new GenericAnimation({

from: { x1: 0.0, x2: 0.5, y1: 0.5, y2: 0.0 },

to: { x1: 4.5, x2: 5.0, y1: 5.0, y2: 4.5 },

duration: 4000,

ease: easing.inOutSine,

onAnimate: (from, to, progress) => {

lineAnnotation.x1 = DoubleAnimator.interpolate(from.x1, to.x1, progress);

lineAnnotation.y1 = DoubleAnimator.interpolate(from.x2, to.x2, progress);

lineAnnotation.x2 = DoubleAnimator.interpolate(from.y1, to.y1, progress);

lineAnnotation.y2 = DoubleAnimator.interpolate(from.y2, to.y2, progress);

},

onCompleted: () => {

console.log("Line Animation Completed");

}

});

sciChartSurface.addAnimation(lineAnimation);

}

drawAnnotationAnimationsChart("scichart");

`import { SciChartSurface, NumericAxis, NumberRange, SciChartJSLightTheme, LineAnnotation, GenericAnimation, easing, DoubleAnimator } from "scichart";`

async function drawAnnotationAnimationsChart(divId: string) {

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divId, {

theme: new SciChartJSLightTheme()

});

// Setup axes

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { visibleRange: new NumberRange(0, 5) }));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { visibleRange: new NumberRange(0, 5) }));

// Setup annotations

const lineAnnotation = new LineAnnotation({ stroke: "#FF6600", strokeThickness: 3, x1: 0.0, x2: 0.5, y1: 0.5, y2: 0.0 });

sciChartSurface.annotations.add(lineAnnotation);

// Setup animations

const lineAnimation = new GenericAnimation({

from: { x1: 0.0, x2: 0.5, y1: 0.5, y2: 0.0 },

to: { x1: 4.5, x2: 5.0, y1: 5.0, y2: 4.5 },

duration: 4000,

ease: easing.inOutSine,

onAnimate: (from, to, progress) => {

lineAnnotation.x1 = DoubleAnimator.interpolate(from.x1, to.x1, progress);

lineAnnotation.y1 = DoubleAnimator.interpolate(from.x2, to.x2, progress);

lineAnnotation.x2 = DoubleAnimator.interpolate(from.y1, to.y1, progress);

lineAnnotation.y2 = DoubleAnimator.interpolate(from.y2, to.y2, progress);

},

onCompleted: () => {

console.log("Line Animation Completed");

}

});

sciChartSurface.addAnimation(lineAnimation);

}

drawAnnotationAnimationsChart("scichart");

### Animating Visible Range

This animation updates visibleRange to zoom the chart. In onComplete we set the from value to the current to value, and then create a new random to value. Calling reset makes the animation start again.

- JS
- TS

`import { SciChartSurface, NumericAxis, NumberRange, SciChartJSLightTheme, GenericAnimation, NumberRangeAnimator, easing, XyDataSeries, FastColumnRenderableSeries } from "scichart";`

const buildFrom = (xAxis, yAxis) => ({

minX: xAxis.visibleRange.min,

maxX: xAxis.visibleRange.max,

minY: yAxis.visibleRange.min,

maxY: yAxis.visibleRange.max

});

const buildTo = (xAxis, yAxis) => ({

minX: xAxis.visibleRange.min + (Math.random() * 10 + 1) * (Math.random() > .5 ? 1 : -1),

maxX: xAxis.visibleRange.max + (Math.random() * 10 + 1) * (Math.random() > .5 ? 1 : -1),

minY: yAxis.visibleRange.min - Math.random(),

maxY: yAxis.visibleRange.max + Math.random(),

});

async function drawVisibleRangeAnimationsChart(divId) {

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divId, {

theme: new SciChartJSLightTheme()

});

// Setup axes

const xAxis = new NumericAxis(wasmContext, { visibleRange: new NumberRange(0, 100) });

const yAxis = new NumericAxis(wasmContext, { visibleRange: new NumberRange(-1, 1.5) });

sciChartSurface.xAxes.add(xAxis);

sciChartSurface.yAxes.add(yAxis);

const columnSeries = new FastColumnRenderableSeries(wasmContext, {

fill: "rgba(176, 196, 222, 1)",

stroke: "#4682b4",

strokeThickness: 2,

dataPointWidth: 0.5,

opacity: 0.7

});

sciChartSurface.renderableSeries.add(columnSeries);

const dataSeries = new XyDataSeries(wasmContext);

for (let i = 0; i < 200; i++) {

dataSeries.append(i, 2 * Math.sin(i * 0.2));

}

columnSeries.dataSeries = dataSeries;

// Setup animations

const visibleRangeAnimation = new GenericAnimation({

from: buildFrom(xAxis, yAxis),

to: buildTo(xAxis, yAxis),

duration: 3000,

ease: easing.inSine,

onAnimate: (from, to, progress) => {

const xInterpolate = NumberRangeAnimator.interpolate(new NumberRange(from.minX, from.maxX), new NumberRange(to.minX, to.maxX), progress);

const yInterpolate = NumberRangeAnimator.interpolate(new NumberRange(from.minY, from.maxY), new NumberRange(to.minY, to.maxY), progress);

xAxis.visibleRange = new NumberRange(xInterpolate.min, xInterpolate.max);

yAxis.visibleRange = new NumberRange(yInterpolate.min, yInterpolate.max);

},

onCompleted: () => {

visibleRangeAnimation.delay = 0;

visibleRangeAnimation.from = visibleRangeAnimation.to;

visibleRangeAnimation.to = buildTo(xAxis, yAxis);

visibleRangeAnimation.reset();

}

});

sciChartSurface.addAnimation(visibleRangeAnimation);

}

drawVisibleRangeAnimationsChart("scichart");

`import { SciChartSurface, NumericAxis, NumberRange, SciChartJSLightTheme, GenericAnimation, NumberRangeAnimator, easing, XyDataSeries, FastColumnRenderableSeries } from "scichart";`

const buildFrom = (xAxis: NumericAxis, yAxis: NumericAxis) => ({

minX: xAxis.visibleRange.min,

maxX: xAxis.visibleRange.max,

minY: yAxis.visibleRange.min,

maxY: yAxis.visibleRange.max

});

const buildTo = (xAxis: NumericAxis, yAxis: NumericAxis) => ({

minX: xAxis.visibleRange.min + (Math.random() * 10 + 1) * (Math.random() > .5 ? 1 : -1),

maxX: xAxis.visibleRange.max + (Math.random() * 10 + 1) * (Math.random() > .5 ? 1 : -1),

minY: yAxis.visibleRange.min - Math.random(),

maxY: yAxis.visibleRange.max + Math.random(),

});

async function drawVisibleRangeAnimationsChart(divId: string) {

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divId, {

theme: new SciChartJSLightTheme()

});

// Setup axes

const xAxis = new NumericAxis(wasmContext, { visibleRange: new NumberRange(0, 100) });

const yAxis = new NumericAxis(wasmContext, { visibleRange: new NumberRange(-1, 1.5) });

sciChartSurface.xAxes.add(xAxis);

sciChartSurface.yAxes.add(yAxis);

const columnSeries = new FastColumnRenderableSeries(wasmContext, {

fill: "rgba(176, 196, 222, 1)",

stroke: "#4682b4",

strokeThickness: 2,

dataPointWidth: 0.5,

opacity: 0.7

});

sciChartSurface.renderableSeries.add(columnSeries);

const dataSeries = new XyDataSeries(wasmContext);

for (let i = 0; i < 200; i++) {

dataSeries.append(i, 2 * Math.sin(i * 0.2));

}

columnSeries.dataSeries = dataSeries;

// Setup animations

const visibleRangeAnimation = new GenericAnimation({

from: buildFrom(xAxis, yAxis),

to: buildTo(xAxis, yAxis),

duration: 3000,

ease: easing.inSine,

onAnimate: (from, to, progress) => {

const xInterpolate = NumberRangeAnimator.interpolate(new NumberRange(from.minX, from.maxX), new NumberRange(to.minX, to.maxX), progress);

const yInterpolate = NumberRangeAnimator.interpolate(new NumberRange(from.minY, from.maxY), new NumberRange(to.minY, to.maxY), progress);

xAxis.visibleRange = new NumberRange(xInterpolate.min, xInterpolate.max);

yAxis.visibleRange = new NumberRange(yInterpolate.min, yInterpolate.max);

},

onCompleted: () => {

visibleRangeAnimation.delay = 0;

visibleRangeAnimation.from = visibleRangeAnimation.to;

visibleRangeAnimation.to = buildTo(xAxis, yAxis);

visibleRangeAnimation.reset();

}

});

sciChartSurface.addAnimation(visibleRangeAnimation);

}

drawVisibleRangeAnimationsChart("scichart");

### Animating AutoRange

The method above is used internally within SciChart to support animating during autoRange. To enable this, set the autoRangeAnimation📘 property on an axis.

### Animating Data and Styles

This example shows another way to do Data Animation. If you need more flexibility than what the built in series animations provide, then you can use this approach to combine data and style changes, or even animate between different series types. Be aware that the built in animations are well optimised for each series type, so if you are trying to animate large amounts of data, you may get better performance using them.

- JS
- TS

`import { SciChartSurface, NumericAxis, NumberRange, SciChartJSLightTheme, GenericAnimation, easing, XyDataSeries, XyScatterRenderableSeries, EllipsePointMarker} from "scichart";`

const initialData = {

xValues: [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5],

yValues: [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]

};

const getData = () => {

const xValues = [];

const yValues = [];

for (let i = 0; i < initialData.xValues.length; i++) {

xValues.push(Math.random() * 5) + 1;

yValues.push(Math.random() * 5) + 1;

}

return {

xValues,

yValues

}

}

const interpolateNumber = (from, to, progress) => {

if (progress < 0) return from;

if (progress > 1) return to;

return from + (to - from) * progress;

};

async function drawDataPointAnimationsChart(divId) {

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divId, {

theme: new SciChartJSLightTheme()

});

// Setup axes

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { visibleRange: new NumberRange(0, 6) }));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { visibleRange: new NumberRange(0, 6) }));

// setup data

const dataSeries = new XyDataSeries(wasmContext, initialData);

const scatterSeries = new XyScatterRenderableSeries(wasmContext, {

dataSeries,

pointMarker: new EllipsePointMarker(wasmContext, {

width: 10,

height: 10,

fill: "#189AB4",

strokeThickness: 0

})

});

sciChartSurface.renderableSeries.add(scatterSeries);

// Setup animations

const dataAnimation = new GenericAnimation({

from: initialData,

to: getData(),

duration: 1000,

ease: easing.inOutSine,

onAnimate: (from, to, progress) => {

const newXValues = [];

const newYValues = []

from.xValues.forEach((value, index) => {

newXValues.push(interpolateNumber(value, to.xValues[index], progress));

newYValues.push(interpolateNumber(from.yValues[index], to.yValues[index], progress));

});

dataSeries.clear();

dataSeries.appendRange(newXValues, newYValues);

},

onCompleted: () => {

dataAnimation.from = dataAnimation.to;

dataAnimation.to = getData();

dataAnimation.reset();

scatterSeries.pointMarker.width += 3;

scatterSeries.pointMarker.height += 3;

console.log("Data Point Animation Completed");

}

});

sciChartSurface.addAnimation(dataAnimation);

}

drawDataPointAnimationsChart("scichart");

`import { SciChartSurface, NumericAxis, NumberRange, SciChartJSLightTheme, GenericAnimation, easing, XyDataSeries, XyScatterRenderableSeries, EllipsePointMarker} from "scichart";`

const initialData = {

xValues: [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5],

yValues: [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]

};

const getData = () => {

const xValues = [];

const yValues = [];

for (let i = 0; i < initialData.xValues.length; i++) {

xValues.push(Math.random() * 5) + 1;

yValues.push(Math.random() * 5) + 1;

}

return {

xValues,

yValues

}

}

const interpolateNumber = (from: number, to: number, progress: number) => {

if (progress < 0) return from;

if (progress > 1) return to;

return from + (to - from) * progress;

};

async function drawDataPointAnimationsChart(divId: string) {

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divId, {

theme: new SciChartJSLightTheme()

});

// Setup axes

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { visibleRange: new NumberRange(0, 6) }));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { visibleRange: new NumberRange(0, 6) }));

// setup data

const dataSeries = new XyDataSeries(wasmContext, initialData);

const scatterSeries = new XyScatterRenderableSeries(wasmContext, {

dataSeries,

pointMarker: new EllipsePointMarker(wasmContext, {

width: 10,

height: 10,

fill: "#189AB4",

strokeThickness: 0

})

});

sciChartSurface.renderableSeries.add(scatterSeries);

// Setup animations

const dataAnimation = new GenericAnimation({

from: initialData,

to: getData(),

duration: 1000,

ease: easing.inOutSine,

onAnimate: (from, to, progress) => {

const newXValues: number[] = [];

const newYValues: number[] = []

from.xValues.forEach((value, index) => {

newXValues.push(interpolateNumber(value, to.xValues[index], progress));

newYValues.push(interpolateNumber(from.yValues[index], to.yValues[index], progress));

});

dataSeries.clear();

dataSeries.appendRange(newXValues, newYValues);

},

onCompleted: () => {

dataAnimation.from = dataAnimation.to;

dataAnimation.to = getData();

dataAnimation.reset();

scatterSeries.pointMarker.width += 3;

scatterSeries.pointMarker.height += 3;

console.log("Data Point Animation Completed");

}

});

sciChartSurface.addAnimation(dataAnimation);

}

drawDataPointAnimationsChart("scichart");

### Combining Animations

Here is example of complex animation of different types of annotations. The custom SVG annotation is animated to random coordinates on a repeating loop. The line figure is built up in stages, with animations for the various parts added during the progress of the main animation.

- JS
- TS

`import { SciChartSurface, NumericAxis, NumberRange, SciChartJSLightTheme, LineAnnotation, CustomAnnotation, EHorizontalAnchorPoint, EVerticalAnchorPoint, GenericAnimation, easing, DoubleAnimator} from "scichart";`

const interpolateLine = (from, to, interpolationFactor) => {

return {

x1: DoubleAnimator.interpolate(from.x1, to.x1, interpolationFactor),

x2: DoubleAnimator.interpolate(from.x2, to.x2, interpolationFactor),

y1: DoubleAnimator.interpolate(from.y1, to.y1, interpolationFactor),

y2: DoubleAnimator.interpolate(from.y2, to.y2, interpolationFactor)

};

};

const getRandomCoords = () => {

return {

x1: Math.floor(Math.random() * 3 + 1),

y1: Math.floor(Math.random() * 3 + 1)

}

}

async function drawAnnotationAnimationsChart(divId) {

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divId, {

theme: new SciChartJSLightTheme()

});

// Setup axes

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { visibleRange: new NumberRange(0, 5) }));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { visibleRange: new NumberRange(0, 5) }));

// Setup annotations

const lineAnnotation = new LineAnnotation({ stroke: "#FF6600", strokeThickness: 3, x1: 0.0, x2: 0.5, y1: 0.5, y2: 0.0 });

const secondLineAnnotation = new LineAnnotation({ stroke: "#FF6600", strokeThickness: 3, x1: 0.0, x2: 0.5, y1: 0.5, y2: 0.0 });

const thirdLineAnnotation = new LineAnnotation({ stroke: "#FF6600", strokeThickness: 3, x1: 0.0, x2: 0.5, y1: 0.5, y2: 0.0 });

const fourthLineAnnotation = new LineAnnotation({ stroke: "#FF6600", strokeThickness: 3, x1: 0.0, x2: 0.5, y1: 0.5, y2: 0.0 });

const svgString = `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="30px" height="30px" viewBox="0 0 30 29" version="1.1">

<g id="surface1">

<path style=" stroke:none;fill-rule:nonzero;fill:rgb(0%,0%,0%);fill-opacity:1;" d="M 29.992188 26.488281 L 29.992188 28.070312 L 0 28.070312 L 0 0.921875 L 1.636719 0.921875 L 1.636719 26.488281 Z M 5.15625 13.300781 C 5.386719 13.300781 5.605469 13.253906 5.8125 13.183594 L 8.84375 17.769531 C 8.421875 18.152344 8.15625 18.695312 8.15625 19.296875 C 8.15625 20.460938 9.132812 21.40625 10.339844 21.40625 C 11.542969 21.40625 12.519531 20.460938 12.519531 19.296875 C 12.519531 18.976562 12.4375 18.671875 12.304688 18.398438 L 16.28125 15.589844 C 16.59375 15.84375 16.988281 16.003906 17.425781 16.003906 C 17.914062 16.003906 18.351562 15.8125 18.671875 15.507812 L 22.742188 17.96875 C 22.53125 18.320312 22.410156 18.726562 22.410156 19.160156 C 22.410156 20.484375 23.523438 21.558594 24.890625 21.558594 C 26.261719 21.558594 27.371094 20.484375 27.371094 19.160156 C 27.371094 17.835938 26.261719 16.761719 24.890625 16.761719 C 24.269531 16.761719 23.699219 16.984375 23.261719 17.351562 L 19.097656 14.835938 C 19.160156 14.664062 19.199219 14.480469 19.199219 14.289062 C 19.199219 13.34375 18.40625 12.578125 17.425781 12.578125 C 16.449219 12.578125 15.65625 13.34375 15.65625 14.289062 C 15.65625 14.527344 15.703125 14.75 15.792969 14.953125 L 11.820312 17.761719 C 11.433594 17.410156 10.914062 17.1875 10.339844 17.1875 C 10.054688 17.1875 9.78125 17.246094 9.53125 17.34375 L 6.503906 12.761719 C 6.851562 12.429688 7.066406 11.964844 7.066406 11.457031 C 7.066406 10.4375 6.210938 9.613281 5.15625 9.613281 C 4.101562 9.613281 3.25 10.4375 3.25 11.457031 C 3.25 12.476562 4.101562 13.300781 5.15625 13.300781 Z M 5.15625 13.300781 "/>

</g>

</svg>`;

const customAnnotation = new CustomAnnotation({

x1: 2.5,

y1: 2.5,

verticalAnchorPoint: EVerticalAnchorPoint.Center,

horizontalAnchorPoint: EHorizontalAnchorPoint.Center,

svgString

});

sciChartSurface.annotations.add(lineAnnotation);

sciChartSurface.annotations.add(secondLineAnnotation);

sciChartSurface.annotations.add(thirdLineAnnotation);

sciChartSurface.annotations.add(fourthLineAnnotation);

sciChartSurface.annotations.add(customAnnotation);

// Setup animations

const lineAnimation = new GenericAnimation({

from: { x1: 0.0, x2: 0.5, y1: 0.5, y2: 0.0 },

to: { x1: 4.5, x2: 5.0, y1: 5.0, y2: 4.5 },

duration: 4000,

ease: easing.inOutSine,

onAnimate: (from, to, progress) => {

const interpolatedLine = interpolateLine(from, to, progress);

if (progress > .25) {

addSecondLineAnimation();

}

if (progress > .5) {

addThirdLineAnimation();

}

if (progress > .75) {

addFourthLineAnimation();

}

lineAnnotation.x1 = interpolatedLine.x1;

lineAnnotation.y1 = interpolatedLine.y1;

lineAnnotation.x2 = interpolatedLine.x2;

lineAnnotation.y2 = interpolatedLine.y2;

},

onCompleted: () => {

console.log("Line Animation Completed");

}

});

sciChartSurface.addAnimation(lineAnimation);

const svgAnimation = new GenericAnimation({

from: { x1: 2.5, y1: 2.5 },

to: getRandomCoords(),

duration: 1500,

ease: easing.cubic,

onAnimate: (from, to, progress) => {

customAnnotation.x1 = from.x1 + (to.x1 - from.x1) * progress;

customAnnotation.y1 = from.y1 + (to.y1 - from.y1) * progress;

},

onCompleted: () => {

svgAnimation.to = getRandomCoords();

svgAnimation.reset();

console.log("SVG Animation Completed");

}

});

sciChartSurface.addAnimation(svgAnimation);

let isSecondAnimationAdded = false;

const addSecondLineAnimation = () => {

if (!isSecondAnimationAdded) {

addLineAnimation({ x1: 5.0, x2: 3.5, y1: 4.5, y2: 4.0 }, 3000, secondLineAnnotation);

isSecondAnimationAdded = true;

}

};

let isThirdAnimationAdded = false;

const addThirdLineAnimation = () => {

if (!isThirdAnimationAdded) {

addLineAnimation({ x1: 4.5, x2: 4.0, y1: 5.0, y2: 3.5 }, 2000, thirdLineAnnotation);

isThirdAnimationAdded = true;

}

}

let isFourthAnimationAdded = false;

const addFourthLineAnimation = () => {

if (!isFourthAnimationAdded) {

addLineAnimation({ x1: 4.0, x2: 3.5, y1: 3.5, y2: 4.0 }, 2000, fourthLineAnnotation);

isFourthAnimationAdded = true;

}

}

const addLineAnimation = (to, duration, annotation) => {

const lineAnimation = new GenericAnimation({

from: { x1: 0.0, x2: 0.5, y1: 0.5, y2: 0.0 },

to,

duration,

ease: easing.linear,

onAnimate: (from, to, progress) => {

const interpolatedLine = interpolateLine(from, to, progress);

annotation.x1 = interpolatedLine.x1;

annotation.y1 = interpolatedLine.y1;

annotation.x2 = interpolatedLine.x2;

annotation.y2 = interpolatedLine.y2;

},

onCompleted: () => {

console.log("Line Animation Completed");

}

});

sciChartSurface.addAnimation(lineAnimation);

}

}

drawAnnotationAnimationsChart("scichart");

`import { SciChartSurface, NumericAxis, NumberRange, SciChartJSLightTheme, LineAnnotation, CustomAnnotation, EHorizontalAnchorPoint, EVerticalAnchorPoint, GenericAnimation, easing, DoubleAnimator} from "scichart";`

const interpolateLine = (from: ILineAnnotationOptions, to: ILineAnnotationOptions, interpolationFactor: number) => {

return {

x1: DoubleAnimator.interpolate(from.x1, to.x1, interpolationFactor),

x2: DoubleAnimator.interpolate(from.x2, to.x2, interpolationFactor),

y1: DoubleAnimator.interpolate(from.y1, to.y1, interpolationFactor),

y2: DoubleAnimator.interpolate(from.y2, to.y2, interpolationFactor)

};

};

const getRandomCoords = () => {

return {

x1: Math.floor(Math.random() * 3 + 1),

y1: Math.floor(Math.random() * 3 + 1)

}

}

async function drawAnnotationAnimationsChart(divId: string) {

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divId, {

theme: new SciChartJSLightTheme()

});

// Setup axes

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { visibleRange: new NumberRange(0, 5) }));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { visibleRange: new NumberRange(0, 5) }));

// Setup annotations

const lineAnnotation = new LineAnnotation({ stroke: "#FF6600", strokeThickness: 3, x1: 0.0, x2: 0.5, y1: 0.5, y2: 0.0 });

const secondLineAnnotation = new LineAnnotation({ stroke: "#FF6600", strokeThickness: 3, x1: 0.0, x2: 0.5, y1: 0.5, y2: 0.0 });

const thirdLineAnnotation = new LineAnnotation({ stroke: "#FF6600", strokeThickness: 3, x1: 0.0, x2: 0.5, y1: 0.5, y2: 0.0 });

const fourthLineAnnotation = new LineAnnotation({ stroke: "#FF6600", strokeThickness: 3, x1: 0.0, x2: 0.5, y1: 0.5, y2: 0.0 });

const svgString = `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="30px" height="30px" viewBox="0 0 30 29" version="1.1">

<g id="surface1">

<path style=" stroke:none;fill-rule:nonzero;fill:rgb(0%,0%,0%);fill-opacity:1;" d="M 29.992188 26.488281 L 29.992188 28.070312 L 0 28.070312 L 0 0.921875 L 1.636719 0.921875 L 1.636719 26.488281 Z M 5.15625 13.300781 C 5.386719 13.300781 5.605469 13.253906 5.8125 13.183594 L 8.84375 17.769531 C 8.421875 18.152344 8.15625 18.695312 8.15625 19.296875 C 8.15625 20.460938 9.132812 21.40625 10.339844 21.40625 C 11.542969 21.40625 12.519531 20.460938 12.519531 19.296875 C 12.519531 18.976562 12.4375 18.671875 12.304688 18.398438 L 16.28125 15.589844 C 16.59375 15.84375 16.988281 16.003906 17.425781 16.003906 C 17.914062 16.003906 18.351562 15.8125 18.671875 15.507812 L 22.742188 17.96875 C 22.53125 18.320312 22.410156 18.726562 22.410156 19.160156 C 22.410156 20.484375 23.523438 21.558594 24.890625 21.558594 C 26.261719 21.558594 27.371094 20.484375 27.371094 19.160156 C 27.371094 17.835938 26.261719 16.761719 24.890625 16.761719 C 24.269531 16.761719 23.699219 16.984375 23.261719 17.351562 L 19.097656 14.835938 C 19.160156 14.664062 19.199219 14.480469 19.199219 14.289062 C 19.199219 13.34375 18.40625 12.578125 17.425781 12.578125 C 16.449219 12.578125 15.65625 13.34375 15.65625 14.289062 C 15.65625 14.527344 15.703125 14.75 15.792969 14.953125 L 11.820312 17.761719 C 11.433594 17.410156 10.914062 17.1875 10.339844 17.1875 C 10.054688 17.1875 9.78125 17.246094 9.53125 17.34375 L 6.503906 12.761719 C 6.851562 12.429688 7.066406 11.964844 7.066406 11.457031 C 7.066406 10.4375 6.210938 9.613281 5.15625 9.613281 C 4.101562 9.613281 3.25 10.4375 3.25 11.457031 C 3.25 12.476562 4.101562 13.300781 5.15625 13.300781 Z M 5.15625 13.300781 "/>

</g>

</svg>`;

const customAnnotation = new CustomAnnotation({

x1: 2.5,

y1: 2.5,

verticalAnchorPoint: EVerticalAnchorPoint.Center,

horizontalAnchorPoint: EHorizontalAnchorPoint.Center,

svgString

});

sciChartSurface.annotations.add(lineAnnotation);

sciChartSurface.annotations.add(secondLineAnnotation);

sciChartSurface.annotations.add(thirdLineAnnotation);

sciChartSurface.annotations.add(fourthLineAnnotation);

sciChartSurface.annotations.add(customAnnotation);

// Setup animations

const lineAnimation = new GenericAnimation({

from: { x1: 0.0, x2: 0.5, y1: 0.5, y2: 0.0 },

to: { x1: 4.5, x2: 5.0, y1: 5.0, y2: 4.5 },

duration: 4000,

ease: easing.inOutSine,

onAnimate: (from, to, progress) => {

const interpolatedLine = interpolateLine(from, to, progress);

if (progress > .25) {

addSecondLineAnimation();

}

if (progress > .5) {

addThirdLineAnimation();

}

if (progress > .75) {

addFourthLineAnimation();

}

lineAnnotation.x1 = interpolatedLine.x1;

lineAnnotation.y1 = interpolatedLine.y1;

lineAnnotation.x2 = interpolatedLine.x2;

lineAnnotation.y2 = interpolatedLine.y2;

},

onCompleted: () => {

console.log("Line Animation Completed");

}

});

sciChartSurface.addAnimation(lineAnimation);

const svgAnimation = new GenericAnimation({

from: { x1: 2.5, y1: 2.5 },

to: getRandomCoords(),

duration: 1500,

ease: easing.cubic,

onAnimate: (from, to, progress) => {

customAnnotation.x1 = from.x1 + (to.x1 - from.x1) * progress;

customAnnotation.y1 = from.y1 + (to.y1 - from.y1) * progress;

},

onCompleted: () => {

svgAnimation.to = getRandomCoords();

svgAnimation.reset();

console.log("SVG Animation Completed");

}

});

sciChartSurface.addAnimation(svgAnimation);

let isSecondAnimationAdded = false;

const addSecondLineAnimation = () => {

if (!isSecondAnimationAdded) {

addLineAnimation({ x1: 5.0, x2: 3.5, y1: 4.5, y2: 4.0 }, 3000, secondLineAnnotation);

isSecondAnimationAdded = true;

}

};

let isThirdAnimationAdded = false;

const addThirdLineAnimation = () => {

if (!isThirdAnimationAdded) {

addLineAnimation({ x1: 4.5, x2: 4.0, y1: 5.0, y2: 3.5 }, 2000, thirdLineAnnotation);

isThirdAnimationAdded = true;

}

}

let isFourthAnimationAdded = false;

const addFourthLineAnimation = () => {

if (!isFourthAnimationAdded) {

addLineAnimation({ x1: 4.0, x2: 3.5, y1: 3.5, y2: 4.0 }, 2000, fourthLineAnnotation);

isFourthAnimationAdded = true;

}

}

const addLineAnimation = (to: ILineAnnotationOptions, duration: number, annotation: LineAnnotation) => {

const lineAnimation = new GenericAnimation({

from: { x1: 0.0, x2: 0.5, y1: 0.5, y2: 0.0 },

to,

duration,

ease: easing.linear,

onAnimate: (from, to, progress) => {

const interpolatedLine = interpolateLine(from, to, progress);

annotation.x1 = interpolatedLine.x1;

annotation.y1 = interpolatedLine.y1;

annotation.x2 = interpolatedLine.x2;

annotation.y2 = interpolatedLine.y2;

},

onCompleted: () => {

console.log("Line Animation Completed");

}

});

sciChartSurface.addAnimation(lineAnimation);

}

}

drawAnnotationAnimationsChart("scichart");

### Updating the DOM with animations

Animations are not limited to updating elements of the chart. In this example the animations are started by a button click event and they update the DOM with progress percentage, progress line and coordinate values.

- JS
- TS

`import {`

SciChartSurface,

NumericAxis,

NumberRange,

SciChartJSLightTheme,

GenericAnimation,

easing,

BoxAnnotation,

CustomAnnotation,

EHorizontalAnchorPoint,

EVerticalAnchorPoint

} from "scichart";

async function drawAnnotationAnimationsChart(divId) {

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divId, {

theme: new SciChartJSLightTheme()

});

// Setup axes

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { visibleRange: new NumberRange(0, 5) }));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { visibleRange: new NumberRange(0, 5) }));

// Setup annotations

const boxAnnotation = new BoxAnnotation({

stroke: "#189AB4",

strokeThickness: 1,

fill: "rgba(255,50,50,0.3)",

x1: 0.5,

x2: 4.5,

y1: 0.5,

y2: 4.5

});

const svgString = `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="30px" height="30px" viewBox="0 0 30 30" version="1.1">

<g id="surface1">

<path style=" stroke:none;fill-rule:nonzero;fill:rgb(29.803922%,76.470588%,94.901961%);fill-opacity:1;" d="M 15.878906 16.179688 L 21.492188 16.179688 L 22.953125 17.445312 L 25.695312 17.445312 L 28.75 18.949219 L 28.75 20 L 26.3125 20 L 26.3125 20.4375 L 23.679688 20.4375 L 23.679688 20 L 12.328125 20 L 10.367188 18.617188 L 3.1875 17.546875 L 1.523438 11.539062 L 2.003906 11.539062 L 5 16.617188 L 15.886719 16.617188 Z M 15.878906 16.179688 "/>

<path style=" stroke:none;fill-rule:nonzero;fill:rgb(3.921569%,33.333333%,49.803922%);fill-opacity:1;" d="M 7.726562 24.175781 L 11.671875 24.175781 L 11.671875 25.054688 L 7.726562 25.054688 Z M 7.726562 24.175781 "/>

<path style=" stroke:none;fill-rule:nonzero;fill:rgb(3.921569%,33.333333%,49.803922%);fill-opacity:1;" d="M 12.550781 24.175781 L 13.429688 24.175781 L 13.429688 25.054688 L 12.550781 25.054688 Z M 12.550781 24.175781 "/>

<path style=" stroke:none;fill-rule:nonzero;fill:rgb(3.921569%,33.333333%,49.803922%);fill-opacity:1;" d="M 18.46875 4.945312 L 22.414062 4.945312 L 22.414062 5.824219 L 18.46875 5.824219 Z M 18.46875 4.945312 "/>

<path style=" stroke:none;fill-rule:nonzero;fill:rgb(3.921569%,33.333333%,49.803922%);fill-opacity:1;" d="M 16.710938 4.945312 L 17.589844 4.945312 L 17.589844 5.824219 L 16.710938 5.824219 Z M 16.710938 4.945312 "/>

<path style=" stroke:none;fill-rule:nonzero;fill:rgb(3.921569%,33.333333%,49.803922%);fill-opacity:1;" d="M 24.554688 20 L 25.4375 20 L 25.4375 20.875 L 24.554688 20.875 Z M 24.554688 20 "/>

<path style=" stroke:none;fill-rule:nonzero;fill:rgb(29.803922%,76.470588%,94.901961%);fill-opacity:1;" d="M 15.878906 10.5 L 16.765625 10.5 L 16.765625 11.558594 L 15.878906 11.558594 Z M 15.878906 10.5 "/>

<path style=" stroke:none;fill-rule:nonzero;fill:rgb(81.176471%,94.509804%,100%);fill-opacity:1;" d="M 15.25 13.976562 L 10.605469 13.976562 L 12.75 12.4375 L 17.355469 12.4375 Z M 15.25 13.976562 "/>

<path style=" stroke:none;fill-rule:nonzero;fill:rgb(81.176471%,94.509804%,100%);fill-opacity:1;" d="M 23.28125 16.5625 L 20.476562 14.132812 L 20.476562 12.96875 L 24.621094 16.5625 Z M 23.28125 16.5625 "/>

<path style=" stroke:none;fill-rule:nonzero;fill:rgb(3.921569%,33.333333%,49.803922%);fill-opacity:1;" d="M 26.039062 16.632812 L 20.203125 11.558594 L 17.640625 11.558594 L 17.640625 9.621094 L 16.761719 9.621094 L 16.761719 8.914062 L 25.921875 10.117188 L 26.039062 9.246094 L 19.6875 8.40625 L 26.03125 7.570312 L 25.914062 6.695312 L 16.324219 7.96875 L 6.726562 6.703125 L 6.609375 7.578125 L 12.957031 8.414062 L 6.609375 9.253906 L 6.726562 10.125 L 15.886719 8.917969 L 15.886719 9.628906 L 15.007812 9.628906 L 15.007812 11.566406 L 12.46875 11.566406 L 9.09375 13.980469 L 7.628906 13.980469 L 7.628906 14.859375 L 15.539062 14.859375 L 18.851562 12.445312 L 19.59375 12.445312 L 19.59375 14.539062 L 22.945312 17.449219 L 25.6875 17.449219 L 28.746094 18.953125 L 28.746094 20.003906 L 26.308594 20.003906 L 26.308594 20.882812 L 28.746094 20.882812 L 28.746094 21.765625 L 14.835938 21.765625 L 13.578125 20.882812 L 23.671875 20.882812 L 23.671875 20.003906 L 12.328125 20.003906 L 10.359375 18.621094 L 3.1875 17.546875 L 1.523438 11.539062 L 2 11.539062 L 4.992188 16.617188 L 15.878906 16.617188 L 15.878906 15.738281 L 5.496094 15.738281 L 2.5 10.660156 L 0.367188 10.660156 L 2.492188 18.335938 L 10.023438 19.453125 L 14.554688 22.640625 L 18.460938 22.640625 L 17.5625 23.554688 L 18.179688 24.175781 L 19.71875 22.640625 L 24.21875 22.640625 L 23.296875 23.554688 L 23.917969 24.175781 L 25.453125 22.640625 L 29.632812 22.640625 L 29.632812 18.398438 Z M 15.878906 10.5 L 16.765625 10.5 L 16.765625 11.558594 L 15.878906 11.558594 Z M 15.25 13.976562 L 10.605469 13.976562 L 12.75 12.4375 L 17.359375 12.4375 Z M 23.28125 16.5625 L 20.476562 14.132812 L 20.476562 12.964844 L 24.621094 16.5625 Z M 23.28125 16.5625 "/>

<path style=" stroke:none;fill-rule:nonzero;fill:rgb(3.921569%,33.333333%,49.803922%);fill-opacity:1;" d="M 16.765625 15.738281 L 17.640625 15.738281 L 17.640625 16.617188 L 16.765625 16.617188 Z M 16.765625 15.738281 "/>

<path style=" stroke:none;fill-rule:nonzero;fill:rgb(3.921569%,33.333333%,49.803922%);fill-opacity:1;" d="M 5.871094 13.976562 L 6.75 13.976562 L 6.75 14.851562 L 5.871094 14.851562 Z M 5.871094 13.976562 "/>

</g>

</svg>`;

const customAnnotation = new CustomAnnotation({

x1: 0.25,

y1: 4.75,

verticalAnchorPoint: EVerticalAnchorPoint.Center,

horizontalAnchorPoint: EHorizontalAnchorPoint.Center,

svgString

});

sciChartSurface.annotations.add(boxAnnotation, customAnnotation);

document.getElementById("svgBtn").addEventListener("click", () => {

startSvgAnimation();

});

document.getElementById("boxBtn").addEventListener("click", () => {

startBoxAnimation();

});

const SVG_STEPS = [{ x: 0.25, y: 4.75 }, { x: 4.75, y: 4.75 }, { x: 4.75, y: 0.25 }, { x: 0.25, y: 0.25 }];

let indexStep = 1;

const startSvgAnimation = () => {

const animation = new GenericAnimation({

from: { x1: SVG_STEPS[0].x, y1: SVG_STEPS[0].y },

to: { x1: SVG_STEPS[indexStep].x, y1: SVG_STEPS[indexStep].y },

duration: 2000,

ease: easing.linear,

onAnimate: (from, to, progress) => {

customAnnotation.x1 = from.x1 + (to.x1 - from.x1) * progress;

customAnnotation.y1 = from.y1 + (to.y1 - from.y1) * progress;

updateSvgUI(progress, customAnnotation.x1, customAnnotation.y1);

},

onCompleted: () => {

indexStep < SVG_STEPS.length - 1 ? indexStep++ : indexStep = 0;

animation.from = animation.to;

animation.to = { x1: SVG_STEPS[indexStep].x, y1: SVG_STEPS[indexStep].y };

animation.reset();

const countEl = document.getElementById("svgInfo").querySelector("span");

countEl.innerHTML = +countEl.innerHTML + 1;

}

});

sciChartSurface.addAnimation(animation);

};

const startBoxAnimation = () => {

const animation = new GenericAnimation({

from: {

x1: 0.5,

x2: 4.5,

y1: 0.5,

y2: 4.5

},

to: {

x1: 2.5,

x2: 2.5,

y1: 2.5,

y2: 2.5,

},

duration: 8000,

ease: easing.linear,

onAnimate: (from, to, progress) => {

boxAnnotation.x1 = from.x1 + (to.x1 - from.x1) * progress;

boxAnnotation.y1 = from.y1 + (to.y1 - from.y1) * progress;

boxAnnotation.x2 = from.x2 + (to.x2 - from.x2) * progress;

boxAnnotation.y2 = from.y2 + (to.y2 - from.y2) * progress;

updateBoxUI(progress, boxAnnotation.x1, boxAnnotation.y1, boxAnnotation.x2, boxAnnotation.y2);

},

onCompleted: () => {

const from = animation.from;

const to = animation.to;

animation.from = to;

animation.to = from;

animation.reset();

const countEl = document.getElementById("boxInfo").querySelector("span");

countEl.innerHTML = +countEl.innerHTML + 1;

}

});

sciChartSurface.addAnimation(animation);

};

const updateSvgUI = (progress, x, y) => {

document.getElementById("svgProgress").innerHTML = Math.round(progress * 100) + '%';

document.getElementById("svgSpinner").style.width = Math.round(progress * 100) + '%';

document.getElementById("svgXCoord").innerHTML = 'X: ' + parseFloat(x).toFixed(2);

document.getElementById("svgYCoord").innerHTML = 'Y: ' + parseFloat(y).toFixed(2);

};

const updateBoxUI = (progress, x1, y1, x2, y2) => {

document.getElementById("boxProgress").innerHTML = Math.round(progress * 100) + '%';

document.getElementById("boxSpinner").style.width = Math.round(progress * 100) + '%';

document.getElementById("boxX1Coord").innerHTML = 'X1: ' + parseFloat(x1).toFixed(2);

document.getElementById("boxY1Coord").innerHTML = 'Y1: ' + parseFloat(y1).toFixed(2);

document.getElementById("boxX2Coord").innerHTML = 'X2: ' + parseFloat(x2).toFixed(2);

document.getElementById("boxY2Coord").innerHTML = 'Y2: ' + parseFloat(y2).toFixed(2);

}

}

drawAnnotationAnimationsChart("scichart");

`import {`

SciChartSurface,

NumericAxis,

NumberRange,

SciChartJSLightTheme,

GenericAnimation,

easing,

BoxAnnotation,

CustomAnnotation,

EHorizontalAnchorPoint,

EVerticalAnchorPoint

} from "scichart";

async function drawAnnotationAnimationsChart(divId: string) {

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divId, {

theme: new SciChartJSLightTheme()

});

// Setup axes

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { visibleRange: new NumberRange(0, 5) }));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { visibleRange: new NumberRange(0, 5) }));

// Setup annotations

const boxAnnotation = new BoxAnnotation({

stroke: "#189AB4",

strokeThickness: 1,

fill: "rgba(255,50,50,0.3)",

x1: 0.5,

x2: 4.5,

y1: 0.5,

y2: 4.5

});

const svgString = `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="30px" height="30px" viewBox="0 0 30 30" version="1.1">

<g id="surface1">

<path style=" stroke:none;fill-rule:nonzero;fill:rgb(29.803922%,76.470588%,94.901961%);fill-opacity:1;" d="M 15.878906 16.179688 L 21.492188 16.179688 L 22.953125 17.445312 L 25.695312 17.445312 L 28.75 18.949219 L 28.75 20 L 26.3125 20 L 26.3125 20.4375 L 23.679688 20.4375 L 23.679688 20 L 12.328125 20 L 10.367188 18.617188 L 3.1875 17.546875 L 1.523438 11.539062 L 2.003906 11.539062 L 5 16.617188 L 15.886719 16.617188 Z M 15.878906 16.179688 "/>

<path style=" stroke:none;fill-rule:nonzero;fill:rgb(3.921569%,33.333333%,49.803922%);fill-opacity:1;" d="M 7.726562 24.175781 L 11.671875 24.175781 L 11.671875 25.054688 L 7.726562 25.054688 Z M 7.726562 24.175781 "/>

<path style=" stroke:none;fill-rule:nonzero;fill:rgb(3.921569%,33.333333%,49.803922%);fill-opacity:1;" d="M 12.550781 24.175781 L 13.429688 24.175781 L 13.429688 25.054688 L 12.550781 25.054688 Z M 12.550781 24.175781 "/>

<path style=" stroke:none;fill-rule:nonzero;fill:rgb(3.921569%,33.333333%,49.803922%);fill-opacity:1;" d="M 18.46875 4.945312 L 22.414062 4.945312 L 22.414062 5.824219 L 18.46875 5.824219 Z M 18.46875 4.945312 "/>

<path style=" stroke:none;fill-rule:nonzero;fill:rgb(3.921569%,33.333333%,49.803922%);fill-opacity:1;" d="M 16.710938 4.945312 L 17.589844 4.945312 L 17.589844 5.824219 L 16.710938 5.824219 Z M 16.710938 4.945312 "/>

<path style=" stroke:none;fill-rule:nonzero;fill:rgb(3.921569%,33.333333%,49.803922%);fill-opacity:1;" d="M 24.554688 20 L 25.4375 20 L 25.4375 20.875 L 24.554688 20.875 Z M 24.554688 20 "/>

<path style=" stroke:none;fill-rule:nonzero;fill:rgb(29.803922%,76.470588%,94.901961%);fill-opacity:1;" d="M 15.878906 10.5 L 16.765625 10.5 L 16.765625 11.558594 L 15.878906 11.558594 Z M 15.878906 10.5 "/>

<path style=" stroke:none;fill-rule:nonzero;fill:rgb(81.176471%,94.509804%,100%);fill-opacity:1;" d="M 15.25 13.976562 L 10.605469 13.976562 L 12.75 12.4375 L 17.355469 12.4375 Z M 15.25 13.976562 "/>

<path style=" stroke:none;fill-rule:nonzero;fill:rgb(81.176471%,94.509804%,100%);fill-opacity:1;" d="M 23.28125 16.5625 L 20.476562 14.132812 L 20.476562 12.96875 L 24.621094 16.5625 Z M 23.28125 16.5625 "/>

<path style=" stroke:none;fill-rule:nonzero;fill:rgb(3.921569%,33.333333%,49.803922%);fill-opacity:1;" d="M 26.039062 16.632812 L 20.203125 11.558594 L 17.640625 11.558594 L 17.640625 9.621094 L 16.761719 9.621094 L 16.761719 8.914062 L 25.921875 10.117188 L 26.039062 9.246094 L 19.6875 8.40625 L 26.03125 7.570312 L 25.914062 6.695312 L 16.324219 7.96875 L 6.726562 6.703125 L 6.609375 7.578125 L 12.957031 8.414062 L 6.609375 9.253906 L 6.726562 10.125 L 15.886719 8.917969 L 15.886719 9.628906 L 15.007812 9.628906 L 15.007812 11.566406 L 12.46875 11.566406 L 9.09375 13.980469 L 7.628906 13.980469 L 7.628906 14.859375 L 15.539062 14.859375 L 18.851562 12.445312 L 19.59375 12.445312 L 19.59375 14.539062 L 22.945312 17.449219 L 25.6875 17.449219 L 28.746094 18.953125 L 28.746094 20.003906 L 26.308594 20.003906 L 26.308594 20.882812 L 28.746094 20.882812 L 28.746094 21.765625 L 14.835938 21.765625 L 13.578125 20.882812 L 23.671875 20.882812 L 23.671875 20.003906 L 12.328125 20.003906 L 10.359375 18.621094 L 3.1875 17.546875 L 1.523438 11.539062 L 2 11.539062 L 4.992188 16.617188 L 15.878906 16.617188 L 15.878906 15.738281 L 5.496094 15.738281 L 2.5 10.660156 L 0.367188 10.660156 L 2.492188 18.335938 L 10.023438 19.453125 L 14.554688 22.640625 L 18.460938 22.640625 L 17.5625 23.554688 L 18.179688 24.175781 L 19.71875 22.640625 L 24.21875 22.640625 L 23.296875 23.554688 L 23.917969 24.175781 L 25.453125 22.640625 L 29.632812 22.640625 L 29.632812 18.398438 Z M 15.878906 10.5 L 16.765625 10.5 L 16.765625 11.558594 L 15.878906 11.558594 Z M 15.25 13.976562 L 10.605469 13.976562 L 12.75 12.4375 L 17.359375 12.4375 Z M 23.28125 16.5625 L 20.476562 14.132812 L 20.476562 12.964844 L 24.621094 16.5625 Z M 23.28125 16.5625 "/>

<path style=" stroke:none;fill-rule:nonzero;fill:rgb(3.921569%,33.333333%,49.803922%);fill-opacity:1;" d="M 16.765625 15.738281 L 17.640625 15.738281 L 17.640625 16.617188 L 16.765625 16.617188 Z M 16.765625 15.738281 "/>

<path style=" stroke:none;fill-rule:nonzero;fill:rgb(3.921569%,33.333333%,49.803922%);fill-opacity:1;" d="M 5.871094 13.976562 L 6.75 13.976562 L 6.75 14.851562 L 5.871094 14.851562 Z M 5.871094 13.976562 "/>

</g>

</svg>`;

const customAnnotation = new CustomAnnotation({

x1: 0.25,

y1: 4.75,

verticalAnchorPoint: EVerticalAnchorPoint.Center,

horizontalAnchorPoint: EHorizontalAnchorPoint.Center,

svgString

});

sciChartSurface.annotations.add(boxAnnotation, customAnnotation);

document.getElementById("svgBtn").addEventListener("click", () => {

startSvgAnimation();

});

document.getElementById("boxBtn").addEventListener("click", () => {

startBoxAnimation();

});

const SVG_STEPS = [{ x: 0.25, y: 4.75 }, { x: 4.75, y: 4.75 }, { x: 4.75, y: 0.25 }, { x: 0.25, y: 0.25 }];

let indexStep = 1;

const startSvgAnimation = () => {

const animation = new GenericAnimation({

from: { x1: SVG_STEPS[0].x, y1: SVG_STEPS[0].y },

to: { x1: SVG_STEPS[indexStep].x, y1: SVG_STEPS[indexStep].y },

duration: 2000,

ease: easing.linear,

onAnimate: (from, to, progress) => {

customAnnotation.x1 = from.x1 + (to.x1 - from.x1) * progress;

customAnnotation.y1 = from.y1 + (to.y1 - from.y1) * progress;

updateSvgUI(progress, customAnnotation.x1, customAnnotation.y1);

},

onCompleted: () => {

indexStep < SVG_STEPS.length - 1 ? indexStep++ : indexStep = 0;

animation.from = animation.to;

animation.to = { x1: SVG_STEPS[indexStep].x, y1: SVG_STEPS[indexStep].y };

animation.reset();

const countEl = document.getElementById("svgInfo").querySelector("span");

countEl.innerHTML = (+countEl.innerHTML + 1).toString();

}

});

sciChartSurface.addAnimation(animation);

};

const startBoxAnimation = () => {

const animation = new GenericAnimation({

from: {

x1: 0.5,

x2: 4.5,

y1: 0.5,

y2: 4.5

},

to: {

x1: 2.5,

x2: 2.5,

y1: 2.5,

y2: 2.5,

},

duration: 8000,

ease: easing.linear,

onAnimate: (from, to, progress) => {

boxAnnotation.x1 = from.x1 + (to.x1 - from.x1) * progress;

boxAnnotation.y1 = from.y1 + (to.y1 - from.y1) * progress;

boxAnnotation.x2 = from.x2 + (to.x2 - from.x2) * progress;

boxAnnotation.y2 = from.y2 + (to.y2 - from.y2) * progress;

updateBoxUI(progress, boxAnnotation.x1, boxAnnotation.y1, boxAnnotation.x2, boxAnnotation.y2);

},

onCompleted: () => {

const from = animation.from;

const to = animation.to;

animation.from = to;

animation.to = from;

animation.reset();

const countEl = document.getElementById("boxInfo").querySelector("span");

countEl.innerHTML = (+countEl.innerHTML + 1).toString();

}

});

sciChartSurface.addAnimation(animation);

};

const updateSvgUI = (progress: number, x: number, y: number) => {

document.getElementById("svgProgress").innerHTML = Math.round(progress * 100) + '%';

document.getElementById("svgSpinner").style.width = Math.round(progress * 100) + '%';

document.getElementById("svgXCoord").innerHTML = 'X: ' + x.toFixed(2);

document.getElementById("svgYCoord").innerHTML = 'Y: ' + y.toFixed(2);

};

const updateBoxUI = (progress: number, x1: number, y1: number, x2: number, y2: number) => {

document.getElementById("boxProgress").innerHTML = Math.round(progress * 100) + '%';

document.getElementById("boxSpinner").style.width = Math.round(progress * 100) + '%';

document.getElementById("boxX1Coord").innerHTML = 'X1: ' + x1.toFixed(2);

document.getElementById("boxY1Coord").innerHTML = 'Y1: ' + y1.toFixed(2);

document.getElementById("boxX2Coord").innerHTML = 'X2: ' + x2.toFixed(2);

document.getElementById("boxY2Coord").innerHTML = 'Y2: ' + y2.toFixed(2);

}

}

drawAnnotationAnimationsChart("scichart");