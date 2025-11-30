---
source: https://www.scichart.com/documentation/js/v4/3d-charts/chart-types/column-3d-chart
scraped_at: 2025-11-28T18:24:56.516884
---

# https://www.scichart.com/documentation/js/v4/3d-charts/chart-types/column-3d-chart

# The Column 3D Chart Type

JavaScript 3D Column Charts can be created using the ColumnRenderableSeries3D📘 type. This chart type draws columns or bars from X,Y,Z data in the 3D world, with a pointmarker denoting the shape of the column. Column 3D Charts can be static or dynamic, and updated in real-time if required.

The JavaScript / React 3D Column Chart Example can be found in the SciChart.Js Examples Suite on Github, or our live demo at scichart.com/demo

## Create a 3D Column Chart

To declare a 3D Column Chart in JavaScript, use the following code:

- TS
- HTML
- CSS

`// Demonstrates how to create a 3D Column chart in SciChart.js`

// Create a SciChart3DSurface in the host <div id=".." />

const { wasmContext, sciChart3DSurface } = await SciChart3DSurface.create(divElementId, {

theme: new SciChartJsNavyTheme(),

worldDimensions: new Vector3(300, 200, 300),

cameraOptions: {

position: new Vector3(-270, 230, -160),

target: new Vector3(0, 50, 0)

}

});

// Declare your axis like this

sciChart3DSurface.xAxis = new NumericAxis3D(wasmContext, {

axisTitle: "X Axis"

});

sciChart3DSurface.yAxis = new NumericAxis3D(wasmContext, {

axisTitle: "Y Axis"

});

sciChart3DSurface.zAxis = new NumericAxis3D(wasmContext, {

axisTitle: "Z Axis"

});

// Create a 2D array and fill this with data. returns 2D array [zIndex][xIndex]

const heightmapArray = generateData(25, 25);

// Unwrap into 3x 1D arrays for xValues, yValues, zValues

const xValues = [];

const zValues = [];

const yValues = heightmapArray.flatMap((row, xIndex) => {

row.forEach((_, zIndex) => {

xValues.push(xIndex); // X corresponds to the row index

zValues.push(zIndex); // Z corresponds to the column index

});

return row; // Flattened Z-values for each row

});

// Declare an XyzDataSeries3D passing in the x,y,zValues which specify 3d positions

// of columns.

// The xValues, zValues provide the position on the floor plane.

// The yValues provide the heights of columns

const dataSeries = new XyzDataSeries3D(wasmContext, {

xValues,

yValues,

zValues,

dataSeriesName: "Column Series 3D"

});

// Add the 3D column series to the chart

sciChart3DSurface.renderableSeries.add(

new ColumnRenderableSeries3D(wasmContext, {

dataSeries,

fill: "#F48420",

dataPointWidthX: 0.5,

dataPointWidthZ: 0.5,

pointMarker: new CubePointMarker3D(wasmContext)

})

);

// Optional: add zooming, panning for the example

sciChart3DSurface.chartModifiers.add(

new MouseWheelZoomModifier3D(), // provides camera zoom on mouse wheel

new OrbitModifier3D(), // provides 3d rotation on left mouse drag

new ResetCamera3DModifier() // resets camera position on double-click

);

`<div class="wrapper">`

<div id="scichart-root"></div>

<div class="titleWrapper">

<p class="title">SciChart.js 3D Column Chart Example</p>

<p class="subtitle">Demonstrates 3D Column Series in SciChart.js</p>

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

Breaking this code down:

We initialize a 3D chart by calling SciChart3DSurface.create()📘. The worldDimensions📘 and cameraOptions📘 are passed to SciChart3DSurface.create()📘 to initialize the 3D scene.

An xAxis, yAxis and zAxis are declared of type NumericAxis3D📘.

Additional code is added to generate some data which is unwrapped into 1D arrays of X,Y and ZValues. These will specify the discrete 3D points on the column chart: X-Z providing the position and Y value providing the height. Data is passed into a XyzDataSeries3D📘 which is the data source for the 3D column chart.

A ColumnRenderableSeries3D📘 is created and added to the SciChart3DSurface.renderableSeries📘 collection. We set the dataPointWidth📘 properties to define the size of the 3D bar as well as the fill📘 and pointMarker📘 properties to define the colour and type (shape) of the column.

This results in the following output:

## Choosing a Column / Bar Type

The ColumnRenderableSeries3D📘 requires X,Y,Z data to render, stored in an XyzDataSeries3D📘. This series supports an optional pointmarker of multiple types, including:

### 3D Marker Types

- SpherePointMarker3D📘 - a 3D Sphere represents each bar/column
- CubePointMarker3D📘 - a 3D Cube represents each bar/column
- PyramidPointMarker3D📘 - a 3D Pyramid represents each bar/column
- CylinderPointMarker3D📘 - a 3D Cylinder represents each bar/column

Changing the ColumnRenderableSeries3D.pointMarker📘 property will update the type / shape of object used to denote a column.

## Colouring Individual Columns

By default, the colour of the Column series is defined by ColumnRenderableSeries.fill📘. This can be overridden on a per-column basis using the metadata📘 array passed to XyzDataSeries3D📘.

Update your code sample as follows:

- TS
- HTML
- CSS

`// Create a SciChart3DSurface in the host <div id=".." />`

const { wasmContext, sciChart3DSurface } = await SciChart3DSurface.create(

divElementId,

{

theme: new SciChartJsNavyTheme(),

worldDimensions: new Vector3(300, 200, 300),

cameraOptions: {

position: new Vector3(-270, 230, -160),

target: new Vector3(0, 50, 0),

},

}

);

// Declare your axis like this

sciChart3DSurface.xAxis = new NumericAxis3D(wasmContext, {

axisTitle: "X Axis",

});

sciChart3DSurface.yAxis = new NumericAxis3D(wasmContext, {

axisTitle: "Y Axis",

});

sciChart3DSurface.zAxis = new NumericAxis3D(wasmContext, {

axisTitle: "Z Axis",

});

// Metadata colours are in ARGB format, e.g. 0xFFFF0000 is red, 0xFF00FF00 is green

// The helper function parseColorToUIntArgb can be used to convert HTML colors to ARGB

const htmlColors = [

"#EC0F6C",

"orange",

"#67BDAF",

"SteelBlue",

"#14233C",

"#67BDAF",

"orange",

"#F48420",

"SteelBlue",

"#EC0F6C",

"#EC0F6C",

"#67BDAF",

"#67BDAF",

"SteelBlue",

"DarkBlue",

"#F48420",

"orange",

"#67BDAF",

"SteelBlue",

"#67BDAF",

];

// Declare a dataSeries with xValues, yValues (heights), zValues

// Metadata can be any javascript object

// metadata.vertexColor is the UINT ARGB color of the column

const dataSeries = new XyzDataSeries3D(wasmContext, {

xValues: [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4],

yValues: [0, 1, 2, 3, 4, 3, 2, 4, 5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 4, 5],

zValues: [

0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,

],

metadata: htmlColors.map((c) => ({ vertexColor: parseColorToUIntArgb(c) })),

});

sciChart3DSurface.renderableSeries.add(

new ColumnRenderableSeries3D(wasmContext, {

dataSeries,

dataPointWidthX: 0.7,

dataPointWidthZ: 0.7,

// Per column coloring using metadata

useMetadataColors: true,

pointMarker: new CylinderPointMarker3D(wasmContext),

})

);

`<div class="wrapper">`

<div id="scichart-root"></div>

<div class="titleWrapper">

<p class="title">SciChart.js 3D Column Chart Example</p>

<p class="subtitle">Demonstrates 3D Column Series in SciChart.js</p>

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

This example also shows a variation in the column type to use CylinderPointMarker3D📘 which must be imported.

Metadata are simply javascript objects attached to the XyzDataSeries3D📘 in SciChart. The property metadata.vertexColor📘 is used to determine column 3D datapoint colour.

Finally, when specifying metadata colors, the property ColumnRenderableSeries3D.useMetadataColors📘 must be set to true.

Here's the updated output: