---
source: https://www.scichart.com/documentation/js/v4/2d-charts/annotations-api/polar-arc-annotation
scraped_at: 2025-11-28T18:24:02.731470
---

# https://www.scichart.com/documentation/js/v4/2d-charts/annotations-api/polar-arc-annotation

# PolarArcAnnotation

The PolarArcAnnotation📘 is used to draw a filled sector or an arc line on a SciChartPolarSurface📘. It is defined by a center point, inner and outer radii, and start and end angles. This annotation is ideal for highlighting specific angular or radial regions in polar charts.

## Create a Polar Arc Annotation

The following code demonstrates how to declare a filled sector and a line arc using PolarArcAnnotation📘 and add them to a polar surface.

- TS

`const {`

SciChartPolarSurface,

PolarNumericAxis,

NumberRange,

PolarArcAnnotation,

SciChartJsNavyTheme,

EPolarAxisMode,

} = SciChart;

// Create a SciChartPolarSurface

const { wasmContext, sciChartSurface } = await SciChartPolarSurface.create(divElementId, {

theme: new SciChartJsNavyTheme(),

});

// Add polar axes

sciChartSurface.xAxes.add(

new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Angular,

visibleRange: new NumberRange(0, 360)

})

);

sciChartSurface.yAxes.add(

new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Radial,

visibleRange: new NumberRange(0, 10)

})

);

// Add a selection of PolarArcAnnotations to the chart

sciChartSurface.annotations.add(

// Filled Sector Annotation from 45 to 135 degrees

new PolarArcAnnotation({

isEditable: true,

x1: 45, // Start Angle

x2: 135, // End Angle

y1: 8, // Outer Radius

y2: 4, // Inner Radius

fill: "rgba(255, 165, 0, 0.3)",

stroke: "#FFA500",

strokeThickness: 2,

}),

// Arc Line Annotation from 225 to 315 degrees

new PolarArcAnnotation({

isEditable: true,

isLineMode: true,

x1: 225, // Start Angle

x2: 315, // End Angle

y1: 9, // Radius

// No need for y2 when `isLineMode` is true

stroke: "#3388FF",

strokeThickness: 3,

})

);

This results in the following output:

In the code above:

- Two instances of PolarArcAnnotation📘 are created and added to a SciChartPolarSurface📘.
- The first annotation is a
**filled sector**. It is defined by start/end angles (`x1`

,`x2`

) and outer/inner radii (`y1`

,`y2`

). - The second annotation is an
**arc line**. This is achieved by setting isLineMode📘:`true`

, which causes the annotation to render as a single line at the`y1`

radius, ignoring the`y2`

property. - Both annotations are editable and can be dragged or resized by the user if isEditable📘:
`true`

is set.

### Unique Properties

The PolarArcAnnotation📘 has several specific properties for its configuration:

| Property | Type | Default | Description |
|---|---|---|---|
| centerX📘 | `number` | 0 | The X coordinate of the arc's center point. |
| centerY📘 | `number` | 0 | The Y coordinate of the arc's center point. |
| x1📘 | `number` | - | The start angle of the annotation. |
| x2📘 | `number` | - | The end angle of the annotation. |
| y1📘 | `number` | - | The outer radius of the annotation. |
| y2📘 | `number` | - | The inner radius of the annotation. This property is ignored when `isLineMode` is true. |
| isLineMode📘 | `boolean` | `false` | If `true` , the annotation renders as a line at the `y1` radius. If `false` , it renders as a filled sector between the `y1` and `y2` radii. |

To draw a simple arc line instead of a filled sector, set the `isLineMode`

property to `true`

. This simplifies the annotation to only require `x1`

, `x2`

, and `y1`

for its shape.

To draw a full pie-slice that starts from the center, set the inner radius `y2`

to `0`

.

#### See Also

- ArcAnnotation📘 - this a similar concept, but for 2D Cartesian surfaces.