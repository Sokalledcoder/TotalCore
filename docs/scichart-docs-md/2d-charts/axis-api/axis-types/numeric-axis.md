---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-types/numeric-axis
scraped_at: 2025-11-28T18:24:08.538072
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-types/numeric-axis

# The Numeric Axis

The NumericAxis📘 is a Value axis and is suitable for X and Y Axis when the data on that axis is numeric (e.g. number in TypeScript). It is not suitable for non-numeric data types.

info

Learn more about the commonalities between axis here.

## Create and Configure a NumericAxis

There are lots of options that can be passed to the constructor of a NumericAxis to configure it. Some of these are in the common AxisBase2D type.

To create and configure a NumericAxis, use the following code:

- TS
- Builder API (JSON Config)

`// Demonstrates how to configure a numeric axis in SciChart.js`

const { SciChartSurface, NumericAxis, SciChartJsNavyTheme, EAutoRange, EAxisAlignment, ENumericFormat } = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

// Create an XAxis on the bottom

const xAxis = new NumericAxis(wasmContext, {

// All these properties are optional

// ...

// Enable flags like drawing gridlines

drawMajorGridLines: true,

drawMinorGridLines: true,

drawLabels: true,

// Set multiline title

axisTitle: ["X Axis, Bottom", "2 decimal places"],

// Set the alignment and autoRange

axisAlignment: EAxisAlignment.Bottom,

autoRange: EAutoRange.Once,

// Enable decision labels with 4 significant figures

labelFormat: ENumericFormat.Decimal,

cursorLabelFormat: ENumericFormat.Decimal,

labelPrecision: 4

});

// Add the xAxis to the chart

sciChartSurface.xAxes.add(xAxis);

// Creating a NumericAxis as a YAxis on the left

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

axisTitle: "Y Axis, Left, 4 dp",

axisAlignment: EAxisAlignment.Left,

labelFormat: ENumericFormat.Decimal,

cursorLabelFormat: ENumericFormat.Decimal,

labelPrecision: 4,

labelPrefix: "$",

labelPostfix: " USD"

})

);

`// Demonstrates how to configure a numeric axis in SciChart.js using the Builder API`

const { chartBuilder, ESeriesType, EThemeProviderType, EAutoRange, EAxisAlignment, ENumericFormat, EAxisType } =

SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: {

type: EAxisType.NumericAxis,

options: {

// All these properties are optional

// ...

// Enable flags like drawing gridlines

drawMajorGridLines: true,

drawMinorGridLines: true,

drawLabels: true,

// Set title, alignment and autorange

axisTitle: "X Axis, Bottom, 2 decimal places",

axisAlignment: EAxisAlignment.Bottom,

autoRange: EAutoRange.Once,

// Enable decision labels with 4 significant figures

labelFormat: ENumericFormat.Decimal,

cursorLabelFormat: ENumericFormat.Decimal,

labelPrecision: 2

}

},

yAxes: {

type: EAxisType.NumericAxis,

options: {

// axisTitle: "Y Axis, Left, default formatting",

axisAlignment: EAxisAlignment.Left,

axisTitle: "Y Axis, Left, 4 dp",

labelFormat: ENumericFormat.Decimal,

cursorLabelFormat: ENumericFormat.Decimal,

labelPrecision: 4,

labelPrefix: "$",

labelPostfix: " USD"

}

},

series: [

{

type: ESeriesType.LineSeries,

xyData: {

xValues: [0, 1, 2, 3, 4, 5, 6, 7, 8],

yValues: [2.5, 3.5, 3.7, 4.0, 5.0, 5.5, 5.0, 4.0, 3.0]

},

options: {

stroke: "#0066FF",

strokeThickness: 5

}

}

]

});

This results in the following output:

info

Further enhancement of the NumericAxis labels including custom formatting, string formatting or dynamic formatting can be achieved with the LabelProvider API.

Also see the documentation page on ENumericFormat