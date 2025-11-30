---
source: https://www.scichart.com/documentation/js/v4/3d-charts/chart-types/lines-3d-chart
scraped_at: 2025-11-28T18:24:56.973532
---

# https://www.scichart.com/documentation/js/v4/3d-charts/chart-types/lines-3d-chart

# The Lines 3D Chart Type

Examples for the Lines 3D Chart can be found in the SciChart.js Demo app which can be viewed on our website, or downloaded from SciChart.Js.Examples Github Repository

3D Line Charts are provided by the PointLineRenderableSeries3D📘 type. This draws line segments from X,Y,Z data in the 3D world, with an optional point-marker. Charts can be static or dynamic, and updated in real-time if required.

The PointLineRenderableSeries3D📘 requires X,Y,Z data to render, stored in an XyzDataSeries3D📘. This series supports an optional pointmarker of multiple types, including:

### 3D Marker Types

- SpherePointMarker3D📘 - a 3D Sphere at each point
- CubePointMarker3D📘 - a 3D Cube at each point
- PyramidPointMarker3D📘 - a 3D Pyramid at each point
- CylinderPointMarker3D📘 - a 3D Cylinder at each point

### Fast 2D Marker types

- PixelPointMarker3D📘 - a single pixel at each point
- QuadPointMarker3D📘 - a Quad (flat square) facing the camera at each point
- EllipsePointMarker3D📘 - a flat ellipse facing the camera at each point
- TrianglePointMarker3D📘 - a flat triangle facing the camera at each point

## Declaring a 3D Point-Line Series

To declare a 3D Point-Line Series with use the following code:

- TS
- HTML
- CSS

`// Demonstrates how to create a 3D Lines chart in SciChart.js`

// Create a SciChart3DSurface in the host <div id=".." />

const { wasmContext, sciChart3DSurface } = await SciChart3DSurface.create(divElementId, {

theme: new SciChartJsNavyTheme(),

worldDimensions: new Vector3(300, 200, 300),

cameraOptions: {

position: new Vector3(-300, 300, -300),

target: new Vector3(0, 50, 0)

}

});

// Declare your axis like this

sciChart3DSurface.xAxis = new NumericAxis3D(wasmContext, {

axisTitle: "X Axis",

autoRange: EAutoRange.Once

});

sciChart3DSurface.yAxis = new NumericAxis3D(wasmContext, {

axisTitle: "Y Axis",

autoRange: EAutoRange.Once

});

sciChart3DSurface.zAxis = new NumericAxis3D(wasmContext, {

axisTitle: "Z Axis",

autoRange: EAutoRange.Once,

growBy: new NumberRange(0.2, 0.2)

});

// returns data in arrays of numbers e.g. xValues = [0,1,2,3,4], yValues = [0,1,2,3,4], zValues = [0,1,2,3,4]

const { xValues, yValues, zValues } = generateData(1);

// Add a PointLineRenderableSeries3D

sciChart3DSurface.renderableSeries.add(

new PointLineRenderableSeries3D(wasmContext, {

dataSeries: new XyzDataSeries3D(wasmContext, { xValues, yValues, zValues }),

opacity: 0.9,

stroke: "#EC0F6C",

strokeThickness: 3

})

);

// Repeat 2x

const dataset1 = generateData(2);

sciChart3DSurface.renderableSeries.add(

new PointLineRenderableSeries3D(wasmContext, {

dataSeries: new XyzDataSeries3D(wasmContext, {

xValues: dataset1.xValues,

yValues: dataset1.yValues,

zValues: dataset1.zValues

}),

opacity: 0.9,

stroke: "#50C7E0",

strokeThickness: 3,

// Pointmarkers are optional. Many different pointmarker types are supported

pointMarker: new EllipsePointMarker3D(wasmContext, { size: 3 })

})

);

const dataset2 = generateData(3);

sciChart3DSurface.renderableSeries.add(

new PointLineRenderableSeries3D(wasmContext, {

dataSeries: new XyzDataSeries3D(wasmContext, {

xValues: dataset2.xValues,

yValues: dataset2.yValues,

zValues: dataset2.zValues

}),

opacity: 0.9,

stroke: "#F48420",

strokeThickness: 3

})

);

// Optional: add zooming, panning for the example

sciChart3DSurface.chartModifiers.add(

new MouseWheelZoomModifier3D(), // provides camera zoom on mouse wheel

new OrbitModifier3D(), // provides 3d rotation on left mouse drag

new ResetCamera3DModifier()

); // resets camera position on double-click

`<div class="wrapper">`

<div id="scichart-root"></div>

<div class="titleWrapper">

<p class="title">SciChart.js 3D Chart Example</p>

<p class="subtitle">Demonstrates a 3D Lines Series in SciChart.js</p>

<p class="subTitle">Zoom, pan the chart with the mouse.</p>

</div>

</div>

`body {`

margin: 0;

font-family: Arial;

}

.wrapper {

width: 100%;

height: 100vh;

position: relative;

}

#scichart-root {

width: 100%;

height: 100%;

position: relative;

}

.titleWrapper {

position: absolute;

width: 100%;

top: 35%;

text-align: center;

pointer-events: none;

color: #ffffffaa;

}

.title {

font-size: 20px;

}

.subTitle {

font-size: 16px;

}

This results in the following output:

## Coloring Individual Line Segments

Line segments in SciChart.js 3D points may be colored or scaled individually using the PointMetada3D API. To do this, set a PointMetadata3D📘 instance with property **vertexColor** at each data-point in the XyzDataSeries3D📘.

Colors are in UInt Argb format. For this example below we use the helper functions parseColorToUIntArgb()📘 to convert from a JavaScript hex code to UInt32, and uintArgbColorLerp()📘 to linearly interpolate two colours.

- TS
- HTML
- CSS

`// returns data in arrays of numbers e.g. xValues = [0,1,2,3,4], yValues = [0,1,2,3,4], zValues = [0,1,2,3,4]`

const { xValues, yValues, zValues } = generateData(1);

const colorHigh = parseColorToUIntArgb("#EC0F6C");

const colorLow = parseColorToUIntArgb("#30BC9A");

const yMin = Math.min(...yValues);

const yMax = Math.max(...yValues);

const metadata = yValues.map((y, i) => {

// interpolate y between colorLow and colorHigh using the helper function uintArgbColorLerp

const t = (y - yMin) / (yMax - yMin);

const color = uintArgbColorLerp(colorLow, colorHigh, t);

return { vertexColor: color }

});

// Add a PointLineRenderableSeries3D

sciChart3DSurface.renderableSeries.add(new PointLineRenderableSeries3D(wasmContext, {

dataSeries: new XyzDataSeries3D(wasmContext, { xValues, yValues, zValues, metadata }),

opacity: 0.9,

// When metadata colors are provided, stroke is ignored

stroke: "#EC0F6C",

strokeThickness: 3,

// pointMarkers are optional

pointMarker: new EllipsePointMarker3D(wasmContext, { size: 3 })

}));

`<div class="wrapper">`

<div id="scichart-root"></div>

<div class="titleWrapper">

<p class="title">SciChart.js 3D Chart Example</p>

<p class="subtitle">Paletted 3D Lines Series in SciChart.js</p>

<p class="subTitle">Zoom, pan the chart with the mouse.</p>

</div>

</div>

`body {`

margin: 0;

font-family: Arial;

}

.wrapper {

width: 100%;

height: 100vh;

position: relative;

}

#scichart-root {

width: 100%;

height: 100%;

position: relative;

}

.titleWrapper {

position: absolute;

width: 100%;

top: 35%;

text-align: center;

pointer-events: none;

color: #ffffffaa;

}

.title {

font-size: 20px;

}

.subTitle {

font-size: 16px;

}

This results in the following output:

IPointMetadata3D📘 can be any javascript object but the property **vertexColor** is used to determine scatter 3D datapoint colour. This is in hex format Alpha, Red, Green, Blue, so 0xFFFF0000 would correspond to red. The helper function parseColorToUIntArgb📘 can convert Javascript Hex codes to this format.