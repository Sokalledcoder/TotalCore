---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/multi-axis-and-layout/vertically-stacked-axis-layout
scraped_at: 2025-11-28T18:24:11.301194
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/multi-axis-and-layout/vertically-stacked-axis-layout

# Vertically Stacked Axis Layout

The Stacked Axis feature in SciChart allows you to specify the layout of the axis panel. Normally when you have multiple YAxis, they are stacked horizontally. However, you can switch this to stack vertically. Custom and complex layouts are possible allowing for all kinds of chart scenarios.

Polar Charts do not support stacked axes yet

## Create a Vertically Stacked Axis Chart

### Step 1: Create a multiple Y-Axis Chart

Typically if you create a chart with several Y-Axis, they are stacked on the left or right of the chart.

The following code with 8 YAxis on the left results in this output:

- TS
- Builder API (JSON Config)

`// Create an XAxis on the bottom`

sciChartSurface.xAxes.add(

new NumericAxis(wasmContext, {

axisTitle: "X Axis",

axisTitleStyle: { fontSize: 13 },

backgroundColor: "#50C7E022",

axisBorder: { color: "#50C7E0", borderTop: 1 }

})

);

// Create several YAxis on the left

// Creating a NumericAxis as a YAxis on the left

const yAxis0 = new NumericAxis(wasmContext, {

axisTitle: "Y Axis 0",

axisAlignment: EAxisAlignment.Left

});

sciChartSurface.yAxes.add(yAxis0);

const yAxis1 = new NumericAxis(wasmContext, {

axisTitle: "Y Axis 1",

axisAlignment: EAxisAlignment.Left

});

sciChartSurface.yAxes.add(yAxis1);

const yAxis2 = new NumericAxis(wasmContext, {

axisTitle: "Y Axis 2",

axisAlignment: EAxisAlignment.Left

});

sciChartSurface.yAxes.add(yAxis2);

const yAxis3 = new NumericAxis(wasmContext, {

axisTitle: "Y Axis 3",

axisAlignment: EAxisAlignment.Left

});

sciChartSurface.yAxes.add(yAxis3);

const yAxis4 = new NumericAxis(wasmContext, {

axisTitle: "Y Axis 4",

axisAlignment: EAxisAlignment.Left

});

sciChartSurface.yAxes.add(yAxis4);

const yAxis5 = new NumericAxis(wasmContext, {

axisTitle: "Y Axis 5",

axisAlignment: EAxisAlignment.Left

});

sciChartSurface.yAxes.add(yAxis5);

const yAxis6 = new NumericAxis(wasmContext, {

axisTitle: "Y Axis 6",

axisAlignment: EAxisAlignment.Left

});

sciChartSurface.yAxes.add(yAxis6);

const yAxis7 = new NumericAxis(wasmContext, {

axisTitle: "Y Axis 7",

axisAlignment: EAxisAlignment.Left

});

sciChartSurface.yAxes.add(yAxis7);

// To make it clearer what's happening, colour the axis backgrounds & borders

const axisColors = ["#50C7E0", "#EC0F6C", "#30BC9A", "#F48420", "#364BA0", "#882B91", "#67BDAF", "#C52E60"];

sciChartSurface.yAxes.asArray().forEach((yAxis, index) => {

yAxis.backgroundColor = axisColors[index] + "22";

yAxis.axisBorder = { color: axisColors[index], borderRight: 1 };

yAxis.axisTitleStyle.fontSize = 13;

});

// Let's add some series to the chart to show how they also behave with axis

const getOptions = index => {

const xValues = Array.from(Array(50).keys());

const yValues = xValues.map(x => Math.sin(x * 0.4 + index));

return {

yAxisId: sciChartSurface.yAxes.asArray()[index].id,

stroke: axisColors[index] + "77",

strokeThickness: 2,

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues })

};

};

sciChartSurface.renderableSeries.add(new FastLineRenderableSeries(wasmContext, { ...getOptions(0) }));

sciChartSurface.renderableSeries.add(new FastLineRenderableSeries(wasmContext, { ...getOptions(1) }));

sciChartSurface.renderableSeries.add(new FastLineRenderableSeries(wasmContext, { ...getOptions(2) }));

sciChartSurface.renderableSeries.add(new FastLineRenderableSeries(wasmContext, { ...getOptions(3) }));

sciChartSurface.renderableSeries.add(new FastLineRenderableSeries(wasmContext, { ...getOptions(4) }));

sciChartSurface.renderableSeries.add(new FastLineRenderableSeries(wasmContext, { ...getOptions(5) }));

sciChartSurface.renderableSeries.add(new FastLineRenderableSeries(wasmContext, { ...getOptions(6) }));

sciChartSurface.renderableSeries.add(new FastLineRenderableSeries(wasmContext, { ...getOptions(7) }));

`const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {`

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: {

type: EAxisType.NumericAxis,

options: {

axisTitle: "X Axis",

axisTitleStyle: { fontSize: 13 },

backgroundColor: "#50C7E022",

axisBorder: { color: "#50C7E0", borderTop: 1 }

}

},

yAxes: [

{

type: EAxisType.NumericAxis,

options: { axisTitle: "Y Axis 0", axisAlignment: EAxisAlignment.Left }

},

{

type: EAxisType.NumericAxis,

options: { axisTitle: "Y Axis 1", axisAlignment: EAxisAlignment.Left }

},

{

type: EAxisType.NumericAxis,

options: { axisTitle: "Y Axis 2", axisAlignment: EAxisAlignment.Left }

},

{

type: EAxisType.NumericAxis,

options: { axisTitle: "Y Axis 3", axisAlignment: EAxisAlignment.Left }

},

{

type: EAxisType.NumericAxis,

options: { axisTitle: "Y Axis 4", axisAlignment: EAxisAlignment.Left }

},

{

type: EAxisType.NumericAxis,

options: { axisTitle: "Y Axis 5", axisAlignment: EAxisAlignment.Left }

},

{

type: EAxisType.NumericAxis,

options: { axisTitle: "Y Axis 6", axisAlignment: EAxisAlignment.Left }

},

{

type: EAxisType.NumericAxis,

options: { axisTitle: "Y Axis 7", axisAlignment: EAxisAlignment.Left }

}

]

});

const axisColors = ["#50C7E0", "#EC0F6C", "#30BC9A", "#F48420", "#364BA0", "#882B91", "#67BDAF", "#C52E60"];

sciChartSurface.yAxes.asArray().forEach((yAxis, index) => {

yAxis.backgroundColor = axisColors[index] + "22";

yAxis.axisBorder = { color: axisColors[index], borderRight: 1 };

yAxis.axisTitleStyle.fontSize = 13;

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

`sciChartSurface.layoutManager.leftOuterAxesLayoutStrategy =`

new LeftAlignedOuterVerticallyStackedAxisLayoutStrategy();

Now the layout is completely changed.

Make sure to assign Layout Strategy to an appropriate property on the Layout Manager accordingly to Axis Alignment.

## Experimenting with different Layout Strategies

The following vertically stacked layout strategies are available and may be applied to the following properties on SciChartSurface.LayoutManager📘:

| Layout Strategy | Use With | Apply to LayoutManager Prop | Behavior |
|---|---|---|---|
| LeftAlignedOuterAxisLayoutStrategy📘 | Y Axis | leftInnerAxisLayoutStrategy📘, leftOuterAxisLayoutStrategy📘 | Default behavior |
| RightAlignedOuterAxisLayoutStrategy📘 | Y Axis | rightInnerAxisLayoutStrategy📘, rightOuterAxisLayoutStrategy📘 | Default behavior |
| LeftAlignedOuterVerticallyStackedAxisLayoutStrategy📘 | Y Axis | rightOuterAxisLayoutStrategy📘 | Vertical stacking behavior |
| RightAlignedOuterVerticallyStackedAxisLayoutStrategy📘 | Y Axis | leftOuterAxisLayoutStrategy📘 | Vertical stacking behavior |

Try experimenting with the Codepen above to see how each of the strategies behave.
Note that a **RightLayoutStrategy** will require Axis.axisAlignment📘 = EAxisAlignment.Right📘 and vice versa.

## Customising Axis Size when Vertically Stacked

The Axis.stackedAxisLength📘 property allows you to customize the size of a Vertically Stacked Axis in SciChart.js. This property may be an absolute number, e.g. 50 pixels, or a percentage e.g. "30%". When left undefined, default equal spacing will be used.

Find an updated example below:

- TS

`sciChartSurface.layoutManager.leftOuterAxesLayoutStrategy =`

new LeftAlignedOuterVerticallyStackedAxisLayoutStrategy();

// ...

// Create several YAxis on the left using stackedAxisLength

const yAxis0 = new NumericAxis(wasmContext, {

axisAlignment: EAxisAlignment.Left,

axisTitle: "50% Size",

stackedAxisLength: "50%" // Occupy 50% of available viewport size

});

sciChartSurface.yAxes.add(yAxis0);

const yAxis1 = new NumericAxis(wasmContext, {

axisAlignment: EAxisAlignment.Left,

axisTitle: "Default"

});

sciChartSurface.yAxes.add(yAxis1);

const yAxis2 = new NumericAxis(wasmContext, {

axisAlignment: EAxisAlignment.Left,

axisTitle: "Default"

});

sciChartSurface.yAxes.add(yAxis2);

const yAxis3 = new NumericAxis(wasmContext, {

axisAlignment: EAxisAlignment.Left,

axisTitle: "200 pixels",

stackedAxisLength: 200 // Occupy exactly 200 pixels

});

sciChartSurface.yAxes.add(yAxis3);

The layout and sizes of the Vertically Stacked Axis now updates as follows:

See Also