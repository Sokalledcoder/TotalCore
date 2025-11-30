---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/common-series-apis/drawing-point-markers
scraped_at: 2025-11-28T18:24:21.496688
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/common-series-apis/drawing-point-markers

# Drawing PointMarkers on Series (Scatter markers)

Every data point of a Scatter, Line, Bubble, Mountain, Spline, Error or Column Series may be marked with a PointMarker📘. So, not just limited to scatter series, you can apply a pointmarker to line series, or error bars to display a repeated marker at the X,Y point.

Simply set BaseRenderableSeries.pointMarker📘 = new EllipsePointMarker()📘 to apply a scatter point to most series types.

Several different types of PointMarker are available in SciChart.js:

- EllipsePointMarker📘 - Renders a circle at each point
- SquarePointMarker📘 - Renders a square at each point
- TrianglePointMarker📘 - Renders a triangle at each point
- CrossPointMarker📘 - Renders a plus sign '+' at each point
- XPointMarker📘 - Renders an 'x' at each point
- SpritePointMarker📘 - Allows an image to be used at each point to create custom pointmarkers

Below we're going to show some options how to use different types of PointMarker in SciChart.

- TS
- Builder API (JSON Config)

`// Create a chart with X,Y axis`

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { growBy: new NumberRange(0.0, 0.4) }));

// Create some data

const { xValues, yValues1, yValues2, yValues3, yValues4, yValues5 } = createData();

const commonOptions = { width: 11, height: 11, strokeThickness: 2 };

// Add a line series with EllipsePointMarker

sciChartSurface.renderableSeries.add(

new XyScatterRenderableSeries(wasmContext, {

pointMarker: new EllipsePointMarker(wasmContext, {

...commonOptions,

fill: "#0077FF99",

stroke: "LightSteelBlue"

}),

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues1 })

})

);

// Add a scatter series with SquarePointMarker

sciChartSurface.renderableSeries.add(

new XyScatterRenderableSeries(wasmContext, {

pointMarker: new SquarePointMarker(wasmContext, {

...commonOptions,

fill: "#FF000099",

stroke: "Red"

}),

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues2 })

})

);

// Add a scatter series with TrianglePointMarker

sciChartSurface.renderableSeries.add(

new XyScatterRenderableSeries(wasmContext, {

pointMarker: new TrianglePointMarker(wasmContext, {

...commonOptions,

fill: "#FFDD00",

stroke: "#FF6600"

}),

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues3 })

})

);

// Add a scatter series with CrossPointMarker

sciChartSurface.renderableSeries.add(

new XyScatterRenderableSeries(wasmContext, {

pointMarker: new CrossPointMarker(wasmContext, {

...commonOptions,

stroke: "#FF00FF"

}),

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues4 })

})

);

// Add a scatter series with Custom Image using SpritePointMarker

const imageBitmap = await createImageAsync("https://www.scichart.com/demo/images/CustomMarkerImage.png");

sciChartSurface.renderableSeries.add(

new XyScatterRenderableSeries(wasmContext, {

pointMarker: new SpritePointMarker(wasmContext, {

image: imageBitmap

}),

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues5 })

})

);

`const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {`

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: { type: EAxisType.NumericAxis },

yAxes: { type: EAxisType.NumericAxis, options: { growBy: new NumberRange(0, 0.15) } },

series: [

{

type: ESeriesType.ScatterSeries,

xyData: {

xValues,

yValues: yValues1

},

options: {

pointMarker: {

type: EPointMarkerType.Ellipse,

options: {

width: 11,

height: 11,

strokeThickness: 2,

fill: "#0077FF99",

stroke: "LightSteelBlue"

}

}

}

},

{

type: ESeriesType.ScatterSeries,

xyData: {

xValues,

yValues: yValues2

},

options: {

pointMarker: {

type: EPointMarkerType.Square,

options: {

width: 11,

height: 11,

strokeThickness: 2,

fill: "#FF000099",

stroke: "Red"

}

}

}

},

{

type: ESeriesType.ScatterSeries,

xyData: {

xValues,

yValues: yValues3

},

options: {

pointMarker: {

type: EPointMarkerType.Triangle,

options: {

width: 11,

height: 11,

strokeThickness: 2,

fill: "#FFDD00",

stroke: "#FF6600"

}

}

}

},

{

type: ESeriesType.ScatterSeries,

xyData: {

xValues,

yValues: yValues4

},

options: {

pointMarker: {

type: EPointMarkerType.Cross,

options: {

width: 11,

height: 11,

strokeThickness: 2,

stroke: "#FF00FF"

}

}

}

},

{

type: ESeriesType.ScatterSeries,

xyData: {

xValues,

yValues: yValues5

},

options: {

pointMarker: {

type: EPointMarkerType.Sprite,

options: {

image: await createImageAsync("https://www.scichart.com/demo/images/CustomMarkerImage.png")

}

}

}

}

]

});

This results in the following output:

## IsLastPointOnly mode for Pointmarkers

The PointMarker type has a property isLastPointOnly📘. When true, only the last point of a scatter series is drawn. This can be useful to highlight a point in say a sweeping ECG chart.

## Additional Tips for PointMarkers

Custom markers can be created using the SpritePointMarker📘 type, which allows loading a custom image as a marker. This uses the helper function createImageAsync📘 which allows loading of a PNG file either from URL, or locally hosted / imported image.

For a TypeScript / npm & webpack example you can see the JavaScript Custom PointMarkers Chart example in the SciChart.js demo.