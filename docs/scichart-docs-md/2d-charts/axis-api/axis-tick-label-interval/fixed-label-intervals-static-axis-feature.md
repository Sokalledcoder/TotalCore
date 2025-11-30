---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-tick-label-interval/fixed-label-intervals-static-axis-feature
scraped_at: 2025-11-28T18:24:07.564358
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-tick-label-interval/fixed-label-intervals-static-axis-feature

# Fixed Label Intervals - Static Axis Feature

Sometimes you want to have a fixed number of labels and major gridlines displayed on a chart, at specific values.

Consider the case where you have a chart with xAxis.visibleRange📘 from 0 to 10, and you want to display labels precisely at 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10. Zooming and panning should not change the number or spacing of the labels. In this case, you can set the axis.isStaticAxis📘 property.

When in this mode, the major gridline positions / label positions and spacing are fixed. If the axis.visibleRange📘 changes then the label values update, not the position or spacing.

## Enabling Static Axis

To enable the static axis mode, use the following code:

- TS
- Builder API (JSON Config)

`// Demonstrates how to configure a chart with Static Axis in SciChart.js`

const { SciChartSurface, NumericAxis, SciChartJsNavyTheme, NumberRange } = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

// Adjust major/minor gridline style to make it clearer for the demo

const styleOptions = {

majorGridLineStyle: { color: "#50C7E077" },

minorGridLineStyle: { color: "#50C7E033" }

};

const xAxis = new NumericAxis(wasmContext, {

axisTitle: "isStaticAxis = true, maxAutoTicks = 10",

isStaticAxis: true,

maxAutoTicks: 10,

...styleOptions

});

const yAxis = new NumericAxis(wasmContext, {

axisTitle: "yAxis.isStaticAxis = false",

growBy: new NumberRange(0.1, 0.1),

...styleOptions

});

sciChartSurface.xAxes.add(xAxis);

sciChartSurface.yAxes.add(yAxis);

`// Demonstrates how to configure a chart with Static Axis in SciChart.js`

const { chartBuilder, EThemeProviderType, EAxisType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: {

type: EAxisType.NumericAxis,

options: {

axisTitle: "isStaticAxis = true, maxAutoTicks = 5",

isStaticAxis: true,

maxAutoTicks: 5

}

},

yAxes: {

type: EAxisType.NumericAxis,

options: {

axisTitle: "yAxis.isStaticAxis = false"

}

}

});

This results in the following output

## Varying the number of Static Axis Ticks & Labels

When axis.isStaticAxis📘 is set to true, the number of major ticks (major gridlines, axis labels) are constrained by axis.maxAutoTicks📘.

For example setting axis.maxAutoTicks📘 = 5 will ensure there are always 5 labels and 5 major gridlines on the chart. These wil be at fixed spacings no matter the zoom level of the chart. Label values will update instead.

## Formatting Labels and Precision (Decimal Places)

When in static axis mode, the axis stil obeys formatting rules provided by the LabelProvider. Read the NumericAxis Docs or the LabelProvider API Docs for more info on how to vary label precision.