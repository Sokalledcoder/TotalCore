---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/stacked-column-renderable-series
scraped_at: 2025-11-28T18:24:44.738947
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/stacked-column-renderable-series

# The Stacked Column Series Type

Stacked Column Charts can be created by a combination of the StackedColumnRenderableSeries📘 and StackedColumnCollection📘 type. StackedColumnRenderableSeries share many properties with the added feature that columns automatically stack vertically or side by side.

- We created 5 StackedColumnRenderableSeries📘 and added them to a StackedColumnCollection📘
- The StackedColumnCollection📘 itself is added to sciChartSurface.renderableSeries collection, not the individual column series.

`// Data for the example`

const xValues = [1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003];

const yValues1 = [10, 13, 7, 16, 4, 6, 20, 14, 16, 10, 24, 11];

const yValues2 = [12, 17, 21, 15, 19, 18, 13, 21, 22, 20, 5, 10];

const yValues3 = [7, 30, 27, 24, 21, 15, 17, 26, 22, 28, 21, 22];

const yValues4 = [16, 10, 9, 8, 22, 14, 12, 27, 25, 23, 17, 17];

const yValues5 = [7, 24, 21, 11, 19, 17, 14, 27, 26, 22, 28, 16];

const dataLabels = {

color: "#FFfFFF",

style: { fontSize: 12, fontFamily: "Arial", padding: new Thickness(0, 0, 4, 0) },

precision: 0,

positionMode: EColumnDataLabelPosition.Outside,

verticalTextPosition: EVerticalTextPosition.Center

};

// Create some RenderableSeries - for each part of the stacked column

// Notice the stackedGroupId. This defines if series are stacked (same), or grouped side by side (different)

const rendSeries1 = new StackedColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues1, dataSeriesName: "EU" }),

fill: "#882B91",

stroke: "#E4F5FC",

strokeThickness: 1,

opacity: 0.8,

stackedGroupId: "StackedGroupId",

dataLabels,

});

const rendSeries2 = new StackedColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues2, dataSeriesName: "Asia" }),

fill: "#EC0F6C",

stroke: "#E4F5FC",

strokeThickness: 1,

opacity: 0.8,

stackedGroupId: "StackedGroupId",

dataLabels

});

const rendSeries3 = new StackedColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues3, dataSeriesName: "USA" }),

fill: "#F48420",

stroke: "#E4F5FC",

strokeThickness: 1,

opacity: 0.8,

stackedGroupId: "StackedGroupId",

dataLabels

});

const rendSeries4 = new StackedColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues4, dataSeriesName: "UK" }),

fill: "#50C7E0",

stroke: "#E4F5FC",

strokeThickness: 1,

opacity: 0.8,

stackedGroupId: "StackedGroupId",

dataLabels

});

const rendSeries5 = new StackedColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues5, dataSeriesName: "Latam" }),

fill: "#30BC9A",

stroke: "#E4F5FC",

strokeThickness: 1,

opacity: 0.8,

stackedGroupId: "StackedGroupId",

dataLabels

});

// To add the series to the chart, put them in a StackedColumnCollection

const stackedColumnCollection = new StackedColumnCollection(wasmContext);

stackedColumnCollection.dataPointWidth = 0.6;

stackedColumnCollection.add(rendSeries1, rendSeries2, rendSeries3, rendSeries4, rendSeries5);

// Add the Stacked Column collection to the chart

sciChartSurface.renderableSeries.add(stackedColumnCollection);

## How the Stacking and Grouping Works for Column Series

StackedColumnRenderableSeries📘 have a property stackedGroupId which defines how columns are grouped and stacked. When two StackedColumnRenderableSeries📘 have a stackedGroupId set the grouping behaves differently.

### A: Stacked Column Mode

By default, the stackedGroupId is undefined. When this is unset, or, when set to the same value, columns stack vertically.

`const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {`

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { growBy: new NumberRange(0, 0.1) }));

const stackedCollection = new StackedColumnCollection(wasmContext);

// Using the same stackedGroupId causes stacking (one above another)

stackedCollection.add(

new StackedColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues1, dataSeriesName: "EU" }),

fill: "#882B91",

stroke: "#E4F5FC",

strokeThickness: 1,

opacity: 0.8,

stackedGroupId: "StackedGroupId"

})

);

stackedCollection.add(

new StackedColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues2, dataSeriesName: "Asia" }),

fill: "#EC0F6C",

stroke: "#E4F5FC",

strokeThickness: 1,

opacity: 0.8,

stackedGroupId: "StackedGroupId"

})

);

stackedCollection.add(

new StackedColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues3, dataSeriesName: "USA" }),

fill: "#F48420",

stroke: "#E4F5FC",

strokeThickness: 1,

opacity: 0.8,

stackedGroupId: "StackedGroupId"

})

);

sciChartSurface.renderableSeries.add(stackedCollection);

### B: Grouped (Side by Side) Mode

When stackedGroupId is different on two columns, then the columns are grouped. This allows you to have multiple stacked groups.

`const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {`

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { growBy: new NumberRange(0, 0.1) }));

const stackedCollection = new StackedColumnCollection(wasmContext);

// Using a different stackedGroupId causes grouping (side-by-side)

stackedCollection.add(

new StackedColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues1, dataSeriesName: "EU" }),

fill: "#882B91",

stroke: "#E4F5FC",

strokeThickness: 1,

opacity: 0.8,

stackedGroupId: "StackedGroupId-First"

})

);

stackedCollection.add(

new StackedColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues2, dataSeriesName: "Asia" }),

fill: "#EC0F6C",

stroke: "#E4F5FC",

strokeThickness: 1,

opacity: 0.8,

stackedGroupId: "StackedGroupId-Second"

})

);

stackedCollection.add(

new StackedColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues3, dataSeriesName: "USA" }),

fill: "#F48420",

stroke: "#E4F5FC",

strokeThickness: 1,

opacity: 0.8,

stackedGroupId: "StackedGroupId-Third"

})

);

sciChartSurface.renderableSeries.add(stackedCollection);

### C: Mixed (Stacked & Grouped) Mode

To demonstrate the purpose of stackedGroupId, below we have set one column to one stackedGroupId, and two other columns to another stackedGroupId. This creates two stacked groups, one with Orange/Red series (which have the same stackedGroupId) and another with the blue series.

`const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {`

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { growBy: new NumberRange(0, 0.1) }));

const stackedCollection = new StackedColumnCollection(wasmContext);

// Using a mixture of stackedGroupId allows mixed stacked/grouped behaviour

stackedCollection.add(

new StackedColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues1, dataSeriesName: "EU" }),

fill: "#882B91",

stroke: "#E4F5FC",

strokeThickness: 1,

opacity: 0.8,

stackedGroupId: "StackedGroupId-First"

})

);

stackedCollection.add(

new StackedColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues2, dataSeriesName: "Asia" }),

fill: "#EC0F6C",

stroke: "#E4F5FC",

strokeThickness: 1,

opacity: 0.8,

stackedGroupId: "StackedGroupId-First"

})

);

stackedCollection.add(

new StackedColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues3, dataSeriesName: "USA" }),

fill: "#F48420",

stroke: "#E4F5FC",

strokeThickness: 1,

opacity: 0.8,

stackedGroupId: "StackedGroupId-Second"

})

);

sciChartSurface.renderableSeries.add(stackedCollection);

### D: 100% Stacked Column Chart Mode

SciChart.js also supports a 100% Stacked Column chart, which can be enabled by setting a single flag: StackedColumnCollection.isOneHundredPercent.

`const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {`

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { growBy: new NumberRange(0, 0.1) }));

const stackedCollection = new StackedColumnCollection(wasmContext, {

// Simply set isOneHundredPercent to enable 100% stacking

isOneHundredPercent: true

});

// Using the same stackedGroupId causes stacking (one above another)

stackedCollection.add(

new StackedColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues1, dataSeriesName: "EU" }),

fill: "#882B91",

stroke: "#E4F5FC",

strokeThickness: 1,

opacity: 0.8,

stackedGroupId: "StackedGroupId"

})

);

stackedCollection.add(

new StackedColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues2, dataSeriesName: "Asia" }),

fill: "#EC0F6C",

stroke: "#E4F5FC",

strokeThickness: 1,

opacity: 0.8,

stackedGroupId: "StackedGroupId"

})

);

stackedCollection.add(

new StackedColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues3, dataSeriesName: "USA" }),

fill: "#F48420",

stroke: "#E4F5FC",

strokeThickness: 1,

opacity: 0.8,

stackedGroupId: "StackedGroupId"

})

);

sciChartSurface.renderableSeries.add(stackedCollection);

## Gradient Fill Example

`// Data for the example`

const xValues = [1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003];

const yValues1 = [10, 13, 7, 16, 4, 6, 5, 14, 16, 10, 24, 11];

const yValues2 = [12, 17, 21, 15, 19, 18, 6, 21, 22, 20, 5, 10];

const yValues3 = [7, 30, 27, 24, 21, 15, 7, 26, 22, 28, 21, 22];

const yValues4 = [16, 10, 9, 8, 22, 14, 8, 27, 25, 23, 17, 17];

const yValues5 = [7, 24, 21, 11, 19, 17, 9, 27, 26, 22, 28, 16];

const dataLabels = {

color: "#FFfFFF",

style: { fontSize: 12, fontFamily: "Arial", padding: new Thickness(0, 0, 4, 0) },

precision: 0,

positionMode: EColumnDataLabelPosition.Outside,

verticalTextPosition: EVerticalTextPosition.Center

};

// Create some RenderableSeries - for each part of the stacked column

// Notice the stackedGroupId. This defines if series are stacked (same), or grouped side by side (different)

const rendSeries1 = new StackedColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues1, dataSeriesName: "EU" }),

fillLinearGradient: new GradientParams(new Point(0, 0), new Point(0, 1), [

{ color: "#882B91", offset: 0 },

{ color: "#EC0F6C", offset: 1 }

]),

opacity: 0.8,

stackedGroupId: "StackedGroupId",

});

const rendSeries2 = new StackedColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues2, dataSeriesName: "Asia" }),

fillLinearGradient: new GradientParams(new Point(0, 0), new Point(0, 1), [

{ color: "#EC0F6C", offset: 0 },

{ color: "#F48420", offset: 1 }

]),

opacity: 0.8,

stackedGroupId: "StackedGroupId",

});

const rendSeries3 = new StackedColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues3, dataSeriesName: "USA" }),

fillLinearGradient: new GradientParams(new Point(0, 0), new Point(0, 1), [

{ color: "#F48420", offset: 0 },

{ color: "#50C7E0", offset: 1 }

]),

opacity: 0.8,

stackedGroupId: "StackedGroupId",

});

const rendSeries4 = new StackedColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues4, dataSeriesName: "UK" }),

fillLinearGradient: new GradientParams(new Point(0, 0), new Point(0, 1), [

{ color: "#50C7E0", offset: 0 },

{ color: "#30BC9A", offset: 1 }

]),

opacity: 0.8,

stackedGroupId: "StackedGroupId",

});

const rendSeries5 = new StackedColumnRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues: yValues5, dataSeriesName: "Latam" }),

fillLinearGradient: new GradientParams(new Point(0, 0), new Point(0, 1), [

{ color: "#30BC9A", offset: 0 },

{ color: "#0652DD", offset: 1 }

]),

opacity: 0.8,

stackedGroupId: "StackedGroupId",

});

// To add the series to the chart, put them in a StackedColumnCollection

const stackedColumnCollection = new StackedColumnCollection(wasmContext);

stackedColumnCollection.dataPointWidth = 0.6;

stackedColumnCollection.add(rendSeries1, rendSeries2, rendSeries3, rendSeries4, rendSeries5);

// Add the Stacked Column collection to the chart

sciChartSurface.renderableSeries.add(stackedColumnCollection);