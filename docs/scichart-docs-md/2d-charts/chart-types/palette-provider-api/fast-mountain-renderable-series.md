---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/palette-provider-api/fast-mountain-renderable-series
scraped_at: 2025-11-28T18:24:36.902287
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/palette-provider-api/fast-mountain-renderable-series

# Per-point Colouring of Mountain Segments

Mountain series can be colored per-point using the PaletteProvider API. To use this, we must create a class (typescript) or object (javascript) which implements or confirms to the IStrokePaletteProvider📘 and IFillPaletteProvider📘 interfaces. Then, apply this to the FastMountainRenderableSeries.paletteProvider📘 property. This allows you to colour data-points based on values, or custom rules with infinite extensiblity.

First, let's create a PaletteProvider class like this:

- TS

`const { DefaultPaletteProvider, EStrokePaletteMode, parseColorToUIntArgb } = SciChart;`

// or, for npm, import { DefaultPaletteProvider, ... } from "scichart"

// Custom PaletteProvider for line series which colours datapoints above a threshold

class MountainPaletteProvider extends DefaultPaletteProvider {

threshold: number;

stroke: number;

fillColor: number;

constructor(threshold) {

super();

this.strokePaletteMode = EStrokePaletteMode.SOLID;

this.threshold = threshold;

this.stroke = parseColorToUIntArgb("#FF0000");

this.fillColor = parseColorToUIntArgb("#FF000077");

}

// This function is called for every data-point.

// Return undefined to use the default color for the line,

// else, return a custom colour as an ARGB color code, e.g. 0xFFFF0000 is red

overrideStrokeArgb(xValue, yValue, index, opacity, metadata) {

return xValue > this.threshold ? this.fillColor : undefined;

}

// This function is called for every data-point

// Return undefined to use the default color for the fill, else, return

// a custom color as ARGB color code e.g. 0xFFFF0000 is red

overrideFillArgb(xValue, yValue, index, opacity, metadata) {

return xValue > this.threshold ? this.fillColor : undefined;

}

}

Next, we can apply the PaletteProvider to the series. This can be done both with the programmatic API and the Builder API:

- TS
- Builder API (JSON Config)

`const threshold = 75;`

// Create a mountain series & add to the chart

const mountainSeries = new FastMountainRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues }),

stroke: "#4682b4",

strokeThickness: 3,

zeroLineY: 0.0,

// when a solid color is required, use fill

fill: "rgba(176, 196, 222, 0.7)",

// when a gradient is required, use fillLinearGradient

fillLinearGradient: new GradientParams(new Point(0, 0), new Point(0, 1), [

{ color: "rgba(70,130,180,0.77)", offset: 0 },

{ color: "rgba(70,130,180,0.0)", offset: 1 }

]),

// Apply the paletteprovider

paletteProvider: new MountainPaletteProvider(threshold)

});

sciChartSurface.renderableSeries.add(mountainSeries);

// Demonstrates how to create a chart with a custom PaletteProvider, using the builder API

const { chartBuilder, EBaseType, ESeriesType, EPaletteProviderType, EThemeProviderType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

// Register the custom ThresholdLinePaletteProvider with the chartBuilder

chartBuilder.registerType(

EBaseType.PaletteProvider,

"MountainPaletteProvider",

options => new MountainPaletteProvider(options.threshold)

);

// Create some data

let yLast = 100.0;

const xValues = [];

const yValues = [];

for (let i = 0; i <= 100; i++) {

const y = yLast + (Math.random() - 0.48);

yLast = y;

xValues.push(i);

yValues.push(y);

}

// Now use the Builder-API to build the chart

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

series: [

{

type: ESeriesType.MountainSeries,

xyData: {

xValues,

yValues

},

options: {

stroke: "#4682b4",

strokeThickness: 3,

zeroLineY: 0.0,

fill: "rgba(176, 196, 222, 0.7)", // when a solid color is required, use fill

fillLinearGradient: {

gradientStops: [

{ color: "rgba(70,130,180,0.77)", offset: 0.0 },

{ color: "rgba(70,130,180,0.0)", offset: 1 }

],

startPoint: { x: 0, y: 0 },

endPoint: { x: 0, y: 1 }

},

// Now you can instantiate using parameters below

paletteProvider: {

type: EPaletteProviderType.Custom,

customType: "MountainPaletteProvider",

options: {

threshold: 75

}

}

// Note: Assigning an instance is also valid, e.g.

// paletteProvider: new ThresholdLinePaletteProvider("Green", yValue => yValue >= 4.0)

}

}

]

});

The code above results in a JavaScript Mountain Chart with the following output. XValues > 200 are colored red, and XValues < 200 are the default series colors.

SciChart won't bisect the line at a threshold value but only changes colour between line segments in the data you already have. If you want to have a perfect transistion from one colour to another at a specific Y-value, you will need to include data-points

## Colouring Mountain Series Point-Markers with PaletteProvider

If applying PointMarkers to the FastMountainRenderableSeries, and you want to adjust per-point coloring of the markers, then you need to implement overridePointMarkerArgb in your paletteprovider.

Find out how in the documentation page Per-Point Colouring of Scatter Charts (or PointMarkers).