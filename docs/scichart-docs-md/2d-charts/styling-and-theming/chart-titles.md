---
source: https://www.scichart.com/documentation/js/v4/2d-charts/styling-and-theming/chart-titles
scraped_at: 2025-11-28T18:24:49.233016
---

# https://www.scichart.com/documentation/js/v4/2d-charts/styling-and-theming/chart-titles

# Chart Styling - Chart Titles

New to SciChart.js v3.1, we've added a Chart Title property allowing for multi-line titles on the top, left, right, bottom of the chart and with various alignment options.

Adding a chart title is simple, you can do so with the following code:

- TS
- Builder API (JSON Config)

`// Demonstrates how to configure chart titles SciChart.js`

const {

SciChartSurface,

NumericAxis,

SciChartJSLightTheme,

Thickness,

EMultiLineAlignment,

ETextAlignment,

ETitlePosition

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJSLightTheme(),

title: "SciChart.js Chart Title",

titleStyle: {

color: "#333333",

fontSize: 32,

padding: Thickness.fromString("14 8 4 8"), // Top, Right, Bottom, Left padding

useNativeText: false, // Use WebGL accelerated text

placeWithinChart: false, // When true, place inside chart, else outside

multilineAlignment: EMultiLineAlignment.Left, // When \n present how does multiline text align (Left, Center, Right)

alignment: ETextAlignment.Center, // Alignment of title (Left, Center, Right)

position: ETitlePosition.Top // Vertical position of title (Top, Bottom, Left, Right)

}

});

// Create an X and Y Axis with title

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

`// Demonstrates how to configure chart titles in SciChart.js using the Builder API`

const {

chartBuilder,

EThemeProviderType,

EAxisType,

Thickness,

EMultiLineAlignment,

ETextAlignment,

ETitlePosition

} = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: {

theme: { type: EThemeProviderType.Dark },

title: "SciChart.js Chart Title",

titleStyle: {

color: "#50C7E0",

fontSize: 24,

padding: Thickness.fromString("14 0 4 0"),

useNativeText: true,

placeWithinChart: false,

multilineAlignment: EMultiLineAlignment.Center,

alignment: ETextAlignment.Center,

position: ETitlePosition.Top

}

},

xAxes: {

type: EAxisType.NumericAxis,

options: { axisTitle: "X Axis" }

},

yAxes: {

type: EAxisType.NumericAxis,

options: { axisTitle: "Y Axis" }

}

});

This results in the following output:

For an example of multiline chart titles see the Chart Title demo in our examples suite.

## Title Styling and Positioning

For styling and positioning a title we can use I2DSurfaceOptions.titleStyle📘 property in constructor options or a surface property SciChartSurface.titleStyle📘. Available styling options are defined by **TChartTitleStyle📘** type.

When setting via a surface instance, titleStyle should be assigned to an object (or partial object) of type instead of directly setting individual properties. The object then will be merged with the current or default title style.

### Text Styling

Base text styling options for a chart title are:

**fontSize****fontFamily****color**

`// Text Styling`

sciChartSurface.titleStyle = {

fontSize: 30,

fontFamily: "Arial",

color: "#EC0F6C",

fontWeight: "900",

fontStyle: "italic",

}

Additionally we can set **fontWeight** and **fontStyle** for non-native text title. Find out more info about limitations in the **Native Text section** of the docs below.

### Title Positioning

A title could be placed on different sides relative to the surface. The options are defined by **ETitlePosition📘** enum and are set by **TChartTitleStyle.position**.

To specify an anchor for a title using **TChartTitleStyle.alignment**, where options are defined in ETextAlignment enum.

Also it is possible to place a title within the series view area using **TChartTitleStyle.placeWithinChart** flag.

`// Title Positioning`

const {

// ...

ETitlePosition,

ETextAlignment,

} = SciChart;

// or import { ETitlePosition, ETextAlignment } from "scichart";

sciChartSurface.titleStyle = {

position: ETitlePosition.Left,

alignment: ETextAlignment.Right,

placeWithinChart: true,

};

## Multiline Chart Titles

To set multiline text as a title we can pass it as an array of lines or split lines with the new line character (\n).

Properties that could be applied to the multiline text are

**TChartTitleStyle.multilineAlignment****TChartTitleStyle.lineSpacing**

The multilineAlignment options are described in EMultiLineAlignment📘 enum. The lineSpacing is a multiple of the line height.

`// Multiline Chart Titles`

const { EMultiLineAlignment } = SciChart;

// Add multiline chart title

sciChartSurface.title = \["First line", "Second line", "Third line"\]; // "Or 'FirstLine \\n Second line'

// Modify multiline text related options for the title

sciChartSurface.titleStyle = {

multilineAlignment: EMultiLineAlignment.Right,

lineSpacing: 1.5

}

## WebGL Native Text Titles

It is possible to enable the Native Text Rendering for the Chart Title. This can improve the rendering performance and allows using custom fonts, but have some differences and limitations compared to the non-native text rendering (e.g. native text doesn't support fontWeight and fontStyle). Find more info about the Native Text API here.

The Native Text Rendering for a chart title is set by **TChartTitleStyle.useNativeText** flag or uses the default value defined in SciChartDefaults.useNativeText📘.

## Title Rendering Customisation

For an advanced customization of the chart title rendering one may use a custom Chart Title Renderer.

The Chart Title renderer could be accessed or set with SciChartSurface.chartTitleRenderer📘 property.

The default Chart Title Renderer additionally provides a debug rendering and caching of non-native text which could be toggled with ChartTitleRenderer.drawDebug📘 and **ChartTitleRenderer.useCache📘** flags appropriately.