---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/donut-chart-type
scraped_at: 2025-11-28T18:24:25.520857
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/donut-chart-type

# The Donut Chart Type

In SciChart.js, the JavaScript Donut Chart type is represented by the SciChartPieSurface📘 type.

The JavaScript Donut Chart Example can be found in the SciChart.Js Examples Suite > Pie Chart on Github, or our live demo at scichart.com/demo.

The Donut Chart represents data in a form of circle divided into segments called PieSegments. A PieSegment📘 represents a percentage that corresponds to a particular value. This value appears drawn on every segment and can be set in code. A PieSegment📘 can be selected by clicking either on it or on the corresponding item in the Legend. This action provides a visual feedback on the chart and the Legend.

## Create a Donut Chart

To create a Donut Chart, you have to create a number of PieSegment📘 instances and add them to the SciChartPieSurface.pieSegments📘 collection. Set the property sciChartPieSurface.pieType = EPieType.Donut📘 to enable a donut chart. Then the property sciChartPieSurface.holeRadius📘 is obeyed to create the donut.

Each PieSegment📘 has properties for value📘, text📘 and color📘, or alternatively colorLinearGradient📘 if you wish to specify a gradient fill. The property isSelected📘 denotes whether the PieSegment📘 is in the selected state or not.

- TS
- Builder API (JSON Config)

`// Demonstrates how to create a pie chart with SciChart.js`

const {

SciChartPieSurface,

EPieType,

SciChartJsNavyTheme,

PieSegment,

ELegendPlacement,

ELegendOrientation,

GradientParams,

Point

} = SciChart;

// or, for npm, import { SciChartPieSurface, ... } from "scichart"

// Create the Donut chart

// Note: Code is the same as a pie chart, but we specify pieType and holeRadius

const sciChartPieSurface = await SciChartPieSurface.create(divElementId, {

theme: new SciChartJsNavyTheme(),

pieType: EPieType.Donut,

holeRadius: 0.6,

animate: true

});

// Additional legend options

sciChartPieSurface.legend.showLegend = true;

sciChartPieSurface.legend.showCheckboxes = true;

sciChartPieSurface.legend.animate = true;

sciChartPieSurface.legend.placement = ELegendPlacement.TopRight;

sciChartPieSurface.legend.orientation = ELegendOrientation.Vertical;

// Create pie segments with value, colour and text

const pieSegment1 = new PieSegment({

color: "#228B22",

value: 40,

text: "Green",

colorLinearGradient: new GradientParams(new Point(0, 0), new Point(0, 1), [

{ color: "#1D976C", offset: 0 },

{ color: "#93F9B9", offset: 1 }

])

});

const pieSegment2 = new PieSegment({

value: 10,

text: "Red",

colorLinearGradient: new GradientParams(new Point(0, 0), new Point(0, 1), [

{ color: "#DD5E89", offset: 0 },

{ color: "#F7BB97", offset: 1 }

])

});

const pieSegment3 = new PieSegment({

value: 20,

text: "Blue",

colorLinearGradient: new GradientParams(new Point(0, 0), new Point(0, 1), [

{ color: "#1FA2FF", offset: 0 },

{ color: "#12D8FA", offset: 0.5 },

{ color: "#A6FFCB", offset: 1 }

])

});

const pieSegment4 = new PieSegment({

value: 15,

text: "Yellow",

colorLinearGradient: new GradientParams(new Point(0, 0), new Point(0, 1), [

{ color: "#F09819", offset: 0 },

{ color: "#EDDE5D", offset: 1 }

])

});

sciChartPieSurface.pieSegments.add(pieSegment1, pieSegment2, pieSegment3, pieSegment4);

`// Demonstrates how to create a pie chart with SciChart.js using the Builder API`

const { chartBuilder, ESciChartSurfaceType, EPieType, EThemeProviderType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const sciChartDonutChart = await chartBuilder.buildChart(divElementId, {

type: ESciChartSurfaceType.Pie2D,

options: {

surface: {

theme: { type: EThemeProviderType.Dark },

holeRadius: 0.6,

pieType: EPieType.Donut

},

segments: [

{ text: "This", value: 10, color: "red", labelStyle: { color: "white " } },

{ text: "That", value: 5, color: "blue", labelStyle: { color: "white " } },

{ text: "Other", value: 7, color: "green", labelStyle: { color: "white " } }

]

}

});

// Alternative API

const donutChart = await chartBuilder.buildPieChart(divElementId, {

surface: {

theme: { type: EThemeProviderType.Dark },

pieType: EPieType.Donut,

holeRadius: 0.6

},

segments: [

{ text: "This", value: 10, color: "red", labelStyle: { color: "white " } },

{ text: "That", value: 5, color: "blue", labelStyle: { color: "white " } },

{ text: "Other", value: 7, color: "green", labelStyle: { color: "white " } }

]

});

This results in the following output:

## Styling Donut Chart Segments & Formatting Labels

Detailed documentation on how to style pie / donut chart segments and format labels can be found at the Pie Chart Documentation page.