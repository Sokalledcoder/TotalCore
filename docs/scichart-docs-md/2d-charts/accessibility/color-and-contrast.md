---
source: https://www.scichart.com/documentation/js/v4/2d-charts/accessibility/color-and-contrast
scraped_at: 2025-11-28T18:23:58.098437
---

# https://www.scichart.com/documentation/js/v4/2d-charts/accessibility/color-and-contrast

# Color and Contrast

Since colors and theming are most likely to be custom for each customer, we don't provide out of the box light and dark theme handling (nor special theme for High Contrast).

But that's easily achievable by using one of the provided themes, or creating a custom one.

## Default Themes

By default SciChart uses **SciChartJSDarkv2Theme**. Also SciChart exposes **SciChartJSDarkTheme** and **SciChartJSLightTheme**.

In this example we will show how to set a desired theme depending on user theme settings.

`// Setting a Theme`

import { SciChartJSDarkTheme, SciChartJSLightTheme } from "scichart";

// ...

const isDarkThemeSelected = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;

const newColorScheme = isDarkThemeSelected

? new SciChartJSDarkTheme()

: new SciChartJSLightTheme();

sciChartSurface.applyTheme(newColorScheme);

The snippet above should set the light or dark theme depending on user preferences.

It's easy to handle the theme change:

- JS
- TS

`const handleSystemThemeChange = (event) => {`

const newColorScheme = event.matches

? new SciChartJSDarkTheme()

: new SciChartJSLightTheme();

sciChartSurface.applyTheme(newColorScheme)

};

window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", handleSystemThemeChange);

`const handleSystemThemeChange = (event: MediaQueryListEvent) => {`

const newColorScheme = event.matches

? new SciChartJSDarkTheme()

: new SciChartJSLightTheme();

sciChartSurface.applyTheme(newColorScheme);

};

window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", handleSystemThemeChange);

Now the chart will detect user dark/light theme preference updates and will use an appropriate theme.

## Custom Themes

Refer to Chart Styling - Creating a Custom Theme.