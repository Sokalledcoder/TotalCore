---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-types/text-string-axis
scraped_at: 2025-11-28T18:24:08.940721
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-types/text-string-axis

# Text / String Axis

There is no specific Text / String Axis in SciChart.js, however, with a combination of the LabelProvider API and the NumericAxis, it's possible to create one.

Use this technique if you want to use strings instead of numbers for the axis labels.

Learn more about the commonalities between axis here.

## Create and Configure a Text Axis

To create a string axis in SciChart.js, we're going to use a TextLabelProvider📘 on an ordinary NumericAxis. This allows you to transform numbers [0, 1, 2, 3, 4] into string labels.

- TS
- Builder API (JSON Config)

`// Demonstrates how to configure a text axis in SciChart.js`

// using TextLabelProvider & NumericAxis

const {

SciChartSurface,

NumericAxis,

SciChartJsNavyTheme,

TextLabelProvider,

FastColumnRenderableSeries,

XyDataSeries,

GradientParams,

Point

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

// Create the labelProvider

const labelProvider = new TextLabelProvider({

// When passed as an array, labels will be used in order

labels: ["Bananas", "Apples", "Oranges", "Strawberries", "Plums"]

});

// Create an XAxis with a TextLabelProvider

const xAxis = new NumericAxis(wasmContext, { labelProvider });

sciChartSurface.xAxes.add(xAxis);

// Create a YAxis

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

// Create a column chart with the data. Labels are mapped to sequential X-values

sciChartSurface.renderableSeries.add(

new FastColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: [0, 1, 2, 3, 4],

yValues: [0.1, 0.2, 0.4, 0.8, 1.1]

}),

fillLinearGradient: new GradientParams(new Point(0, 0), new Point(0, 1), [

{ color: "rgba(70,130,180,0.77)", offset: 0 },

{ color: "rgba(70,130,180,0.0)", offset: 1 }

]),

stroke: "#FFFFFF77",

strokeThickness: 2

})

);

`// Demonstrates how to configure a text axis in SciChart.js using the Builder API`

const { chartBuilder, ESeriesType, EThemeProviderType, ELabelProviderType, EAxisType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: {

type: EAxisType.NumericAxis,

options: {

labelProvider: {

type: ELabelProviderType.Text,

options: {

// When passed as an array, labels will be used in order

labels: ["Bananas", "Apples", "Oranges", "Strawberries", "Plums"]

}

}

}

},

yAxes: {

type: EAxisType.NumericAxis,

options: {}

},

series: [

{

type: ESeriesType.ColumnSeries,

xyData: {

xValues: [0, 1, 2, 3, 4],

yValues: [0.1, 0.2, 0.4, 0.8, 1.1]

},

options: {

fillLinearGradient: {

gradientStops: [

{ color: "rgba(70,130,180,0.77)", offset: 0.0 },

{ color: "rgba(70,130,180,0.0)", offset: 1 }

],

startPoint: { x: 0, y: 0 },

endPoint: { x: 0, y: 1 }

},

stroke: "#FFFFFF77",

strokeThickness: 2

}

}

]

});

This results in the following output:

## Controlling the Order of Labels

If you want to control the order of labels with data, pass the labels as an object, using numbers as fields:

- TS
- Builder API (JSON Config)

`// Create the labelProvider`

const labelProvider = new TextLabelProvider({

// When passed as an object, x values will be mapped to fields

labels: {

0: "Plums",

1: "Strawberries",

2: "Oranges",

3: "Apples",

4: "Bananas"

}

});

// Create an XAxis with a TextLabelProvider

const xAxis = new NumericAxis(wasmContext, { labelProvider });

sciChartSurface.xAxes.add(xAxis);

// Data values are

// xValues: [0,1,2,3,4],

// yValues: [0.1, 0.2, 0.4, 0.8, 1.1],

`const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {`

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: {

type: EAxisType.NumericAxis,

options: {

labelProvider: {

type: ELabelProviderType.Text,

options: {

// When passed as an object, x values will be mapped to fields

labels: {

0: "Plums",

1: "Strawberries",

2: "Oranges",

3: "Apples",

4: "Bananas"

}

}

}

}

},

// ... );

With the same data as before, the label order is reversed.

## Multiline Text Labels

TextLabelProvider📘 has a maxLength📘 option which if greater than 0 will do basic word-wrap to that number of characters. The text will only be split at spaces. Words will not be split.

You can ensure the lines appear exactly as you want by passing them as an array. Note that this can be used in conjunction with word wrap using maxLength. A label given as text will be split according to the maxLength, but one passed as an array will be displayed exactly as given, as shown in the following example:

- TS
- Builder API (JSON Config)

`// Create an XAxis with 90-degree rotated labels`

const xAxis = new NumericAxis(wasmContext, {

labelProvider: new TextLabelProvider({

// When passed as an object, x values will be mapped to fields

labels: [

// Provide multiple lines directly

["Apples", "and Bananas"],

["Strawberries", "and Raspberries"],

["Lemons, Limes", "and Oranges"],

// These will be auto-wrapped

"Apples and Bananas",

"Strawberries and Raspberries",

"Lemons Limes and Oranges"

],

maxLength: 7

}),

labelStyle: {

alignment: ELabelAlignment.Center

}

});

sciChartSurface.xAxes.add(xAxis);

`const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {`

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: {

type: EAxisType.NumericAxis,

options: {

labelProvider: {

type: ELabelProviderType.Text,

options: {

labels: [

// Provide multiple lines directly

["Apples", "and Bananas"],

["Strawberries", "and Raspberries"],

["Lemons, Limes", "and Oranges"],

// These will be auto-wrapped

"Apples and Bananas",

"Strawberries and Raspberries",

"Lemons Limes and Oranges"

],

maxLength: 7

}

}

}

},

// ... );

This results in the following output:

Note the difference between the way the first three labels are wrapped, compared to the second three.

You can provide an alternative wrapping function by overriding the TextLabelProvider.wrapText📘 method which takes the label text and returns an array of lines.

When using multiline, the TextLabelProvider.lineSpacing📘 option controls the line spacing. It is expressed as a fraction of the normal line height and defaults to 1.1, ie 10% spacing between lines.

### Further notes on Label Culling & Spacing

The TextLabelProvider obeys other rules of axis tick spacing and label culling. Take a look at the section on Gridline and Label Spacing (Interval) for some more information how this works.

Finally, the property axis.axisRenderer.hideOverlappingLabels📘 may be set to false if you wish to disable culling of labels which overlap. This property may also be set via the axis constructor option hideOverlappingLabels📘.