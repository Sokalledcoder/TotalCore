---
source: https://www.scichart.com/documentation/js/v4/2d-charts/builder-api/complex-options
scraped_at: 2025-11-28T18:24:12.908801
---

# https://www.scichart.com/documentation/js/v4/2d-charts/builder-api/complex-options

# Complex Options

Many things in SciChart.js are customised by providing a particular subclass, eg `PointMarkers`

. The type signature in the options in these cases will be something like IPointMarker📘 | TPointMarkerDefinition📘.

Many of these classes require a `wasmContext`

in the constructor, which you won’t have if you are trying to pass everything in a single definition, so instead use the Definition style, which as usual is `{ type, options }`

.

For example:

- TS

`return chartBuilder.buildChart(divElementId, {`

series: {

type: ESeriesType.ScatterSeries,

xyData: {

xValues: [1, 3, 4, 7, 9],

yValues: [10, 6, 7, 2, 16]

},

options: {

pointMarker: {

type: EPointMarkerType.Ellipse,

options: {

stroke: "red",

fill: "white",

}

}

}

}

});

This works for **Themes**, **PointMarkers**, **Effects**, **Animations**, **PaletteProviders** and **LabelProviders**.

Alternatively you can take the same approach as for option 3 of creating data and call buildChart📘 or build2DChart📘 with a partial definition, to get your wasmContext, then create an instance of the necessary class, then call buildSeries and pass it in. This is useful if you want to keep a reference to the object to be able to update it later.

- Building with complex options

`const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {});`

const pointMarker = new EllipsePointMarker(wasmContext, {

stroke: "red",

fill: "white",

});

const seriesArray = await chartBuilder.buildSeries(wasmContext, {

type: ESeriesType.ScatterSeries,

xyData: {

xValues: [1, 3, 4, 7, 9],

yValues: [10, 6, 7, 2, 16]

},

options: {

pointMarker: pointMarker // you can use the pointMarker instance created above

}

});

sciChartSurface.renderableSeries.add(...seriesArray);

## Function Options

Some options properties are actually functions, such as the templating functions on RolloverModifier, or the callbacks on SeriesSelectionModifier. These have a signature which is essentially `function | string`

eg

`onSelectionChanged?: ((args: SelectionChangedArgs) => void) | string;`

Here, the choice depends very specifically on whether or not you need to be able to serialise and deserialise the chart to a JSON string. If you don’t need to, just specify the option as a function as normal. If you do need to, then you will need to register your function, and pass the registered name eg:

- Building with function options

`const { sciChartSurface, wasmContext } = await chartBuilder.build2DChart(divElementId, {`

series: {

type: ESeriesType.LineSeries,

xyData: {

xValues: [1, 3, 4, 7, 9],

yValues: [10, 6, 7, 2, 16]

}

}

});

const logOnSelectionChanged = (args: SelectionChangedArgs) => {

console.log(args)

};

chartBuilder.registerFunction(EBaseType.OptionFunction, "logOnSelectionChanged", logOnSelectionChanged);

const [chartModifier] = chartBuilder.buildModifiers({

type: EChart2DModifierType.SeriesSelection,

options: { onSelectionChanged: "logOnSelectionChanged" }

});

sciChartSurface.chartModifiers.add(chartModifier);

When the modifier is built, SciChart will look up the function in its registry and assign it. When you serialize the chart, you will get the function name in the definition. It is very important when doing this that the function definition and registration actually occurs before it is needed in a chart.

## onCreated Function

Specific to the builder api, there is an **onCreated** option in the ISciChart2DDefinition📘 which is a callback that is run after the chart is built and takes the sciChartSurface as a parameter. It can be used to run zoomExtents, or perform further configuration using the standard api.