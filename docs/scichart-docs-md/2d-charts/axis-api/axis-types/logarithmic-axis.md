---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-types/logarithmic-axis
scraped_at: 2025-11-28T18:24:08.281061
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-types/logarithmic-axis

# The Logarithmic Axis

The LogarithicAxis📘 is a Value axis similar to the normal NumericAxis, but where the tick values increase exponentially. Plotting data on such an axis is equivalent to plotting the log of that data. You can set the logarithmic base using the logBase property. eg logBase: 10 (the default) will result in ticks like 1, 10, 100, 1000. logBase 2 will result in ticks like 2, 4, 8, 16, 32.

Learn more about the commonalities between axis here.

## Create and Configure a LogarithmicAxis

To create and configure a LogarithmicAxis, use the following code:

- TS
- Builder API (JSON Config)

`// Demonstrates how to configure a logarithmic axis in SciChart.js`

const { SciChartSurface, LogarithmicAxis, SciChartJsNavyTheme, ENumericFormat, NumberRange } = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

// Create an X and Y Axis

const xAxisLogarithmic = new LogarithmicAxis(wasmContext, {

logBase: 10,

// Format with E

labelFormat: ENumericFormat.Exponential,

labelPrecision: 2,

minorsPerMajor: 10,

// Adjust major/minor gridline style to make it clearer for the demo

majorGridLineStyle: { color: "#50C7E077" },

minorGridLineStyle: { color: "#50C7E033" },

axisTitle: "Log(10) Axis with Exponential Format",

visibleRange: new NumberRange(1, 10_000_000)

});

sciChartSurface.xAxes.add(xAxisLogarithmic);

// The LogarithmicAxis will apply logarithmic scaling and labelling to your data.

// Simply replace a NumericAxis for a LogarithmicAxis on X or Y to apply this scaling

// Note options logBase, labelFormat which lets you specify exponent on labels

const yAxisLogarithmic = new LogarithmicAxis(wasmContext, {

logBase: 10,

// Format with superscript

labelFormat: ENumericFormat.Scientific,

labelPrecision: 2,

minorsPerMajor: 10,

majorGridLineStyle: { color: "#50C7E077" },

minorGridLineStyle: { color: "#50C7E033" },

axisTitle: "Log(10) Axis with Scientific Format",

visibleRange: new NumberRange(0.1, 1_000_000)

});

sciChartSurface.yAxes.add(yAxisLogarithmic);

`// Demonstrates how to create a line chart with SciChart.js using the Builder API`

const { chartBuilder, EThemeProviderType, NumberRange, ENumericFormat, EAxisType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: {

type: EAxisType.LogarithmicAxis,

options: {

logBase: 10,

// Format with E

labelFormat: ENumericFormat.Exponential,

labelPrecision: 2,

minorsPerMajor: 10,

// Adjust major/minor gridline style to make it clearer for the demo

majorGridLineStyle: { color: "#EEEEEE77" },

minorGridLineStyle: { color: "#EEEEEE33" },

axisTitle: "Log(10) Axis with Exponential Format",

visibleRange: new NumberRange(1, 10_000_000)

}

},

yAxes: {

type: EAxisType.LogarithmicAxis,

options: {

logBase: 10,

// Format with superscript

labelFormat: ENumericFormat.Scientific,

labelPrecision: 2,

minorsPerMajor: 10,

majorGridLineStyle: { color: "#EEEEEE77" },

minorGridLineStyle: { color: "#EEEEEE33" },

axisTitle: "Log(10) Axis with Scientific Format",

visibleRange: new NumberRange(0.1, 1_000_000)

}

}

});

This results in the following output:

## Configuration Options for Log Axis

### labelFormat property

When using logarithmicAxis and the labelFormat ENumericFormat.Scientific📘, the logBase of the axis will be used as the base for the label. This is NOT the case for ENumericFormat.Exponential📘 which is always base 10.

`const logAxis = new LogarithmicAxis(wasmContext, {`

// Format with Scientific notation e.g. 1x10^3

labelFormat: ENumericFormat.Scientific,

labelPrecision: 2,

minorsPerMajor: 10,

});

### Plotting Negative Numbers

LogarithmicAxis cannot show both positive and negative numbers on the same axis, so if your data is negative you need to set isNegative on the axis. If you need to show positive and negative log data, you need to split it into positive and negative sets and plot them on seperate vertically stacked axes.

### Minor Tick Mode

By default, Major gridlines are spaced logarithmically, and Minor gridlines are spaced linearly between them. If your visible range is extremely large, you may want to switch to logarithmic spacing for minor gridlines, which you can do with the LogarithmicAxis.minorTickMode📘 property which is an ELogarithmicMinorTickMode📘 which can be Logarithmic, Linear or Auto

Auto mode means it switches from linear to Logarithmic when the visible range is such that the first linear minor tick would be more than 70% of the major tick

### Major Tick Mode - Financial Log Charts

For financial charts you often want base 2, with a relatively small range, but you don't want your tick labels to be powers of 2. In this case set LogarithmicAxis.majorTickMode📘 to ELogarithmicMajorTickMode.RoundNumbers📘. This will give you labels with nice round numbers, at the expense of gridlines that are not exactly equally spaced.

### LabelFormat

**labelFormat: ENumericFormat.SignificantFigures📘** is also helpful as it retains precision for very small values, while not resulting in unnecessary decimal places for large values.

## Worked Example - LogAxis Configuration Options

Here's a worked example that combines some of the techniques above.

- TS
- Builder API (JSON Config)

`// Create Log(10) axis with options`

sciChartSurface.xAxes.add(

new LogarithmicAxis(wasmContext, {

logBase: 10,

// Format with E

labelFormat: ENumericFormat.SignificantFigures,

majorTickMode: ELogarithmicMajorTickMode.EqualSpacing,

minorTickMode: ELogarithmicMinorTickMode.Logarithmic,

// Adjust major/minor gridline style to make it clearer for the demo

majorGridLineStyle: { color: "#50C7E077" },

minorGridLineStyle: { color: "#50C7E033" },

axisTitle: "Log(10) Axis with equally spaced gridlines",

visibleRange: new NumberRange(1, 10_000_000)

})

);

// Creating a Log(2) Axis with options

sciChartSurface.yAxes.add(

new LogarithmicAxis(wasmContext, {

logBase: 2,

// Format with 2 decimal places

labelFormat: ENumericFormat.Decimal,

labelPrecision: 2,

labelPrefix: "$",

majorTickMode: ELogarithmicMajorTickMode.RoundNumbers,

minorTickMode: ELogarithmicMinorTickMode.Linear,

// Adjust major/minor gridline style to make it clearer for the demo

majorGridLineStyle: { color: "#50C7E077" },

minorGridLineStyle: { color: "#50C7E033" },

axisTitle: "Log(2) Axis configured for financial",

visibleRange: new NumberRange(100, 1000)

})

);

`const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {`

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: {

type: EAxisType.LogarithmicAxis,

options: {

logBase: 10,

// Format with E

labelFormat: ENumericFormat.SignificantFigures,

majorTickMode: ELogarithmicMajorTickMode.EqualSpacing,

minorTickMode: ELogarithmicMinorTickMode.Logarithmic,

// Adjust major/minor gridline style to make it clearer for the demo

majorGridLineStyle: { color: "#50C7E077" },

minorGridLineStyle: { color: "#50C7E033" },

axisTitle: "Log(10) Axis with equally spaced gridlines",

visibleRange: new NumberRange(1, 10_000_000)

}

},

yAxes: {

type: EAxisType.LogarithmicAxis,

options: {

logBase: 2,

// Format with 2 decimal places

labelFormat: ENumericFormat.Decimal,

labelPrecision: 2,

labelPrefix: "$",

majorTickMode: ELogarithmicMajorTickMode.RoundNumbers,

minorTickMode: ELogarithmicMinorTickMode.Linear,

// Adjust major/minor gridline style to make it clearer for the demo

majorGridLineStyle: { color: "#50C7E077" },

minorGridLineStyle: { color: "#50C7E033" },

axisTitle: "Log(2) Axis configured for financial",

visibleRange: new NumberRange(100, 1000)

}

}

});

This produces something like this. If you want even more control over the tick values and gridlines see Axis Ticks.