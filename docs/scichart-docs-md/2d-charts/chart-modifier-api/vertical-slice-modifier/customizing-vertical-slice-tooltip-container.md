---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/vertical-slice-modifier/customizing-vertical-slice-tooltip-container
scraped_at: 2025-11-28T18:24:19.440396
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/vertical-slice-modifier/customizing-vertical-slice-tooltip-container

# Customizing VerticalSliceModifier Tooltip Containers

**Background reading:** If you haven't already, read the article The VerticalSliceModifier Type which will show you how to setup a VerticalSliceModifier📘 with default options for tooltips.

This article goes into further detail on customising the tooltip items (formatting, text content)

## Basic Customization of VerticalSliceModifier Tooltips via properties

Basic customisation of the VerticalSliceModifier📘 appearance can be made through the following properties.

- The vertical line thickness, dash and stroke color can be changed with the VerticalSliceModifier.rolloverLineStroke📘, VerticalSliceModifier.rolloverLineStrokeThickness📘 and VerticalSliceModifier.rolloverLineStrokeDashArray📘 properties.
- The line selection color can be set via the VerticalSliceModifier.lineSelectionColor📘 property.
- The tooltip can be turned on/off (to have a simple cursor) with the VerticalSliceModifier.showTooltip📘 property.
- The tooltip background and text color can be changed with tooltipColor📘 and tooltipTextColor📘 properties, found on RenderableSeries.rolloverModifierProps📘 on a per-series basis.
- Axis labels can be turned on/off via the VerticalSliceModifier.verticalLine.showLabel📘 property, (where VerticalSliceModifier.verticalLine📘 is simply a LineAnnotation📘).
- Axis Label backgrounds and text color can be changed with the properties found on VerticalSliceModifier.verticalLine📘, such as axisLabelStroke📘, axisLabelFill📘.

## Deep Customization of VerticalSliceModifier Tooltips via SVG Templates

Deeper customisation of the tooltip appearance can be achieved via the tooltipSvgTemplate📘 property.

This defines the actual SVG used to host the tooltip container. This property expects a function in the following format (see TCursorTooltipSvgTemplate📘):

- cursotTooltipSvgTemplate function signature

`tooltipSvgTemplate: (`

seriesInfos: SeriesInfo[],

svgAnnotation: CursorTooltipSvgAnnotation

) => string

The input/output parameters are:

**Input**: an array of SeriesInfo📘: a data object which stores info about the series under the mouse.**Input**: svgAnnotation (CursorTooltipSvgAnnotation📘) which is the current tooltip SVG annotation**Output**: string, containing the new SVG to define the tooltip container.

Let's create a simple example which shows you how to customize the tooltip container.

- TS

const customTooltipTemplate = (

id, // : string

seriesInfo, // : SeriesInfo,

rolloverTooltip // : RolloverTooltipSvgAnnotation

) => {

const width = 120;

const height = 120;

rolloverTooltip.updateSize(width, height);

return `

<svg width="${width}" height="${height}">

<circle cx="50%" cy="50%" r="50%" fill="${seriesInfo.stroke}"/>

<text y="40" font-size="13" font-family="Verdana" dy="0" fill="${"white"}">

<tspan x="15" dy="1.2em">${seriesInfo.seriesName}</tspan>

<tspan x="15" dy="1.2em">x: ${seriesInfo.formattedXValue} y: ${seriesInfo.formattedYValue}</tspan>

</text>

</svg>`;

};

lineSeries1.rolloverModifierProps.tooltipTemplate = (

id, // : string

seriesInfo, // : SeriesInfo

rolloverTooltip // : RolloverTooltipSvgAnnotation

) => {

return customTooltipTemplate(id, seriesInfo, rolloverTooltip);

};

lineSeries2.rolloverModifierProps.tooltipTemplate = (

id, // : string

seriesInfo, // : SeriesInfo

rolloverTooltip // : RolloverTooltipSvgAnnotation

) => {

return customTooltipTemplate(id, seriesInfo, rolloverTooltip);

};

const getTooltipLegendTemplate = (seriesInfos, svgAnnotation) => {

let outputSvgString = "";

// Foreach series there will be a seriesInfo supplied by SciChart. This contains info about the series under the house

seriesInfos.forEach((seriesInfo, index) => {

if (seriesInfo.isWithinDataBounds) {

const lineHeight = 30;

const y = 50 + index * lineHeight;

// Use the series stroke for legend text colour

const textColor = seriesInfo.stroke;

// Use the seriesInfo formattedX/YValue for text on the

outputSvgString += `<text x="8" y="${y}" font-size="16" font-family="Verdana" fill="${textColor}">

${seriesInfo.seriesName}: X=${seriesInfo.formattedXValue}, Y=${seriesInfo.formattedYValue}

</text>`;

}

});

// Content here is returned for the custom legend placed in top-left of the chart

return `<svg width="100%" height="100%">

<text x="8" y="20" font-size="15" font-family="Verdana" fill="lightblue">Custom Rollover Legend</text>

${outputSvgString}

</svg>`;

};

const vSlice1 = new VerticalSliceModifier({

x1: 5.06,

xCoordinateMode: ECoordinateMode.DataValue,

isDraggable: true,

// Defines if rollover vertical line is shown

showRolloverLine: true,

rolloverLineStrokeThickness: 1,

rolloverLineStroke: "green",

lineSelectionColor: "green",

// Shows the default tooltip

showTooltip: true,

// Optional: Overrides the legend template to display additional info top-left of the chart

tooltipLegendTemplate: getTooltipLegendTemplate

});

const vSlice2 = new VerticalSliceModifier({

x1: 0.75,

xCoordinateMode: ECoordinateMode.Relative,

isDraggable: true,

// Defines if rollover vertical line is shown

showRolloverLine: true,

rolloverLineStrokeThickness: 1,

rolloverLineStroke: "orange",

lineSelectionColor: "orange",

// Shows the default tooltip

showTooltip: true

});

sciChartSurface.chartModifiers.add(vSlice1, vSlice2);

This results in the following output: