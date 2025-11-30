---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/chart-modifier-api-overview
scraped_at: 2025-11-28T18:24:13.725337
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/chart-modifier-api-overview

# What is the ChartModifier API

Within the SciChart.js JavaScript Chart SDK, ChartModifiers are the classes which can be added to a SciChartSurface📘 to give it a **certain** **behavior**. For instance, all **zooming, panning operations**, **tooltips**, **legends** and even **selection** of points or lines are handled by ChartModifierBase📘 derived classes in the SciChart codebase.

There are many different ChartModifiers provided by SciChart and each one deserves an article by itself! This article is concerned with simply giving an overview of the modifiers and where you can find the examples in our Examples Suite which demonstrate them.

There are also several individual articles on the ChartModifiers and how to configure them in the SciChart.js Documentation. Please find them at the bottom of this page.

## Zoom, Pan Modifiers

The following modifiers can be used if you want to add scrolling or zooming behavior to a chart:

| Modifier Name | Description |
|---|---|
ZoomPanModifier | Pans the chart in X, Y or both directions with inertia via finger sliding. |
MouseWheelZoomPanModifier | Zooms the chart in or out on mouse-wheel (or two finger scroll). |
XAxisDragModifier | Scales or pans an X Axis via mouse-drag. |
YAxisDragModifier | Scales or pans a Y Axis via mouse-drag. |
RubberBandXyZoomModifier | Zooms a chart inside a rectangle or horizontal section that is drawn on the chart with a finger. |
ZoomExtentsModifier | Resets the zoom to the data extents via double-tapping. |
SciChartOverview | Creates an overview chart that allows you to zoom and pan the main chart. |

## Interactivity, Tooltips, Cursor Modifiers

These modifiers allow to interact with chart series or inspect them:

Modifier Name | Description |
|---|---|
RolloverModifier | Provides a vertical slice cursor with tooltips and markers rolling over a series. |
CursorModifier | Provides a crosshairs with a tooltip and axis labels. |

## Miscellaneous Modifiers

Modifiers below are used as helpers and can be a useful addition to a chart:

Modifier Name | Description |
|---|---|
LegendModifier | Allows creation and configuration a Legend for a chart. |

To learn more about ChartModifiers API, please read the Common ChartModifiers Features article. To find out about a specific ChartModifier type, please refer to a corresponding article about this Modifier type.

## Polar Modifiers

Below it the list of chart modifiers for Polar Charts.

Modifier Name | Description |
|---|---|
PolarArcZoomModifier | Allows zooming to a selected arc on Polar surface. |
PolarCursorModifier | Displays a tooltip for closest data point when hovering over the polar chart |
PolarDataPointSelectionModifier | Allows for data point selection for polar charts |
PolarLegendModifier | Allows creation and configuration a Legend for a Polar chart. |
PolarMouseWheelZoomModifier | Allows users to rotate or zoom in and out of a polar chart using the mouse wheel |
PolarPanModifier | Allows users to pan, rotate and zoom in/out a polar chart using the mouse |
PolarZoomExtends | Allows users to reset chart to initial state |