---
source: https://www.scichart.com/documentation/js/v4/2d-charts/builder-api/pie-chart
scraped_at: 2025-11-28T18:24:13.274246
---

# https://www.scichart.com/documentation/js/v4/2d-charts/builder-api/pie-chart

# Creating a Pie Chart

SciChart provides a powerful API for creating various types of charts, including **Pie Charts**.

The buildChart📘 function can be used to build both 2D Charts, **Pie Charts**, 2D Polar Charts & 3D Charts, so the returned object type will differ depending on the chart type.

## Using buildChart📘 to create a Pie Chart

- TS

`const { chartBuilder, ESciChartSurfaceType } = SciChart;`

const pieSurface = chartBuilder.buildChart(divElementId, {

type: ESciChartSurfaceType.Pie2D,

options: {

segments: [

{ text: "This", value: 10, color: "red" },

{ text: "That", value: 5, color: "blue" },

{ text: "Other", value: 7, color: "green" }

]

}

});

## Using buildPieChart📘 to explicitly create a Pie Chart:

- TS

`const { chartBuilder } = SciChart;`

const pieSurface = chartBuilder.buildPieChart(divElementId, {

segments: [

{ text: "This", value: 10, color: "red" },

{ text: "That", value: 5, color: "blue" },

{ text: "Other", value: 7, color: "green" }

]

});

Both of these methods will result in this output: