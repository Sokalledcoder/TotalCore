---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/data-point-labels/getting-labels-from-metadata
scraped_at: 2025-11-28T18:24:24.017388
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/data-point-labels/getting-labels-from-metadata

# Getting Labels from Metadata

DataLabels allow per data-point text labels to be drawn on series, or arbitrary text labels at x,y positions on the chart.

You can see several datalabel examples on the SciChart.js demo:

- The Line Chart example
- The Column Chart example
- The PaletteProvider example
- The DataLabels demo
- The Stacked Column Chart demo
- The Population Pyramid demo

Explore these for some rich examples of how to use this API.

## Formatting a DataLabel using metaDataSelector

Metadata allows you to assign optional javascript objects to individual x,y datapoints. To learn more about the Metadata API, see here.

DataLabels support rendering text from metadata as standard. You just need to provide a function to the metaDataSelector📘 option that tells SciChart how to turn your metaData into text.

Find an example below:

- TS
- Builder API (JSON Config)

`const {`

SciChartSurface,

NumericAxis,

FastLineRenderableSeries,

EllipsePointMarker,

XyDataSeries,

NumberRange,

SciChartJsNavyTheme

} = SciChart;

// or for npm: import { SciChartSurface, ... } from "scichart"

// Create a SciChartSurface with X,Y Axis

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { growBy: new NumberRange(0.1, 0.1) }));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { growBy: new NumberRange(0.1, 0.1) }));

const metadata = [

{ text: "Bananas", isSelected: false },

{ text: "Apples", isSelected: false },

{ text: "Pears", isSelected: false },

{ text: "Pineapples", isSelected: false },

{ text: "Plums", isSelected: false },

{ text: "Cherries", isSelected: false },

{ text: "Strawberries", isSelected: false },

{ text: "Blueberries", isSelected: false },

{ text: "Lemons", isSelected: false },

{ text: "Limes", isSelected: false },

{ text: "Papaya", isSelected: false },

{ text: "Guava", isSelected: false }

];

// Create a chart with line series with a point-marker

// optional metadata is also passed with javascript objects into the dataSeries

sciChartSurface.renderableSeries.add(

new FastLineRenderableSeries(wasmContext, {

stroke: "SteelBlue",

strokeThickness: 3,

pointMarker: new EllipsePointMarker(wasmContext, {

width: 10,

height: 10,

strokeThickness: 2,

stroke: "SteelBlue",

fill: "LightSteelBlue"

}),

dataSeries: new XyDataSeries(wasmContext, {

xValues: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],

yValues: [4.3, 5.3, 6, 6.3, 6, 5.2, 4.5, 4.6, 5, 6, 7, 8],

metadata

}),

// Next, add the dataLabels. Simply setting dataLabel style makes labels visible

// We also pass a metaDataSelector which is a function that can be used to format labels from metadata objects

dataLabels: {

metaDataSelector: metaData => (metaData as any).text,

style: {

fontFamily: "Default",

fontSize: 16

},

color: "#EEE"

}

})

);

`// Demonstrates how to add DataLabels to a chart with SciChart.js using the Builder API`

const { chartBuilder, ESeriesType, EThemeProviderType, EPointMarkerType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const metadata = [

{ text: "Bananas", isSelected: false },

{ text: "Apples", isSelected: false },

{ text: "Pears", isSelected: false },

{ text: "Pineapples", isSelected: false },

{ text: "Plums", isSelected: false },

{ text: "Cherries", isSelected: false },

{ text: "Strawberries", isSelected: false },

{ text: "Blueberries", isSelected: false },

{ text: "Lemons", isSelected: false },

{ text: "Limes", isSelected: false },

{ text: "Papaya", isSelected: false },

{ text: "Guava", isSelected: false }

];

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

series: [

{

type: ESeriesType.LineSeries,

xyData: {

xValues: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],

yValues: [4.3, 5.3, 6, 6.3, 6, 5.2, 4.5, 4.6, 5, 6, 7, 8],

metadata

},

options: {

stroke: "SteelBlue",

strokeThickness: 3,

pointMarker: {

type: EPointMarkerType.Ellipse,

options: {

width: 10,

height: 10,

strokeThickness: 2,

stroke: "SteelBlue",

fill: "LightSteelBlue"

}

},

// Next, add the dataLabels. Simply setting dataLabel style makes labels visible

// We also pass a metaDataSelector which is a function that can be used to format labels from metadata objects

dataLabels: {

metaDataSelector: metaData => (metaData as any).text,

style: {

fontFamily: "Default",

fontSize: 16

},

color: "#EEE"

}

}

}

]

});

This results in the following output:

## Accessing Metadata from getText() and DataLabelState

The metaDataSelector📘 option allows you to return values stored in the metadata of a dataSeries, but what if you wanted to have more complex formatting mixing index, x, y value or the metadata values?

You can also access metadata via a custom DataLabelProvider.getText()📘 function. This technique is covered in the article Custom DataLabel Formatting.

Once you've setup a custom formatting function, you can then use dataLabelState.getMetaData()📘 to get the metaData for the current point.

Here's an example:

- TS
- JS

`// Assuming metadata has been constructed in the dataseries and dataLabels enabled,`

// you can format labels with metadata using dataLabelProvider.getText(dataLabelState)

(sciChartSurface.renderableSeries.get(0).dataLabelProvider as LineSeriesDataLabelProvider).getText =

dataLabelState => {

return `index=${dataLabelState.index},

x,y=[${dataLabelState.xVal()}, ${dataLabelState.yVal()}],

metadata="${(dataLabelState.getMetaData() as any)?.text}"`;

};

`// Assuming metadata has been constructed in the dataseries and dataLabels enabled,`

// you can format labels with metadata using dataLabelProvider.getText(dataLabelState)

sciChartSurface.renderableSeries.get(0).dataLabelProvider.getText =

dataLabelState => {

return `index=${dataLabelState.index},

x,y=[${dataLabelState.xVal()}, ${dataLabelState.yVal()}],

metadata="${dataLabelState.getMetaData()?.text}"`;

};

This results in the following output.