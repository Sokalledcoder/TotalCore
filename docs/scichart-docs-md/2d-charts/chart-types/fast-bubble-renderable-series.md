---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/fast-bubble-renderable-series
scraped_at: 2025-11-28T18:24:27.429510
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/fast-bubble-renderable-series

# The Bubble Series Type

Bubble Series can be created using the FastBubbleRenderableSeries📘 type.

The JavaScript Bubble Chart Example can be found in the SciChart.Js Examples Suite > Bubble Series on Github, or our live demo at scichart.com/demo.

## Create a Bubble Series

To create a Javascript Bubble Chart with SciChart.js, use the following code:

- TS
- Builder API (JSON Config)

`// Demonstrates how to create a bubble chart with SciChart.js`

const {

SciChartSurface,

NumericAxis,

XyzDataSeries,

FastBubbleRenderableSeries,

EllipsePointMarker,

SciChartJsNavyTheme

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

const xValues = [];

const yValues = [];

const sizes = [];

for (let i = 0; i < 30; i++) {

xValues.push(i);

yValues.push(0.2 * Math.sin(i * 0.2) - Math.cos(i * 0.04));

sizes.push(Math.sin(i) * 60 + 3);

}

const xyzDataSeries = new XyzDataSeries(wasmContext, {

xValues,

yValues,

zValues: sizes

});

const bubbleSeries = new FastBubbleRenderableSeries(wasmContext, {

dataSeries: xyzDataSeries,

pointMarker: new EllipsePointMarker(wasmContext, {

// choose a suitably large size for pointmarker. This will be scaled per-point

width: 64,

height: 64,

strokeThickness: 0,

fill: "#4682b477"

})

});

sciChartSurface.renderableSeries.add(bubbleSeries);

`// Demonstrates how to create a scatter with SciChart.js using the Builder API`

const { chartBuilder, ESeriesType, EPointMarkerType, EThemeProviderType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const xValues = [];

const yValues = [];

const sizes = [];

for (let i = 0; i < 30; i++) {

xValues.push(i);

yValues.push(0.2 * Math.sin(i * 0.2) - Math.cos(i * 0.04));

sizes.push(Math.sin(i) * 60 + 3);

}

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

series: [

{

type: ESeriesType.BubbleSeries,

xyzData: {

xValues,

yValues,

zValues: sizes

},

options: {

pointMarker: {

type: EPointMarkerType.Ellipse,

options: {

// choose a suitably large size for pointmarker. This will be scaled per-point

width: 64,

height: 64,

strokeThickness: 0,

fill: "#4682b477"

}

}

}

}

]

});

In the code above:

- A Bubble Series instance is created and added to the SciChartSurface.renderableSeries📘 collection.
- We set a PointMarker📘 with a width, height = 64. Note that this pointmarker will be scaled up or down relative to bubble size. Having a strokeThickness📘 of 0 can create a better visual.
- We assign a DataSeries📘 - which stores the Xyz data to render, where X,Y is position and Z is scale factor.

This results in the following output:

Because the Bubble Series renders a single point-market but scales for each point, **it is advisable not to use a Stroke on the PointMarker**, as this could get pixellated when the bubble is scaled up or down. This approach of ours results in extremely high performance charts - hundreds of thousands of data-points are possible with SciChart.js.

## Scaling Bubble sizes per-point

The Bubble chart sizes are scaled using the zValue on the XyzDataSeries📘. By default, the z-value is pixels.

You can scale up/down the entire bubble series by setting the FastBubbleRenderableSeries.zMultiplier📘 property. Default value=1.

You can modify or edit sizes by adjusting the zValues via xyzDataSeries.updateXyz()📘 or similar. See the DataSeries Documentation pages for more info about data updates.

Bubble sizes can be scaled using the DataSeries zValue, or the zMultiplier property (see above). What if you wanted to scale a bubble series depending on the zoom level of the viewport? Here's a quick worked example:

- TS

`const bubbleSeries = new FastBubbleRenderableSeries(wasmContext, {`

dataSeries: new XyzDataSeries(wasmContext, { xValues, yValues, zValues: sizes }),

pointMarker: new EllipsePointMarker(wasmContext, {

width: 256,

height: 256,

strokeThickness: 0,

fill: "#4682b477"

})

});

// Adjust zMultiplier based on zoom level

const adjustSeriesStyle = () => {

const xAxis = sciChartSurface.xAxes.get(0);

// Get the max range of the xAxis and calculate how zoomed in we are

const seriesRange = xAxis.getMaximumRange();

const zoomMultiplier = seriesRange.diff / xAxis.visibleRange.diff;

// Calculate & apply a zoom factor

const size =

(Math.round(sciChartSurface.seriesViewRect.width) * zoomMultiplier) / bubbleSeries.dataSeries.count();

bubbleSeries.zMultiplier = size * 0.05;

};

const usePreRenderCallback = (sciChartSurface, callback) => {

let wasRendered = false;

// initial setup - trigger on first redraw

sciChartSurface.rendered.subscribe(() => {

if (!wasRendered) {

wasRendered = true;

callback();

}

});

// subsequent calls - trigger before render

sciChartSurface.preRender.subscribe(() => {

if (wasRendered) {

callback();

}

});

};

// Callback called before render on SciChartSurface

usePreRenderCallback(sciChartSurface, () => {

adjustSeriesStyle();

});

sciChartSurface.renderableSeries.add(bubbleSeries);

This results in the following output:

## Render a Gap in a Bubble Series

It is possible to have null points or gaps in a Bubble Series by passing a data point with a **NaN** value as the **Y** value. Or, by simply skipping a point if using a value-axis. Please refer to the Common Series Features - Draw Gaps in Series article for more details.

## Different Point-Markers on a Bubble Series

Every data point of a Bubble Series is marked with a PointMarker📘. Several different types of PointMarker are available in SciChart.js:

- EllipsePointMarker📘 - Renders a circle at each point
- SquarePointMarker📘 - Renders a square at each point
- TrianglePointMarker📘 - Renders a triangle at each point
- CrossPointMarker📘 - Renders a plus sign '+' at each point
- XPointMarker📘 - Renders an 'x' at each point
- SpritePointMarker📘 - Allows an image to be used at each point to create custom pointmarkers

Any of these can be used to create a bubble chart.

To learn more about the types of Point Marker in SciChart.js, see the Point Markers API documentation.

There is also a TypeScript example of custom pointmarkers in the SciChart.js Demo.

## Painting Bubbles with Different Colors

It is possible to define the colour of PointMarkers individually using the PaletteProvider API.

For more info on how to do this, see the PaletteProvider - Per-point colouring of Scatter Charts documentation page.