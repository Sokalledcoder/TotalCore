---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/vertical-slice-modifier/vertical-slice-modifier-overview
scraped_at: 2025-11-28T18:24:19.661324
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/vertical-slice-modifier/vertical-slice-modifier-overview

# The VerticalSliceModifier Type

With the VerticalSliceModifier📘, SciChart.js provides the ability to place multiple vertical lines on the chart, which can show tooltips intersecting chart series.

This provides a similar behaviour to the RolloverModifier, except instead of a single vertical line plus tooltips which track the mouse, you can place multiple draggable vertical lines on the chart, which intersect line series and display tooltips.

The VerticalSliceModifier📘 allows you to:

- Place one or more vertical lines on the chart at data-values, relative coordinates or pixel coordinates
- Vertical lines intersect chart series
- Tooltips may be displayed at the intersections
- Optionally show/hide or customize the tooltip content
- Vertical lines may be dragged or edited
- Vertical lines may be removed from the chart.

The Using VerticalSliceModifier Example can be found in the SciChart.Js Examples Suite on Github, or our live demo at scichart.com/demo

## Adding a VerticalSliceModifier to a Chart

One or more VerticalSliceModifiers📘 can be added to the sciChartSurface.chartModifiers📘 collection to enable draggable lines with crosshair/cursor behavior. For example, this code adds a crosshair, enables default tooltips and allows dragging of the vertical lines.

- TS
- Builder API (JSON Config)

`// Create a chart surface`

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme(),

titleStyle: { fontSize: 16 }

});

// For the example to work, axis must have EAutoRange.Always

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { axisTitle: "X Axis" }));

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

visibleRange: new NumberRange(-2, 0.5),

axisTitle: "Y Axis"

})

);

// Add some vertical slices to the chart

const vSlice1 = new VerticalSliceModifier({

x1: 10.1,

xCoordinateMode: ECoordinateMode.DataValue,

isDraggable: true,

// Defines if rollover vertical line is shown

showRolloverLine: true,

rolloverLineStrokeThickness: 1,

rolloverLineStroke: "#FF6600",

lineSelectionColor: "#FF6600",

// Shows the default tooltip

showTooltip: true

});

const vSlice2 = new VerticalSliceModifier({

x1: 30.0,

xCoordinateMode: ECoordinateMode.DataValue,

isDraggable: true,

// Defines if rollover vertical line is shown

showRolloverLine: true,

rolloverLineStrokeThickness: 1,

rolloverLineStroke: "#50C7E0",

lineSelectionColor: "#50C7E0",

// Shows the default tooltip

showTooltip: true

});

sciChartSurface.chartModifiers.add(vSlice1, vSlice2);

`// Demonstrates how to configure the VerticalSliceModifier in SciChart.js using the Builder API`

const { chartBuilder, EThemeProviderType, ECoordinateMode, EChart2DModifierType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

modifiers: [

{

type: EChart2DModifierType.VerticalSlice,

options: {

x1: 10.1,

xCoordinateMode: ECoordinateMode.DataValue,

isDraggable: true,

// Defines if rollover vertical line is shown

showRolloverLine: true,

rolloverLineStrokeThickness: 1,

rolloverLineStroke: "#FF6600",

lineSelectionColor: "#FF6600",

// Shows the default tooltip

showTooltip: true

}

},

{

type: EChart2DModifierType.VerticalSlice,

options: {

x1: 30.0,

xCoordinateMode: ECoordinateMode.DataValue,

isDraggable: true,

// Defines if rollover vertical line is shown

showRolloverLine: true,

rolloverLineStrokeThickness: 1,

rolloverLineStroke: "#50C7E0",

lineSelectionColor: "#50C7E0",

// Shows the default tooltip

showTooltip: true

}

}

]

});

This results in the following output:

Many of the properties here are optional - they have been included to show the configuration possibilities for the cursor. See IVerticalSliceOptions📘 for more.

## Removing a VerticalSliceModifier from the Chart

`sciChartSurface.chartModifiers.remove(vSlice);`

## Styling & Visibility of VerticalSliceModifier Elements

The following elements can be turned on or off when using the VerticalSliceModifier📘.

- VerticalSliceModifier visibility

`verticalSliceModifier.showTooltip = true; // Show or hide the tooltip`

verticalSliceModifier.showRolloverLine = true; // Show or hide the vertical line

verticalSliceModifier.verticalLine.showLabel = true; // Show or hide the X-Axis label

In addition, the line may be made editable (draggable) by setting the isDraggable📘 property

- VerticalSliceModifier editing

`verticalSliceModifier.isDraggable = true; // Enable or disable dragging of the line`

The line colour, dash pattern, strokethickness and selection color of the VerticalSliceModifier📘 can also be set. e.g.

Property | Description |
|---|---|
| VerticalSliceModifier.rolloverLineStroke📘 | Sets the colour of the rollover line as an HTML colour code |
| VerticalSliceModifier.rolloverLineStrokeDashArray📘 | Sets the dash pattern (see Dash Line Styling for guidelines) |
| VerticalSliceModifier.rolloverLineStrokeThickness📘 | Sets the rollover line thickness |

- VerticalSliceModifier styling

`verticalSliceModifier.rolloverLineStrokeThickness = 1; // Sets the line thickness`

verticalSliceModifier.rolloverLineStroke = "Orange"; // Sets the line colour

verticalSliceModifier.lineSelectionColor = "Red"; // Change the highlight color when selected

Properties of the tooltip can be controlled on a per-series basis as per the RolloverModifier via the RenderableSeries.rolloverModifierProps📘 property

Property | Description |
|---|---|
| series.rolloverModifierProps.tooltipTextColor📘 | The text foreground color of the tooltip, on a per-series basis |
| series.rolloverModifierProps.tooltipColor📘 | The tooltip container color on a per-series basis |
| series.rolloverModifierProps.tooltipLabelX📘 | Prefix label in the tooltip for X values. Defaults to 'X: ' |
| series.rolloverModifierProps.tooltipLabelY📘 | Prefix label in the tooltip for Y values. Defaults to 'Y: ' |

- VerticalSliceModifier Tooltip styling

`// On a per series basis, you can control the tooltip background/foreground`

series.rolloverModifierProps.tooltipTextColor = "White";

series.rolloverModifierProps.tooltipColor = "Red";

series.rolloverModifierProps.tooltipLabelX = "X Value:";

series.rolloverModifierProps.tooltipLabelY = "Y Value:";

Finally, the vertical line itself is simply a LineAnnotation so all the properties there may be accessed via the verticalSliceModifier.verticalLine📘 property after instantiation.

- VerticalSliceModifier.verticalLine Styling

`// Add some vertical slices to the chart`

const vSlice1 = new VerticalSliceModifier({

// options ...

});

vSlice1.verticalLine.showLabel = true; // Show axis label

vSlice1.verticalLine.axisLabelFill = "#FF6600"; // Style axis label outline and font

vSlice1.verticalLine.axisLabelStroke = "White";