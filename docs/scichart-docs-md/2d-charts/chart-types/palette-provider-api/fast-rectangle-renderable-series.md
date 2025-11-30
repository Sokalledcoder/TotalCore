---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/palette-provider-api/fast-rectangle-renderable-series
scraped_at: 2025-11-28T18:24:37.044047
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/palette-provider-api/fast-rectangle-renderable-series

# Per-Point Coloring for Rectangle Series

Rectangle series can be colored per-point using the PaletteProvider API. To use this, we must create a class (typescript) or object (javascript) which implements or confirms to the IStrokePaletteProvider📘 and IFillPaletteProvider📘 interfaces. Then, apply this to the FastRectangleRenderableSeries.paletteProvider📘 property. This allows you to colour data-points based on values, or custom rules with infinite extensiblity.

First, let's create a PaletteProvider class like this:

- TS

`import { DefaultPaletteProvider, EStrokePaletteMode, parseColorToUIntArgb } from "scichart";`

// Custom PaletteProvider for rectangle series which colours datapoints above a threshold

class RectanglePaletteProvider extends DefaultPaletteProvider {

threshold: number;

stroke: number;

fillColor: number;

constructor(threshold: number) {

super();

this.strokePaletteMode = EStrokePaletteMode.SOLID;

this.threshold = threshold;

this.stroke = parseColorToUIntArgb("#FF0000");

this.fillColor = parseColorToUIntArgb("#FF000077");

}

// This function is called for every data-point.

// Return undefined to use the default color for the rectangle,

// else, return a custom colour as an ARGB color code, e.g. 0xFFFF0000 is red

overrideStrokeArgb(xValue: number, yValue: number, index: number, opacity: number, metadata: any) {

return yValue > this.threshold

? this.fillColor

: undefined;

}

// This function is called for every data-point

// Return undefined to use the default color for the fill, else, return

// a custom color as ARGB color code e.g. 0xFFFF0000 is red

overrideFillArgb(xValue: number, yValue: number, index: number, opacity: number, metadata: any) {

return yValue > this.threshold

? this.fillColor

: undefined;

}

}

Next, we can apply the PaletteProvider to the series. This can be done both with the programmatic API:

- TS

`const rectangleSeries = new FastRectangleRenderableSeries(wasmContext, {`

dataSeries: new XyxyDataSeries(wasmContext, {

xValues: [0, 6, 10, 17, 23],

yValues: [0, 6, 2, 5, 8],

x1Values: [5, 9, 15, 25, 30],

y1Values: [5, 9, 8, 10, 15]

}),

columnXMode: EColumnMode.StartEnd, // x, x1

columnYMode: EColumnYMode.TopBottom, // y, y1

fill: "skyblue",

stroke: "white",

strokeThickness: 2,

opacity: 0.5,

paletteProvider: new RectanglePaletteProvider(4.5) // rectangles with yValue > 4.5 will be coloured red

});

For a more detailed example of FastRectangleRenderableSeries📘, see the Javascript Treemap Chart Example. Each rectangle is coloured based on its value, the larger the value, the darker the green, while negative values are coloured red in the same fashion.