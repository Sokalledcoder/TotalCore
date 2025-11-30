---
source: https://www.scichart.com/documentation/js/v4/2d-charts/builder-api/working-with-data
scraped_at: 2025-11-28T18:24:13.814788
---

# https://www.scichart.com/documentation/js/v4/2d-charts/builder-api/working-with-data

# Working with Data

## Creating or Updating Data on Builder API Created charts

Data can be supplied to charts created with the SciChart.js Builder API in one of three ways:

### 1. Supply Data via Values properties

Values properties can be supplied within the series definition property.

This method is demonstrated below. This is also the format you will get by default when you serialise a chart containing data.

- TS

`const { sciChartSurface, wasmContext } = await chartBuilder.buildChart(divElementId, {`

series: {

type: ESeriesType.LineSeries,

xyData: {

xValues: [1, 3, 4, 7, 9],

yValues: [10, 6, 7, 2, 16]

}

}

});

### 2. Reference sharedData using dataId properties

Often you will want to define the structure of the chart, and reuse it with different data. Instead of setting `xValues`

and `yValues`

, you set `xDataId`

and `yDataId`

to the names you use in a `sharedData`

section.

For example:

- JS

`const { chartBuilder, ESeriesType } = SciChart;`

const DATA = {

x: [1, 2, 3, 4, 5],

col: [8, 2, 3, 7, 10],

line: [10, 6, 7, 2, 16]

};

const { sciChartSurface, wasmContext } = await chartBuilder.build2DChart(divElementId, {

series: [

{ type: ESeriesType.ColumnSeries, xyData: { xDataId: "x", yDataId: "col" } },

{ type: ESeriesType.LineSeries, xyData: { xDataId: "x", yDataId: "line" } },

],

sharedData: DATA // pass the shared data object

});

This is good for multiple series which share x data, but is not as convenient if you want to be able to update the data later. For this you need to use our DataSeries API.

### 3. Create a DataSeries and Manually Assign it

Once the chart is created, you can use the `wasmContext`

that is returned to create a `dataSeries`

in the normal way.

Here we’re using build2DChart📘 rather than buildChart📘 so that we don’t have to cast the result.

Note that build2DChart📘 (and buildChart📘) returns a `Promise`

so we need to resolve it to use the result, e.g. use `async/await`

syntax or `Promise chaining`

.

- JS

`const { chartBuilder, XyDataSeries, ESeriesType } = SciChart;`

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

series: [

{

type: ESeriesType.ColumnSeries,

options: {

id: "columnSeries1",

stroke: "blue",

fill: "rgba(0, 0, 255, 0.3)"

}

// no "xyData" provided just yet, we will add it later

}

]

});

const dataSeries = new XyDataSeries(wasmContext, {

xValues: [1, 2, 3, 4, 5],

yValues: [8, 2, 3, 7, 10]

});

// assign the dataSeries to the renderable series

sciChartSurface.renderableSeries.get(0).dataSeries = dataSeries;

// Alternatively, you can set the dataSeries by ID:

// sciChartSurface.renderableSeries.getById("columnSeries1").dataSeries = dataSeries;

Note that Charts, Series and DataSeries created when using the Builder API can be accessed and modified using the JavaScript programmatic API in SciChart.js. If you want deep customization of the chart but a simple way to create templates, then this API is very powerful!

## Using the Filters API with the Builder API

SciChart.js v2.x features a new Filters API, which allows you to apply dynamic data transforms to data series which update as your underlying data updates.

Here is an example of adding a `Filter`

or `DataTransform`

to a SciChartSurface when using the Builder API:

- TS

`const { chartBuilder, ESeriesType, EDataFilterType } = SciChart;`

const xyData = {

xValues: [1, 2, 3, 4, 5, 6],

yValues: [2, 5, 7, 4, 10, 15]

};

chartBuilder.buildChart(divElementId, {

series: [

{

type: ESeriesType.LineSeries,

xyData,

},

{

type: ESeriesType.LineSeries,

options: { stroke: "red" },

xyData: {

...xyData,

filter: { type: EDataFilterType.XyLinearTrend }

}

}

]

});

For more details regarding the Filters API, check the Filter API Documentation.

## Using PointMetadata with the Builder API

SciChart.js v2.x features a new PointMetadata API, which allows you to tag any X, Y datapoint with a custom object confirming to the IPointMetadata📘 interface.

This lets you tag datapoints with objects, mark them as selected or deselected, or include further information to display in tooltips, on hit-test or selection etc...

When working with the Builder API, some extra consideration is needed if you are planning to serialize and deserialize metadata.

- You need a copy of the same metadata object applied to every point. This is needed to support datapoint selection. In this case, set the metadata poroperty on the dataSeries options to your desired object and it will be cloned to every point that is added. It will be serialized exactly as added.

`xyData: {`

metadata: {

isSelected: false

}

}

2.You need to set an array of metadata with values specific to each data point. As long as your metadata object is pure data, just set the array on the metadata property.

3.Your metadata object contains functions. Now you need to supply a type name of a registered IMetadataGenerator📘. This interface can return a single object which will be used to populate each data point, or as I1DMetadataGenerator📘 (or I2DMetadataGenerator📘 for heatmap data) it can return an array which should be the same size as your data. In this case you will probably want to set the data property, which will be passed into the function you register to create your metadataGenerator. In this case, the output of the toJSON method on the metadataGenerator should match the format of data passed in. As before, don’t forget to define and register these things on the client. Hopefully now the type signature of the metadata option makes some sense.

`metadata?:`

| IPointMetadata[]

| IPointMetadata

| { type: string; data?: any };

For more information regarding the PointMetadata API, check the PointMetadata API Documentation.