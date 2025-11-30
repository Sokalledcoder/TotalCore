---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/cursor-modifier/formatting-cursor-modifier-tooltip-items
scraped_at: 2025-11-28T18:24:15.133612
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/cursor-modifier/formatting-cursor-modifier-tooltip-items

# Formatting CursorModifier Tooltip Items

Background reading:

If you haven't already, read the article The CursorModifier Type which will show you how to setup a **CursorModifier** with default options for tooltips. This article goes into further detail on customising the tooltip items (formatting, text content)

## Basic CursorModifier Tooltip Formatting Options

Tooltip and Axis Label formatting comes from the axis.labelprovider.formatCursorLabel()📘 function and is axis-specific. You can read more about the Axis.LabelProvider API here, including how to specify formats from Enums and override formatting programmatically.

Below we're going to show you how to apply cursor formatting to enable four-decimal places on tooltips.

- TS
- Builder API (JSON Config)

`const {`

SciChartSurface,

NumericAxis,

FastLineRenderableSeries,

XyDataSeries,

SciChartJsNavyTheme,

ENumericFormat,

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

sciChartSurface.xAxes.add(

new NumericAxis(wasmContext, {

// label format options applied to the X-Axis

labelPrecision: 2,

labelFormat: ENumericFormat.Decimal,

// label format options applied to cursors & tooltips

cursorLabelPrecision: 4,

cursorLabelFormat: ENumericFormat.Decimal

})

);

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

// label format options applied to the X-Axis

labelPrecision: 1,

labelFormat: ENumericFormat.Decimal,

// label format options applied to cursors & tooltips

cursorLabelPrecision: 4,

cursorLabelFormat: ENumericFormat.Decimal

})

);

// Add a CursorModifier to the chart

const cursorModifier = new CursorModifier({

showTooltip: true,

showAxisLabels: true,

hitTestRadius: 10

});

sciChartSurface.chartModifiers.add(cursorModifier);

`const { chartBuilder, EThemeProviderType, EAxisType, EChart2DModifierType, ENumericFormat } = SciChart;`

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: {

type: EAxisType.NumericAxis,

options: {

// label format options applied to the X-Axis

labelPrecision: 2,

labelFormat: ENumericFormat.Decimal,

// label format options applied to cursors & tooltips

cursorLabelPrecision: 4,

cursorLabelFormat: ENumericFormat.Decimal

}

},

yAxes: {

type: EAxisType.NumericAxis,

options: {

// label format options applied to the X-Axis

labelPrecision: 2,

labelFormat: ENumericFormat.Decimal,

// label format options applied to cursors & tooltips

cursorLabelPrecision: 4,

cursorLabelFormat: ENumericFormat.Decimal

}

},

modifiers: [

{

type: EChart2DModifierType.Cursor,

options: {

showTooltip: true,

showAxisLabels: true,

hitTestRadius: 10

}

}

]

});

Here's a **Codepen** which shows the effect of these properties on the axis on cursor tooltips:

For further customisation on a per-axis basis, consider using the LabelProvider feature to create a custom labelprovider, and override formatCursorLabel.

## Tooltip DataTemplates

Further customisation of tooltip content can be achieved with the CursorModifier.tooltipDataTemplate📘 property. This defines the content inside the tooltip e.g. what values are shown (x, y, values from metadata), if the series name is shown and so on.

This property expects a function in the following format (see TCursorTooltipDataTemplate📘):

- tooltipDataTemplate function signature

`tooltipDataTemplate: (`

seriesInfos: SeriesInfo[],

tooltipTitle: string

) => string[];

The input/output parameters are:

**Input**: an array of SeriesInfo📘: a data object which stores info about the series under the mouse.**Input**: a tooltipTitle (string) which comes from renderableSeries.rolloverModifierProps.tooltipTitle📘.**Output**: an array of strings, each one corresponding to a line in the tooltip.

Let's create a simple example which shows you how to access properties on XySeriesInfo📘 and output to tooltips.

- TS
- Builder API (JSON Config)

`// Create a chart surface`

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme(),

titleStyle: { fontSize: 16 }

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

// Add a CursorModifier to the chart

const cursorModifier = new CursorModifier({

showTooltip: true,

showAxisLabels: true,

hitTestRadius: 10,

// Add a custom tooltip data template

tooltipDataTemplate: (seriesInfos, tooltipTitle) => {

// each element in this array = 1 line in the tooltip

const lineItems = [];

// See SeriesInfo docs at https://www.scichart.com/documentation/js/v4/typedoc/classes/xyseriesinfo.html

seriesInfos.forEach(si => {

// If hit (within hitTestRadius of point)

if (si.isHit) {

// SeriesInfo.seriesName comes from dataSeries.dataSeriesName

lineItems.push(`${si.seriesName}`);

// seriesInfo.xValue, yValue are available to be formatted

// Or, preformatted values are available as si.formattedXValue, si.formattedYValue

lineItems.push(`X: ${si.xValue.toFixed(2)}`);

lineItems.push(`Y: ${si.yValue.toFixed(2)}`);

// index to the dataseries is available

lineItems.push(`Index: ${si.dataSeriesIndex}`);

// Which can be used to get anything from the dataseries

lineItems.push(

`Y-value from dataSeries: ${si.renderableSeries.dataSeries

.getNativeYValues()

.get(si.dataSeriesIndex)

.toFixed(4)}`

);

// Location of the hit in pixels is available

lineItems.push(`Location: ${si.xCoordinate.toFixed(0)}, ${si.yCoordinate.toFixed(0)}`);

}

});

return lineItems;

}

});

sciChartSurface.chartModifiers.add(cursorModifier);

`// Demonstrates how to configure the PinchZoomModifier in SciChart.js using the Builder API`

const { chartBuilder, EThemeProviderType, EAxisType, EChart2DModifierType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

modifiers: [

{

type: EChart2DModifierType.Cursor,

options: {

showTooltip: true,

showAxisLabels: true,

hitTestRadius: 10,

// Add a custom tooltip data template

tooltipDataTemplate: (seriesInfos, tooltipTitle) => {

// each element in this array = 1 line in the tooltip

const lineItems = [];

// See SeriesInfo docs at https://www.scichart.com/documentation/js/v4/typedoc/classes/xyseriesinfo.html

seriesInfos.forEach(si => {

// If hit (within hitTestRadius of point)

if (si.isHit) {

// SeriesInfo.seriesName comes from dataSeries.dataSeriesName

lineItems.push(`${si.seriesName}`);

// seriesInfo.xValue, yValue are available to be formatted

// Or, preformatted values are available as si.formattedXValue, si.formattedYValue

lineItems.push(`X: ${si.xValue.toFixed(2)}`);

lineItems.push(`Y: ${si.yValue.toFixed(2)}`);

// index to the dataseries is available

lineItems.push(`Index: ${si.dataSeriesIndex}`);

// Which can be used to get anything from the dataseries

lineItems.push(

`Y-value from dataSeries: ${si.renderableSeries.dataSeries

.getNativeYValues()

.get(si.dataSeriesIndex)

.toFixed(4)}`

);

// Location of the hit in pixels is available

lineItems.push(`Location: ${si.xCoordinate.toFixed(0)}, ${si.yCoordinate.toFixed(0)}`);

}

});

return lineItems;

}

}

}

]

});

This results in the following output

## Accessing Metadata in Tooltip DataTemplates

In the above example we access properties of XySeriesInfo📘 to format lines in the CursorModifier tooltip.

You can also access metadata to store any custom object in your X,Y data, then read that data out in tooltips.

For a worked example see PointMetadata API - Metadata and Tooltips.