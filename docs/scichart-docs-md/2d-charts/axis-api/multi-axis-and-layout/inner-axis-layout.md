---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/multi-axis-and-layout/inner-axis-layout
scraped_at: 2025-11-28T18:24:11.336600
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/multi-axis-and-layout/inner-axis-layout

# Inner Axis Layout

SciChart allows you to customize how axes are placed around and within the surface. Axes can be placed:

**Outside the drawing area,**called Outer Axes. This is the default. The drawing area is reduced to give space for the axes and their labels and titles.**Inside the drawing area**, called Inner Axes. The drawing area fills the entire space of the chart.

Inner axes can either be around the edges of the area, or bound to a coordinate so they appear in the middle of the drawing area. These are referred to as **Central Axes**.

## Inner Axes

To create an Inner axis simply set isInnerAxis: true📘 on the axis options:

- TS
- Builder API (JSON Config)

`// Configure an axis to display inside the chart`

const xAxis = new NumericAxis(wasmContext, {

isInnerAxis: true,

axisTitle: "Inner axis",

// To allow easier visualisation of axis position

backgroundColor: "#50C7E022"

});

// Add the xAxis to the chart

sciChartSurface.xAxes.add(xAxis);

`// Demonstrates how to configure an inner axis in SciChart.js using the Builder API`

const { chartBuilder, EThemeProviderType, EAxisType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: {

type: EAxisType.NumericAxis,

options: {

isInnerAxis: true,

axisTitle: "Inner axis",

// To allow easier visualisation of axis position

backgroundColor: "#50C7E022"

}

},

yAxes: {

type: EAxisType.NumericAxis,

options: {

axisTitle: "Outer axis",

// To allow easier visualisation of axis position

backgroundColor: "#F4842022"

}

}

});

Now the x axis is an inner axis, while the y axis is the default outer axis.

## DrawSeriesBehindAxis property

SciChart.js also allows you to draw all chart series behind axis by setting a single flag on the parent SciChartSurface.

The default behaviour is to draw axis on the outside of the chart area. If you need more space on the chart (if axis are taking up too much space), you can set a single flag to draw the series behind the axis and pull the axis areas inside the chart area:

- TS

`sciChartSurface.drawSeriesBehindAxis = true;`

This results in the following output.