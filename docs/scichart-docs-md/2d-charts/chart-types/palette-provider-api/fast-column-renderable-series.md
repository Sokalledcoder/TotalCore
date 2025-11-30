---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/palette-provider-api/fast-column-renderable-series
scraped_at: 2025-11-28T18:24:36.162944
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/palette-provider-api/fast-column-renderable-series

# Per-Point Colouring of Column Charts

Column series can be colored per-point or per line-segment using the PaletteProvider API. To use this, we must create a class (typescript) or object (javascript) which implements or confirms to the IStrokePaletteProvider📘 and IFillPaletteProvider📘 interfaces. Then, apply this to the FastColumnRenderableSeries.paletteProvider📘 property. This allows you to colour data-points based on values, or custom rules with infinite extensiblity.

First, let's create a PaletteProvider class like this:

- TS

`const { DefaultPaletteProvider, EStrokePaletteMode, parseColorToUIntArgb } = SciChart;`

// or, for npm, import { DefaultPaletteProvider, ... } from "scichart"

// Custom PaletteProvider for column series which colours datapoints above a threshold

class ColumnPaletteProvider extends DefaultPaletteProvider {

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

return yValue > this.threshold ? this.fillColor : undefined;

}

// This function is called for every data-point

// Return undefined to use the default color for the fill, else, return

// a custom color as ARGB color code e.g. 0xFFFF0000 is red

overrideFillArgb(xValue, yValue, index, opacity, metadata) {

return yValue > this.threshold ? this.fillColor : undefined;

}

}

Next, we can apply the PaletteProvider to the series. This can be done both with the programmatic API and the Builder API:

- TS
- Builder API (JSON Config)

`// Create some data`

const xValues = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19];

const yValues = [

0.1, 0.2, 0.4, 0.8, 1.1, 1.5, 2.4, 4.6, 8.1, 11.7, 14.4, 16.0, 13.7, 10.1, 6.4, 3.5, 2.5, 1.4, 0.4, 0.1

];

// Create and add a column series

const columnSeries = new FastColumnRenderableSeries(wasmContext, {

fill: "rgba(176, 196, 222, 0.5)",

stroke: "rgba(176, 196, 222, 1)",

strokeThickness: 2,

dataPointWidth: 0.7,

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues }),

paletteProvider: new ColumnPaletteProvider(10)

});

sciChartSurface.renderableSeries.add(columnSeries);

// Demonstrates how to create a chart with a custom PaletteProvider, using the builder API

const { chartBuilder, EBaseType, ESeriesType, EPaletteProviderType, EThemeProviderType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

// Register the custom ColumnPaletteProvider with the chartBuilder

chartBuilder.registerType(

EBaseType.PaletteProvider,

"ColumnPaletteProvider",

options => new ColumnPaletteProvider(options.threshold)

);

// Create some data

const xValues = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19];

const yValues = [

0.1, 0.2, 0.4, 0.8, 1.1, 1.5, 2.4, 4.6, 8.1, 11.7, 14.4, 16.0, 13.7, 10.1, 6.4, 3.5, 2.5, 1.4, 0.4, 0.1

];

// Now use the Builder-API to build the chart

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

series: [

{

type: ESeriesType.ColumnSeries,

xyData: {

xValues,

yValues

},

options: {

fill: "rgba(176, 196, 222, 0.5)",

stroke: "rgba(176, 196, 222, 1)",

strokeThickness: 2,

dataPointWidth: 0.7,

// Now you can instantiate using parameters below

paletteProvider: {

type: EPaletteProviderType.Custom,

customType: "ColumnPaletteProvider",

options: {

threshold: 10

}

}

// Note: Assigning an instance is also valid, e.g.

// paletteProvider: new ColumnPaletteProvider(10)

}

}

]

});

The code above results in a JavaScript Column Chart with the following output. YValues > 10 are colored red, and YValues < 10 are the default series stroke and fill colors.

## Troubleshooting

For FastColumnRenderableSeries📘 you may notice that **palette provider stops working when zoomed out to the point that columns are 1px wide**. It may happens when a palette provider class overrides only fill and do not override stroke. When we zoom out far enough to reach one pixel width the drawing engine does not use fill any more it uses stroke. Therefore in order to make it look always the same color you would need to override both fill and stroke. For example:

`import {`

EFillPaletteMode,

IFillPaletteProvider,

IStrokePaletteProvider,

IPointMetadata,

IRenderableSeries,

EStrokePaletteMode,

} from 'scichart';

export class BarPaletteProvider

implements IFillPaletteProvider, IStrokePaletteProvider

{

fillPaletteMode = EFillPaletteMode.SOLID;

strokePaletteMode = EStrokePaletteMode.SOLID;

private color: number;

constructor(color: string) {

this.color = BarPaletteProvider.argbColorToNumber(color);

}

onAttached(parentSeries: IRenderableSeries): void {}

onDetached(): void {}

overrideFillArgb(

xValue: number,

yValue: number,

index: number,

opacity?: number,

metadata?: IPointMetadata

): number {

return this.color;

}

overrideStrokeArgb(

xValue: number,

yValue: number,

index: number,

opacity?: number,

metadata?: IPointMetadata

): number | undefined {

return this.color;

}

private static argbColorToNumber(color: string) {

return parseInt(color.substring(1), 16);

}

}