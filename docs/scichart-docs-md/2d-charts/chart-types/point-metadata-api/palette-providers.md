---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/point-metadata-api/palette-providers
scraped_at: 2025-11-28T18:24:38.876198
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/point-metadata-api/palette-providers

# Metadata and PaletteProviders

Using the PaletteProvider API you can control the colour of data-points, line segments or columns / bars based on a programmatic rule, e.g. if Y>5 or index < 100.

By combining this with Metadata now you can control the point colour based on any javascript object. Useful if you want to host additional data in your chart such as validity of data or alarm/alert values alongside x-y points.

Background reading:

- If you haven't already, read the article DataSeries PointMetadata API which will show you how to setup a DataSeries with point metadata (javascript objects).
- Also take a look at the PaletteProvider API docs to find out how to programmatically change series-color on a per-point basis.

## Example: Metadata + PaletteProviders

Below is a worked example showing how to store series point colours in metadata and render them using a custom paletteprovider.

Let's start off by creating the PaletteProvider:

- PaletteProvider code JS

`const { DefaultPaletteProvider, EStrokePaletteMode, parseColorToUIntArgb } = SciChart;`

// or for npm import { DefaultPaletteProvider, EStrokePaletteMode } from "scichart"

// PaletteProvider to use data from metadata to color the line segments

class LinePaletteProvider extends DefaultPaletteProvider {

constructor() {

super();

this.strokePaletteMode = EStrokePaletteMode.SOLID;

}

overrideStrokeArgb(xValue, yValue, index, opacity, metadata) {

if (metadata && metadata.color) {

// if metadata.color exists, parse this from HTML Hex code to a UInt ARGB value

// Note: for performance reasons its better to preconvert hex to UInt rather than do it on the fly here

return parseColorToUIntArgb(metadata.color);

} else {

// Returning undefined means use default series stroke color

return undefined;

}

}

}

By inheriting DefaultPaletteProvider📘 we can override functions like overrideStrokeArgb, overrideFillArgb and overridePointMarkerArgb. Returning a colour code in Uint ARGB format overrides the colour for that data-point. Returning undefined uses the default series colour.

Next, we can apply the PaletteProvider and metadata to a chart like this.

- JS
- Builder API (JSON Config)

`const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {`

theme: new SciChartJsNavyTheme()

});

const growBy = new NumberRange(0.1, 0.1);

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { growBy }));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { growBy }));

// Create metadata with initial values. Metadata can be any JS object

const dataSeries = new XyDataSeries(wasmContext, {

xValues: [1, 2, 3, 4, 5, 6, 7, 8],

yValues: [4.3, 5.3, 6, 6.3, 6.4, 6.1, 5.9, 5.5],

metadata: [

{ color: "#ff6600" },

{ color: "#50C7E0" },

{ color: "#50C7E0" },

{ color: "#ff6600" },

{ color: "#50C7E0" },

undefined, // nothing at this index

{ color: "#EC0F6C" },

{ color: "#ff6600" }

]

});

// Add a line series with the metadata and palette provider

sciChartSurface.renderableSeries.add(

new FastLineRenderableSeries(wasmContext, {

strokeThickness: 2,

dataSeries,

// Apply the PaletteProvider

paletteProvider: new LinePaletteProvider(),

pointMarker: new EllipsePointMarker(wasmContext, {

width: 5,

height: 5,

fill: "White",

strokeThickness: 0

})

})

);

`// Demonstrates how to combine PointMetadata and PaletteProviders in SciChart.js with the Builder API`

const {

chartBuilder,

ESeriesType,

EThemeProviderType,

EChart2DModifierType,

EPointMarkerType,

EBaseType,

EPaletteProviderType

} = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

// Register the custom LinePaletteProvider with the chartBuilder

chartBuilder.registerType(EBaseType.PaletteProvider, "LinePaletteProvider", options => new LinePaletteProvider());

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

series: [

{

type: ESeriesType.LineSeries,

// Metadata is set in xyData property

xyData: {

xValues: [1, 2, 3, 4, 5, 6, 7, 8],

yValues: [4.3, 5.3, 6, 6.3, 6.4, 6.1, 5.9, 5.5],

metadata: [

{ color: "#ff6600" },

{ color: "#50C7E0" },

{ color: "#50C7E0" },

{ color: "#ff6600" },

{ color: "#50C7E0" },

undefined, // nothing at this index

{ color: "#EC0F6C" },

{ color: "#ff6600" }

]

},

options: {

stroke: "#C52E60",

// Now you can instantiate using parameters below

paletteProvider: {

type: EPaletteProviderType.Custom,

customType: "LinePaletteProvider"

},

// Note: Assigning an instance is also valid, e.g.

// paletteProvider: new ThresholdLinePaletteProvider("Green", yValue => yValue >= 4.0)

pointMarker: {

type: EPointMarkerType.Ellipse,

options: {

width: 5,

height: 5,

fill: "White"

}

}

}

}

],

// Configure a Rollovermodifier to display metadata

modifiers: [

{

type: EChart2DModifierType.Rollover,

options: {

snapToDataPoint: true,

tooltipDataTemplate: seriesInfo => [

`X: ${seriesInfo.formattedXValue}`,

`Y: ${seriesInfo.formattedYValue}`,

`index: ${seriesInfo.dataSeriesIndex}`,

`Metadata.color: ${seriesInfo.pointMetadata?.color ?? "null"}`

]

}

}

]

});

This results in the following output:

To learn more about the PaletteProvider API, see the documentation pages here.