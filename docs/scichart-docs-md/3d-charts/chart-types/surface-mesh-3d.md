---
source: https://www.scichart.com/documentation/js/v4/3d-charts/chart-types/surface-mesh-3d
scraped_at: 2025-11-28T18:24:57.339880
---

# https://www.scichart.com/documentation/js/v4/3d-charts/chart-types/surface-mesh-3d

# The SurfaceMesh 3D Chart Type

Examples for the Surface Mesh 3D Chart can be found in the SciChart.js Demo app which can be viewed on our website, or downloaded from SciChart.Js.Examples Github Repository

3D Surface (topology, grid) Mesh Charts are provided by the SurfaceMeshRenderableSeries3D📘 type. The surface mesh renders a two-dimensional array as a heightmap. This allows a number of configurable chart types in SciChart.js 3D, including:

- Dynamic, updating Surfaces (terrains or height maps)
- Texturing of surfaces or terrains or height maps
- Contour mapping or wireframe on terrain or height maps

Background reading: it may be helpful to read the 2D Heatmap documentation. Heatmaps share a lot of similarities with 3D Surface Mesh charts as both use 2-dimensional `number[][]`

arrays, and both use colorMaps to map cell values to cell color.

## Declaring a Surface Mesh with Uniform Data

To declare a Surface Mesh with uniform data, use the following code:

- TS
- HTML
- CSS

`// Create a SciChart3DSurface in the host <div id=".." />`

const { wasmContext, sciChart3DSurface } = await SciChart3DSurface.create(divElementId, {

theme: new SciChartJsNavyTheme(),

worldDimensions: new Vector3(300, 200, 300),

cameraOptions: {

position: new Vector3(-300, 300, -300),

target: new Vector3(0, 50, 0)

}

});

// Declare your X,Y,Z axis

sciChart3DSurface.xAxis = new NumericAxis3D(wasmContext, { axisTitle: "X Axis" });

sciChart3DSurface.yAxis = new NumericAxis3D(wasmContext, {

axisTitle: "Y Axis",

visibleRange: new NumberRange(0, 1)

});

sciChart3DSurface.zAxis = new NumericAxis3D(wasmContext, { axisTitle: "Z Axis" });

// Create a 2D array and fill this with data. returns 2D array [zIndex][xIndex]

const heightmapArray = generateData(40, 40);

const dataSeries = new UniformGridDataSeries3D(wasmContext, {

yValues: heightmapArray,

xStep: 1, // Defines each cell in X occupies 1 data point on the X axis

zStep: 1, // Defines each cell in Z occupies 1 data point on the Z axis

dataSeriesName: "Uniform Surface Mesh"

});

// Create the color map. GradientColorPalette maps heightMap values to a color range

const colorMap = new GradientColorPalette(wasmContext, {

gradientStops: [

{ offset: 1, color: "#EC0F6C" },

{ offset: 0.55, color: "#F48420" },

{ offset: 0.3, color: "#67BDAF" },

{ offset: 0.2, color: "#50C7E0" },

{ offset: 0.1, color: "#264B93" },

{ offset: 0, color: "#14233C" }

]

});

// Finally, create a SurfaceMeshRenderableSeries3D and add to the chart

const series = new SurfaceMeshRenderableSeries3D(wasmContext, {

// Apply the Data to the series. Data can be updated dynamically

dataSeries,

minimum: 0, // minimum value corresponds to colorMap offset=0

maximum: 1.0, // maximum value corresponds to colorMap offset=1

stroke: "White", // Wireframe stroke

strokeThickness: 1.5,

drawSkirt: false, // Draws solid wall to zero

drawMeshAs: EDrawMeshAs.SOLID_WIREFRAME, // Draw mesh as solid, wireframe or solid wireframe

meshPaletteMode: EMeshPaletteMode.HEIGHT_MAP_SOLID_CELLS, // Interpolation mode for cell colors

meshColorPalette: colorMap

});

sciChart3DSurface.renderableSeries.add(series);

`<div class="wrapper">`

<div id="scichart-root"></div>

<div class="titleWrapper">

<p class="title">SciChart.js 3D Chart Example</p>

<p class="subTitle">Demonstrates the 3D Surface Mesh type</p>

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

color: #ffffffaa;

}

.title {

font-size: 20px;

}

.subTitle {

font-size: 16px;

}

this results in the following output

Breaking this down:

- We create a 2-dimensional array of numbers to store the heights (yValues). This is in the format
`number[][]`

and contains double precision values. - Height values are applied to a UniformGridDataSeries3D📘. The dataSeries is set on the dataSeries property of a SurfaceMeshRenderableSeries3D📘
- Data-values are mapped to colours using a MeshColorPalette📘. In this example we use GradientColorPalette📘 to map heights to a list of gradient stops.
- Other properties are set to control wireframe, X,Y,Z axis and drawing.

The dimensions of the yValues height 2D array are `[zIndex][xIndex]`

.

## Applying Color Palettes (Heightmaps) to Surfaces

yValues📘 in the UniformGridDataSeries3D are a 2-dimensional array of type `number[][]`

. These are mapped to heights in the 3D world, and are also mapped to colors using the SurfaceMeshRenderableSeries3D.meshColorPalette📘 property.

The mapping is similar to the method used by the 2D Heatmap Series. Let's explain by digging into a simple example below.

- TS
- HTML
- CSS

`// Create a Surface Mesh with MeshColorPalette`

const series = new SurfaceMeshRenderableSeries3D(wasmContext, {

minimum: 0, // minimum value corresponds to colorMap offset=0

maximum: 10, // maximum value corresponds to colorMap offset=1

dataSeries: new UniformGridDataSeries3D(wasmContext, {

yValues: [

[0, 1, 2, 3, 4],

[5, 6, 7, 8, 9],

[10, 11, 12, 13, 14],

],

}),

meshColorPalette: new GradientColorPalette(wasmContext, {

gradientStops: [

{offset: 1, color: "#EC0F6C"}, // yValues >= maximum mapped to this color

{offset: 0.55, color: "#F48420"},

{offset: 0.3, color: "#67BDAF"},

{offset: 0.2, color: "#50C7E0"},

{offset: 0.1, color: "#264B93"},

{offset: 0, color: "#14233C"} // yValues <= minimum mapped to this color

],

}),

opacity: 0.77,

stroke: "White",

strokeThickness: 2,

drawSkirt: false,

lightingFactor: 0,

drawMeshAs: EDrawMeshAs.SOLID_WIREFRAME, // Draw mesh as solid, wireframe or solid wireframe

meshPaletteMode: EMeshPaletteMode.HEIGHT_MAP_SOLID_CELLS, // Interpolation mode for cell colors

});

sciChart3DSurface.renderableSeries.add(series);

`<div class="wrapper">`

<div id="scichart-root"></div>

<div class="titleWrapper">

<p class="title">SciChart.js 3D Chart Example</p>

<p class="subTitle">Demonstrates mapping of 3D Surface data to Color</p>

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

color: #ffffffaa;

}

.title {

font-size: 20px;

}

.subTitle {

font-size: 16px;

}

What this means:

- The GradientStop at Offset = 0 with corresponds to the SurfaceMeshRenderableSeries3D.minimum📘 value of 0
- The GradientStop at Offset = 1 corresponds to SurfaceMeshRenderableSeries3D.maximum📘 value of 14.
- Data within this range will be blended according to the gradient stops between 0 and 1
- Data outside this range will be clamped to the minimum or maximum colors in the GradientColorPalette📘

## Overlaying a Heightmap Legend on the Surface

Adding a Legend to a 3D Surface Mesh can be done with the HeatmapLegend control. See the Surface Mesh Demo at scichart.com/demo for a code sample showing how.

## Configuring the Wireframe on the Surface

The wireframe on the Surface Mesh can be configured with the following properties:

| Property | Description |
|---|---|
| stroke📘 | The stroke color of the wireframe. |
| strokeThickness📘 | The strokethickness of the wireframe. |
| drawMeshAs📘 | Enumeration defines whether the wireframe is drawn or not. Set to EDrawMeshAs📘. WIREFRAME, SOLID_WIREFRAME or SOLID_WIREFRAME_WITH_CONTOURS to enable mesh wireframe drawing. |

## Configuring Contours on the Surface

Contours may be configured on the mesh by setting additional properties.

| Property | Description |
|---|---|
| contourStroke📘 | The stroke color of contours. |
| contourStrokeThickness📘 | The strokethickness of contours. |
| contourOffset📘 | A constant offset of where to start calculating contours from. |
| contourInterval📘 | A factor defining the interval of Y-value between contours. |
| drawMeshAs📘 | Enumeration defines whether the contours are drawn or not. Set to EDrawMeshAs📘: CONTOURS, SOLID_WITH_CONTOURS, or SOLID_WIREFRAME_WITH_CONTOURS to enable mesh wireframe drawing. |

## Additional Surface Mesh Properties

Additional properties can be set to control surface mesh rendering and appearance. These are found below.

| Property | Description |
|---|---|
| meshPaletteMode📘 | Defines how cells are filled by palettes. E.g. interpolated, or solid cells, or textured. |
| drawSkirt📘 | When true, draws a wall to zero around the edges of the surface mesh. |
| heightScaleFactor📘 | Scaling factor for heights. Default = 1. When between 0..1, this is a multiplier on the final height of the mesh. |
| lightingFactor📘 | Setting from 0..1 which affects surface mesh rendering shininess or lighting. |
| yOffset📘 | A constant offset applied to a surface mesh in the Y-direction (height). |