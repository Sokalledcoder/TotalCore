---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/polar-partial-chart-type
scraped_at: 2025-11-28T18:24:40.731721
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/polar-partial-chart-type

# The Partial Polar Chart Type

The JavaScript Partial Polar Chart Example can be found in the SciChart.Js Examples Suite > Polar Partial Arc on Github, or our live demo at scichart.com/demo.

This demo shows how a Polar plot can be used to look similar to a Cartesian plot, by setting innerRadius📘: to `0.998`

(from the default of `0`

) and totalAngle📘: to `0.001 * Math.PI`

radians (from the default of 2 * Math.PI), so that it only displays a very small section of the total circle / polar system, which auto-ranges and zooms to fit in the parent div.

The gridlines are never actually parallel, but the radius of the imaginary circle it's drawn on is so large when setting these 2 properties this way, that it looks like a Cartesian plot.

## What is a Partial Polar Chart?

The Partial Polar Chart is just a regular polar chart, but with the totalAngle📘 property of the **Angular** axis set to a value less than `2 * Math.PI`

(or `360`

degrees). This allows you to create a chart that only displays a portion of the polar coordinate system, which can be useful for visualizing data that is only relevant within a specific angular range.

The example above is extreme, but partial polar charts refers to all plots that span across an angle that is less than `360`

degrees (or `2 * Math.PI`

radians).

## Other examples of Partial Polar Charts:

### 1. Gauge Charts

Many Gauge charts have sweeping arcs in between

`180`

and`270`

degrees. Check this out for more info: Gauge Chart Documentation

### 2. Polar Column / Line / Mountain series

They might also not need the full

`360`

degrees, but rather a partial arc

### 3. Polar Uniform Heatmap Chart

A polar uniform heatmap chart can also be created by setting the totalAngle📘 property of the

Angularaxis to a value less than`2 * Math.PI`

(or`360`

degrees).

For more information about polar chart layout, styling and axes, check out these documentation pages: