---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/ranging-scaling/auto-range
scraped_at: 2025-11-28T18:24:11.935937
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/ranging-scaling/auto-range

# Axis Ranging - AutoRange

At the outset, the Axis.visibleRange📘 is adjusted to be equal to the data range of an axis. However, an axis won't adjust its VisibleRange automatically when data changes, unless it is configured to do this. The default behavior can be changed using different AutoRange📘 modes.

## AutoRange Once

This is the **default setting**. The axis will attempt to autorange once to fit the data as you start the chart. This is an one-time action - the VisibleRange won't adjust to any data changes in future.

Note: Specifying axis.visibleRange📘 at startup will set that as the first default range. AutoRange.Once is ignored when a visibleRange is set

- TS
- Builder API (JSON Config)

`const { SciChartSurface, NumericAxis, SciChartJsNavyTheme, EAutoRange } = SciChart;`

// or, for npm, import { SciChartSurface, ... } from "scichart"

// Create a chart with X,Y axis

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

// Set AutoRange on the yAxis

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

autoRange: EAutoRange.Once

})

);

`const { chartBuilder, ESeriesType, EThemeProviderType, EAutoRange, EAxisType } = SciChart;`

// or, for npm, import { chartBuilder, ... } from "scichart"

const xValues = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19];

const yValues = xValues.map(x => Math.sin(x * 0.2));

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: {

type: EAxisType.NumericAxis,

options: { axisTitle: "X Axis" }

},

yAxes: {

type: EAxisType.NumericAxis,

options: { axisTitle: "Y Axis", autoRange: EAutoRange.Once }

},

series: [

{

type: ESeriesType.LineSeries,

xyData: {

xValues,

yValues

},

options: {

stroke: "#50C7E0",

strokeThickness: 3

}

}

]

});

## AutoRange Always

In this mode, the axis will attempt to autorange always to fit the data every time the chart is drawn. The **VisibleRange** **will adjust** to data changes correspondingly.

Please be aware that this **setting will override any other ranging**, including zooming and panning by modifiers, but is useful in situations where you always want to view the extents of the data.

To combine AutoRanging and user-zooming you need to use **ZoomState** - a special technique we will talk about later.

- TS
- Builder API (JSON Config)

`const { SciChartSurface, NumericAxis, SciChartJsNavyTheme, EAutoRange } = SciChart;`

// or, for npm, import { SciChartSurface, ... } from "scichart"

// Create a chart with X,Y axis

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

// Set AutoRange on the yAxis

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

autoRange: EAutoRange.Always

})

);

`const { chartBuilder, ESeriesType, EThemeProviderType, EAutoRange, EAxisType } = SciChart;`

// or, for npm, import { chartBuilder, ... } from "scichart"

const xValues = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19];

const yValues = xValues.map(x => Math.sin(x * 0.2));

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: {

type: EAxisType.NumericAxis,

options: { axisTitle: "X Axis" }

},

yAxes: {

type: EAxisType.NumericAxis,

options: {

axisTitle: "Y Axis",

autoRange: EAutoRange.Always

}

},

series: [

{

type: ESeriesType.LineSeries,

xyData: {

xValues,

yValues

},

options: {

stroke: "#50C7E0",

strokeThickness: 3

}

}

]

});

## AutoRange Never

The **axis will never autorange**. With this option, you would need to set the VisibleRange manually. The **VisibleRange** **won't adjust** to any data changes.

- TS
- Builder API (JSON Config)

`const { SciChartSurface, NumericAxis, SciChartJsNavyTheme, EAutoRange } = SciChart;`

// or, for npm, import { SciChartSurface, ... } from "scichart"

// Create a chart with X,Y axis

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

// Set AutoRange on the yAxis

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

autoRange: EAutoRange.Never

})

);

`const { chartBuilder, ESeriesType, EThemeProviderType, EAutoRange, EAxisType } = SciChart;`

// or, for npm, import { chartBuilder, ... } from "scichart"

const xValues = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19];

const yValues = xValues.map(x => Math.sin(x * 0.2));

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: {

type: EAxisType.NumericAxis,

options: { axisTitle: "X Axis" }

},

yAxes: {

type: EAxisType.NumericAxis,

options: { axisTitle: "Y Axis", autoRange: EAutoRange.Never }

},

series: [

{

type: ESeriesType.LineSeries,

xyData: {

xValues,

yValues

},

options: {

stroke: "#50C7E0",

strokeThickness: 3

}

}

]

});

## Adding Padding or Spacing with GrowBy

Also, it is possible to **add spacing** or padding to the visibleRange when the chart autoranges via the GrowBy📘 property. It allows to specify two fractions which will be always applied to the Min, Max values of visibleRange :

- TS
- Builder API (JSON Config)

`const { SciChartSurface, NumericAxis, SciChartJsNavyTheme, EAutoRange, NumberRange } = SciChart;`

// or, for npm, import { SciChartSurface, ... } from "scichart"

// Create a chart with X,Y axis

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

// Set GrowBy on the yAxis to add 20% padding above/below

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

autoRange: EAutoRange.Always,

growBy: new NumberRange(0.2, 0.2)

})

);

`const { chartBuilder, ESeriesType, EThemeProviderType, EAutoRange, EAxisType, NumberRange } = SciChart;`

// or, for npm, import { chartBuilder, ... } from "scichart"

const xValues = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19];

const yValues = xValues.map(x => Math.sin(x * 0.2));

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: {

type: EAxisType.NumericAxis,

options: { axisTitle: "X Axis" }

},

yAxes: {

type: EAxisType.NumericAxis,

options: {

axisTitle: "Y Axis",

autoRange: EAutoRange.Always,

growBy: new NumberRange(0.2, 0.2)

}

},

series: [

{

type: ESeriesType.LineSeries,

xyData: {

xValues,

yValues

},

options: {

stroke: "#50C7E0",

strokeThickness: 3

}

}

]

});

## Programmatically Ranging an Axis

See the section on Setting and Getting VisibleRange for more details.