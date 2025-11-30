---
source: https://www.scichart.com/documentation/js/v4/3d-charts/chart-modifier-3d-api/tooltip-modifier-3d
scraped_at: 2025-11-28T18:24:55.465194
---

# https://www.scichart.com/documentation/js/v4/3d-charts/chart-modifier-3d-api/tooltip-modifier-3d

# Tooltip Modifier 3D

Tooltips in SciChart.js 3D are performed by the TooltipModifier3D📘. This is a ChartModifierBase3D📘 derived type which executes on touch over the data point and shows tooltips for the data-points under the mouse.

## Declaring a TooltipModifier3D

Declaring a TooltipModifier3D📘 is as simple as adding one to the SciChart3DSurface.chartModifiers📘 property. This can be done as a single modifier, or as part of a group.

- TS
- HTML
- CSS

`// Declare a tooltip and add to the chart like this.`

// Optional parameters help define tooltip operation

const tooltipModifier = new TooltipModifier3D({

isCrosshairVisible: true,

crosshairStroke: "#83D2F5",

crosshairStrokeThickness: 3,

tooltipContainerBackground: "#537ABD",

tooltipTextStroke: "White",

tooltipLegendOffsetX: 10,

tooltipLegendOffsetY: 10

});

sciChart3DSurface.chartModifiers.add(tooltipModifier);

`<div class="wrapper">`

<div id="scichart-root"></div>

<div class="titleWrapper">

<p class="title">SciChart.js 3D Chart Example</p>

<p class="subTitle">Hover the points to see tooltips</p>

</div>

</div>

`body {`

margin: 0;

font-family: Arial;

}

.wrapper {

width: 100%;

height: 100vh;

position: relative;

}

#scichart-root {

width: 100%;

height: 100%;

position: relative;

}

.titleWrapper {

position: absolute;

width: 100%;

top: 35%;

text-align: center;

pointer-events: none;

color: #ffffff77;

}

.title {

font-size: 20px;

}

.subTitle {

font-size: 16px;

}

This results in the following behaviour added to the chart.

## Styling the Tooltip Output

### Properties which affect Tooltip style

Some simple properties which affect the tooltip style are:

| Property | Description |
|---|---|
isCrosshairVisible | When true (default), a crosshair is drawn from the hovered datapoint to the far axis wall. |
crosshairStroke | The stroke color as a Hex code of the crosshair line. |
crosshairStrokeThickness | The stroke thickness of the crosshair line. |
tooltipContainerBackground | The background color of the tooltip container as a Hex code. |
tooltipLegendOffsetX / Y | Offset in pixels of the tooltip from the hovered datapoint. |
tooltipTextStroke | The text color on the tooltip. |

For further customisation of the tooltip content & container, read on.

### Tooltip Text Formatting

Tooltips obey formatting rules on the Axis. These can be defined by setting axis.labelProvider.cursorPrecision📘, cursorNumericFormat📘 or overriding formatCursorLabel📘. For more information on text formatting, see the LabelProvider documentation.

### Modifying the Tooltip Content

You can modify the content output by tooltip via the **TooltipModifier3D.tooltipDataTemplate** property. This accepts a function with **SeriesInfo3D** and **TooltipSvgAnnotation3D** arguments where you can access data about the series that was hit.

- TS
- HTML
- CSS

`// Declare a tooltip and add to the chart`

const tooltipModifier = new TooltipModifier3D({

crosshairStroke: "#83D2F5",

crosshairStrokeThickness: 3,

tooltipContainerBackground: "#537ABD",

tooltipTextStroke: "White",

tooltipLegendOffsetX: 10,

tooltipLegendOffsetY: 10

});

sciChart3DSurface.chartModifiers.add(tooltipModifier);

// Customize the tooltip content

tooltipModifier.tooltipDataTemplate = (seriesInfo, svgAnnotation) => {

// Create an array to hold strings (lines) to show in the tooltip

const valuesWithLabels = [];

if (seriesInfo && seriesInfo.isHit) {

// You can access the renderableSeries which was hit via the seriesInfo

const renderableSeries = seriesInfo.renderableSeries;

// And the parent Chart from that

const parentSurface = renderableSeries.parentSurface;

// Push lines to the array to display in the tooltip

valuesWithLabels.push(`dataSeriesName: "${seriesInfo.dataSeriesName}"`);

valuesWithLabels.push(` ${parentSurface.xAxis.axisTitle}: ${seriesInfo.xValue.toFixed(2)}`);

valuesWithLabels.push(` ${parentSurface.yAxis.axisTitle}: ${seriesInfo.yValue.toFixed(2)}`);

valuesWithLabels.push(` ${parentSurface.zAxis.axisTitle}: ${seriesInfo.zValue.toFixed(2)}`);

// access the metadata (if exists)". Any JS object on the data-points can be accessed

// in tooltips

const md = (seriesInfo as XyzSeriesInfo3D).pointMetadata as TMyMetadata;

if (md) {

valuesWithLabels.push(` Metadata: "${md.customString}"`);

}

}

return valuesWithLabels;

};

`<div class="wrapper">`

<div id="scichart-root"></div>

<div class="titleWrapper">

<p class="title">SciChart.js 3D Chart Example</p>

<p class="subTitle">Hover the points to see tooltips</p>

</div>

</div>

`body {`

margin: 0;

font-family: Arial;

}

.wrapper {

width: 100%;

height: 100vh;

position: relative;

}

#scichart-root {

width: 100%;

height: 100%;

position: relative;

}

.titleWrapper {

position: absolute;

width: 100%;

top: 35%;

text-align: center;

pointer-events: none;

color: #ffffff77;

}

.title {

font-size: 20px;

}

.subTitle {

font-size: 16px;

}

This results in the following output.

The arguments to the **tooltipDataTemplate** function are **SeriesInfo3D** and **TooltipSvgAnnotation3D**. You can access any info about the series, parent chart or axis from SeriesInfo3D. Inspect these types in the TypeDoc to see what properties are available.

### Modifying the Tooltip Container

The container of the tooltip can be modified as well. Extending the example above further, we override **TooltipModifier3D.tooltipSvgTemplate** to customize the background/foreground color before rendering the tooltip.

- TS
- HTML
- CSS

`// Declare a tooltip and add to the chart`

const tooltipModifier = new TooltipModifier3D({

crosshairStroke: "#83D2F5",

crosshairStrokeThickness: 3,

tooltipContainerBackground: "#537ABD",

tooltipTextStroke: "White",

tooltipLegendOffsetX: 10,

tooltipLegendOffsetY: 10

});

// Customize the tooltip container like this

const defaultTemplate = tooltipModifier.tooltipSvgTemplate;

tooltipModifier.tooltipSvgTemplate = (seriesInfo, svgAnnotation) => {

if (seriesInfo) {

const md = (seriesInfo as XyzSeriesInfo3D).pointMetadata;

const backgroundColor = md ? parseArgbToHtmlColor(md.vertexColor) : seriesInfo.renderableSeries.stroke;

svgAnnotation.containerBackground = backgroundColor;

svgAnnotation.textStroke = "white";

}

return defaultTemplate(seriesInfo, svgAnnotation);

};

sciChart3DSurface.chartModifiers.add(tooltipModifier);

`<div class="wrapper">`

<div id="scichart-root"></div>

<div class="titleWrapper">

<p class="title">SciChart.js 3D Chart Example</p>

<p class="subTitle">Hover the points to see tooltips</p>

</div>

</div>

`body {`

margin: 0;

font-family: Arial;

}

.wrapper {

width: 100%;

height: 100vh;

position: relative;

}

#scichart-root {

width: 100%;

height: 100%;

position: relative;

}

.titleWrapper {

position: absolute;

width: 100%;

top: 35%;

text-align: center;

pointer-events: none;

color: #ffffff77;

}

.title {

font-size: 20px;

}

.subTitle {

font-size: 16px;

}

This results in the following output:

## Placing the Tooltip as a Separate Legend

The tooltip can be placed as a legend in the corner of the chart by using the **TooltipModifier3D.placementDivId** property. This simply changes the location in the HTML Dom where tooltips are placed.

Here's a quick example:

- TS
- HTML
- CSS

`// Declare a tooltip and add to the chart like this.`

const tooltipModifier = new TooltipModifier3D({

crosshairStroke: "#83D2F5",

crosshairStrokeThickness: 3,

tooltipContainerBackground: "#537ABD",

tooltipTextStroke: "White",

tooltipLegendOffsetX: 10,

tooltipLegendOffsetY: 10,

// Allows placement of tooltip in a custom div anywhere in your app

placementDivId: "tooltipContainerDivId"

});

sciChart3DSurface.chartModifiers.add(tooltipModifier);

`<div class="wrapper">`

<div id="scichart-root"></div>

<div class="titleWrapper">

<p class="title">SciChart.js 3D Chart Example</p>

<p class="subTitle">Hover the points to see tooltips</p>

</div>

<div id="tooltipContainerDivId">

<!-- Tooltips are placed here -->

</div>

</div>

`body {`

margin: 0;

font-family: Arial;

}

.wrapper {

width: 100%;

height: 100vh;

position: relative;

}

#scichart-root {

width: 100%;

height: 100%;

position: relative;

}

.titleWrapper {

position: absolute;

width: 100%;

top: 35%;

text-align: center;

pointer-events: none;

color: #ffffff77;

}

.title {

font-size: 20px;

}

.subTitle {

font-size: 16px;

}

#tooltipContainerDivId {

position: absolute;

top: 10px;

left: 10px;

pointer-events: none;

}

This results in the following output:

If you hover over data points you will notice that the tooltips appears in the left top part of the chart.