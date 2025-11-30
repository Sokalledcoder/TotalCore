---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/palette-provider-api/polar-band-renderable-series
scraped_at: 2025-11-28T18:24:37.453182
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/palette-provider-api/polar-band-renderable-series

# Per-Point Coloring for Polar Band Series

Polar Band series can be colored per-point or per line-segment using the PaletteProvider API. To use this, we must create a class (TS) or object (JS) which implements or confirms to the IStrokePaletteProvider📘 and IFillPaletteProvider📘 interfaces. Then, apply this to the PolarBandRenderableSeries.paletteProvider📘 property. This allows you to colour data-points based on values, or custom rules with infinite extensiblity.

First, let's create a PaletteProvider📘 class like this:

- Creating the PaletteProvider

`const {`

DefaultPaletteProvider,

EStrokePaletteMode,

EFillPaletteMode,

parseColorToUIntArgb

} = SciChart;

// or, for npm, import { DefaultPaletteProvider, ... } from "scichart"

// Custom PaletteProvider for line series which colours datapoints above a threshold

class PolarBandPaletteProvider extends DefaultPaletteProvider {

strokePaletteMode = EStrokePaletteMode.SOLID;

fillPaletteMode = EFillPaletteMode.SOLID;

orange = parseColorToUIntArgb("#DD8800");

lightOrange = parseColorToUIntArgb("#DD880044");

overrideFillArgb(xValue: number, yValue: number, index: number, opacity: number, metadata: any) {

if ((xValue >= 3 && xValue < 6) || (xValue >= 9 && xValue < 12)) {

return this.lightOrange;

} else {

return undefined;

}

}

overrideStrokeArgb(xValue: number, yValue: number, index: number, opacity: number, metadata: any) {

if ((xValue > 3 && xValue <= 6) || (xValue > 9 && xValue <= 12)) {

return this.orange;

} else {

return undefined; // use the default stroke color

}

}

}

Next, we can apply the PaletteProvider to the series. This can be done both with the programmatic API and the Builder API:

- TS
- Builder API (JSON Config)

`const polarBand1 = new PolarBandRenderableSeries(wasmContext, {`

dataSeries: new XyyDataSeries(wasmContext, {

xValues: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],

yValues: [1, 2.5, 3, 1, 2.5, 3, 1, 2.5, 3, 1, 2.5, 3, 1],

y1Values: [2, 5, 6, 2, 5, 6, 2, 5, 6, 2, 5, 6, 2]

}),

stroke: "#FF0000",

fill: "#FF000044",

strokeThickness: 3,

paletteProvider: new PolarBandPaletteProvider()

});

`// Demonstrates how to create a band chart with SciChart.js using the Builder API`

const {

EThemeProviderType,

chartBuilder,

EPolarAxisMode,

EAxisAlignment,

EPolarLabelMode,

EAxisType,

ESeriesType,

} = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DPolarChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Navy } },

xAxes: [

{

type: EAxisType.PolarNumericAxis,

options: {

polarAxisMode: EPolarAxisMode.Angular,

axisAlignment: EAxisAlignment.Top,

polarLabelMode: EPolarLabelMode.Parallel

}

}

],

yAxes: [

{

type: SciChart.EAxisType.PolarNumericAxis,

options: {

axisAlignment: EAxisAlignment.Right,

polarAxisMode: EPolarAxisMode.Radial,

labelPrecision: 0,

innerRadius: 0.1

}

}

],

series: [

{

type: ESeriesType.PolarBandSeries,

xyyData: {

xValues: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],

yValues: [1, 2.5, 3, 1, 2.5, 3, 1, 2.5, 3, 1, 2.5, 3, 1],

y1Values: [2, 5, 6, 2, 5, 6, 2, 5, 6, 2, 5, 6, 2]

},

options: {

stroke: "#FF0000",

fill: "#FF000044",

strokeThickness: 3,

paletteProvider: new PolarBandPaletteProvider()

}

}

]

});

return { sciChartSurface, wasmContext };

The code above results in a Polar Band Series with the following rule: **change color once every 3 points**. The result is shown below:

In the code above:

- We create a class that extends DefaultPaletteProvider📘 to override overrideFillArgb📘 and overrideStrokeArgb📘 methods by
`xValue`

, more specifically, the orange fill & stroke when this custom rule is met:

`((xValue > 3 && xValue <= 6) || (xValue > 9 && xValue <= 12))`

#### See Also

- Band Series PaletteProvider API - check out the 2D version of this article for more info