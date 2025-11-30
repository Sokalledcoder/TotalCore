---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/palette-provider-api/palette-factory
scraped_at: 2025-11-28T18:24:37.163809
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/palette-provider-api/palette-factory

# The PaletteFactory Helper Class

We've created a helper class called PaletteFactory📘 to create some commonly used PaletteProviders. These work with all series types in SciChart.js that support the PaletteProvider API.

## PaletteFactory.createYGradient

The function PaletteFactory.createYGradient📘 generates a PaletteProvider API for use in renderable series which applies a gradient fill dependent on Y-value.

Below find an example of usage:

- TS

`const yGradientPalette = PaletteFactory.createYGradient(`

wasmContext,

new GradientParams(new Point(0, 0), new Point(0, 1), [

{ offset: 0, color: "#3333FF" },

{ offset: 0.5, color: "#33FFAA" },

{ offset: 1, color: "#FF6600" }

]),

// the range of y-values to apply the gradient to

new NumberRange(0, 1.5),

// Optional parameters to control which elements of the palette are enabled

{

enableFill: false, // Applies to fills on mountain, column

enableStroke: true, // Applies to stroke on all series

enablePointMarkers: true, // Applies to pointmarkers if present

strokeOpacity: 1.0,

pointMarkerOpacity: 0.7,

fillOpacity: 0.0

}

);

sciChartSurface.renderableSeries.add(

new FastLineRenderableSeries(wasmContext, {

strokeThickness: 5,

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues }),

pointMarker: new EllipsePointMarker(wasmContext, {

width: 20,

height: 20,

strokeThickness: 0

}),

paletteProvider: yGradientPalette

})

);

This creates a Y-Gradient from blue, to green to red for Y-values ranging from 0 to +1.5. Values outside that range are clamped to the colours at the start/end of the list of gradient stops.

Here's an example output & codepen you can edit to try this out:

To separately control the output of the generated PaletteProvider, check the IGradientPaletteOptions📘 parameter passed in. Using this, you can enable fill, stroke, pointmarkers and opacity for different elements of the series.

## PaletteFactory.createGradient

Another helper function PaletteFactory.createGradient📘 allows you to create gradient fills in the X-Direction. The parameters for this are largely the same.

Below find an example of usage:

- TS

`const gradientPalette = PaletteFactory.createGradient(`

wasmContext,

new GradientParams(new Point(0, 0), new Point(1, 1), [

{ color: "red", offset: 0 },

{ color: "pink", offset: 0.2 },

{ color: "yellow", offset: 0.5 },

{ color: "purple", offset: 0.7 },

{ color: "green", offset: 1 }

]),

// Optional parameters to control which elements of the palette are enabled

{

enableFill: false, // Applies to fills on mountain, column

enableStroke: true, // Applies to stroke on all series

enablePointMarkers: true, // Applies to pointmarkers if present

strokeOpacity: 1.0,

pointMarkerOpacity: 0.7,

fillOpacity: 0.0

}

);

sciChartSurface.renderableSeries.add(

new FastLineRenderableSeries(wasmContext, {

strokeThickness: 5,

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues }),

pointMarker: new EllipsePointMarker(wasmContext, {

width: 20,

height: 20,

strokeThickness: 0

}),

paletteProvider: gradientPalette

})

);

This creates a X-Gradient from Red, to Yellow, Purple to Green for X-values ranging from the start of the series to the end. Values outside that range are clamped to the colours at the start/end of the list of gradient stops.

Here's an example output & codepen you can edit to try this out: