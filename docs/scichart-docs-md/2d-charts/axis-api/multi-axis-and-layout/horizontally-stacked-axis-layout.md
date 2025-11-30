---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/multi-axis-and-layout/horizontally-stacked-axis-layout
scraped_at: 2025-11-28T18:24:11.053543
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/multi-axis-and-layout/horizontally-stacked-axis-layout

# Horizontally Stacked Axis Layout

The Stacked Axis feature in SciChart allows you to specify the layout of the axis panel. Normally when you have multiple XAxis, they are stacked vertically. However, you can switch this to stack horizontally. Custom and complex layouts are possible allowing for all kinds of chart scenarios.

Polar Charts do not support stacked axes yet

In the previous article we demonstrated Vertically Stacked Axis. This is where you specify a layout strategy for Y Axis on the left or right of the chart to stack axis above each other.

## Create a Horizontally Stacked Axis Chart

### Step 1: Create a Multi X-Axis Chart

Typically if you create a chart with several X-Axis, they are stacked on the top or bottom of the chart.

The following code with 4 XAxis on the bottom results in this output:

- TS
- Builder API (JSON Config)

`// Create an YAxis on the Left`

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

axisTitle: "Y Axis",

axisTitleStyle: { fontSize: 13 },

backgroundColor: "#50C7E022",

axisBorder: { color: "#50C7E0", borderRight: 1 },

axisAlignment: EAxisAlignment.Left,

growBy: new NumberRange(0.1, 0.1)

})

);

// Create several XAxis on the bottom

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { axisTitle: "X Axis 0" }));

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { axisTitle: "X Axis 1" }));

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { axisTitle: "X Axis 2" }));

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { axisTitle: "X Axis 3" }));

// To make it clearer what's happening, colour the axis backgrounds & borders

const axisColors = ["#50C7E0", "#EC0F6C", "#30BC9A", "#F48420"];

sciChartSurface.xAxes.asArray().forEach((xAxis, index) => {

xAxis.backgroundColor = axisColors[index] + "22";

xAxis.axisBorder = { color: axisColors[index], borderTop: 1 };

xAxis.axisTitleStyle.fontSize = 13;

});

// Let's add some series to the chart to show how they also behave with axis

const getOptions = index => {

const xValues = Array.from(Array(50).keys());

const yValues = xValues.map(x => Math.sin(x * 0.4 + index));

return {

xAxisId: sciChartSurface.xAxes.asArray()[index].id,

stroke: axisColors[index],

strokeThickness: 2,

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues })

};

};

sciChartSurface.renderableSeries.add(new FastLineRenderableSeries(wasmContext, { ...getOptions(0) }));

sciChartSurface.renderableSeries.add(new FastLineRenderableSeries(wasmContext, { ...getOptions(1) }));

sciChartSurface.renderableSeries.add(new FastLineRenderableSeries(wasmContext, { ...getOptions(2) }));

sciChartSurface.renderableSeries.add(new FastLineRenderableSeries(wasmContext, { ...getOptions(3) }));

`const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {`

surface: { theme: { type: EThemeProviderType.Dark } },

yAxes: {

type: EAxisType.NumericAxis,

options: {

axisTitle: "Y Axis",

axisTitleStyle: { fontSize: 13 },

backgroundColor: "#50C7E022",

axisBorder: { color: "#50C7E0", borderRight: 1 },

axisAlignment: EAxisAlignment.Left

}

},

xAxes: [

{

type: EAxisType.NumericAxis,

options: {

id: "XAxis0",

axisTitle: "X Axis 0",

backgroundColor: "#50C7E022",

axisBorder: { borderTop: 1, color: "#50C7E0" }

}

},

{

type: EAxisType.NumericAxis,

options: {

id: "XAxis1",

axisTitle: "X Axis 1",

backgroundColor: "#EC0F6C22",

axisBorder: { borderTop: 1, color: "#EC0F6C" }

}

},

{

type: EAxisType.NumericAxis,

options: {

id: "XAxis2",

axisTitle: "X Axis 2",

backgroundColor: "#30BC9A22",

axisBorder: { borderTop: 1, color: "#30BC9A" }

}

},

{

type: EAxisType.NumericAxis,

options: {

id: "XAxis3",

axisTitle: "X Axis 3",

backgroundColor: "#F4842022",

axisBorder: { borderTop: 1, color: "#F48420" }

}

}

],

series: [

{

type: ESeriesType.LineSeries,

options: { stroke: "#50C7E0", strokeThickness: 2, xAxisId: "XAxis0" },

xyData: { xValues, yValues }

},

{

type: ESeriesType.LineSeries,

options: { stroke: "#EC0F6C", strokeThickness: 2, xAxisId: "XAxis1" },

xyData: { xValues, yValues: yValues1 }

},

{

type: ESeriesType.LineSeries,

options: { stroke: "#30BC9A", strokeThickness: 2, xAxisId: "XAxis2" },

xyData: { xValues, yValues: yValues2 }

},

{

type: ESeriesType.LineSeries,

options: { stroke: "#F48420", strokeThickness: 2, xAxisId: "XAxis3" },

xyData: { xValues, yValues: yValues3 }

}

]

});

### Step 2: Apply the Layout Strategy

To change the behaviour of axis stacking you need to set the appropriate layoutStrategy property on the SciChartSurface.LayoutManager📘 with the stacked version.

SciChart provides the following Outer Axes Layout Strategies:

- LeftAlignedOuterVerticallyStackedAxisLayoutStrategy📘
- RightAlignedOuterVerticallyStackedAxisLayoutStrategy📘
- TopAlignedOuterHorizontallyStackedAxisLayoutStrategy📘
- BottomAlignedOuterHorizontallyStackedAxisLayoutStrategy📘

Modify the code above to set this property on the SciChartSurface.LayoutManager📘:

- TS

`// Enable stacking of axis`

sciChartSurface.layoutManager.bottomOuterAxesLayoutStrategy =

new BottomAlignedOuterHorizontallyStackedAxisLayoutStrategy();

Now the layout is completely changed.

## LayoutStrategies Applicable to X-Axis

The following horizontally stacked layout strategies are available and may be applied to the following properties on SciChartSurface.LayoutManager📘:

| Layout Strategy | Use With | Apply to LayoutManager Prop | Behavior |
|---|---|---|---|
| TopAlignedOuterAxisLayoutStrategy📘 | X Axis | topInnerAxisLayoutStrategy📘, topOuterAxisLayoutStrategy📘 | Default behavior |
| BottomAlignedOuterAxisLayoutStrategy📘 | X Axis | bottomInnerAxisLayoutStrategy📘, bottomOuterAxisLayoutStrategy📘 | Default behavior |
| TopAlignedOuterHorizontallyStackedAxisLayoutStrategy📘 | X Axis | topOuterAxisLayoutStrategy📘 | Horizontal stacking behavior |
| BottomAlignedOuterHorizontallyStackedAxisLayoutStrategy📘 | X Axis | bottomOuterAxisLayoutStrategy📘 | Horizontal stacking behavior |

Try experimenting with the Codepen above to see how each of the strategies behave.
Note that a **TopLayoutStrategy** will require Axis.axisAlignment📘 = EAxisAlignment.Top📘 and vice versa.

## Customising Axis Size when Horizontally Stacked

The Axis.stackedAxisLength📘 property allows you to customize the size of a Horizontally Stacked Axis in SciChart.js. This property may be an absolute number, e.g. 50 pixels, or a percentage e.g. "30%". When left undefined, default equal spacing will be used.

Try the following code to see how it affects stacked axis size.

- stackedAxisLength

`// This stacked axis has 100 pixel length`

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { axisTitle: "X Axis 0", stackedAxisLength: 100 }));

// This stacked axis occupies 50% of available space

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { axisTitle: "X Axis 1", stackedAxisLength: "50%" }));

// These stacked axis obey default spacing

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { axisTitle: "X Axis 2" }));

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { axisTitle: "X Axis 3" }));

## Combining Vertical (rotated) Charts & Stacked Axis

Part of the magic of SciChart.js is the sheer number of combinations you can have for chart and axis layout!

If we combine the Vertical Chart feature where you set **XAxis.axisAlignment** = Left and **YAxis.axisAlignment** = Top with the Horizontally Stacked Axis feature where we can re-arrange the layout of axis on the top/bottom of the chart, we can achieve things like this:

- TS

`sciChartSurface.layoutManager.topOuterAxesLayoutStrategy =`

new TopAlignedOuterHorizontallyStackedAxisLayoutStrategy();

// Create an XAxis on the left

sciChartSurface.xAxes.add(

new NumericAxis(wasmContext, {

axisTitle: "Rotated X Axis",

axisTitleStyle: { fontSize: 13 },

backgroundColor: "#50C7E022",

axisBorder: { color: "#50C7E0", borderRight: 1 },

axisAlignment: EAxisAlignment.Left

})

);

// Create several Y-Axis on the Top

const axisAlignment = EAxisAlignment.Top;

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, { axisTitle: "Rotated, Stacked Y Axis 0", axisAlignment })

);

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, { axisTitle: "Rotated, Stacked Y Axis 1", axisAlignment })

);

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, { axisTitle: "Rotated, Stacked Y Axis 2", axisAlignment })

);

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, { axisTitle: "Rotated, Stacked Y Axis 3", axisAlignment })

);