---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-labels/label-style-alignment-and-positioning
scraped_at: 2025-11-28T18:24:05.321039
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-labels/label-style-alignment-and-positioning

# Label Style, Alignment and Positioning

## The LabelStyle property

The Axis includes a LabelStyle📘 property. This may be set in the constructor options or set on the axis itself. Apply a labelStyle as follows to an axis:

`// Label Style`

import { NumericAxis, ELabelAlignment, Thickness } from "scichart";

const axis = new NumericAxis(wasmContext, {

labelStyle: {

alignment: ELabelAlignment.Auto,

fontFamily: "Arial",

fontSize: 16,

color: "White",

} // type TTextStyle

});

The type for LabelStyle is TTextStyle📘. The Definition for TTextStyle is found below:

`// TTextStyle definition`

/**

* A type class to contain information about Axis Label text styles

* @remarks

* - Set the fontFamily as a string to set the font

* - Set the fontSize as you would in HTML/CSS

* - Set the fontWeight and fontStyle as you would in HTML/CSS

* - Set the color as an HTML Color code to define the color

*/

export type TTextStyle = {

fontSize?: number;

fontFamily?: string;

fontWeight?: string;

fontStyle?: string;

color?: string;

/** Padding is left 4, right 4, top 2, bottom 0 by default. This is because there is natural space below the text baseline.

* If you are using text labels rather than just numbers, or when using native text,

* you may want to increase the bottom padding.

*/

padding?: Thickness;

/** Horizontal label alignment for vertical axes. Default Auto */

alignment?: ELabelAlignment;

};

## Rotated and Multiline Native Text Labels

The standard axis labels supported rotation, but the positioning is poor for angles outside the 0 to 90 range. With native text labels, this is fixed. Note that rotation is a property on the labelProvider, not the axis itself.

When using angles that are not a multiple of 90, you probably want to set **hideOverlappingLabels: false** as the overlap is calculated using the bounding rectangle of the text.

Multiline labels are supported simply by using newline characters (\n) in the label text. lineSpacing is a property on the labelProvider. The alignment property on labelStyle also affects the alignment for multiple lines.

Note: for more info about Text and MultiLine labels see this article. For rotation of labels see this article.

## Label Alignment & Padding

The **labelStyle** option on an axis contains **padding** and **alignment** which can be used to adjust the positioning of axis labels.

Padding refers to the space around the label.

- By default, a label will not be displayed if if would overlap with the previous label, and this overlap includes padding.
- By default the padding is 4 pixels left and right, 2 pixels top, and 0 bottom padding. This is because the font height includes space below the baseline of the text.
- For numbers this usually results in nicely centered labels for a vertical axis, but depending on your font size and style, or if you are using text, you may want to adjust the padding to improve the vertical alignment, or to fit in labels that would otherwise be hidden.

- Alignment is an ELabelAlignment📘 which can be one of the options below. Auto is the default.

## KeepLabelsWithinAxis property

Another property which defines label placement is keepLabelsWithinAxis.

By default the first and last labels on an axis are shifted so that they stay within the bounds of the axis itself. If you want to turn this off so that all labels are centered, you can disable **keepLabelsWithinAxis** as follows:

`// keepLabelsWithinAxis Example`

// Either

const xAxis = new NumericAxis(wasmContext, {

// Allow labels to overlap

keepLabelsWithinAxis: false

});

// Or

const xAxis = new NumericAxis(wasmContext);

// Allow rotated labels to overlap

xAxis.axisRenderer.keepLabelsWithinAxis= false;

## Worked Example: Alignment of labels

In the example below we show how to apply the ELabelAlignment📘 enum to an axis. We've chosen LogarithmicAxis for this demo to get different length labels, such as "10", "100", "1000". Try editing the label alignment in the sandbox below to see how it affects the chart.

- TS
- Builder API (JSON Config)

`// Demonstrates how to configure label alignment in SciChart.js`

const {

SciChartSurface,

NumericAxis,

LogarithmicAxis,

SciChartJsNavyTheme,

EAxisAlignment,

ELabelAlignment,

NumberRange,

ENumericFormat

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

// Create an XAxis on the bottom

const xAxis = new NumericAxis(wasmContext, {

axisTitle: "X Axis, center aligned labels",

keepLabelsWithinAxis: false,

axisBorder: { color: "#50C7E077", borderTop: 1 },

backgroundColor: "#50C7E022"

});

// Add the xAxis to the chart

sciChartSurface.xAxes.add(xAxis);

// Creating a NumericAxis as a YAxis on the left

sciChartSurface.yAxes.add(

new LogarithmicAxis(wasmContext, {

axisTitle: "Y Axis, left-aligned labels",

axisAlignment: EAxisAlignment.Left,

labelFormat: ENumericFormat.Decimal,

labelStyle: { alignment: ELabelAlignment.Left },

visibleRange: new NumberRange(0.1, 1e6),

logBase: 10,

axisBorder: { color: "#50C7E077", borderRight: 1 },

backgroundColor: "#50C7E022"

})

);

// Creating a NumericAxis as a YAxis on the right

sciChartSurface.yAxes.add(

new LogarithmicAxis(wasmContext, {

axisTitle: "Y Axis, right-aligned labels",

axisAlignment: EAxisAlignment.Right,

labelFormat: ENumericFormat.Decimal,

labelStyle: { alignment: ELabelAlignment.Right },

visibleRange: new NumberRange(0.1, 1e6),

logBase: 10,

axisBorder: { color: "#50C7E077", borderLeft: 1 },

backgroundColor: "#50C7E022"

})

);

`// Demonstrates how to configure a numeric axis in SciChart.js using the Builder API`

const {

chartBuilder,

EThemeProviderType,

EAxisAlignment,

ELabelAlignment,

EAxisType,

ENumericFormat,

NumberRange

} = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: {

type: EAxisType.NumericAxis,

options: {

axisTitle: "X Axis, center aligned labels",

keepLabelsWithinAxis: false,

axisBorder: { color: "#50C7E077", borderTop: 1 },

backgroundColor: "#50C7E022"

}

},

yAxes: [

{

type: EAxisType.LogarithmicAxis,

options: {

axisTitle: "Y Axis, left-aligned labels",

axisAlignment: EAxisAlignment.Left,

labelFormat: ENumericFormat.Decimal,

labelStyle: { alignment: ELabelAlignment.Left },

visibleRange: new NumberRange(0.1, 1e6),

logBase: 10,

axisBorder: { color: "#50C7E077", borderRight: 1 },

backgroundColor: "#50C7E022"

}

},

{

type: EAxisType.LogarithmicAxis,

options: {

axisTitle: "Y Axis, right-aligned labels",

axisAlignment: EAxisAlignment.Right,

labelFormat: ENumericFormat.Decimal,

labelStyle: { alignment: ELabelAlignment.Right },

visibleRange: new NumberRange(0.1, 1e6),

logBase: 10,

axisBorder: { color: "#50C7E077", borderLeft: 1 },

backgroundColor: "#50C7E022"

}

}

]

});

This results in the following output:

Label alignment only applies to vertical axis. Labels for horizontal axes are always centered horizontally.