---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/fast-box-plot-renderable-series
scraped_at: 2025-11-28T18:24:26.841574
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/fast-box-plot-renderable-series

# The Box Plot Series Type

A box plot (also called a box-and-whisker plot) is a statistical visualization that displays the distribution of a dataset through five key statistical measures. It's one of the most effective ways to show data distribution, identify outliers, and compare multiple datasets. The Box Plot Series Type is a powerful visualization tool that displays the distribution of data based on a five-number summary: minimum, first quartile (Q1), median (Q2), third quartile (Q3), and maximum. It is particularly useful for identifying outliers and understanding the spread of data.

## Key Configuration Options

### Data Point Width Modes

Sets the mode which determines how dataPointWidth is interpreted. Available values are EDataPointWidthMode📘. Default is Relative.

- EDataPointWidthMode.Relative: Interprets Data Point Width as a relative to the full width which is axis length / number of columns. This assumes that there are no gaps in the data. If you are plotting sparse columns on a NumericAxis, consider Range mode
- EDataPointWidthMode.Absolute: Interprets Data Point Width as an absolute pixel value
- EDataPointWidthMode.Range: Interprets Data Point Width as the x data range per column. This is useful if you are plotting sparse columns on a NumericAxis

### Styling Components

- Main Box: Defined by stroke, fill, opacity, and strokeThickness
- Whiskers: Vertical lines extending from box to min/max values
- Caps: Horizontal lines at whisker ends
- Median Line: Horizontal line inside the box

## Create a Box Plot Chart

To create a Box Plot Chart with SciChart.js we need to use FastBoxPlotRenderableSeries📘 and BoxPlotDataSeries📘. Start with the following code:

- TS
- JS

`// Demonstrates how to create a box plot chart with SciChart.js`

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

const isVertical = true;

const isXCategoryAxis = false;

const configCategoryAxis: ICategoryAxisOptions = {

labelFormat: ENumericFormat.Decimal,

labelPrecision: 0,

cursorLabelFormat: ENumericFormat.Decimal,

cursorLabelPrecision: 0

};

const configX = {

axisAlignment: isVertical ? EAxisAlignment.Bottom : EAxisAlignment.Left,

growBy: new NumberRange(0.05, 0.05),

autoRange: EAutoRange.Once,

flippedCoordinates: false

};

sciChartSurface.xAxes.add(

isXCategoryAxis

? new CategoryAxis(wasmContext, { ...configX, ...configCategoryAxis })

: new NumericAxis(wasmContext, configX)

);

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

axisAlignment: isVertical ? EAxisAlignment.Left : EAxisAlignment.Bottom,

growBy: new NumberRange(0.05, 0.05),

autoRange: EAutoRange.Once,

flippedCoordinates: !isVertical

})

);

const xValues = [4, 5, 6];

const minimumValues = [0, 1, 0.5];

const maximumValues = [10, 9, 9.5];

const medianValues = [4.5, 5.5, 5];

const lowerQuartileValues = [3, 4, 3.5];

const upperQuartileValues = [7, 6, 6.5];

const boxPlotDataSeries = new BoxPlotDataSeries(wasmContext, {

xValues,

minimumValues,

maximumValues,

medianValues,

lowerQuartileValues,

upperQuartileValues

});

const boxSeries = new FastBoxPlotRenderableSeries(wasmContext, {

dataSeries: boxPlotDataSeries,

stroke: "black",

strokeThickness: 1,

dataPointWidthMode: EDataPointWidthMode.Relative,

dataPointWidth: 0.5,

fill: "green",

opacity: 0.6,

whiskers: {

stroke: "green",

strokeThickness: 2

},

cap: {

stroke: "green",

strokeThickness: 2,

dataPointWidth: 0.3

},

medianLine: {

stroke: "black",

strokeThickness: 2

}

});

sciChartSurface.renderableSeries.add(boxSeries);

`// Demonstrates how to create a box plot chart with SciChart.js`

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

const isVertical = true;

const isXCategoryAxis = false;

const configCategoryAxis = {

labelFormat: ENumericFormat.Decimal,

labelPrecision: 0,

cursorLabelFormat: ENumericFormat.Decimal,

cursorLabelPrecision: 0

};

const configX = {

axisAlignment: isVertical ? EAxisAlignment.Bottom : EAxisAlignment.Left,

growBy: new NumberRange(0.05, 0.05),

autoRange: EAutoRange.Once,

flippedCoordinates: false

};

sciChartSurface.xAxes.add(isXCategoryAxis

? new CategoryAxis(wasmContext, { ...configX, ...configCategoryAxis })

: new NumericAxis(wasmContext, configX));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, {

axisAlignment: isVertical ? EAxisAlignment.Left : EAxisAlignment.Bottom,

growBy: new NumberRange(0.05, 0.05),

autoRange: EAutoRange.Once,

flippedCoordinates: !isVertical

}));

const xValues = [4, 5, 6];

const minimumValues = [0, 1, 0.5];

const maximumValues = [10, 9, 9.5];

const medianValues = [4.5, 5.5, 5];

const lowerQuartileValues = [3, 4, 3.5];

const upperQuartileValues = [7, 6, 6.5];

const boxPlotDataSeries = new BoxPlotDataSeries(wasmContext, {

xValues,

minimumValues,

maximumValues,

medianValues,

lowerQuartileValues,

upperQuartileValues

});

const boxSeries = new FastBoxPlotRenderableSeries(wasmContext, {

dataSeries: boxPlotDataSeries,

stroke: "black",

strokeThickness: 1,

dataPointWidthMode: EDataPointWidthMode.Relative,

dataPointWidth: 0.5,

fill: "green",

opacity: 0.6,

whiskers: {

stroke: "green",

strokeThickness: 2

},

cap: {

stroke: "green",

strokeThickness: 2,

dataPointWidth: 0.3

},

medianLine: {

stroke: "black",

strokeThickness: 2

}

});

sciChartSurface.renderableSeries.add(boxSeries);

This results in the following output:

## Box Plot Complex Example

The JavaScript Box Plot Chart Example can be found in the SciChart.Js Examples Suite > Box Plot Series on Github, or our live demo at scichart.com/demo.