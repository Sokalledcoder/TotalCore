---
source: https://www.scichart.com/documentation/js/v4/3d-charts/axis-3d-api/axis-3d-text-label-formatting
scraped_at: 2025-11-28T18:24:55.250841
---

# https://www.scichart.com/documentation/js/v4/3d-charts/axis-3d-api/axis-3d-text-label-formatting

# Axis3D Text (Label) Formatting

Axis 3D Label Formatting obeys the same rules as SciChart 2D.

Each axis has a labelProvider📘 property, which allows you to attach pre-built classes to format numbers, dates, as well as create your own.

Background reading: Read the Axis LabelProvider API Overview to learn more about this powerful API

## Simple examples of formatting Labels

Axis can have simple label formatting via constructor options. Things like setting the **number of decimal places**, **prefix** and **postfix**, and **scientific notation** can be achieved by just setting some properties.

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

## Date Formatting

There is no date axis in SciChart.js 3D, however it is possible to achieve date or time formatting using labelProviders. Take a look at this quick example:

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

## Custom Label Formatting Rules

Using the labelProvider API, more complex rules can be created to format axis labels in SciChart.js 3D.

Below we've adapted the example from 2D Charts - Custom LabelProviders: Readable Numbers to apply it to a 3D axis.

First, delcare the custom LabelProvider class by inheriting one of the available base types in SciChart.js.

- TS

`// A custom class which inherits NumericLabelProvider for advanced numeric formatting`

// You can also inherit DateLabelProvider for date formatting

class CustomNumericLabelProvider extends NumericLabelProvider {

customFormat = "Commas"; // Options are "Default", "Commas" and "KMBT"

// Options accepts values from ILabel2DOptions or 'customFormat' e.g.

// { customFormat: "Commas", labelPrefix: "$", labelPrecision: 2 } or { customFormat: "KMBT" }

constructor(options) {

super(options);

this.customFormat = options?.customFormat ?? "Commas";

}

// Called for each label

// @ts-ignore TODO base class defines instance member as accessor

formatLabel(dataValue) {

if (this.customFormat === "Default") {

return super.formatLabel(dataValue);

} else if (this.customFormat === "Commas") {

// Format numbers using the default format, but with commas e.g. 1,000,000

return this.formatNumberWithCommas(dataValue);

} else if (this.customFormat === "KMBT") {

// Format large numbers with K, M, B abbreviations e.g. 1.5M

return this.formatNumberKMBT(dataValue);

}

return "";

}

// Called for each tooltip/cursor label

// @ts-ignore TODO base class defines instance member as accessor

formatCursorLabel(dataValue) {

return this.formatLabel(dataValue);

}

// Formats a label with commas e.g. 1000000 becomes 1,000,000

formatNumberWithCommas(dataValue) {

const labelValue = super.formatLabel(dataValue);

const commasRegex = /\B(?=(\d{3})+(?!\d))/g;

const output = labelValue.replace(commasRegex, ",");

// Log what happened for educational purposes

console.log(`formatNumberWithCommas: ${dataValue} => ${labelValue} => ${output}`);

return output;

}

// Returns a number formatted as K, M, B, T for thousands, millions, billions, trillions

formatNumberKMBT(dataValue) {

// formatLabel applies decimal, significant figure formatting and adds prefix, postfix

let originalLabel = super.formatLabel(dataValue);

let result = originalLabel;

// Now we need to inject K, M, B, T into the label before the postfix

// e.g. formatLabel(1000000) with prefix="$", postfix="USD" = "$1000000 USD" => "$1M USD"

if (dataValue >= 1_000_000_000_000) {

result = super.formatLabel(dataValue / 1_000_000_000_000).replace(this.postfix, "T" + this.postfix);

} else if (dataValue >= 1_000_000_000) {

result = super.formatLabel(dataValue / 1_000_000_000).replace(this.postfix, "B" + this.postfix);

} else if (dataValue >= 1_000_000) {

result = super.formatLabel(dataValue / 1_000_000).replace(this.postfix, "M" + this.postfix);

} else if (dataValue >= 1_000) {

result = super.formatLabel(dataValue / 1_000).replace(this.postfix, "K" + this.postfix);

}

// Log what happened for educational purposes

console.log(`formatNumberKMBT: ${dataValue} => ${originalLabel} => ${result}`);

return result;

}

}

Next, we create a chart and attach it to chart axis.

- TS
- HTML
- CSS

`async function labelProvider3D(divElementId) {`

// Create a SciChart3DSurface in the host <div id=".." />

const { wasmContext, sciChart3DSurface } = await SciChart3DSurface.create(divElementId, {

theme: new SciChartJsNavyTheme(),

worldDimensions: new Vector3(300, 200, 300),

cameraOptions: {

position: new Vector3(-300, 300, -300),

target: new Vector3(0, 50, 0)

}

});

// Declare an X,Y,Z axis using custom labelProviders

sciChart3DSurface.xAxis = new NumericAxis3D(wasmContext, {

axisTitle: "X Axis [Commas]",

visibleRange: new NumberRange(1000, 1000000),

labelProvider: new CustomNumericLabelProvider({

customFormat: "Commas",

labelPrecision: 0

})

});

sciChart3DSurface.yAxis = new NumericAxis3D(wasmContext, {

axisTitle: "Y Axis [Default]",

visibleRange: new NumberRange(0, 100)

});

sciChart3DSurface.zAxis = new NumericAxis3D(wasmContext, {

axisTitle: "Z Axis [KMBT]",

visibleRange: new NumberRange(0, 10000000),

labelPrefix: "$",

labelPostfix: " USD",

labelProvider: new CustomNumericLabelProvider({

customFormat: "KMBT",

labelPrefix: "$",

labelPostfix: " USD",

labelPrecision: 2,

labelFormat: ENumericFormat.SignificantFigures

})

});

// Optional: add zooming, panning for the example

sciChart3DSurface.chartModifiers.add(

new MouseWheelZoomModifier3D(), // provides camera zoom on mouse wheel

new OrbitModifier3D(), // provides 3d rotation on left mouse drag

new ResetCamera3DModifier()

); // resets camera position on double-click

}

`<div class="wrapper">`

<div id="scichart-root" ></div>

<div class="titleWrapper">

<p class="title">SciChart.js 3D Chart Example</p>

<p class="subTitle">Demonstrates Advanced Text Label Formatting</p>

<p class="subTitle">using LabelProviders</p>

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

## Custom Fonts in Labels and Titles in 3D Charts

To assign custom font to labels and titles in SciChart.js 3D charts, you can use the labelStyle and axisTitleStyle properties on your 3D axes.

Only Arial is included in the webassembly data as standard. Other fonts must either be hosted on your server, or registered if coming from a remote location. In either case, fonts are only downloaded once, and are then cached in the browser (in indexdb).

Use `sciChartSurface.registerFont`

to provide a remote url to load a font file from. Note that this requires a sciChartSurface instance - it is not a static method. The method returns a promise which resolves once the file is downloaded. If you do not await this method, the text will render using Arial until the font is available. There is a timeout (set by SciChartDefaults.nativeFontTimeout, default 2000ms) after which SciChart will fall back to Arial and stop trying to load the custom font. You might need to increase this if you need to load fonts over a slow connection, but in general it is better to await the registerFont method.

There is currently a limitation in that the font fetching from webassembly will not follow a http 302 redirection, so you need to pass the url to the actual file. For instance, when downloading from github, https://github.com/google/fonts/blob/main/ofl/braahone/BraahOne-Regular.ttf redirects to https://raw.githubusercontent.com/google/fonts/main/ofl/braahone/BraahOne-Regular.ttf so you need to use the githubusercontent.com link.

// Register font

await sciChart3DSurface.registerFont(

"braahone",

"https://raw.githubusercontent.com/google/fonts/main/ofl/braahone/BraahOne-Regular.ttf"

);

// In case that font is hosted on your server register font would look like this

// await sciChart3DSurface.registerFont(

// "myFont",

// "MyFont.ttf"

// );

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

labelStyle: {

fontFamily: "braahone",

fontSize: 14,

color: "white"

},

titleOffset: 100,

axisTitleStyle: {

fontFamily: "braahone",

fontSize: 16,

color: "white"

}

});

// Create the Y and Z-Axis and assign to SciChart3DSurface

sciChart3DSurface.yAxis = new NumericAxis3D(wasmContext, {

axisTitle: "Y Axis",

labelStyle: {

fontFamily: "braahone",

fontSize: 14,

color: "white"

},

titleOffset: 100,

axisTitleStyle: {

fontFamily: "braahone",

fontSize: 16,

color: "white"

}

});

sciChart3DSurface.zAxis = new NumericAxis3D(wasmContext, {

axisTitle: "Z Axis",

labelStyle: {

fontFamily: "braahone",

fontSize: 14,

color: "white"

},

titleOffset: 100,

axisTitleStyle: {

fontFamily: "braahone",

fontSize: 16,

color: "white"

}

});

### Registering multiple fonts

Here is how to register multiple fonts:

`// Registering multiple fonts`

const fonts = [

{ name: "arial", url: "" },

{

name: "braahone",

url: "https://raw.githubusercontent.com/google/fonts/main/ofl/braahone/BraahOne-Regular.ttf"

},

{

name: "iceland",

url: "https://raw.githubusercontent.com/google/fonts/main/ofl/iceland/Iceland-Regular.ttf"

},

{ name: "antic", url: "https://raw.githubusercontent.com/google/fonts/main/ofl/antic/Antic-Regular.ttf" },

{ name: "coda", url: "https://raw.githubusercontent.com/google/fonts/main/ofl/coda/Coda-Regular.ttf" },

{ name: "forum", url: "https://raw.githubusercontent.com/google/fonts/main/ofl/forum/Forum-Regular.ttf" },

{ name: "freeman", url: "https://raw.githubusercontent.com/google/fonts/main/ofl/freeman/Freeman-Regular.ttf" },

{ name: "geo", url: "https://raw.githubusercontent.com/google/fonts/main/ofl/geo/Geo-Regular.ttf" }

];

// Register all fonts from "fonts" array in parallel

await Promise.all(fonts.map(font => sciChart3DSurface.registerFont(font.name, font.url)));