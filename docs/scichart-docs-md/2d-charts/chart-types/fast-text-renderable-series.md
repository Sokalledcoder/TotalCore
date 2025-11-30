---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/fast-text-renderable-series
scraped_at: 2025-11-28T18:24:28.926606
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/fast-text-renderable-series

# The Text Series Type

There are several ways to add text to a SciChart.js chart. These include the TextAnnotation, series DataLabels and also the FastTextRenderableSeries (Text Series).

Text Series should be used when you want to render a lot of text, not necessarily at X,Y positions of other chart series.

The JavaScript Text / Word Cloud Chart Example can be found in the SciChart.Js Examples Suite > Text Series Chart on Github, or our live demo at scichart.com/demo

## Creating a Text Series

To create a chart using FastTextRenderableSeries📘 use the following code.

**Note** that it is required to set `style: { fontSize: X }`

and `color`

in the dataLabels property in order for text to be drawn.

FastTextRenderableSeries uses the special XyTextDataSeries📘 which allows you to supply text values directly on the dataSeries, rather than having to use metadata.

- TS
- Builder API (JSON Config)

`// Demonstrates how to create a text chart with SciChart.js`

const {

SciChartSurface,

NumericAxis,

FastTextRenderableSeries,

XyTextDataSeries,

SciChartJsNavyTheme,

NumberRange

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { visibleRange: new NumberRange(0, 9) }));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { visibleRange: new NumberRange(0, 9) }));

// Create a chart with textSeries

const textSeries = new FastTextRenderableSeries(wasmContext, {

dataSeries: new XyTextDataSeries(wasmContext, {

xValues: [1, 2, 3, 4, 5, 6],

yValues: [3, 5, 6, 4, 2, 5],

textValues: ["This", "text", "is", "drawn", "using", "FastTextRenderableSeries"]

}),

// font and size is required for text to be drawn

dataLabels: {

style: {

fontFamily: "Default",

fontSize: 18

},

color: "white"

}

});

sciChartSurface.renderableSeries.add(textSeries);

`// Demonstrates how to create a line chart with SciChart.js using the Builder API`

const { chartBuilder, ESeriesType, EThemeProviderType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

series: [

{

type: ESeriesType.TextSeries,

xyTextData: {

xValues: [1, 2, 3, 4, 5, 6],

yValues: [3, 5, 6, 4, 2, 5],

textValues: ["This", "text", "is", "drawn", "using", "FastTextRenderableSeries"]

},

options: {

dataLabels: {

style: {

fontFamily: "Default",

fontSize: 18

},

color: "white"

}

}

}

]

});

This results in the following output:

## Customising the Text Series

FastTextRenderableSeries📘 uses TextDataLabelProvider📘 for the generation and drawing of text, which has a slightly reduced api compared with the full DataLabels api.

It has getPosition📘 and getColor📘 functions, but text is always taken from the **XyTextDataSeries**, and there is no label skipping - all labels are drawn even if they overlap.

There is however an onAfterGenerate📘 function that is called with the dataLabels before they are drawn which you can use to perform additional adjustments. If you need to rely on the label sizes in this function, make sure to set **calculateTextBounds: true** in dataLabels.

FastTextRenderableSeries📘 supports pointmarkers and also horizontalTextPosition📘 and verticalTextPosition📘 dataLabels options.

Text is drawn using Native Text rendering, so to use any font other than Arial you will need ensure that font is available on your server (as fontname.ttf), or registered using **sciChartSurface.registerFont(...)** if coming from a remote url.

- TS

`// Register a remote font`

await sciChartSurface.registerFont(

"notoserif",

"https://raw.githubusercontent.com/google/fonts/main/ofl/notoserif/NotoSerif-Regular.ttf"

);

// Create a textSeries with custom fond

const textSeries = new FastTextRenderableSeries(wasmContext, {

dataSeries: new XyTextDataSeries(wasmContext, {

xValues: [1, 2, 3, 4, 5, 6],

yValues: [1, 1, 1, 1, 1, 1],

textValues: ["This", "text", "is", "drawn", "using", "FastTextRenderableSeries"]

}),

// font and size is required for text to be drawn

dataLabels: {

style: {

// Set custom font

fontFamily: "notoserif",

fontSize: 18

},

color: "white",

// Set text position relative to the data point

horizontalTextPosition: EHorizontalTextPosition.Center,

verticalTextPosition: EVerticalTextPosition.Center,

// force the label sizes to be calculated as we need them below

calculateTextBounds: true

}

});

// Handle further customisation of positioning and color

(textSeries.dataLabelProvider as TextDataLabelProvider).getColor = (state, text) => {

if (state.xVal() < 4) {

return parseColorToUIntArgb("red");

} else {

return state.color;

}

};

(textSeries.dataLabelProvider as TextDataLabelProvider).onAfterGenerate = dataLabels => {

for (let i = 0; i < dataLabels.length; i++) {

const label = dataLabels[i];

if (i < dataLabels.length - 1) {

// Shift this label down if it would overlap the next one

if (label.rect.right > dataLabels[i + 1].rect.left) {

// @ts-ignore

label.position.y += label.rect.height;

}

}

}

};

// Add the TextSeries to the chart

sciChartSurface.renderableSeries.add(textSeries);

This results in the following output: