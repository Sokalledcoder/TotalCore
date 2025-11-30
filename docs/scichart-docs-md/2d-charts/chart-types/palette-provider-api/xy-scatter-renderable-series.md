---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/palette-provider-api/xy-scatter-renderable-series
scraped_at: 2025-11-28T18:24:38.341154
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/palette-provider-api/xy-scatter-renderable-series

# Per-Point Colouring of Scatter Charts (or PointMarkers)

## Colouring Scatter Points Individually with PaletteProvider

It is possible to override the Scatter series point-marker fill & stroke colour on a per-datapoint basis in SciChart.js using the PaletteProvider API.

To use this, we must create a class which implements or confirms to the IPointMarkerPaletteProvider📘 interface. Then, apply this to the XyScatterRenderableSeries.paletteProvider📘 property. This allows you to colour data-points based on values, or custom rules with infinite extensiblity.

Let's start off by creating a PaletteProvider class:

- TS

`const { DefaultPaletteProvider, EStrokePaletteMode, parseColorToUIntArgb } = SciChart;`

// or, for npm, import { DefaultPaletteProvider, ... } from "scichart"

// Custom PaletteProvider for scatter points which colours datapoints above a threshold

class ScatterPaletteProvider extends DefaultPaletteProvider {

rule: any;

overrideStroke: number;

overrideFill: number;

constructor(stroke, fill, rule) {

super();

this.strokePaletteMode = EStrokePaletteMode.SOLID;

this.rule = rule;

// Use the helper function parseColorToUIntArgb to convert a hex string

// e.g. #FF00FF77 into ARGB numeric format 0xFF00FF77 expected by scichart

this.overrideStroke = parseColorToUIntArgb(stroke);

this.overrideFill = parseColorToUIntArgb(fill);

}

// This function is called for every data-point.

// Return undefined to use the default color for the pointmarker,

// else, return a custom colour as an ARGB color code, e.g. 0xFFFF0000 is red

overridePointMarkerArgb(xValue, yValue, index, opacity, metadata) {

// Draw points outside the range a different color

if (this.rule(yValue)) {

return { stroke: this.overrideStroke, fill: this.overrideFill };

}

// Undefined means use default colors

return undefined;

}

}

It is important that overridePointMarkerArgb returns an object containing both stroke and fill.

Next, we can apply the PaletteProvider to a Scatter Series. This can be done both with the programmatic API and the Builder API:

- TS
- Builder API (JSON Config)

`// The ScatterPaletteProvider we created before is applied to a XyScatterRenderableSeries`

const scatterSeries = new XyScatterRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues }),

pointMarker: new EllipsePointMarker(wasmContext, {

width: 7,

height: 7,

strokeThickness: 1,

fill: "steelblue",

stroke: "LightSteelBlue"

}),

// PaletteProvider feature allows coloring per-point based on a rule

paletteProvider: new ScatterPaletteProvider("Red", "Purple", yValue => yValue > 0.0)

});

sciChartSurface.renderableSeries.add(scatterSeries);

// Add this label & annotation to the chart

sciChartSurface.annotations.add(

new HorizontalLineAnnotation({

y1: 0,

stroke: "#EC0F6C",

axisLabelFill: "White",

labelPlacement: ELabelPlacement.BottomRight,

labelValue: "Values above this line are red",

showLabel: true

})

);

`// Register the custom ScatterPaletteProvider with the chartBuilder`

chartBuilder.registerType(

EBaseType.PaletteProvider,

"ScatterPaletteProvider",

options => new ScatterPaletteProvider(options.stroke, options.fill, options.rule)

);

// Use the Builder-API to build the chart and apply a paletteprovider

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

series: [

{

type: ESeriesType.ScatterSeries,

xyData: {

xValues,

yValues

},

options: {

stroke: "White",

strokeThickness: 5,

pointMarker: {

type: EPointMarkerType.Ellipse,

options: {

width: 7,

height: 7,

strokeThickness: 1,

fill: "steelblue",

stroke: "LightSteelBlue"

}

},

// Now you can instantiate using parameters below

paletteProvider: {

type: EPaletteProviderType.Custom,

customType: "ScatterPaletteProvider",

options: {

stroke: "Red",

fill: "Purple",

rule: yValue => yValue >= 0.0

}

}

// Note: Assigning an instance is also valid, e.g.

// paletteProvider: new ScatterPaletteProvider("Green", "Red", yValue => yValue >= 4.0)

}

}

],

annotations: [

{

type: EAnnotationType.RenderContextHorizontalLineAnnotation,

options: {

y1: 0,

stroke: "#EC0F6C",

axisLabelFill: "White",

labelPlacement: ELabelPlacement.BottomRight,

labelValue: "Values above this line are red",

showLabel: true

}

}

]

});

This results in the following output. Values above 0.0 are coloured red, while values below this threshold use the default colour.