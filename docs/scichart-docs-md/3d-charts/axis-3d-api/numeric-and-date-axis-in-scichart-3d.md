---
source: https://www.scichart.com/documentation/js/v4/3d-charts/axis-3d-api/numeric-and-date-axis-in-scichart-3d
scraped_at: 2025-11-28T18:24:54.765367
---

# https://www.scichart.com/documentation/js/v4/3d-charts/axis-3d-api/numeric-and-date-axis-in-scichart-3d

# Numeric and Date Axis in SciChart3D

SciChart.js 3D features several axis types. All inherit from AxisBase3D📘. The Axis are the logical representation of the XZ, ZY, YX planes in the Axis Cube.

X,Y,Z axis are required to measure the sciChart3DSurface.renderableSeries📘, for instance, an axis is responsible for the transformation between data-values (provided by your code) and world coordinates (X,Y,Z values in 3D Space).

See the article on Coordinates in 3D Space to explain the difference between World and Data coordinates and how to define the dimensions of the Axis Cube.

## NumericAxis3D

The NumericAxis3D📘 is a Value-Axis and is suitable when the data on that axis is numeric (e.g. JavaScript number - 64-bit double precision values).

The API between SciChart.js 2D and 3D is shared, so all properties related to showing/hiding gridlines, formatting labels or spacing of labels are shared between 2D & 3D charts.

Here's a short example showing how to configure this axis type.

You will find the code here.

- TS
- HTML
- CSS

`import {`

SciChart3DSurface,

NumericAxis3D,

Vector3,

NumberRange,

SciChartJsNavyTheme,

ENumericFormat,

MouseWheelZoomModifier3D,

OrbitModifier3D,

ResetCamera3DModifier

} from "scichart";

async function numericAxis3D(divElementId) {

// Demonstrates how to create a 3D chart with X,Y,Z axis in SciChart.js

// Create a SciChart3DSurface in the host <div id=".." />

const { wasmContext, sciChart3DSurface } = await SciChart3DSurface.create(divElementId, {

theme: new SciChartJsNavyTheme(),

worldDimensions: new Vector3(300, 200, 300),

cameraOptions: {

position: new Vector3(300, 300, 300),

target: new Vector3(0, 50, 0)

}

});

// Create an xAxis and assign to SciChart3DSurface

sciChart3DSurface.xAxis = new NumericAxis3D(wasmContext, {

// All these properties are optional

// Enable flags like drawing gridlines

drawMajorGridLines: true,

drawMinorGridLines: true,

drawLabels: true,

axisTitle: "X Axis, 4-decimal places",

// set VisibleRange. If not SciChart will calculate this on startup

visibleRange: new NumberRange(0, 1000),

// Enable decision labels with 4 significant figures

labelFormat: ENumericFormat.Scientific,

cursorLabelFormat: ENumericFormat.Decimal,

labelPrecision: 4,

// Hint to show no more than 5 labels on the axis

maxAutoTicks: 5,

// Offset our labels so that they dont overlap

titleOffset: 50,

tickLabelsOffset: 10

});

// Create the Y-Axis and assign to SciChart3DSurface

sciChart3DSurface.yAxis = new NumericAxis3D(wasmContext, {

axisTitle: "Y Axis, 2 dp, prefix & postfix",

labelPrecision: 2,

labelPrefix: "$",

labelPostfix: " USD",

visibleRange: new NumberRange(10, 10000),

// Hint to show no more than 5 labels on the axis

maxAutoTicks: 5,

// Offset our labels so that they dont overlap

titleOffset: 50,

tickLabelsOffset: 10

});

sciChart3DSurface.zAxis = new NumericAxis3D(wasmContext, {

axisTitle: "Z Axis, 0 dp",

// labelFormat: ENumericFormat.Scientific,

visibleRange: new NumberRange(0, 1000),

labelPrecision: 0,

labelPostfix: " kWh",

// Hint to show no more than 5 labels on the axis

maxAutoTicks: 5,

// Offset our labels so that they dont overlap

titleOffset: 50,

tickLabelsOffset: 10

});

// Optional: add zooming, panning for the example

sciChart3DSurface.chartModifiers.add(

new MouseWheelZoomModifier3D(), // provides camera zoom on mouse wheel

new OrbitModifier3D(), // provides 3d rotation on left mouse drag

new ResetCamera3DModifier()

); // resets camera position on double-click

}

numericAxis3D("scichart-root");

`<div class="wrapper">`

<div id="scichart-root" ></div>

<div class="titleWrapper">

<p class="title">SciChart.js 3D Chart Example</p>

<p class="subTitle">Demonstrate label formatting in 3D</p>

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

## Date Axis 3D

At the time of writing, there is no date-specific axis in SciChart.js 3D. However, it is still possible to use NumericAxis3D📘 with date formatting, assuming your data is included as linux timestamps / 1000.

For this to work, the values in the X-direction must be linux timestamps / 1000 (seconds since 01-01-1970). Axis.visibleRange also expects values in this format.

You will find the code here.

- TS
- HTML
- CSS

`import {`

SciChart3DSurface,

NumericAxis3D,

Vector3,

NumberRange,

SciChartJsNavyTheme,

ENumericFormat,

MouseWheelZoomModifier3D,

OrbitModifier3D,

ResetCamera3DModifier

} from "scichart";

async function numericAxisFormattedAsDates3D(divElementId) {

// Demonstrates how to create a 3D chart with X,Y,Z axis in SciChart.js

// Create a SciChart3DSurface in the host <div id=".." />

const { wasmContext, sciChart3DSurface } = await SciChart3DSurface.create(divElementId, {

theme: new SciChartJsNavyTheme(),

worldDimensions: new Vector3(300, 200, 300),

cameraOptions: {

position: new Vector3(300, 300, 300),

target: new Vector3(0, 50, 0)

}

});

// If you want to show an XAxis with dates between 1st March 2023 and 10th March 2023

const minDate = new Date("2023-03-01");

const maxDate = new Date("2023-03-10");

// Create an xAxis and assign to SciChart3DSurface

sciChart3DSurface.xAxis = new NumericAxis3D(wasmContext, {

axisTitle: "XAxis DD-MM-YYYY",

// We need to specify some visibleRange to see these two dates

// SciChart.js expects linux timestamp / 1000

visibleRange: new NumberRange(minDate.getTime() / 1000, maxDate.getTime() / 1000),

// Enable formatting as dates. Expects values on this axis to be in seconds since 1970-01-01

labelFormat: ENumericFormat.Date_DDMMYYYY,

titleOffset: 100

});

// Create the Y and Z-Axis and assign to SciChart3DSurface

sciChart3DSurface.yAxis = new NumericAxis3D(wasmContext, {

axisTitle: "Y Axis"

});

sciChart3DSurface.zAxis = new NumericAxis3D(wasmContext, {

axisTitle: "Z Axis"

});

// Optional: add zooming, panning for the example

sciChart3DSurface.chartModifiers.add(

new MouseWheelZoomModifier3D(), // provides camera zoom on mouse wheel

new OrbitModifier3D(), // provides 3d rotation on left mouse drag

new ResetCamera3DModifier()

); // resets camera position on double-click

}

numericAxisFormattedAsDates3D("scichart-root");

`<div class="wrapper">`

<div id="scichart-root" ></div>

<div class="titleWrapper">

<p class="title">SciChart.js 3D Chart Example</p>

<p class="subTitle">Formatting values as Dates</p>

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