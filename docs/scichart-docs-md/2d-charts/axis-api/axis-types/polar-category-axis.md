---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-types/polar-category-axis
scraped_at: 2025-11-28T18:24:08.988869
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-types/polar-category-axis

# The Polar Category Axis

The PolarCategoryAxis📘 brings category (discrete, label-based, or index-based) data to polar charts—enabling radar, spider, and circular bar charts where each sector represents a category or qualitative dimension.

**Key features:**

- Lets you plot non-numeric, ordinal, or named categories around a circle (e.g., "Defense", "Shooting", ...).
- Works in both angular (sweep) and radial (outward) modes.
- Supports custom label lists via labels📘, startAngle📘, totalAngle📘, gridline style, and many more.
- Collapses “gaps” in your data, making it perfect for displaying categorical time-series or performance data.

## Key Options

- labels📘 – Array of strings for each category.
- polarAxisMode📘 – Set to Angular📘 to lay categories around the sweep; or Radial📘 for concentric category rings.
- startAngle / startAngleDegrees📘 – Where the axis begins (e.g.,
`Math.PI / 2`

for 12 o’clock). - flippedCoordinates📘 – Set to
`true`

for clockwise domain. - polarLabelMode📘 – Controls label orientation (parallel, perpendicular, horizontal, etc).

## Example: Category Radar Chart

`const {`

SciChartPolarSurface,

SciChartJsNavyTheme,

PolarCategoryAxis,

PolarLineRenderableSeries,

XyDataSeries,

EPolarAxisMode,

NumberRange,

EPolarGridlineMode,

EAxisAlignment,

EPolarLabelMode

} = SciChart;

const { sciChartSurface, wasmContext } = await SciChartPolarSurface.create(rootElement, {

theme: new SciChartJsNavyTheme()

});

// Angular axis: goes around the circle, from 0 to 360 degrees

const angularAxis = new PolarCategoryAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Angular, // Lines around the center

axisAlignment: EAxisAlignment.Top,

drawMinorGridLines: false,

startAngle: Math.PI / 2, // Start chart at 12 o'clock

labels: ["Bandwidth", "Latency", "Throughput", "Capacity", "Efficiency", "Scalability", "Reliability"],

});

sciChartSurface.xAxes.add(angularAxis);

// Radial axis: from center outward, with circular gridlines

const radialAxis = new PolarCategoryAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Radial,

axisAlignment: EAxisAlignment.Right,

polarLabelMode: EPolarLabelMode.Perpendicular,

innerRadius: 0.1,

gridlineMode: EPolarGridlineMode.Polygons, // radar chart look

flippedCoordinates: true, // from "Low" to "Excellent"

labels: ["Low", "Medium", "High", "Very High", "Excellent"],

visibleRange: new NumberRange(0, 4),

startAngle: Math.PI / 2, // draw radial labels at 12 o'clock

});

sciChartSurface.yAxes.add(radialAxis);

sciChartSurface.renderableSeries.add(

new PolarLineRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: Array.from({ length: 8 }, (_, i) => i),

yValues: [1, 2, 3, 4, 0, 4, 3, 1] // Example values for each category

}),

stroke: "#FF6600",

strokeThickness: 3,

})

);

tip

The number of string elements inside the labels📘 array determines the number of *possible* text tick labels, it does not force the chart to render that amount of ticks directly, that is still determined by the visibleRange📘 of the angular axis, or the x/y-range calculated to include all the renderable series's points, if present.

## Common Use Cases

- Stats, analytics, comparisons between entities
- Product or feature comparison (radar charts)
- Survey, KPI, and performance dashboards
- Any polar visualization with qualitative or ordinal axes