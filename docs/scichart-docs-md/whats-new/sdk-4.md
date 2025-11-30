---
source: https://www.scichart.com/documentation/js/v4/whats-new/sdk-4.0
scraped_at: 2025-11-28T18:25:08.562173
---

# https://www.scichart.com/documentation/js/v4/whats-new/sdk-4.0

# What's New in SciChart.js SDK v4.0

## SciChart.js v4.0 Release Overview

SciChart.js v4.0 is a major update introducing new chart types, enhanced modifiers, and improved customization for high-performance JavaScript and React charting applications.

## Key Highlights

-
**Polar charts:**Line, column, mountain, band, scatter, heatmap, pie, stacked series, gauges, and partial polar charts. -
**New cartesian types:**Triangle, rectangle, box plot, polygon, and line-segment charts. -
**Flexible DataSeries support:**Custom formats for advanced charting scenarios, such as box plots and multi-series sharing axes. -
**Annotation updates:**HTML text, SVG, arc segments, arrows, polar pointers, and custom annotations. -
**Modifiers and interactions:**Polar arc-zoom, cursor, pan, mousewheel zoom, zoom extents, data-point selection, and legend modifiers—plus sub-chart support combining cartesian and polar types. -
**Styling improvements:**Texture backgrounds, gradients, ordered rendering, and annotation clipping. -
**Compatibility:**Ultra high-performance React, Angular, WebGL, and JavaScript support.

## List of New Features, Demos and Docs

## Changes and Fixes

| Title | Description |
|---|---|
| Reduced SciChart.js bundle size (SCJS-1521, SCJS-1522, SCJS-1689) | Wasm file size has been optimized and scichart.data file (and scichart3d.data file) which contained various assets, has been merged into the main wasm file, shrinking the total size of the file to be loaded. Check out Deploying Wasm (WebAssembly) with your app docs |
| Emscripten update (SCJS-1702) | Emscripten has been updated to version 3.1.73 |
| Improved UpdateSuspender mechanism (SCJS-1706) | Batching updates or temporary suspending drawing mechanism has been improved. UpdateSuspender docs |
| Improved performance for 3D (SCJS-3122) | Performance for 3D has been improved by eliminating unnecessary re-rendering |
| BuilderAPI support for 3D (SCJS-1957) | Docs |
| Drawing subcharts outside of the visible range (SCJS-1697) | Allow subcharts to be drawn partially offscreen. Which make it possible to create examples like this one |
| SubCharts now support both Cartesian and Polar charts (SCJS-1654) | It is possible to combine both Polar and Cartesian charts on one surface. Check out docs |
| SubCharts layout issue with VerticalGroup (SCJS-1891) | The issue has been fixed for subcharts using both VerticalGroup and HorizontalGroup on the axes at the same time |
| Improved performance by defaulting axis labels to NativeText | SciChartDefaults.useNativeText has been changed to default to true, which means that by default, axis labels will be rendered using WebGL instead of by Canvas, unless useNativeText is set false on the axis or labelProvider. Check out NativeText API docs |
| Gridline drawing performance improvements (SCJS-1691) | Improved by using native vectors for storing tick coordinates |
| Simplified multi-axis API, by auto-generating Axis IDs (SCJS-1838) | AxisCore.DEFAULT_AXIS_ID has been removed. From now on value for AxisCore.id is an auto generated guid and there is now need to set axis IDs explicitly for a multi-axis scenarios. |
| SciChartSurface.zoomExtents() has got parameter to include selected axes (SCJS-1712) | You can use xAxisSelectorFn and yAxisSelectorFn selectors to filter out axes. Find more information here SciChartSurface.zoomExtents TypeDoc |
| Improved syncing widths of axes (SCJS-1634) | SciChartVerticalGroup and SynchronisedLayoutManager should synchronize the width of the axis viewRect as well as the total size so that axis backgrounds line up |
| XyNDataSeries to store data with multiple Y-values (SCJS-1807) | DataSeries has been refactor and XyNDataSeries has been introduced, which allows for storing data with multiple Y-values. Check out DataSeries docs |
| Gradient fill support for StackedColumnRenderableSeries | Gradient fill docs |
| zOffset property for UniformContoursRenderableSeries (SCJS-1915) | UniformContoursRenderableSeries.zOffset gives control at what Z-value the contour lines start |
| Ability to set renderable series name (SCJS-1824) | seriesName property has been added to IRenderableSeries.seriesName. This property is used in HitTestInfo.dataSeriesName and in tooltips and legends. |
| Per annotation clipping mode (SCJS-1745) | Annotations now have their own clipping property, which applies to both native and SVG annotations, allowing for more annotation types to be used over the axes. AnnotationBase.clipping TypeDoc |
| NativeTextAnnotation got background (SCJS-2094) | Now it is possible to set a background on NativeTextAnnotation. NativeTextAnnotation.background TypeDoc |
| Ability to clip Annotation Adorners to series area (SCJS-1655) | The standard behaviour is for adorners to extend, but some users need a different bahavior. Example code |
| Chart modifier’s axis and series inclusion API has been improved (SCJS-1711) | Axis and series inclusion are now standardized across modifiers. Check out TypeDocs ChartModifierBase2D.includedSeries, ChartModifierBase2D.includedXAxes, ChartModifierBase2D.includedYAxes |
| executeCondition API has been added to chart modifiers | ChartModifierBase.executeOn has been replaced by ChartModifierBase.executeCondition. This provides a general way of specifying when you want a modifier to activate based on both mouse button and ctrl/alt/shift keys. |
| Make pinch zoom enabled by default in ZoomPanModier (SCJS-1938) | ZoomPanModier docs |
| ClipPath Rect issue in Firefox (SCJS-1883) | This bug occurs when some specific conditions take place: clipPath has a single child element and clipped element has a child with position “absolute”. |
| Default delete on clear for ObverableArray to prevent memory leaks (SCJS-2062) | In ObservableArrays in remove, removeAt and clear methods default behaivior has changed to call delete on the removed item |
| cornerRadius Column Series bug has been fixed (SCJS-1301) | When FastColumnRenderableSeries.cornerRadius was set and StrokeThickness = 0, fillLinearGradient did not work |