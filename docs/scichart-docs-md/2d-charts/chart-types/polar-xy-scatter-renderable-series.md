---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/polar-xy-scatter-renderable-series
scraped_at: 2025-11-28T18:24:42.332497
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/polar-xy-scatter-renderable-series

# The Polar Scatter Chart Type

The PolarXyScatterRenderableSeries📘 visualizes discrete points in a polar (circular) coordinate system, using customizable point markers. Each `(x, y)`

data point is mapped as an "angle" (theta, usually in degrees or radians) and a "radius" (distance from center), making this chart type ideal for:

- Visualizing measurement data around a circle (e.g., wind direction/speed)
- Radar, sonar, and astronomy applications
- Medical/engineering polar data, and more

Above: The JavaScript Polar Xy Scatter Series Chart example from the SciChart.js Demo

## Properties

Key options for IPolarXyScatterRenderableSeriesOptions📘:

- dataSeries📘: The XyDataSeries📘 containing your X and Y arrays (angle & radius, respectively)
- pointMarker📘: Type, shape, and color of marker (EllipsePointMarker📘, TrianglePointMarker📘, etc.)
- paletteProvider📘: Optional for dynamic/color-by-value marker coloring
- clipToTotalAngle📘: If set, clips points outside the angular axis' total angle
- dataLabels📘: Optionally show and style labels for individual points

## Examples

### Basic Polar Scatter Series

`// Demonstrates how to create a scatter chart with SciChart.js`

const {

SciChartPolarSurface,

SciChartJsNavyTheme,

XyDataSeries,

PolarNumericAxis,

EPolarAxisMode,

NumberRange,

EAxisAlignment,

EPolarLabelMode,

PolarXyScatterRenderableSeries,

TrianglePointMarker,

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { sciChartSurface, wasmContext } = await SciChartPolarSurface.create(rootElement, {

theme: new SciChartJsNavyTheme()

});

const radialYAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Radial,

axisAlignment: EAxisAlignment.Right,

drawLabels: false,

});

sciChartSurface.yAxes.add(radialYAxis);

const angularXAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Angular,

axisAlignment: EAxisAlignment.Top,

polarLabelMode: EPolarLabelMode.Parallel,

visibleRange: new NumberRange(0, 360),

autoTicks: false, // Control the tick intervals manually

majorDelta: 30, // Go from 0 to 360 in steps of 30 degrees

labelPrecision: 0,

labelPostfix: `°`, // Degree symbol

});

sciChartSurface.xAxes.add(angularXAxis);

const scatterExample = new PolarXyScatterRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: Array.from({ length: 36 }, (_, i) => i * 10),

yValues: Array.from({ length: 36 }, () => Math.random()),

}),

pointMarker: new TrianglePointMarker(wasmContext, {

width: 10,

height: 9,

strokeThickness: 1.5,

fill: "#000000",

stroke: "#FF8800",

}),

});

sciChartSurface.renderableSeries.add(scatterExample);

In the code above:

- The PolarXyScatterRenderableSeries📘 is created and linked to an XyDataSeries📘.
- TrianglePointMarker📘 is used to draw each point, but you can substitute with any point marker class.
- Angular axis is configured to have a visible range from
`0`

to`360`

and this coincides with the default totalAngle📘 of`360 degrees`

, thus we added the labelPostfix📘 as`°`

to further clarify the angle unit. - The radial axis is used for "distance from center"; here labels are hidden for a minimalist look.

### Polar Scatter with the BuilderAPI schema

The Scatter series's pointMarker📘 property can be configured using a json type - options schema, great for dynamically assigning point marker types for a large dataset.

`const scatterExample = new PolarXyScatterRenderableSeries(wasmContext, {`

dataSeries: new XyDataSeries(wasmContext, {

xValues: Array.from({ length: 36 }, (_, i) => i * Math.PI / 18),

yValues: Array.from({ length: 36 }, () => Math.random()),

}),

pointMarker: {

type: EPointMarkerType.Cross,

options: {

width: 20,

height: 8,

strokeThickness: 2,

stroke: "#44AAFF",

}

}

});

sciChartSurface.renderableSeries.add(scatterExample);

## Point Marker Types & Customization

Any pointmarker type available in SciChart.js can be used for polar scatter charts:

- EllipsePointMarker📘
- SquarePointMarker📘
- TrianglePointMarker📘
- CrossPointMarker📘
- XPointMarker📘
- SpritePointMarker📘 for custom image markers
- Styles such as
`fill`

,`stroke`

,`size`

, and`strokeThickness`

are all customizable.