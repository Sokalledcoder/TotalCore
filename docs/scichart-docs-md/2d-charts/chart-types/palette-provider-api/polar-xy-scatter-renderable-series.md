---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/palette-provider-api/polar-xy-scatter-renderable-series
scraped_at: 2025-11-28T18:24:38.105896
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/palette-provider-api/polar-xy-scatter-renderable-series

# Per-Point Coloring for Polar Scatter Series

Polar Scatter series can be colored per-point using the PaletteProvider API. To use this, we must create a class (TS) or object (JS) which implements or confirms to the IStrokePaletteProvider📘 and IFillPaletteProvider📘 interfaces. Then, apply this to the PolarXyScatterRenderableSeries.paletteProvider📘 property. This allows you to colour data-points based on values, or custom rules with infinite extensiblity.

First, let's create a PaletteProvider📘 class like this:

- Creating the PaletteProvider

`const { `

DefaultPaletteProvider,

EStrokePaletteMode,

parseColorToUIntArgb

} = SciChart;

// or, for npm, import { DefaultPaletteProvider, ... } from "scichart"

type TRule = (yValue: number) => boolean;

// Custom PaletteProvider for scatter points which colours datapoints above a threshold

class ScatterPaletteProvider extends DefaultPaletteProvider {

public rule: TRule;

public overrideStroke: number;

public overrideFill: number;

public strokePaletteMode = EStrokePaletteMode.SOLID;

constructor(stroke: string, fill: string, rule: TRule) {

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

overridePointMarkerArgb(xValue: number, yValue: number, index: number, opacity: number, metadata: IPointMetadata) {

// Draw points outside the range a different color

if (this.rule(yValue)) {

return { stroke: this.overrideStroke, fill: this.overrideFill };

}

// Undefined means use default colors

return undefined;

}

}

Next, we can apply the PaletteProvider to the series. This can be done both with the programmatic API and the Builder API:

- TS
- Builder API (JSON Config)

`// The ScatterPaletteProvider we created before is applied to a PolarXyScatterRenderableSeries`

const scatterSeries = new PolarXyScatterRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: Array.from({ length: 100 }, (_, i) => i),

yValues: Array.from({ length: 100 }, (_, i) => Math.random() * 2 - 1), // Random values between -1 and 1

}),

pointMarker: new EllipsePointMarker(wasmContext, {

width: 7,

height: 7,

strokeThickness: 1,

fill: "green",

stroke: "lightgreen"

}),

// PaletteProvider feature allows coloring per-point based on a rule

paletteProvider: new ScatterPaletteProvider("Red", "Purple", (yValue) => yValue > 0.0)

});

`// Demonstrates how to create an interpolated polar line chart with SciChart.js using the Builder API`

const {

EPolarAxisMode,

EAxisAlignment,

ESeriesType,

EThemeProviderType,

chartBuilder,

EAxisType,

EPointMarkerType,

EBaseType,

EPaletteProviderType

} = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

// Register the custom ScatterPaletteProvider with the chartBuilder

chartBuilder.registerType(

EBaseType.PaletteProvider,

"ScatterPaletteProvider",

options => new ScatterPaletteProvider(

options.stroke,

options.fill,

options.rule

)

);

const { wasmContext, sciChartSurface } = await chartBuilder.build2DPolarChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Navy } },

xAxes: [

{

type: EAxisType.PolarNumericAxis,

options: {

polarAxisMode: EPolarAxisMode.Angular,

axisAlignment: EAxisAlignment.Top,

}

}

],

yAxes: [

{

type: SciChart.EAxisType.PolarNumericAxis,

options: {

axisAlignment: EAxisAlignment.Right,

polarAxisMode: EPolarAxisMode.Radial,

}

}

],

series: [

{

type: ESeriesType.PolarScatterSeries,

xyData: {

xValues: Array.from({ length: 100 }, (_, i) => i),

yValues: Array.from({ length: 100 }, (_, i) => Math.random() * 2 - 1), // Random values between -1 and 1

},

options: {

stroke: "pink",

strokeThickness: 4,

pointMarker: {

type: EPointMarkerType.Triangle,

options: {

width: 10,

height: 10,

fill: "green",

stroke: "lightgreen"

}

},

paletteProvider: {

type: EPaletteProviderType.Custom,

customType: "ScatterPaletteProvider",

options: {

stroke: "Red",

fill: "Purple",

rule: (yValue: number) => yValue > 0.0

}

}

}

}

]

});

The code above results in a Polar Xy Scatter Series with the following rule: **change color if value is greater than 0**. The result is shown below:

#### See Also

- Xy Scatter Series PaletteProvider API - check out the 2D version of this article for more info