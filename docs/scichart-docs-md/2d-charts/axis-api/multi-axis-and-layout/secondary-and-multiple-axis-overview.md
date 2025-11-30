---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/multi-axis-and-layout/secondary-and-multiple-axis-overview
scraped_at: 2025-11-28T18:24:10.920301
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/multi-axis-and-layout/secondary-and-multiple-axis-overview

# Secondary and Multiple Axes

SciChart.js supports **unlimited, multiple X or Y axis** which can be aligned to the Right, Left, Top, Bottom sides of a chart.

## How to Setup a Chart with Multiple Axes

- Axis may be placed by setting the AxisBase2D.axisAlignment📘 property.
- Axis.Id📘 identifies an axis in multi-axis scenarios
- Series, Annotations and some Modifiers have
**yAxisId**,**yAxisId**properties. These are used to assign chart items to an axis in multi-axis scenarios.

When you create an axis it automatically gets a unique id, which you can use to assign to Series, Annotations and some Modifiers.

- TS

`renderableSeries.xAxisId = xAxis.id;`

renderableSeries.yAxisId = yAxis.id;

...

annotation.xAxisId = xAxis.id;

annotation.yAxisId = yAxis.id;

There's little more to it than that. However, there are many configurations in SciChart.js which we will get into later.

Here's a worked example:

- TS
- Builder API (JSON Config)

`const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {`

theme: new SciChartJsNavyTheme()

});

// Add a primary X,Y Axis pair

sciChartSurface.xAxes.add(

new NumericAxis(wasmContext, {

axisAlignment: EAxisAlignment.Bottom,

axisTitle: "X Axis Bottom",

axisTitleStyle: titleStyle1,

labelStyle: labelStyle1,

backgroundColor: "#50C7E022",

axisBorder: {

borderTop: 1,

color: "#50C7E0"

}

})

);

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

axisAlignment: EAxisAlignment.Left,

axisTitle: "Y Axis Left",

axisTitleStyle: titleStyle1,

labelStyle: labelStyle1,

growBy: new NumberRange(0.1, 0.1),

backgroundColor: "#50C7E022",

axisBorder: {

borderRight: 1,

color: "#50C7E0"

}

})

);

// Add a secondary X,Y Axis pair

// Capture the axis instance as you may need it's Id which is auto generated

const xAxis2 = new NumericAxis(wasmContext, {

axisTitleStyle: titleStyle2,

labelStyle: labelStyle2,

axisAlignment: EAxisAlignment.Top,

axisTitle: "X Axis Top",

backgroundColor: "#F4842022",

axisBorder: {

borderBottom: 1,

color: "#F48420"

}

});

sciChartSurface.xAxes.add(xAxis2);

const yAxis2 = new NumericAxis(wasmContext, {

axisTitleStyle: titleStyle2,

labelStyle: labelStyle2,

axisAlignment: EAxisAlignment.Right,

axisTitle: "Y Axis Right",

labelFormat: ENumericFormat.Decimal,

labelPrecision: 2,

growBy: new NumberRange(0.1, 0.1),

backgroundColor: "#F4842022",

axisBorder: {

borderLeft: 1,

color: "#F48420"

}

});

sciChartSurface.yAxes.add(yAxis2);

`const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {`

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: [

{

type: EAxisType.NumericAxis,

options: {

axisAlignment: EAxisAlignment.Bottom,

axisTitle: "X Axis Bottom",

axisTitleStyle: titleStyle1,

labelStyle: labelStyle1,

backgroundColor: "#50C7E022",

axisBorder: {

borderTop: 1,

color: "#50C7E0"

}

}

},

{

type: EAxisType.NumericAxis,

options: {

axisTitleStyle: titleStyle2,

labelStyle: labelStyle2,

axisAlignment: EAxisAlignment.Top,

axisTitle: "X Axis Top",

backgroundColor: "#F4842022",

axisBorder: {

borderBottom: 1,

color: "#F48420"

}

}

}

],

yAxes: [

{

type: EAxisType.NumericAxis,

options: {

axisAlignment: EAxisAlignment.Left,

axisTitle: "Y Axis Left",

axisTitleStyle: titleStyle1,

labelStyle: labelStyle1,

growBy: new NumberRange(0.1, 0.1),

backgroundColor: "#50C7E022",

axisBorder: {

borderRight: 1,

color: "#50C7E0"

}

}

},

{

type: EAxisType.NumericAxis,

options: {

axisTitleStyle: titleStyle2,

labelStyle: labelStyle2,

axisAlignment: EAxisAlignment.Right,

axisTitle: "Y Axis Right",

labelFormat: ENumericFormat.Decimal,

labelPrecision: 2,

growBy: new NumberRange(0.1, 0.1),

backgroundColor: "#F4842022",

axisBorder: {

borderLeft: 1,

color: "#F48420"

}

}

}

]

});

This code results in the following configuration of axis. Also seen in our Multiple Axis Demo.

## Attaching Chart Series to an Axis

Every RenderableSeries (the chart types in SciChart.js e.g. Line, Candlestick, Column) and every Annotation (Trendlines, text or markers laid over the chart) and some ChartModifiers (zoom, pan behaviours) need to be attached to a particular axis.

The link between series and axis is done via AxisCore.id📘, and BaseRenderableSeries.xAxisId📘 and BaseRenderableSeries.yAxisId📘 properties.

With a single X,Y Axis you never have to set these properties as they gets set automatically. When a series, annotation or modifier gets attached to SciChartSurface, xAxis.id and yAxis.id get values from the first X and Y axes.

However, in a multiple axis scenario, series must be attached to an axis. To do this, ensure that you set the BaseRenderableSeries.xAxisId📘 and BaseRenderableSeries.yAxisId📘 equal to the YAxis.id📘 or XAxis.id📘 you wish to attach to.