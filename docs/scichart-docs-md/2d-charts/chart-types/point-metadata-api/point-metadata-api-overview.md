---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/point-metadata-api/point-metadata-api-overview
scraped_at: 2025-11-28T18:24:39.937502
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/point-metadata-api/point-metadata-api-overview

# PointMetadata API

The PointMetadata API in SciChart.js allows you to:

**Tag any X,Y point in a DataSeries with a custom JavaScript object**- It can be used with the DataPoint Selection Modifier to enable per-point
**selection** - It can be used with the PaletteProvider API to provide
**custom colouring**of data-points in a series. - It can be used with
**tooltips**such as CursorModifier and RolloverModifier to display extra data or info inside a tooltip - Finally, it can be used in the result of any Hit-Test operation where X,Y,Metadata can be queried on click

## Adding Metadata to Charts

Metadata is optional and can be set when a dataseries is first created, or whenever data is added or updated. Metadata is just a JavaScript object and can contain any properties, objects, even functions.

See the example below for how to create metadata when constructing an XyDataSeries📘 and how to consume it in a RolloverModifier.

- TS
- Builder API (JSON Config)
- MyMetadata class

`const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {`

theme: new SciChartJsNavyTheme()

});

const growBy = new NumberRange(0.1, 0.1);

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { growBy }));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { growBy }));

// Create metadata with initial values. Metadata can be any JS object

const dataSeries = new XyDataSeries(wasmContext, {

xValues: [1, 2, 3, 4, 5],

yValues: [4.3, 5.3, 6, 6.3, 6.4],

metadata: [

new MyMetadata("Here's", 7),

undefined, // nothing at this index

new MyMetadata("Some"),

new MyMetadata(),

new MyMetadata("Metadata", 99, true)

]

});

// Add a line series with the metadata

sciChartSurface.renderableSeries.add(

new FastLineRenderableSeries(wasmContext, {

dataSeries,

pointMarker: new EllipsePointMarker(wasmContext, {

width: 11,

height: 11,

fill: "#364BA0",

stroke: "#50C7E0",

strokeThickness: 2

})

})

);

// Add a RolloverModifier configured to output X,Y,Metadata.stringValue and customValue

sciChartSurface.chartModifiers.add(

new RolloverModifier({

snapToDataPoint: true,

tooltipDataTemplate: seriesInfo => [

`X: ${seriesInfo.formattedXValue}`,

`Y: ${seriesInfo.formattedYValue}`,

`Metadata.stringValue: ${(seriesInfo.pointMetadata as MyMetadata)?.stringValue ?? "null"}`,

`Metadata.customValue: ${(seriesInfo.pointMetadata as MyMetadata)?.customValue ?? "null"}`

]

})

);

`const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {`

surface: { theme: { type: EThemeProviderType.Dark } },

series: [

{

type: ESeriesType.LineSeries,

// Metadata is set in xyData property

xyData: {

xValues: [1, 2, 3, 4, 5],

yValues: [4.3, 5.3, 6, 6.3, 6.4],

metadata: [

{ stringValue: "Here's", customValue: 7 },

undefined, // nothing at this index

{ stringValue: "Some" },

{}, // empty object at this index

{ stringValue: "Metadata", customValue: 99 }

]

},

options: {

stroke: "#C52E60",

pointMarker: {

type: EPointMarkerType.Ellipse,

options: {

width: 11,

height: 11,

fill: "White"

}

}

}

}

],

// Configure a Rollovermodifier to display metadata

modifiers: [

{

type: EChart2DModifierType.Rollover,

options: {

snapToDataPoint: true,

tooltipDataTemplate: seriesInfo => [

`X: ${seriesInfo.formattedXValue}`,

`Y: ${seriesInfo.formattedYValue}`,

`Metadata.stringValue: ${seriesInfo.pointMetadata?.stringValue ?? "null"}`,

`Metadata.customValue: ${seriesInfo.pointMetadata?.customValue ?? "null"}`

]

}

}

]

});

`class MyMetadata implements IPointMetadata {`

stringValue: string;

customValue: number;

isSelected: boolean;

constructor(stringValue: string = "", customValue: number = 0, isSelected: boolean = false) {

this.stringValue = stringValue;

this.customValue = customValue;

this.isSelected = isSelected;

}

}

This results in the following output

Note: You do not have to set metadata on every point. The structure of the metadata does not have to be the same for every point.

In TypeScript, all metadata must implement the IPointMetadata📘 interface, ie `{ isSelected: boolean }`

. For JavaScript, this property can be omitted.

## Metadata Templates

If you just need to set the same metadata on every point, you can supply a single metadata object and it will be used as a template and be cloned onto each datapoint. For example:

- JS
- Builder API (JSON Config)

`// Set a single object, this will be cloned as a template for all metadata on the dataseries`

const dataSeries = new XyDataSeries(wasmContext, {

xValues: [1, 2, 3, 4, 5],

yValues: [4.3, 5.3, 6, 6.3, 6.4],

metadata: { stringValue: "All the same value", customValue: 7 }

});

// Update just a metadata value

// Update just a metadata value. This will not trigger a chart redraw

dataSeries.getMetadataAt(0).stringValue = "Updated #0";

// To force a redraw, use update and pass a new metadata object

dataSeries.update(1, 5.3, { stringValue: "Updated #1 with redraw", customValue: 99 });

// Or, to trigger a redraw, call invalidateElement() on the parent SciChartSurface

sciChartSurface.invalidateElement();

`const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {`

surface: { theme: { type: EThemeProviderType.Dark } },

series: [

{

type: ESeriesType.LineSeries,

// Metadata is set in xyData property

xyData: {

xValues: [1, 2, 3, 4, 5],

yValues: [4.3, 5.3, 6, 6.3, 6.4],

metadata: { stringValue: "All the same value", customValue: 7 }

},

// ...

## Metadata Generators

If you want to set complex metadata using the Builder Api you have the option to take control of how the metadata is deserialized and serialized by passing a **MetadataGenerator**. This is a class that should accept raw data in its constructor and have a **getMetadata** method that returns a metadata array.

- JS

`// Create a metadata class. Confirms to interface I1DMetadataGenerator`

class ExampleMetadataGenerator {

// Accept and store the raw data in the constructor

constructor(stringArray) {

console.log(`${stringArray}`);

this.stringValues = stringArray;

this.type = "ExampleMetadataGenerator";

}

// This is called by SciChart to get the metadata to set when the dataSeries is created

getMetadata = () => this.stringValues.map(s => ({ stringValue: s }));

// Unused for this example. Used to create a clone of metadata template for each datapoint

getSingleMetadata = () => ({ stringValue: "" });

// Required for serialization and builder API

toJSON = () => ({ type: this.type, data: this.stringValues });

}

Before this class can be used with the builder api it must be registered. Then, it can be used like this:

- JS
- Builder API (JSON Config)

`// call chartBuilder.registerType to register a new custom type`

chartBuilder.registerType(EBaseType.MetadataGenerator, "ExampleMetadataGenerator", data => new ExampleMetadataGenerator(data));

// Assign a Metadata generator instance to create metadata dynamically

const dataSeries = new XyDataSeries(wasmContext, {

xValues: [1, 2, 3, 4, 5],

yValues: [4.3, 5.3, 6, 6.3, 6.4],

metadata: { type: "ExampleMetadataGenerator", data: ["Here's", "Some", "Metadata", "From", "Generator"] }

});

`// call chartBuilder.registerType to register a new custom type`

chartBuilder.registerType(EBaseType.MetadataGenerator, "ExampleMetadataGenerator", data => new ExampleMetadataGenerator(data));

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

series: [

{

type: ESeriesType.LineSeries,

// Metadata is set in xyData property

xyData: {

xValues: [1, 2, 3, 4, 5],

yValues: [4.3, 5.3, 6, 6.3, 6.4],

metadata: {

type: "ExampleMetadataGenerator",

data: ["Here's", "Some", "Metadata", "From", "Generator"]

}

},

// ...

Note: for more info about the Builder API, please see the section in our documentation here.