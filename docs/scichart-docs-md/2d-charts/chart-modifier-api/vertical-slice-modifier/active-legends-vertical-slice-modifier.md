---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/vertical-slice-modifier/active-legends-vertical-slice-modifier
scraped_at: 2025-11-28T18:24:19.371108
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/vertical-slice-modifier/active-legends-vertical-slice-modifier

# Active Legends - VerticalSliceModifier output to a Legend

**Background reading:** If you haven't already, read the article The VerticalSliceModifier Type which will show you how to setup a VerticalSliceModifier📘 with default options for tooltips.

This article goes into further detail on customising the tooltip items (formatting, text content)

## VerticalSliceModifier tooltipLegendTemplates

The VerticalSliceModifier📘 supports a tooltipLegendTemplate📘 property which allows you to specify a function to transform VerticalSliceModifier📘 content into a legend which can be placed in the top left of the chart. This active legend updates with series values as you drag the vertical lines, or when a series updates.

The tooltipLegendTemplate📘 property expects a function in the following format (see TRolloverLegendSvgTemplate📘):

- tooltipLegendTemplate function signature

`TRolloverLegendSvgTemplate: (`

seriesInfos: SeriesInfo[],

svgAnnotation: RolloverLegendSvgAnnotation

) => string

The input/output parameters are:

In/Out | Parameter | Description |
|---|---|---|
Input | seriesInfos | an array of SeriesInfo📘: a data object which stores info about the series that intersects the Vertical Line |
Input | svgAnnotation | The RolloverLegendSvgAnnotation📘 that will be used to render the legend. From here you can access properties of the underlying legend container, such as tooltipLegendOffsetX📘 / Y or tooltipLegendTemplate📘 |
Return | string[] | A string containing the result SVG to display inside the RolloverLegendSvgAnnotation📘 |

Let's create a simple example which shows you how to access properties on XySeriesInfo📘 and output to a custom legend.

Here's a worked example below, which shows how to place the hit-test result from a vertical line into an active legend elsewhere in your application.

- TS

`// Create a tooltip legend template`

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

<text x="8" y="20" font-size="15" font-family="Verdana" fill="lightblue">Custom VerticalSlice Legend</text>

${outputSvgString}

</svg>`;

};

// Apply it to a VerticalSliceModifier

const vSlice = new VerticalSliceModifier({

x1: 30.0,

xCoordinateMode: ECoordinateMode.DataValue,

isDraggable: true,

showRolloverLine: true,

rolloverLineStrokeThickness: 1,

rolloverLineStroke: "#50C7E0",

lineSelectionColor: "#50C7E0",

showTooltip: true,

// Optional: Overrides the legend template to display additional info top-left of the chart

tooltipLegendTemplate: getTooltipLegendTemplate

});

sciChartSurface.chartModifiers.add(vSlice);

This results in the following output:

## Using External placementDivId with the VerticalSliceModifier

Another way you can control the placement of the VerticalSliceModifier📘 tooltip is using the placementDivId📘 property. This places the standard VerticalSliceModifier tooltip into a div of your choice (which can be anywhere on the app).

Note, it does not currently work with tooltipLegendTemplate📘, however we are working on more options for styling, placement and configuration of tooltips soon.

Try the following code in your application:

- TS

`// Create a VerticalSliceModifier and add to the chart`

const vSlice = new VerticalSliceModifier({

x1: 30.0,

xCoordinateMode: ECoordinateMode.DataValue,

isDraggable: true,

showRolloverLine: true,

rolloverLineStrokeThickness: 1,

rolloverLineStroke: "#50C7E0",

lineSelectionColor: "#50C7E0",

showTooltip: true,

// Optional: Places the tooltip output in a div with id="legend-root"

placementDivId: "legend-root"

});

sciChartSurface.chartModifiers.add(vSlice);

- HTML

`<body>`

<div id="container">

<div id="scichart-root"></div>

<div id="legend-root"></div>

</div>

</body>

- CSS

`body {`

margin: 0;

}

#container {

width: 100%;

height: 100vh;

position: relative;

}

#scichart-root {

width: 100%;

height: 100%;

position: relative;

}

#legend-root {

position: absolute;

left: 20px;

top: 20px;

}

This results in the following output.