---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/vertical-slice-modifier/formatting-vertical-slice-tooltip-items
scraped_at: 2025-11-28T18:24:19.276234
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/vertical-slice-modifier/formatting-vertical-slice-tooltip-items

# Formatting VerticalSlice Tooltip Items

**Background reading:** If you haven't already, read the article The VerticalSliceModifier Type which will show you how to setup a VerticalSliceModifier📘 with default options for tooltips.

This article goes into further detail on customising the tooltip items (formatting, text content)

## Basic VerticalSliceModifier Tooltip Formatting Options

The VerticalSliceModifier📘 obeys similar rules to the CursorModifier and RolloverModifier for customizing the tooltip content and appearance.

Tooltip and Axis Label formatting comes from the axis.labelprovider.formatCursorLabel()📘 function and is axis-specific. You can read more about the Axis.LabelProvider API here, including how to specify formats from Enums and override formatting programmatically.

Below we're going to show you how to apply tooltip formatting to enable four-decimal places on VerticalSliceModifier📘 tooltips.

- TS
- Builder API (JSON Config)

`// Create a chart surface`

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme(),

titleStyle: { fontSize: 16 }

});

// For the example to work, axis must have EAutoRange.Always

sciChartSurface.xAxes.add(

new NumericAxis(wasmContext, {

axisTitle: "X Axis",

// label format options applied to the X-Axis

labelPrecision: 1,

labelFormat: ENumericFormat.Decimal,

// label format options applied to cursors & tooltips

cursorLabelPrecision: 2,

cursorLabelFormat: ENumericFormat.Decimal

})

);

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

visibleRange: new NumberRange(-2, 0.5),

axisTitle: "Y Axis",

// label format options applied to the X-Axis

labelPrecision: 1,

labelFormat: ENumericFormat.Decimal,

// label format options applied to cursors & tooltips

cursorLabelPrecision: 6,

cursorLabelFormat: ENumericFormat.Decimal

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

vSlice1.verticalLine.showLabel = true;

vSlice1.verticalLine.axisLabelFill = "#FF6600";

vSlice1.verticalLine.axisLabelStroke = "White";

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

vSlice2.verticalLine.showLabel = true;

vSlice2.verticalLine.axisLabelFill = "#50C7E0";

vSlice2.verticalLine.axisLabelStroke = "White";

sciChartSurface.chartModifiers.add(vSlice1, vSlice2);

`// Demonstrates how to configure the PinchZoomModifier in SciChart.js using the Builder API`

const {

chartBuilder,

EThemeProviderType,

ECoordinateMode,

EChart2DModifierType,

ENumericFormat,

EAxisType,

NumberRange

} = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: {

type: EAxisType.NumericAxis,

options: {

axisTitle: "X Axis",

// label format options applied to the X-Axis

labelPrecision: 1,

labelFormat: ENumericFormat.Decimal,

// label format options applied to cursors & tooltips

cursorLabelPrecision: 2,

cursorLabelFormat: ENumericFormat.Decimal

}

},

yAxes: {

type: EAxisType.NumericAxis,

options: {

visibleRange: new NumberRange(-2, 0.5),

axisTitle: "Y Axis",

// label format options applied to the X-Axis

labelPrecision: 1,

labelFormat: ENumericFormat.Decimal,

// label format options applied to cursors & tooltips

cursorLabelPrecision: 6,

cursorLabelFormat: ENumericFormat.Decimal

}

},

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

Here's a **Codepen** which shows the effect of these properties on the axis on cursor tooltips.

For further customisation on a per-axis basis, consider using the LabelProvider feature to create a custom labelprovider, and override formatCursorLabel.

## Tooltip DataTemplates

Further customisation of VerticalSliceModifier📘 tooltip content can be achieved with the VerticalSliceModifier.tooltipDataTemplate📘 property. This defines the content inside the tooltip e.g. what values are shown (x, y, values from metadata), if the series name is shown and so on.

This property expects a function in the following format (see TRolloverTooltipDataTemplate📘):

- tooltipDataTemplateFunction

`TRolloverTooltipDataTemplate: (`

seriesInfo: SeriesInfo,

tooltipTitle: string,

tooltipLabelX: string,

tooltipLabelY: string

) => string[]

The input/output parameters are:

In/Out | Parameter | Description |
|---|---|---|
Input | seriesInfo | an instance of SeriesInfo📘: a data object which stores info about the series that intersects the Vertical Line |
Input | tooltipTitle | a tooltipTitle (string) which comes from renderableSeries.rolloverModifierProps.tooltipTitle📘. |
Input | tooltipLabelX | A prefix (string) which comes from renderableSeries.rolloverModifierProps.tooltipLabelX📘 |
Input | tooltipLabelY | A prefix (string) which comes from renderableSeries.rolloverModifierProps.tooltipLabelY📘 |
Return | string[] | An array of strings, each one corresponding to a line in the tooltip |

Let's create a simple example which shows you how to access properties on XySeriesInfo📘 and output to tooltips.

- TS
- Builder API (JSON Config)

`// Add a custom tooltip data template`

const tooltipDataTemplate = (seriesInfo, tooltipTitle, tooltipLabelX, tooltipLabelY) => {

// each element in this array = 1 line in the tooltip

const lineItems = [];

// See SeriesInfo docs at https://www.scichart.com/documentation/js/v4/typedoc/classes/xyseriesinfo.html

// SeriesInfo.seriesName comes from dataSeries.dataSeriesName

lineItems.push(`${seriesInfo.seriesName}`);

// seriesInfo.xValue, yValue are available to be formatted

// Or, preformatted values are available as si.formattedXValue, si.formattedYValue

lineItems.push(`X: ${seriesInfo.xValue.toFixed(2)}`);

lineItems.push(`Y: ${seriesInfo.yValue.toFixed(2)}`);

// index to the dataseries is available

lineItems.push(`Index: ${seriesInfo.dataSeriesIndex}`);

// Which can be used to get anything from the dataseries

lineItems.push(

`Y-value from dataSeries: ${seriesInfo.renderableSeries.dataSeries

.getNativeYValues()

.get(seriesInfo.dataSeriesIndex)

.toFixed(4)}`

);

// Location of the hit in pixels is available

lineItems.push(`Location: ${seriesInfo.xCoordinate.toFixed(0)}, ${seriesInfo.yCoordinate.toFixed(0)}`);

return lineItems;

};

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

showTooltip: true,

// The tooltip data template

tooltipDataTemplate

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

showTooltip: true,

// The tooltip data template

tooltipDataTemplate

});

sciChartSurface.chartModifiers.add(vSlice1, vSlice2);

`// Demonstrates how to configure the PinchZoomModifier in SciChart.js using the Builder API`

const {

chartBuilder,

EThemeProviderType,

ECoordinateMode,

EChart2DModifierType,

} = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

// Add a custom tooltip data template

const tooltipDataTemplate = (seriesInfo, tooltipTitle, tooltipLabelX, tooltipLabelY) => {

// each element in this array = 1 line in the tooltip

const lineItems = [];

// See SeriesInfo docs at https://www.scichart.com/documentation/js/v4/typedoc/classes/xyseriesinfo.html

// SeriesInfo.seriesName comes from dataSeries.dataSeriesName

lineItems.push(`${seriesInfo.seriesName}`);

// seriesInfo.xValue, yValue are available to be formatted

// Or, preformatted values are available as si.formattedXValue, si.formattedYValue

lineItems.push(`X: ${seriesInfo.xValue.toFixed(2)}`);

lineItems.push(`Y: ${seriesInfo.yValue.toFixed(2)}`);

// index to the dataseries is available

lineItems.push(`Index: ${seriesInfo.dataSeriesIndex}`);

// Which can be used to get anything from the dataseries

lineItems.push(

`Y-value from dataSeries: ${seriesInfo.renderableSeries.dataSeries

.getNativeYValues()

.get(seriesInfo.dataSeriesIndex)

.toFixed(4)}`

);

// Location of the hit in pixels is available

lineItems.push(`Location: ${seriesInfo.xCoordinate.toFixed(0)}, ${seriesInfo.yCoordinate.toFixed(0)}`);

return lineItems;

};

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

showTooltip: true,

// Add the tooltip data template

tooltipDataTemplate

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

showTooltip: true,

// Add the tooltip data template

tooltipDataTemplate

}

}

]

});

This results in the following output