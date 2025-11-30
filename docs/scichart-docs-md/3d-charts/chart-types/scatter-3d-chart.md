---
source: https://www.scichart.com/documentation/js/v4/3d-charts/chart-types/scatter-3d-chart
scraped_at: 2025-11-28T18:24:56.818511
---

# https://www.scichart.com/documentation/js/v4/3d-charts/chart-types/scatter-3d-chart

# The Scatter 3D Chart Type

Examples for the Scatter 3D Chart can be found in the SciChart.js Demo app which can be viewed on our website, or downloaged from SciChart.Js.Examples Github Repository

3D Scatter Charts are provided by the ScatterRenderableSeries3D📘 type. This draws a single PointMarker at an X,Y,Z location in the 3D world. Charts can be static or dynamic, and updated in real-time if required.

The ScatterRenderableSeries3D📘 supports multiple pointmarkers, including:

### 3D Marker Types

- SpherePointMarker3D📘 - a 3D Sphere at each point
- CubePointMarker3D📘 - 3D Cube at each point
- PyramidPointMarker3D📘 - a 3D Pyramid at each point
- CylinderPointMarker3D📘 - a 3D Cylinder at each point

### Fast 2D Marker types

- PixelPointMarker3D📘 - a single pixel at each point
- QuadPointMarker3D📘 - a Quad (flat square) facing the camera at each point
- EllipsePointMarker3D📘 - a flat ellipse facing the camera at each point
- TrianglePointMarker3D📘 - a flat triangle facing the camera at each point

## Declaring a 3D Scatter Series

To declare a 3D Scatter Series with PointMarker use the following code:

- TS
- HTML
- CSS

`import {`

SciChart3DSurface,

NumericAxis3D,

Vector3,

SciChartJsNavyTheme,

ScatterRenderableSeries3D,

XyzDataSeries3D,

SpherePointMarker3D,

MouseWheelZoomModifier3D,

OrbitModifier3D,

ResetCamera3DModifier,

NumberRange

} from "scichart";

const generateData = () => {

const gaussianRandom = (mean, stdev) => {

const u = 1 - Math.random(); // Converting [0,1) to (0,1]

const v = Math.random();

const z = Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);

// Transform to the desired mean and standard deviation:

return z * stdev + mean;

};

const xValues = [];

const yValues = [];

const zValues = [];

for (let i = 0; i < 1000; i++) {

xValues.push(gaussianRandom(0, 1));

yValues.push(gaussianRandom(0, 1));

zValues.push(gaussianRandom(0, 1));

}

return { xValues, yValues, zValues };

};

async function scatter3dChart(divElementId) {

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

visibleRange: new NumberRange(-3, 3)

});

sciChart3DSurface.yAxis = new NumericAxis3D(wasmContext, {

axisTitle: "Y Axis",

visibleRange: new NumberRange(-3, 3)

});

sciChart3DSurface.zAxis = new NumericAxis3D(wasmContext, {

axisTitle: "Z Axis",

visibleRange: new NumberRange(-3, 3)

});

// returns data in arrays of numbers e.g. xValues = [0,1,2,3,4], yValues = [0,1,2,3,4], zValues = [0,1,2,3,4]

const { xValues, yValues, zValues } = generateData();

// Add a ScatterRenderableSeries3D

sciChart3DSurface.renderableSeries.add(

new ScatterRenderableSeries3D(wasmContext, {

dataSeries: new XyzDataSeries3D(wasmContext, {

xValues,

yValues,

zValues

}),

opacity: 0.5,

pointMarker: new SpherePointMarker3D(wasmContext, {

fill: "#EC0F6C",

size: 10

})

})

);

// Optional: add zooming, panning for the example

sciChart3DSurface.chartModifiers.add(

new MouseWheelZoomModifier3D(), // provides camera zoom on mouse wheel

new OrbitModifier3D(), // provides 3d rotation on left mouse drag

new ResetCamera3DModifier()

); // resets camera position on double-click

}

scatter3dChart("scichart-root");

`<div class="wrapper">`

<div id="scichart-root"></div>

<div class="titleWrapper">

<p class="title">SciChart.js 3D Chart Example</p>

<p class="subtitle">Demonstrates a Per-point Color Scatter Chart</p>

<p class="subTitle">metadata.vertexColor defines color</p>

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

color: #ffffff77;

}

.title {

font-size: 20px;

}

.subTitle {

font-size: 16px;

}

This results in the following output:

## Coloring Individual Scatter Points

Scatter points may be colored or scaled individually using the PointMetadata3D API. To do this, set a PointMetadata3D📘 instance with property **vertexColor** at each data-point in the XyzDataSeries3D.

- TS
- HTML
- CSS

`// returns data in arrays of numbers e.g. xValues = [0,1,2,3,4], yValues = [0,1,2,3,4], zValues = [0,1,2,3,4]`

const { xValues, yValues, zValues } = generateData();

const colors = ["#EC0F6C", "#F48420", "#DC7969", "#67BDAF", "#50C7E0", "#264B93", "#14233C"];

// Metadata in scichart.js 3D overrides the color of a scatter point. It can also hold additional optional properties

// Below we format the xValues array into a metadata array, where each point is colored individually

const metadata = xValues.map((x, i) => {

// Return a random colour from the array above

const color = colors[Math.floor(Math.random() * colors.length)];

return { vertexColor: parseColorToUIntArgb(color) };

});

// Add a ScatterRenderableSeries3D

sciChart3DSurface.renderableSeries.add(

new ScatterRenderableSeries3D(wasmContext, {

dataSeries: new XyzDataSeries3D(wasmContext, {

xValues,

yValues,

zValues,

metadata // Optional metadata here. Property vertexColor is read to color the point

}),

// When metadata colours are provided, the pointMarker.fill is ignored

pointMarker: new SpherePointMarker3D(wasmContext, {

size: 7

})

})

);

`<div class="wrapper">`

<div id="scichart-root"></div>

<div class="titleWrapper">

<p class="title">SciChart.js 3D Chart Example</p>

<p class="subtitle">Demonstrates a Gaussian Distribution Scatter Chart</p>

<p class="subTitle">Drag the mouse to rotate, use MouseWheel to zoom</p>

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

color: #ffffff77;

}

.title {

font-size: 20px;

}

.subTitle {

font-size: 16px;

}

This results in the following output:

IPointMetadata3D📘 can be any javascript object but the property **vertexColor** is used to determine scatter 3D datapoint colour. This is in hex format Alpha, Red, Green, Blue, so 0xFFFF0000 would correspond to red. The helper function parseColorToUIntArgb📘 can convert Javascript Hex codes to this format.