---
source: https://www.scichart.com/documentation/js/v4/2d-charts/surface/scichart-polar-surface-type
scraped_at: 2025-11-28T18:24:53.902798
---

# https://www.scichart.com/documentation/js/v4/2d-charts/surface/scichart-polar-surface-type

# The SciChartPolarSurface Type

The root polar chart view is called the SciChartPolarSurface📘. This is the JavaScript chart control you will be adding to your applications wherever you need a **Polar Chart**. You can add more than one SciChartPolarSurface to an HTML page and combine them with Cartesian SciChartSurface, you can configure them independently, and you can link them together.

The SciChartPolarSurface📘 extends SciChartSurface📘 and inherits the same properties and functions which allow you to configure and control the chart.

You will find information about the parent SciChartSurface class here.

Info about the properties and functions available can be found at the TypeDoc API Documentation for SciChart📘.

## Surface Type Check for Renderable Series, Annotations and Chart Modifiers

When IRenderableSeries📘 is attached to SciChartSurface📘 or to SciChartPolarSurface📘 a type check is performed, renderableSeries.isPolar📘 property should match the surface type.

When IChartModifierBase📘 is attached to the surface a type check is also performed, chartModifier.modifierType📘 property should match sciChartSurface.surfaceType📘.

For renderable series and annotations the surface type should be obvious from the name as the polar items have it in the name. For example, FastLineRenderableSeries and PolarLineRenderableSeries, CursorModifier and PolarCursorModifier.

A similar check is implemented for annotations. When IAnnotation📘 is attached to SciChartSurface📘 or to SciChartPolarSurface📘 a type check is performed, annotation.surfaceTypes📘 should contain the ESurfaceType📘. However, unlike the renderable series, the annotations can be compatible with normal surface type `ESurfaceType.SciChartSurfaceType`

, polar surface type `ESurfaceType.SciChartPolarSurfaceType`

or with both surface types at the same time.

In an annotation is only for polar surface it has "Polar" prefix. For example, PolarPointerAnnotation. If annotation has no "Polar" prefix it can be either for normal surface only or for both depending on annotation.surfaceTypes📘 property.

**These are the annotations compatible with both surface types SciChartSurface and SciChartPolarSurface**: