---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/cursor-modifier/cursor-modifier-overview
scraped_at: 2025-11-28T18:24:14.956123
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/cursor-modifier/cursor-modifier-overview

# The CursorModifier Type

SciChart.js provides a cursors / crosshairs behavior via the CursorModifier📘, available out of the box. Besides common features which are inherited from the ChartModifierBase class, the CursorModifier📘 allows to you to:

**Place a crosshair (cursor) on the chart which tracks the mouse****Place a single aggregated tooltip for all series at the crosshair site**- Optionally show/hide and style vertical/horizontal line in the crosshair
- Optionally show/hide axis labels on the X,Y axis
- Format the axis labels
- Allow customisation of the tooltip style and contents
- Place a legend at an external
`<div>`

with tooltip info - Configure when the tooltip is shown (always, only on hover of a point)
- Configure which series react to the Tooltip (all, some, or specific series)

The Using CursorModifier Example can be found in the SciChart.Js Examples Suite on Github, or our live demo at scichart.com/demo

## Adding a CursorModifier to a Chart

A CursorModifier can be added to the sciChartSurface.chartModifiers📘 collection to enable crosshair/cursor behavior. For example, this code adds a crosshair, enables default tooltips and axis labels.

- TS
- Builder API (JSON Config)

`const {`

SciChartSurface,

NumericAxis,

FastLineRenderableSeries,

XyDataSeries,

SciChartJsNavyTheme,

EAutoRange,

NumberRange,

CursorModifier,

TextAnnotation,

EHorizontalAnchorPoint,

ECoordinateMode,

EllipsePointMarker

} = SciChart;

// or for npm import { SciChartSurface, ... } from "scichart"

// Create a chart surface

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme(),

titleStyle: { fontSize: 16 }

});

// For the example to work, axis must have EAutoRange.Always

sciChartSurface.xAxes.add(

new NumericAxis(wasmContext, {

autoRange: EAutoRange.Always,

axisTitle: "X Axis"

})

);

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

visibleRange: new NumberRange(-2, 0.5),

axisTitle: "Y Axis"

})

);

// Add a CursorModifier to the chart

const cursorModifier = new CursorModifier({

// Optional properties to configure what parts are shown

showTooltip: true,

showAxisLabels: true,

showXLine: true,

showYLine: true,

// How close to a datapoint to show the tooltip? 10 = 10 pixels. 0 means always

hitTestRadius: 10,

// Optional properties to configure the axis labels

axisLabelFill: "#b36200",

axisLabelStroke: "#fff",

// Optional properties to configure line and tooltip style

crosshairStroke: "#ff6600",

crosshairStrokeThickness: 1,

tooltipContainerBackground: "#000",

tooltipTextStroke: "#ff6600"

});

sciChartSurface.chartModifiers.add(cursorModifier);

`// Demonstrates how to configure the CursorModifier in SciChart.js using the Builder API`

const { chartBuilder, EThemeProviderType, EAxisType, EChart2DModifierType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { sciChartSurface, wasmContext } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

modifiers: [

{

type: EChart2DModifierType.Cursor,

options: {

// Optional properties to configure what parts are shown

showTooltip: true,

showAxisLabels: true,

showXLine: true,

showYLine: true,

// How close to a datapoint to show the tooltip? 10 = 10 pixels. 0 means always

hitTestRadius: 10,

// Optional properties to configure the axis labels

axisLabelFill: "#b36200",

axisLabelStroke: "#fff",

// Optional properties to configure line and tooltip style

crosshairStroke: "#ff6600",

crosshairStrokeThickness: 1,

tooltipContainerBackground: "#000",

tooltipTextStroke: "#ff6600"

}

}

]

});

This results in the following output:

Many of the properties here are optional - they have been included to show the configuration possibilities for the cursor. See ICursorModifierOptions📘 for more.