---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/custom-modifiers/detecting-clicks-on-chart-parts
scraped_at: 2025-11-28T18:24:16.384434
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/custom-modifiers/detecting-clicks-on-chart-parts

# Detecting Clicks On Chart Parts with a Custom Modifier

One of the uses of the custom ChartModifier API is to allow you to create custom behaviours and add them onto a SciChartSurface. These behaviours can be simple or complex, and perform zooming, panning operations or more.

Below we give an example of how to detect clicks on chart parts using the ChartModifier API. This results in the following output on mouse over.

## Detecting Click or MouseOver on Axis, RenderableSeries

In the sample below we've created a custom chartmodifier which allows us to detect whether the mouse is over chart parts such as XAxis, YAxis and RenderableSeries.

The process to create a chart modifier is by extending ChartModifierBase2D and overridding one or more of the functions or callbacks that are called when we interact with the chart.

- TypeScript
- JavaScript

`import {`

ChartModifierBase2D,

EChart2DModifierType,

ModifierMouseArgs,

testIsInBounds,

Rect,

RubberBandSvgRect,

DpiHelper

} from "scichart";

// A custom modifier which detects clicks on chart parts

export class DetectClicksOnChartPartsModifier extends ChartModifierBase2D {

readonly type: EChart2DModifierType = EChart2DModifierType.Custom;

private debugRect: RubberBandSvgRect;

override onAttach() {

super.onAttach();

// Rectangle used to show visually what chart part you clicked

this.debugRect = new RubberBandSvgRect(this.parentSurface.domSvgAdornerLayer, "#FF000033", "Transparent", 0);

}

override onDetach() {

super.onDetach();

this.debugRect.delete();

}

override modifierMouseMove(args: ModifierMouseArgs) {

super.modifierMouseMove(args);

if (!this.isAttached) {

throw new Error("Should not call DetectClicksOnChartPartsModifier.modifierMouseDown if not attached");

}

const mousePoint = args.mousePoint;

this.updateDebugRectangle(undefined);

// Check if the mouse was over A YAxis

this.parentSurface?.yAxes.asArray().forEach(yAxis => {

const { left, right, top, bottom } = yAxis.viewRect;

if (testIsInBounds(mousePoint.x, mousePoint.y, left, bottom, right, top)) {

console.log("Mouse is over YAxis ID=" + yAxis.id);

this.updateDebugRectangle(yAxis.viewRect);

}

});

// Check if the mouse was over an XAxis

this.parentSurface?.xAxes.asArray().forEach(xAxis => {

const { left, right, top, bottom } = xAxis.viewRect;

if (testIsInBounds(mousePoint.x, mousePoint.y, left, bottom, right, top)) {

console.log("Mouse is over XAxis ID=" + xAxis.id);

this.updateDebugRectangle(xAxis.viewRect);

}

});

// Check if the mouse was over the main chart area

const { left, right, top, bottom } = this.parentSurface?.seriesViewRect;

if (testIsInBounds(mousePoint.x, mousePoint.y, left, bottom, right, top)) {

console.log("Mouse is over main Chart area");

this.updateDebugRectangle(this.parentSurface?.seriesViewRect);

// Check if the mouse was over any series

this.parentSurface?.renderableSeries.asArray().forEach(rSeries => {

const hitTestInfo = rSeries.hitTestProvider.hitTest(mousePoint.x, mousePoint.y);

if (hitTestInfo.isHit) {

console.log(`RenderableSeries with seriesname=${rSeries.dataSeries.dataSeriesName} was hovered`);

rSeries.isHovered = true;

} else {

rSeries.isHovered = false;

}

});

}

}

private updateDebugRectangle(rect: Rect) {

if (!rect) {

this.debugRect.isHidden = true;

return;

}

this.debugRect.isHidden = false;

this.debugRect.x1 = rect.x / DpiHelper.PIXEL_RATIO;

this.debugRect.y1 = rect.y / DpiHelper.PIXEL_RATIO;

this.debugRect.x2 = rect.x / DpiHelper.PIXEL_RATIO + rect.width / DpiHelper.PIXEL_RATIO;

this.debugRect.y2 = rect.y / DpiHelper.PIXEL_RATIO + rect.height / DpiHelper.PIXEL_RATIO;

this.debugRect.isHidden = false;

}

}

`import { ChartModifierBase2D, EChart2DModifierType, testIsInBounds, RubberBandSvgRect, DpiHelper } from "scichart";`

// A custom modifier which detects clicks on chart parts

export class DetectClicksOnChartPartsModifier extends ChartModifierBase2D {

type = EChart2DModifierType.Custom;

debugRect;

onAttach() {

super.onAttach();

// Rectangle used to show visually what chart part you clicked

this.debugRect = new RubberBandSvgRect(this.parentSurface.domSvgAdornerLayer, "#FF000033", "Transparent", 0);

}

onDetach() {

super.onDetach();

this.debugRect.delete();

}

modifierMouseMove(args) {

super.modifierMouseMove(args);

if (!this.isAttached) {

throw new Error("Should not call DetectClicksOnChartPartsModifier.modifierMouseDown if not attached");

}

const mousePoint = args.mousePoint;

this.updateDebugRectangle(undefined);

// Check if the mouse was over A YAxis

this.parentSurface?.yAxes.asArray().forEach(yAxis => {

const { left, right, top, bottom } = yAxis.viewRect;

if (testIsInBounds(mousePoint.x, mousePoint.y, left, bottom, right, top)) {

console.log("Mouse is over YAxis ID=" + yAxis.id);

this.updateDebugRectangle(yAxis.viewRect);

}

});

// Check if the mouse was over an XAxis

this.parentSurface?.xAxes.asArray().forEach(xAxis => {

const { left, right, top, bottom } = xAxis.viewRect;

if (testIsInBounds(mousePoint.x, mousePoint.y, left, bottom, right, top)) {

console.log("Mouse is over XAxis ID=" + xAxis.id);

this.updateDebugRectangle(xAxis.viewRect);

}

});

// Check if the mouse was over the main chart area

const { left, right, top, bottom } = this.parentSurface?.seriesViewRect;

if (testIsInBounds(mousePoint.x, mousePoint.y, left, bottom, right, top)) {

console.log("Mouse is over main Chart area");

this.updateDebugRectangle(this.parentSurface?.seriesViewRect);

// Check if the mouse was over any series

this.parentSurface?.renderableSeries.asArray().forEach(rSeries => {

const hitTestInfo = rSeries.hitTestProvider.hitTest(mousePoint.x, mousePoint.y);

if (hitTestInfo.isHit) {

console.log(`RenderableSeries with seriesname=${rSeries.dataSeries.dataSeriesName} was hovered`);

rSeries.isHovered = true;

}

else {

rSeries.isHovered = false;

}

});

}

}

updateDebugRectangle(rect) {

if (!rect) {

this.debugRect.isHidden = true;

return;

}

this.debugRect.isHidden = false;

this.debugRect.x1 = rect.x / DpiHelper.PIXEL_RATIO;

this.debugRect.y1 = rect.y / DpiHelper.PIXEL_RATIO;

this.debugRect.x2 = rect.x / DpiHelper.PIXEL_RATIO + rect.width / DpiHelper.PIXEL_RATIO;

this.debugRect.y2 = rect.y / DpiHelper.PIXEL_RATIO + rect.height / DpiHelper.PIXEL_RATIO;

this.debugRect.isHidden = false;

}

}

Above: we create a custom chartmodifier by extending ChartModifierBase2D.

We override `onModifierMouseMove`

(you could easily override onModifierMouseDown, MouseUp, MouseDoubleClick).

Next, we perform a series of tests to see if the mouse pointer is over an axis, or a series.

Try the above code with the following test harness:

- Custom Modifiers Sandbox

`import {`

SciChartSurface,

NumericAxis,

EAxisAlignment,

FastLineRenderableSeries,

XyDataSeries,

LegendModifier

} from "scichart";

import { DetectClicksOnChartPartsModifier } from "./DetectClicksOnChartPartsModifier";

import { SimpleChartModifierTs } from "./SimpleChartModifierTs";

export async function customModifiersSandboxTs(divId: string) {

console.log('customModifier typescript example');

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divId);

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { id: "XAxis_0", axisTitle: "XAxis 0", axisAlignment: EAxisAlignment.Top}));

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { id: "XAxis_1", axisTitle: "XAxis 1", axisAlignment: EAxisAlignment.Bottom}));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { id: "YAxis_0", axisTitle: "YAxis 0", axisAlignment: EAxisAlignment.Left}));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { id: "YAxis_1", axisTitle: "YAxis 1", axisAlignment: EAxisAlignment.Right}));

sciChartSurface.chartModifiers.add(new DetectClicksOnChartPartsModifier());

sciChartSurface.chartModifiers.add(new SimpleChartModifierTs());

sciChartSurface.chartModifiers.add(new LegendModifier());

const xValues = Array.from(Array(25).keys())

const yValues = xValues.map(x => Math.sin(x * 0.1));

console.log(yValues);

sciChartSurface.renderableSeries.add(new FastLineRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues, dataSeriesName: "Yellow series" }),

strokeThickness: 3,

stroke: "Yellow",

yAxisId: "YAxis_0",

xAxisId: "XAxis_0",

onHoveredChanged: sourceSeries => sourceSeries.strokeThickness = sourceSeries.isHovered ? 7 : 3,

}));

// We need setTimeout to wait the Legend being rendered

setTimeout(()=> {

// SciChart legend is always generated with scichart__legend class

const divElement = document.getElementsByClassName('scichart__legend')[1];

divElement.addEventListener('click', () => {

console.log('Click on the Legend TS example');

});

});

}

customModifiersSandboxTs("scichart-root");

Find the full code sample for detecting clicks or mouse-over chart parts at github.com/ABTSoftware/SciChart.JS.Examples/tree/master/Sandbox/DocumentationSnippets/ChartModifierAPI