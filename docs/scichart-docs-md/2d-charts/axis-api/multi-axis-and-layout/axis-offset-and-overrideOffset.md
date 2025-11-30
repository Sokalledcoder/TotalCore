---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/multi-axis-and-layout/axis-offset-and-overrideOffset
scraped_at: 2025-11-28T18:24:09.896923
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/multi-axis-and-layout/axis-offset-and-overrideOffset

# Axis Offset and OverrideOffset

## Default Axis Offset

In SciChart.js, each axis has an offset parameter that defines its position along the chart layout. By default, this offset is set internally (commonly as -1 for normal axes). This default lets the layout engine manage axis positioning automatically so axes do not crowd or overlap with the chart or each other.

Regular axes use the internal offset assigned by the chart’s layout system. This ensures enough spacing for labels, ticks, gridlines, and keeps the chart visually organized.

## Why Use overrideOffset and Not offset

To manually control axis positioning, you should use overrideOffset📘 rather than trying to set offset📘 directly.

The offset property is managed by SciChart’s layout strategies (especially when you have stacked or multi-axis layouts). Overriding this manually can cause unexpected results if the internal layout logic adjusts it later.

Setting overrideOffset📘 ensures that the value you supply takes precedence, overriding whatever offset value the layout system would otherwise use.

## How overrideOffset Creates the 3D Waterfall Effect

Here is the code from the example that shows how overrideOffset📘 is used:

` for (let i = 0; i < seriesCount; i++) {`

// Create one yAxis per series

const yAxis = new NumericAxis(wasmContext, {

id: "Y" + i,

axisAlignment: EAxisAlignment.Left,

maxAutoTicks: 5,

drawMinorGridLines: false,

visibleRange: new NumberRange(-50, 60),

isVisible: i === seriesCount - 1,

overrideOffset: 3 * -i,

});

sciChartSurface.yAxes.add(yAxis);

// Create a shared, default xaxis

const xAxis = new NumericAxis(wasmContext, {

id: "X" + i,

axisAlignment: EAxisAlignment.Bottom,

maxAutoTicks: 5,

drawMinorGridLines: false,

growBy: new NumberRange(0, 0.2),

isVisible: i === seriesCount - 1,

overrideOffset: 2 * i,

});

sciChartSurface.xAxes.add(xAxis);

...

In interactive waterfall charts where several series are visually stacked in an overlapping “3D” style overrideOffset📘 is critical for achieving the desired offset between axes.

Each “layer” or “slice” in a waterfall chart typically gets its own axis with a unique overrideOffset📘. By increasing the overrideOffset📘 value for successive axes, you move each axis and corresponding series further away from the previous one, creating the illusion of depth making the chart look like a 3D waterfall.

Manual control via overrideOffset📘 allows precise tuning: you control how much each series/axis is visually offset, stacking the axes apart and making each new series appear "further back" in the chart layout.

This method is especially useful in interactive waterfall charts where multiple stacked axes and series must not overlap and each needs unique spacing for clarity and aesthetics.

The Interactive Waterfall Spectral Chart can be found in the SciChart.Js Examples Suite > Interactive Waterfall Chart Example on Github.

## Summary Table

| Property | Default Behavior | When to Use | Key Use-case |
|---|---|---|---|
| offset | Managed by layout engine (default usually -1) | Never set directly | Used internally for positioning |
| overrideOffset | Unset; enables manual control | Set explicitly to control axis position | Essential for stacking (e.g., 3D waterfall charts) |

In SciChart.js, always use overrideOffset to manually set axis positions especially in interactive, multi axis layouts (like waterfall charts) for visual separation and to achieve advanced effects such as 3D stacking. Directly setting offset is not recommended as it’s controlled by the internal engine and may not persist or behave as expected.