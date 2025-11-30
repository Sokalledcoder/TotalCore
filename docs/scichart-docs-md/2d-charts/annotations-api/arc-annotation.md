---
source: https://www.scichart.com/documentation/js/v4/2d-charts/annotations-api/arc-annotation
scraped_at: 2025-11-28T18:23:59.776522
---

# https://www.scichart.com/documentation/js/v4/2d-charts/annotations-api/arc-annotation

# ArcAnnotation

The ArcAnnotation📘 is used to draw a filled arc sector or a curved line on a 2D Cartesian SciChartSurface📘. Unlike the PolarArcAnnotation📘 which uses angles, the ArcAnnotation📘 is defined by two data points (`x1, y1`

and `x2, y2`

) and a `height`

property, which controls the arc's curvature.

## Create an Arc Annotation

The following code demonstrates how to declare a filled arc segment and a curved line using the ArcAnnotation📘 and add them to a chart.

- TS

`const {`

SciChartSurface,

NumericAxis,

ArcAnnotation,

SciChartJsNavyTheme,

ECoordinateMode

} = SciChart;

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme(),

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

// Filled Arc Segment with positive height

const filledArc = new ArcAnnotation({

isEditable: true,

x1: 3,

y1: 7,

x2: 7,

y2: 7,

height: 4,

innerRadius: 0.4, // Creates a segment instead of a full sector

fill: "rgba(176, 196, 222, 0.3)",

stroke: "rgba(176, 196, 222, 1)",

strokeThickness: 5,

});

// Arc Line with negative height

const arcLine = new ArcAnnotation({

isEditable: true,

isLineMode: true,

x1: 3,

y1: 5,

x2: 7,

y2: 5,

height: -1.5, // Negative height curves the arc downwards

stroke: "#FF6347",

strokeThickness: 5,

selectionBoxStroke: "rgba(255, 255, 255, 0.5)",

});

const absoluteArc = new ArcAnnotation({

isEditable: true,

isLineMode: true,

x1: 30,

y1: 50,

x2: 70,

y2: 50,

height: -1.5, // Negative height curves the arc downwards

stroke: "#FF6347",

strokeThickness: 5,

selectionBoxStroke: "rgba(255, 255, 255, 0.5)",

xCoordinateMode: ECoordinateMode.Pixel,

yCoordinateMode: ECoordinateMode.Pixel,

});

// Add ArcAnnotations to the chart

sciChartSurface.annotations.add(filledArc, arcLine, absoluteArc);

This results in the following output:

In the code above:

- Two instances of ArcAnnotation📘 are created and added to a SciChartSurface📘.
- The first annotation is a
**filled arc segment**. It is defined by its start/end points and a positive height📘 for upward curvature. The innerRadius📘 property makes it a segment rather than a full sector. - The second annotation is an
**arc line**. This is achieved by setting isLineMode📘:`true`

. Its negative`height`

causes it to curve downwards. - Both annotations are made editable by setting isEditable📘:
`true`

.

### Unique Properties

The ArcAnnotation📘 has several specific properties for its configuration:

| Property | Type | Default | Description |
|---|---|---|---|
| height📘 | `number` | 0 | The height of the arc from the center of the baseline. Negative values produce an arc with opposite curvature. |
| innerRadius📘 | `number` | 0 | A value from 0 to 1 that defines the inner radius as a proportion of the outer radius. Ignored when `isLineMode` is true. |
| isLineMode📘 | `boolean` | `false` | If `true` , the annotation renders as a curved line. If `false` , it renders as a filled sector. |

tip

Use a negative height📘 value to flip the curvature of the arc.

tip

To draw a full sector that extends to the baseline (like a slice of a pie), set the innerRadius📘 property to `0`

.

#### See Also

- PolarArcAnnotation - The equivalent annotation for Polar Surfaces.
- The Annotations API Overview