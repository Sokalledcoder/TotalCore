---
source: https://www.scichart.com/documentation/js/v4/2d-charts/styling-and-theming/theme-manager-api
scraped_at: 2025-11-28T18:24:50.108602
---

# https://www.scichart.com/documentation/js/v4/2d-charts/styling-and-theming/theme-manager-api

# Chart Styling - ThemeManager API

SciChart ships with a light and dark theme out of the box, which you can select and apply to the charts in your application. Most of the components of SciChart are also stylable, and you can create your own themes, so you can truly customize the chart to fit your application.

You can view our themes live at the ThemeManager example, over at the SciChart.js Examples Suite.

## SciChart Dark Theme

SciChart had a dark theme before dark-mode was cool :) Here's our default theme, SciChart Dark, in all it's glory below.

- Applying dark theme

`import { SciChartSurface, SciChartJSDarkv2Theme } from "scichart";`

// For best results & applying to the loader animation, apply theme before chart creation

const { wasmContext, sciChartSurface } = await SciChartSurface.create("div-element-id", {

theme: new SciChartJSDarkv2Theme()

});

// You can also change the theme after creation

sciChartSurface.applyTheme(new SciChartJSDarkv2Theme());

## SciChart Light Theme

For applications with a white or lighter background color, we also ship a light theme. This is how it looks:

- Applying light Theme

`import { SciChartSurface, SciChartJSLightTheme } from "scichart";`

// For best results & applying to the loader animation, apply theme before chart creation

const { wasmContext, sciChartSurface } = await SciChartSurface.create("div-element-id", {

theme: new SciChartJSLightTheme()

});

// You can also change the theme after creation

sciChartSurface.applyTheme(new SciChartJSLightTheme());

## SciChart Navy Theme

In SciChart.js v3, we've added a new Navy theme. This looks great on both a light & dark background. This can be enabled as follows:

- Applying Navy Theme

`import { SciChartSurface, SciChartJsNavyTheme } from "scichart";`

// For best results & applying to the loader animation, apply theme before chart creation

const { wasmContext, sciChartSurface } = await SciChartSurface.create("div-element-id", {

theme: new SciChartJsNavyTheme()

});

// Changing theme after creation

sciChartSurface.applyTheme(new SciChartJsNavyTheme());