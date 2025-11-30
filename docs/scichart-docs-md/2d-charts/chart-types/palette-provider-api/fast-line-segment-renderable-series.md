---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/palette-provider-api/fast-line-segment-renderable-series
scraped_at: 2025-11-28T18:24:36.558040
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/palette-provider-api/fast-line-segment-renderable-series

# Per-Point Coloring for Line Segment Series

Line Segment series can be colored per line-segment using the PaletteProvider API. To use this, we must create a class (typescript) or object (javascript) which implements or confirms to the IStrokePaletteProvider📘 interface. Then, apply this to the FastLineSegmentRenderableSeries.paletteProvider📘 property.

Let's start off with the PaletteProvider class:

- TS

`const { DefaultPaletteProvider, EStrokePaletteMode, parseColorToUIntArgb, EPaletteProviderType } = SciChart;`

// or, for npm, import { DefaultPaletteProvider, ... } from "scichart"

// Custom PaletteProvider for line segment series which colours datapoints differently on odd and even points (differently on both ends)

class LineSegmentPaletteProvider extends DefaultPaletteProvider {

public readonly strokePaletteMode = EStrokePaletteMode.GRADIENT;

private readonly palettedStart = parseColorToUIntArgb("orange");

private readonly palettedEnd = parseColorToUIntArgb("cyan");

// tslint:disable-next-line:no-empty

public onAttached(parentSeries: IRenderableSeries): void {}

// tslint:disable-next-line:no-empty

public onDetached(): void {}

public overrideStrokeArgb(xValue: number, yValue: number, index: number): number {

return index % 2 === 0 ? this.palettedStart : this.palettedEnd;

}

}

Next, we can apply the PaletteProvider to the line segment series. This can be done both with the programmatic API and the Builder API:

- TS

`function generateVectorFieldSegments(gridSize = 30) {`

const xValues = [];

const yValues = [];

const spacing = 10 / (gridSize - 1); // spacing between grid points

const scale = 0.6; // scale for vector length

for (let i = 0; i < gridSize; i++) {

for (let j = 0; j < gridSize; j++) {

const x = i * spacing;

const y = j * spacing;

// Vector field direction (can modify here)

const angle = Math.sin(x) + Math.cos(y);

const dx = Math.cos(angle) * scale;

const dy = Math.sin(angle) * scale;

const x1 = x;

const y1 = y;

const x2 = x + dx;

const y2 = y + dy;

// Ensure segments stay in [0, 10]

if (x2 < 0 || x2 > 10 || y2 < 0 || y2 > 10) continue;

xValues.push(x1, x2);

yValues.push(y1, y2);

}

}

return { xValues, yValues };

}

const { xValues, yValues } = generateVectorFieldSegments(30);

const lineSegment1 = new FastLineSegmentRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: xValues,

yValues: yValues,

}),

strokeThickness: 3,

paletteProvider: new LineSegmentPaletteProvider(),

});

sciChartSurface.renderableSeries.add(lineSegment1);

This results in the following output:

In TypeScript you only need to implement an interface such as IStrokePaletteProvider📘, whereas in JavaScript you must extend the DefaultPaletteProvider📘 class.

SciChart won't bisect the line at a threshold value but only changes colour between line segments in the data you already have.

That being said, a EStrokePaletteMode.SOLID📘 transition will not work with 2 points and a line drawn in between them (as it is done within the segment) - the result will only show 1 colour, so try to stick to EStrokePaletteMode.GRADIENT📘 for line segments' PaletteProviders.