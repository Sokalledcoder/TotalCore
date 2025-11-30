---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/cursor-modifier/customizing-cursor-modifier-tooltip-container-appearance
scraped_at: 2025-11-28T18:24:14.899664
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/cursor-modifier/customizing-cursor-modifier-tooltip-container-appearance

# Customizing the CursorModifier Tooltip Container Appearance

Background reading:

If you haven't already, read the article The CursorModifier type which will show you how to setup a CursorModifier with default options for tooltips. This article goes into further detail on customising the tooltip items (formatting, text content)

Basic customisation of the cursor and tooltip appearance can be made through the following properties.

- The crosshair line thickness and stroke color can be changed with the crosshairStrokeThickness📘 and crosshairStroke📘 properties.
- Axis labels can be turned on/off via the showAxisLabels📘 property.
- The tooltip can be turned on/off (to have a simple cursor) with the showTooltip📘 property.
- Axis Label backgrounds and text color can be changed with the axisLabelStroke📘, axisLabelFill📘 properties.
- The tooltip background and text color can be changed with the tooltipContainerBackground📘 and tooltipTextStroke📘 properties.

Deeper customisation of the tooltip appearance can be achieved via the tooltipSvgTemplate📘 property.

This defines the actual SVG used to host the tooltip container. This property expects a function in the following format (see TCursorTooltipSvgTemplate📘):

- cursorTooltipSvgTemplate function signature

` cursorTooltipSvgTemplate: (`

seriesInfos: SeriesInfo[],

svgAnnotation: CursorTooltipSvgAnnotation

) => string

Where the input/output parameters are:

**Input**: an array of SeriesInfo📘: a data object which stores info about the series under the mouse.**Input**: svgAnnotation (CursorTooltipSvgAnnotation📘) which is the current tooltip SVG annotation**Output**: string, containing the new SVG to define the tooltip container.

Let's create a simple example which shows you how to customize the tooltip container.

- TS

`const tooltipSvgTemplate = (seriesInfos, svgAnnotation) => {`

const width = 120;

const height = 120;

const seriesInfo = seriesInfos[0];

if (!seriesInfo?.isWithinDataBounds) {

return "<svg></svg>";

}

let seriesName;

let xValue;

let yValue;

let index;

let yValueFromDS;

seriesInfos.forEach(si => {

// If hit (within hitTestRadius of point)

if (si.isHit) {

// SeriesInfo.seriesName comes from dataSeries.dataSeriesName

seriesName = si.seriesName;

// seriesInfo.xValue, yValue

xValue = si.xValue.toFixed(2);

yValue = si.yValue.toFixed(2);

// index to the dataseries is available

index = si.dataSeriesIndex;

// Which can be used to get anything from the dataseries

yValueFromDS = si.renderableSeries.dataSeries.getNativeYValues().get(si.dataSeriesIndex).toFixed(4);

}

});

if (!seriesName) {

return "<svg></svg>";

}

const x = seriesInfo ? seriesInfo.formattedXValue : "";

const y = seriesInfo ? seriesInfo.formattedYValue : "";

// this calculates and sets svgAnnotation.xCoordShift and svgAnnotation.yCoordShift. Do not set x1 or y1 at this point.

adjustTooltipPosition(width, height, svgAnnotation);

return `

<svg width="${width}" height="${height}">

<rect x="0" y="0" rx="${seriesName === "Sinewave 1" ? "10" : "100"}" ry="${seriesName === "Sinewave 1" ? "10" : "100"}" width="${width}" height="${height}" fill="${seriesName === "Sinewave 1" ? "#FF6600" : "#50C7E0"}"/>

<text y="35" font-family="Verdana" font-size="12" fill="white">

<tspan x="50%" text-anchor="middle" font-size="14">${seriesName}</tspan>

<tspan x="50%" text-anchor="middle" dy="2.4em">x: ${xValue}</tspan>

<tspan x="50%" text-anchor="middle" dy="1.2em">y: ${yValue}</tspan>

<tspan x="50%" text-anchor="middle" dy="1.2em">index: ${index}</tspan>

</text>

</svg>`;

};

// Add a CursorModifier to the chart

const cursorModifier = new CursorModifier({

showTooltip: true,

showAxisLabels: true,

hitTestRadius: 10,

tooltipSvgTemplate

});

sciChartSurface.chartModifiers.add(cursorModifier);

This results in the following output: