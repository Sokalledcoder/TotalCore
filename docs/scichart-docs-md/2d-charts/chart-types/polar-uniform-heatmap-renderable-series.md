---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/polar-uniform-heatmap-renderable-series
scraped_at: 2025-11-28T18:24:42.433102
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/polar-uniform-heatmap-renderable-series

# The Polar Uniform Heatmap Chart Type

The PolarUniformHeatmapRenderableSeries📘 displays "heat" values as colored cells in a polar (circular) coordinate system—perfect for visualizing intensity, density, or other matrix-like data in a circular form. Each cell is mapped from a two-dimensional array of z-values, with color gradients representing the data's magnitude.

The JavaScript Polar Uniform Heatmap Chart can be found in the SciChart.Js Examples Suite > Polar Uniform Heatmap Chart on Github, or our live demo at scichart.com/demo.

## Properties

Key options for IPolarUniformHeatmapRenderableSeriesOptions📘 include:

- dataSeries📘 — A UniformHeatmapDataSeries📘 containing a 2D array of
`zValues`

, and X / Y Step and Start. - colorMap📘 — Maps zValues to colors via HeatmapColorMap📘.
- useLinearTextureFiltering📘 — Enables smooth texture filtering (default:
`false`

). - fillValuesOutOfRange📘 — Fills cells outside the color map’s min/max with a defined edge color.
- stroke📘 and strokeThickness📘 — Cell border styling.
- dataLabels📘 — Enable and style per-cell text labels.

## Examples

### Basic Polar Heatmap

`const {`

PolarMouseWheelZoomModifier,

SciChartJsNavyTheme,

PolarZoomExtentsModifier,

PolarPanModifier,

EAxisAlignment,

PolarNumericAxis,

EPolarLabelMode,

SciChartPolarSurface,

EPolarAxisMode,

NumberRange,

HeatmapColorMap,

UniformHeatmapDataSeries,

PolarUniformHeatmapRenderableSeries,

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { sciChartSurface, wasmContext } = await SciChartPolarSurface.create(divElementId, {

theme: new SciChartJsNavyTheme(),

});

const HEATMAP_WIDTH = 48;

const HEATMAP_HEIGHT = 10;

const angularXAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Angular,

axisAlignment: EAxisAlignment.Left,

visibleRange: new NumberRange(0, HEATMAP_WIDTH),

autoTicks: false,

majorDelta: 1,

polarLabelMode: EPolarLabelMode.Perpendicular,

flippedCoordinates: true, // go clockwise

totalAngle: Math.PI * 2,

});

sciChartSurface.xAxes.add(angularXAxis);

const radialYAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Radial,

axisAlignment: EAxisAlignment.Bottom,

visibleRange: new NumberRange(0, HEATMAP_HEIGHT),

drawLabels: false, // hide radial labels

innerRadius: 0.1,

});

sciChartSurface.yAxes.add(radialYAxis);

// Add a heatmap series to the chart

const heatmapSeries = new PolarUniformHeatmapRenderableSeries(wasmContext, {

dataSeries: new UniformHeatmapDataSeries(wasmContext, {

zValues: Array.from({ length: HEATMAP_HEIGHT }, () => {

return Array.from({ length: HEATMAP_WIDTH }, () => {

return Math.random() * 100;

});

}),

xStart: 0,

yStart: 0,

xStep: 1,

yStep: 1,

}),

colorMap: new HeatmapColorMap({

minimum: 0,

maximum: 100,

gradientStops: [

{ offset: 0, color: "lightblue" },

{ offset: 1, color: "indigo" },

]

}),

});

sciChartSurface.renderableSeries.add(heatmapSeries);

In the code above:

- A 2D array of
`zValues`

is generated via`Array.from`

, representing value "intensity" at each polar sector. - PolarUniformHeatmapRenderableSeries📘 is constructed, passing a UniformHeatmapDataSeries📘 and a custom HeatmapColorMap📘 with gradient stops, from 0 to 100.
- Polar axes are configured for angular and radial sweep.
- Chart modifiers such as PolarPanModifier📘, PolarZoomExtentsModifier📘, and PolarMouseWheelZoomModifier📘 provide interaction.

### Polar Heatmap with Legend

`const COLOR_MAP = new HeatmapColorMap({`

minimum: 0,

maximum: 100,

gradientStops: [

{ offset: 0, color: "#000000" },

{ offset: 1, color: "#3333AAAA" },

]

});

// Add a heatmap series to the chart

const heatmapSeries = new PolarUniformHeatmapRenderableSeries(wasmContext, {

dataSeries: new UniformHeatmapDataSeries(wasmContext, {

zValues: Array.from({ length: HEATMAP_HEIGHT }, () => {

return Array.from({ length: HEATMAP_WIDTH }, () => {

return Math.random() * 100;

});

}),

xStart: 0,

yStart: 0,

xStep: 1,

yStep: 1,

}),

colorMap: COLOR_MAP,

});

sciChartSurface.renderableSeries.add(heatmapSeries);

// also pass "scichart-legend-root" as `legendElementId` in drawExample()

const { heatmapLegend } = await HeatmapLegend.create(legendElementId, {

theme: {

...new SciChartJsNavyTheme(),

sciChartBackground: "transparent",

loadingAnimationBackground: "indigo"

},

yAxisOptions: {

isInnerAxis: true,

labelStyle: {

fontSize: 14,

color: "white",

},

axisBorder: {

borderRight: 2,

color: "white",

},

majorTickLineStyle: {

color: "white",

tickSize: 8,

strokeThickness: 2,

},

minorTickLineStyle: {

color: "white",

tickSize: 4,

strokeThickness: 1,

},

},

colorMap: COLOR_MAP

});

You also need an additional HTML element for the legend:

`<section>`

<div id="scichart-root"></div>

<div id="scichart-legend-root"></div>

</section>

With these CSS properties:

`body { margin: 0; }`

section { width: 100%; height: 100vh; display: flex; }

#scichart-root { width: 100%; height: 100%; }

#scichart-legend-root { height: 100%; width: 65px; }

In the code above:

- The HeatmapLegend📘 component creates an interactive vertical legend, visually linking the z-value color range.
- A custom color map with
**multiple gradient stops**is defined for meaningful value zones. - Data is generated using a
`generateHeatmapData`

utility function (see demo source for details). - Both the heatmap and the legend share the same HeatmapColorMap📘 instance to keep color mapping consistent.
- Axes are positioned and styled for optimal polar data presentation.

### Medical Imaging (Ultrasound Heatmap)

For the full code walkthrough and live demo, see the **Polar Ultrasound Heatmap Example**

## Tips & Best Practices

**Performance**: For large polar heatmaps, enable useLinearTextureFiltering📘 for smoother visual transitions, or disable it for sharp, pixelated looks.**Legend**: Use HeatmapLegend📘 for accessible, interpretable color mapping.**Donut charts**: Set the innerRadius📘 property of the radial axis for donut-shaped polar heatmaps.**Manipulate Angles**: Use totalAngle📘 or totalAngleDegrees📘 properties of the angular axis to control the heatmap's angular range. From`0`

to`2π radians`

or`360 degrees`

.**Interactivity**:- PolarPanModifier📘, PolarZoomExtentsModifier📘, and PolarMouseWheelZoomModifier📘 can all be added for advanced user navigation.
- Don't forget about annotations! Use LineArrowAnnotation📘 or TextAnnotation📘 to highlight specific areas or values in your polar heatmap. All other annotations from SciChart.js are also supported.

## Use Cases

Polar heatmaps are widely used in:

- Physics and engineering for field visualization
- Medical imaging (e.g.
**ultrasound**, see Polar Ultrasound Demo) - Environmental mapping
- Radar and sonar data

PolarUniformHeatmapRenderableSeries📘 enables powerful, visually compelling circular heatmaps in JavaScript. With SciChart.js, you can combine rich color gradients, advanced axis control, interaction, and even medical imaging overlays in a performant, interactive chart component.