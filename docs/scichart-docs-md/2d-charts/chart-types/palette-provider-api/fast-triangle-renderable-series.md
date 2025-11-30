---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/palette-provider-api/fast-triangle-renderable-series
scraped_at: 2025-11-28T18:24:36.803668
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/palette-provider-api/fast-triangle-renderable-series

# Per-Point Coloring for Triangle Series

Triangle series can be colored per-point using the PaletteProvider API. To use this, we must create a class (typescript) or object (javascript) which implements or confirms to the IStrokePaletteProvider📘 and IFillPaletteProvider📘 interfaces. Then, apply this to the FastTriangleRenderableSeries.paletteProvider📘 property. This allows you to colour data-points based on values, or custom rules with infinite extensiblity.

First, let's create a PaletteProvider class like this:

- TS

`import { EFillPaletteMode, IFillPaletteProvider, parseColorToUIntArgb } from "scichart";`

// Custom PaletteProvider for triangle series which colours datapoints above a threshold

const COLORS = ["#f39c12", "#27ae60", "#2980b9", "#8e44ad" ]

class TrianglePaletteProvider implements IFillPaletteProvider {

public readonly fillPaletteMode = EFillPaletteMode.SOLID;

public onAttached(): void {}

public onDetached(): void {}

public overrideFillArgb(_xValue: number, _yValue: number, index: number, opacity: number): number {

const opacityFix = Math.round(opacity * 255);

return parseColorToUIntArgb(COLORS[Math.floor(index / 3)], opacityFix);

}

}

Next, we can apply the PaletteProvider to the series. This can be done both with the programmatic API:

- TS

`const coordinates = [`

[0, 150],

[0, 50],

[50, 0],

[150, 0],

[200, 50],

[200, 150],

[150, 200],

[50, 200],

[0, 150],

[0, 50]

];

const dataSeries = new XyDataSeries(wasmContext, {

xValues: coordinates.map(p => p[0]),

yValues: coordinates.map(p => p[1])

});

const triangleSeries = new FastTriangleRenderableSeries(wasmContext, {

dataSeries,

drawMode: ETriangleSeriesDrawMode.Strip, // each group of three consecutive points in the list defines a triangle, every point is connected to the last two points

fill: "cornflowerblue",

opacity: 0.5,

paletteProvider: new TrianglePaletteProvider()

});

For a more detailed example of FastTriangleRenderableSeries📘, see the Javascript Treemap Chart Example. Each rectangle is coloured based on its value, the larger the value, the darker the green, while negative values are coloured red in the same fashion.