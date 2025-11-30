---
source: https://www.scichart.com/documentation/js/v4/3d-charts/chart-types/bubble-3d-chart
scraped_at: 2025-11-28T18:24:56.122541
---

# https://www.scichart.com/documentation/js/v4/3d-charts/chart-types/bubble-3d-chart

# The Bubble 3D Chart Type

Examples for the Scatter/Bubble 3D Chart can be found in the SciChart.js Demo app which can be viewed on our website, or downloaded from SciChart.Js.Examples Github Repository

3D Bubble Charts are provided by the ScatterRenderableSeries3D📘 type. This draws a single PointMarker at an X,Y,Z location in the 3D world with a per-point scaling factor. Charts can be static or dynamic, and updated in real-time if required.

The ScatterRenderableSeries3D📘 allows creation of 3D Bubble charts and supports multiple pointmarkers, including:

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

## Declaring a 3D Bubble Series with custom Sizes & Colors

To declare a 3D Bubble Series with individual sizes & colors, use the following code.

- TS
- HTML
- CSS

`// returns data in arrays of numbers e.g. xValues = [0,1,2,3,4], yValues = [0,1,2,3,4], zValues = [0,1,2,3,4]`

const { xValues, yValues, zValues } = generateData();

const colors = ["#EC0F6C", "#F48420", "#DC7969", "#67BDAF", "#50C7E0", "#264B93", "#14233C"];

// Metadata in scichart.js 3D overrides the color of a scatter point. It can also hold additional optional properties

// Below we format the xValues array into a metadata array, where each point is colored individually

const metadata = [];

for (let i = 0; i < xValues.length; i++) {

const { x, y, z } = { x: xValues[i], y: yValues[i], z: zValues[i] };

// Compute a scale factor based on distance from origin

const distanceFromOrigin = Math.sqrt(x * x + y * y + z * z);

const scaleFactor = 1 - distanceFromOrigin / 3;

// Return a random colour from the array above

const color = colors[Math.floor(Math.random() * colors.length)];

console.log(`Point ${i} has scale factor ${scaleFactor} and color ${color}`);

// Return IPointMetadat3D with pointScale and vertexColor properties

metadata.push({

vertexColor: parseColorToUIntArgb(color),

pointScale: scaleFactor

});

}

// Add a ScatterRenderableSeries3D configured as bubble chart

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

size: 25

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