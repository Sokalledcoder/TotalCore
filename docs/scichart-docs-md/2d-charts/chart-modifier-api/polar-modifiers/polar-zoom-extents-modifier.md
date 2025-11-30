---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/polar-modifiers/polar-zoom-extents-modifier
scraped_at: 2025-11-28T18:24:17.177120
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/polar-modifiers/polar-zoom-extents-modifier

# PolarZoomExtentsModifier

SciChart.js provides the ability to Zoom Extents the polar chart (zoom to fit data) by double-clicking the chart area with the PolarZoomExtentsModifier📘, available out of the box.

Here is how to define the PolarZoomExtentsModifier📘 in your code:

- TS
- Builder API (JSON Config)

`const { PolarZoomExtentsModifier, Point } = SciChart;`

// or for npm: import { PolarZoomExtentsModifier } from "scichart";

sciChartSurface.chartModifiers.add(

// Zoom Extents Modifier:

new PolarZoomExtentsModifier({

centerPoint: new Point(0, 0),

animationDuration: 1000,

innerRadius: 0.2

})

);

`// Demonstrates how to configure the PolarZoomExtentsModifier in SciChart.js using the Builder API`

const {

chartBuilder,

EAxisAlignment,

EThemeProviderType,

EAxisType,

EChart2DModifierType,

EPolarAxisMode,

Point,

ESeriesType

} = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DPolarChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: [

{

type: EAxisType.PolarNumericAxis,

options: {

polarAxisMode: EPolarAxisMode.Radial,

axisAlignment: EAxisAlignment.Left,

innerRadius: 0.1,

startAngleDegrees: 90

}

}

],

yAxes: [

{

type: EAxisType.PolarNumericAxis,

options: {

polarAxisMode: EPolarAxisMode.Angular,

axisAlignment: EAxisAlignment.Bottom,

startAngleDegrees: 90

}

}

],

series: {

type: ESeriesType.PolarColumnSeries,

options: {

stroke: "#50C7E0",

fill: "#50C7E044",

strokeThickness: 2

},

xyData: {

xValues: Array.from({ length: 5 }, (_, i) => i),

yValues: Array.from({ length: 5 }, (_, i) => 1 + Math.sin(i * 0.3))

}

},

modifiers: [

{

type: EChart2DModifierType.PolarZoomExtents,

options: {

xStartAngle: Math.PI / 4,

yStartAngle: 0,

totalAngle: Math.PI * 2,

centerPoint: new Point(0, 0),

animationDuration: 1000

}

}

]

});

## Zoom to a Preset Range

If you would like the double-click to zoom to some preset range, rather than the data range, you can set `zoomExtentsRange`

on the axes. In addition, if you are setting an initial visibleRange on an axis and would like zoomExtents to return to this range, you can just set `zoomExtentsToInitialRange`

true, which will set `zoomExtentsRange`

to the `visibleRange`

passed in.

Besides common features which are inherited from the base ZoomExtentsModifier📘 class, the PolarZoomExtentsModifier📘 has many more polar-specific features, such as:

| Property | Type | Description |
|---|---|---|
| xStartAngle📘 | number | The start angle for the X-axis in the polar chart. |
| yStartAngle📘 | number | The start angle for the Y-axis in the polar chart. |
| totalAngle📘 | number | The total angle of the polar chart, which defines the range of angles covered by the chart. |
| lengthScale📘 | number | The scale factor for the radian axis |
| innerRadius📘 | number | The inner radius of the polar chart, which defines the minimum distance from the center to the edge of the chart. |
| centerPoint📘 | Point📘 | Center point of the polar chart, which defines the origin of the polar coordinates. |
| resetStartAngles📘 | boolean | Whether to reset the start angles for both the X and Y axes to their initial values. |
| resetTotalAngle📘 | boolean | Whether to reset the total angle to its initial value. |
| resetRanges📘 | boolean | Whether to reset the ranges for both the radial and angular axes to their initial values. |
| resetLengthScale📘 | boolean | Whether to reset the length scale to its initial value. |
| resetCenterPoint📘 | boolean | Whether to reset the center point to its initial value. |
| resetInnerRadius📘 | boolean | Whether to reset the inner radius to its initial value. |

See all at IPolarZoomExtentsModifierOptions📘.