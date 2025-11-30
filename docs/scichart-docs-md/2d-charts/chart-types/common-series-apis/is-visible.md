---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/common-series-apis/is-visible
scraped_at: 2025-11-28T18:24:21.721401
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/common-series-apis/is-visible

# Series isVisible and isVisibleChanged API

Each RenderableSeries has an isVisible📘 property. This defines whether the series is included in rendering or not.

isVisible can be set programmatically, or is also set by SciChart.js when checking or unchecking a Legend row checkbox (see LegendModifier API).

You can listen to isVisible changes via the BaseRenderableSeries.isVisibleChanged📘 event. Listen to the event (get a callback) using the following code:

- TS

`// Create and add a series with onIsVisibleChanged handler`

const scatterSeries = new XyScatterRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues,

yValues,

dataSeriesName: "Scatter Series"

}),

pointMarker: new EllipsePointMarker(wasmContext, {

width: 7,

height: 7,

strokeThickness: 2,

fill: "steelblue",

stroke: "LightSteelBlue"

}),

onIsVisibleChanged: (sourceSeries, isVisible) => {

console.log(`Series ${sourceSeries.type} was set to isVisible=${isVisible}`);

}

});

// You can also subscribe to isVisibleChanged like this

scatterSeries.isVisibleChanged.subscribe(seriesVisibleChangedArgs => {

// See SeriesVisibleChangedArgs in typedoc

const renderableSeries = seriesVisibleChangedArgs.sourceSeries;

const isVisible = seriesVisibleChangedArgs.isVisible;

console.log(`isVisibleChanged handler: Series ${renderableSeries.type} was set to isVisible=${isVisible}`);

textAnnotation.text = `${renderableSeries.dataSeries.dataSeriesName} is ${isVisible ? "visible" : "hidden"}`;

});

// Explicitly set visibility like this

scatterSeries.isVisible = true;

sciChartSurface.renderableSeries.add(scatterSeries);

This can be used to get feedback about the current visibility state of a series, as in the following demo:

See the onIsVisibleChanged parameter in IBaseRenderableSeriesOptions.onIsVisibleChanged📘 for type information.

The BaseRenderableSeries.isVisibleChanged📘 event handler also has args of type SeriesVisibleChangedArgs📘. In TypeScript, the code would look like this:

**Typescript isVisibleChanged**

`series.isVisibleChanged.subscribe((args: SeriesVisibleChangedArgs) => {`

console.log(`isVisibleChanged handler: Series ${args.sourceSeries.type} was set to isVisible=${args.isVisible}`);

});