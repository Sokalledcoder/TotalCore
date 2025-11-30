---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/renderable-series-api-overview
scraped_at: 2025-11-28T18:24:43.142491
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/renderable-series-api-overview

# RenderableSeries Overview

The RenderableSeries in SciChart are visual representations of **X,Y Numeric** or **Date** data. Other libraries call them 'Chart Types'.

Some RenderableSeries render simple X,Y values (2D points in space), while some render additional information (such as X,Y0,Y1 values, or X,Y,Z values).

## Chart Types in SciChart.js

SciChart.js supports a number of 2D & 3D Chart types. These include:

Click on the links above to see documentation and live embedded code snippets for each of the chart types in SciChart.js

## Common 2D Chart Features

As well as just render 2D Data, a number of chart types support additional properties and features.

For example, most 2D Chart types in SciChart.js support:

| SciChart.js Feature | Description |
|---|---|
Dynamic Data Updates | All SciChart.js chart types support dynamic updates to data out of the box. Insert, append, update, delete - modify data and the chart updates FAST. See the DataSeries API documentation for more details. |
Per-point coloring | SciChart.js chart types support per-point coloring based on a rule. Xy values over/under a threshold, values with a property can be colored individually. See the PaletteProvider API for more details. |
Data-point markers | SciChart.js chart types support adding a pointmarker (circle, square, triangle, cross marker) at data-points. See the PointMarkers documentation for more details. |
Data-point Text Labels | SciChart.js supports fast, WebGL based text labels at datapoints, which can be customised. See the DataLabels API for more details. |
Render Data Transforms | Allows transforming data right before rendering. Used, for example, to add or remove data points just before rendering. See the RenderDataTransforms API |
Showing / hiding series | You can show/hide series in SciChart.js as well as be notified when a series is hidden. See the isVisibleChanged documentation for more details. |
Select series | Using a ChartModifier (an attached behaviour) you can add Series Selection, Hover callbacks and styling into SciChart.js. See the SeriesSelectionModifier documentation for more details. |
Select data-points | Using a ChartModifier (attached behaviour), you can add data-point selection detection, callbacks and styling into SciChart.js. See the DataPointSelectionModifier docs for more details. |
Tooltips and Cursors | Of course, SciChart.js supports customisable tooltips and cursors using ChartModifiers (attached behaviour). See the CursorModifier or RolloverModifier docs for more details. |
Nulls (Gaps) in Data | For line charts, mountain charts and 2D cartesian chart types you can draw nulls (gaps) in data, or even change style in the line using a technique we have. See the Drawing Gaps in Series documentation for more details. |

We are continually improving and adding features to SciChart.js. Some of the things on the roadmap are: more chart types, more interactions & even allowing custom drawing.

## The RenderableSeries Class

All 2D Chart types in SciChart.js are derived from the BaseRenderableSeries📘 type. This is a JavaScript class which is added to the sciChartSurface.renderableSeries📘 collection and is rendered using our own proprietary WebAssembly / WebGL based rendering engine.

Each RenderableSeries is rendered to the screen, displaying the data from an associated DataSeries.

### Renderable Series Properties

The properties common to the BaseRenderableSeries class📘 are listed below.

**BaseRenderableSeries** **property**

Here's the converted content in a two-column Markdown table with headers:

| Property | Description |
|---|---|
dataLabelProvider📘 | (New to v3.0) The dataLabelprovider allows creation of per data-point text labels. Please see the Data Labels API section for a complete walk-through of text labels on chart series. |
dataSeries📘 | The DataSeries is the data-source for the RenderableSeries. Please see DataSeries API section for a complete walk-through of the DataSeries API |
drawNanAs📘 | How to treat NAN (Not a number) values in the input dataSeries. See ELineDrawMode📘 for a list of values. |
renderDataTransform📘 | (New to v3.4) A RenderDataTransform may be optionally applied to a RenderableSeries to transform data immediately before drawing. Can be used to change the visual output e.g. create interpolated series, insert points into series and change styles in a series without changing the data. |
pointMarker📘 | A PointMarker📘 is used to draw an optional point-marker at each data-point. Applicable to some series types only. |
stroke📘 | A Stroke for lines, outlines and edges of this RenderableSeries. Acceptable values include RGB format e.g. "#FF0000", RGBA format e.g. "#FF000077" and RGBA format e.g. "rgba(255,0,0,0.5)" |
strokeThickness📘 | The Stroke Thickness for lines, outlines and edges of this RenderableSeries |
strokeDashArray📘 | Some chart types which support lines (e.g. Line series, Spline Line series, Mountain Series) support dashed lines. This property accepts an array which defines [dot, dash] length in pixels |
opacity📘 | An Opacity factor of the Series that controls its semi-transparency level, where value 1 means the Series is opaque; 0 means transparent. |
xAxisId📘 | The XAxisId of the series allows you to attach a series to a specific axis. If you only have single X and Y Axis you can leave this default. |
xAxis📘 | Link to the associated X Axis |
yAxisId📘 | The YAxisId of the series allows you to attach a series to a specific axis. If you only have single X and Y Axis you can leave this default. |
yAxis📘 | Link to the associated Y Axis |
isvisible📘 | When true, the series is visible. To hide a series, set IsVisible = false. |
isVisibleChanged📘 | An EventHandler📘 allowing you to subscribe to isVisible changed callbacks |
effect📘 | An optional ShaderEffect for modifying the render output of a RenderableSeries. |
paletteProvider📘 | The PaletteProvider API allows changing the color of a series on a per-point basis. For more details about the PaletteProvider API see the individual examples for Line Series, Column Series etc... |
hitTestProvider📘 | The HitTestProvider📘 exposes the Hit-Test API, used to determine whether a series has been clicked on, hovered or find the nearest Xy datapoint to a mouse coordinate. |

### Constructor options on RenderableSeries

Every RenderableSeries has a set of constructor options allowing for fast initialization and setup by passing in a javascript object. Each property reflected on the series has an optional constructor option parameter.

For example this code:

**Setting properties of series**

`const lineSeries = new FastLineRenderableSeries(wasmContext);`

lineSeries.stroke = "Red";

lineSeries.strokeThickness = 3;

lineSeries.dataSeries = new XyDataSeries(wasmContext, {xValues, yValues});

lineSeries.isVisible = true;

lineSeries.opacity = 0.7;

is equivalent to this:

**Constructor parameters of series**

`const lineSeries = new FastLineRenderableSeries(wasmContext, {`

stroke: "Red",

strokeThickness: 3,

dataSeries: new XyDataSeries(wasmContext, {xValues, yValues}),

isVisible: true,

opacity: 0.7

});

## Where Next?

To learn about a specific chart type, and to find out how to configure them, visit the following pages: