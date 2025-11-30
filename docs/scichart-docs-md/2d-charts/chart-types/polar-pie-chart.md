---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/polar-pie-chart
scraped_at: 2025-11-28T18:24:41.089776
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/polar-pie-chart

# The Pie Chart (using Polar Columns)

The Polar Pie Chart type is achieved using SciChart's `PolarColumnRenderableSeries`

and some data manipulation to mimic pie segments while using the SciChartPolarSurface📘 class.
It is the native way to create pie charts in SciChart.js, as opposed to using the SciChartPieSurface📘

The Polar Pie Chart is not yet able to support all features a regular pie chart would have, such as certain animation effects or selection behaviors, but it is a useful way to visualize data in a pie format using polar coordinates.

## Create a Basic Polar Pie Chart

To create a Javascript Polar Pie Chart with SciChart.js, use the following code:

`// Demonstrates how to create a basic polar pie chart using SciChart.js`

const {

SciChartPolarSurface,

PolarNumericAxis,

PolarColumnRenderableSeries,

EPolarAxisMode,

NumberRange,

XyxDataSeries,

Thickness,

EColumnMode,

MetadataPaletteProvider,

SciChartJsNavyTheme,

EColumnDataLabelPosition,

EPolarLabelMode,

EMultiLineAlignment

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { sciChartSurface, wasmContext } = await SciChartPolarSurface.create(divElementId, {

padding: Thickness.fromNumber(20),

theme: new SciChartJsNavyTheme(),

});

const radialYAxis = new PolarNumericAxis(wasmContext, {

visibleRangeLimit: new NumberRange(0, 1),

polarAxisMode: EPolarAxisMode.Radial,

startAngleDegrees: 90, // start at 12 o'clock

isVisible: false

});

sciChartSurface.yAxes.add(radialYAxis);

const angularXAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Angular,

startAngleDegrees: 90, // start at 12 o'clock

flippedCoordinates: true, // set to true to go clockwise (biggest values first, starting from 12 o'clock, clockwise)

isVisible: false

});

sciChartSurface.xAxes.add(angularXAxis);

const DATA = [

{ xValue: 60, label: "First", color: "dodgerblue" },

{ xValue: 50, label: "Second", color: "orangered" },

{ xValue: 40, label: "Third", color: "darkorchid" },

{ xValue: 30, label: "Fourth", color: "salmon" },

{ xValue: 20, label: "Fifth", color: "darkolivegreen" },

{ xValue: 10, label: "Sixth", color: "indianred" }

];

const metadata = [];

const xValues = [];

const x1Values = [];

const yValues = [];

let xSum = 0;

DATA.forEach((item, i) => {

xValues.push(xSum);

x1Values.push(item.xValue);

yValues.push(1);

xSum += item.xValue;

metadata.push({

isSelected: false,

fill: item.color, // each column will have a different color, handled by the MetadataPaletteProvider

customLabel: item.label,

value: item.xValue // add value for optional data-labels

});

});

const polarColumn = new PolarColumnRenderableSeries(wasmContext, {

dataSeries: new XyxDataSeries(wasmContext, {

xValues,

x1Values,

yValues,

metadata

}),

stroke: "#110533",

strokeThickness: 2,

columnXMode: EColumnMode.StartWidth, // makes columns span from x to x1 value

paletteProvider: new MetadataPaletteProvider(), // use colors from the metadata for each column value

dataLabels: {

metaDataSelector: (metadata: IPointMetadata) => {

// @ts-ignore

if (metadata.xValue < 35) {

// @ts-ignore

return metadata.customLabel + ' - ' + metadata.value + '%'; // keep smaller segments' label single-line

} else {

// @ts-ignore

return metadata.customLabel + '\n' + metadata.value + '%';

}

// you can avoid the ts-ignore's with a custom point metadata interface casting with all values you'll use.

},

style: {

fontSize: 16,

multiLineAlignment: EMultiLineAlignment.Center,

lineSpacing: 12

},

color: "#EEE",

labelYPositionMode: EColumnDataLabelPosition.Inside,

polarLabelMode: EPolarLabelMode.Perpendicular,

}

});

sciChartSurface.renderableSeries.add(polarColumn);

In the code above:

- We prepare the data from an array of values to 2 arrays:
`xValues`

and`x1Values`

, showing the start and end angles of each "segment", while the`yValues`

array is just filled with 1s. - The
`X`

and`X1`

value arrays along with columnXMode📘: EColumnMode.StartWidth📘, are used to create different-width columns, mimicking pie segments. - The coloring for each segment must be different, we cannot set "fill", and have columns be the same color. Instead, we use the MetadataPaletteProvider📘 so that each segment may have its own color.

## How Does It Work?

- Data is preprocessed into arrays of:
`xValues`

— start angle of each segment (in degrees or radians)`x1Values`

— end angle of each segment`yValues`

— (typically all 1) for equal segment radius- A metadata array for coloring

- The
`PolarColumnRenderableSeries`

📘 is set to`columnXMode: EColumnXMode.StartWidth`

📘, which means each column gets its own custom angular width (i.e., pie slice). - A
`MetadataPaletteProvider`

📘 is used to apply a unique color to each pie segment. - Using the metadata, you can als

## Tips & Best Practices

- Use the
**metadata**array to assign tooltip data, custom colors, labels, or selection state to each segment - Adjust the
**radial axis**’ innerRadius📘 for donut/ring-style pie charts - Set the
**start angle**to rotate your entire pie as needed - Add annotations or labels for segment values or percentage displays if needed
- Combine with other polar series (lines, scatter) for hybrid visualizations!

## Related API and Demos

- PolarColumnRenderableSeries📘
- MetadataPaletteProvider📘
- Polar Column & Pie Demo
- SciChartPieSurface for Classic Pie📘

The **Polar Pie Chart** is a powerful hybrid, bringing all the flexibility of scientific polar charts to the familiar and insightful pie chart format!