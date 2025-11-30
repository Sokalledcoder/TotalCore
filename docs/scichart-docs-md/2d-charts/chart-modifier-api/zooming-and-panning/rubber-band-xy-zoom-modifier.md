---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/zooming-and-panning/rubber-band-xy-zoom-modifier
scraped_at: 2025-11-28T18:24:20.387351
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/zooming-and-panning/rubber-band-xy-zoom-modifier

# RubberBandXyZoomModifier

SciChart.js provides the ability to Drag an area to zoom the chart (known as Rubber-band zoom) using the RubberBandXyZoomModifier📘, available out of the box.

Besides common features which are inherited from the ChartModifierBase class, the RubberBandXyZoomModifier📘 allows animated zooming via the isAnimated📘, animationDuration📘 and easingFunction📘 properties. The drag rectangle can be styled via the fill📘, stroke📘 and strokeThickness📘 properties.

## Adding a RubberBandXyZoomModifier to a Chart

A RubberBandXyZoomModifier📘 can be added to the sciChartSurface.chartModifiers📘 collection to enable zoom to fit behavior. For example:

- TS
- Builder API (JSON Config)

`import { RubberBandXyZoomModifier, easing } from "scichart";`

// Add Zoom Extents behavior

const rubberBandXyZoomModifier = new RubberBandXyZoomModifier({

isAnimated: true,

animationDuration: 400,

easingFunction: easing.outExpo,

fill: "#FFFFFF33",

stroke: "#FFFFFF77",

strokeThickness: 1,

});

sciChartSurface.chartModifiers.add(rubberBandXyZoomModifier);

`// Demonstrates how to configure the RubberBand Zoom Modifier in SciChart.js using the Builder API`

const { chartBuilder, EChart2DModifierType, easing } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

modifiers: [

{

type: EChart2DModifierType.RubberBandXYZoom,

options: {

isAnimated: true,

animationDuration: 400,

easingFunction: easing.outExpo,

fill: "#FFFFFF33",

stroke: "#FFFFFF77",

strokeThickness: 1,

}

}

]

});

This results in the following behavior when dragging the chart: