---
source: https://www.scichart.com/documentation/js/v4/2d-charts/annotations-api/axis-marker-annotation/axis-marker-annotation-overview
scraped_at: 2025-11-28T18:24:00.467785
---

# https://www.scichart.com/documentation/js/v4/2d-charts/annotations-api/axis-marker-annotation/axis-marker-annotation-overview

# AxisMarkerAnnotation

The AxisMarkerAnnotation📘 allows you to add a label on to the Axis at a specific X or Y value.

## Declaring a AxisMarkerAnnotation in code

The following code will declare an AxisMarkerAnnotation📘 add it to the chart.

- TS
- Builder API (JSON Config)

`const { AxisMarkerAnnotation, NumericAxis, SciChartSurface, ELabelPlacement, SciChartJsNavyTheme } = SciChart;`

// or for npm import { SciChartSurface, ... } from "scichart"

async function addAnnotationToChart(divElementId) {

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

// Add a selection of annotations to the chart

sciChartSurface.annotations.add(

// An AxisMarkerAnnotation at Y=5.2 showing the y-value

new AxisMarkerAnnotation({

y1: 5.2,

fontSize: 20,

fontStyle: "Bold",

backgroundColor: "SteelBlue",

color: "White",

fontFamily: "Default",

fontWeight: "700"

}),

// An AxisMarkerAnnotation at Y=7 with a custom label

new AxisMarkerAnnotation({

y1: 7,

fontSize: 16,

fontStyle: "Bold",

backgroundColor: "#FF6600",

color: "Black",

fontFamily: "Default",

formattedValue: "Custom Label"

})

);

}

addAnnotationToChart("scichart-root");

`const { chartBuilder, EAnnotationType } = SciChart;`

// or for npm import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

annotations: [

{

type: EAnnotationType.RenderContextAxisMarkerAnnotation,

options: {

y1: 5.2,

fontSize: 12,

fontStyle: "Bold",

backgroundColor: "SteelBlue",

color: "White",

fontFamily: "Default"

}

},

{

type: EAnnotationType.RenderContextAxisMarkerAnnotation,

options: {

y1: 7,

fontSize: 16,

fontStyle: "Bold",

backgroundColor: "#FF6600",

color: "Black",

fontFamily: "Default",

formattedValue: "Custom Label"

}

}

]

});

Results in the following output:

## Styling the AxisMarkerAnnotation

The following properties can be set to style the AxisMarkerAnnotation📘:

Property | Description |
|---|---|
| backgroundColor📘 | The box fill color for the axis label |
| color📘 | The text-color for the axis label |
| fontFamily📘 | The font family for the axis label text |
| fontSize📘 | The font size for the axis label text |
| fontStyle📘 | The font style, e.g. Bold or Italic for the axis label text |
| formattedValue📘 | The formatted value on the axis label. This defaults to the Y-value formatted by the yAxis.labelProvider📘. This can be overridden by a custom label value by setting this property. |
| annotationGripsFill📘 | The fill color for the annotations grips when editing (dragging) |
| annotationsGripsRadius📘 | The radius for the annotations grips when editing (dragging) |
| annotationGripsStroke📘 | The stroke color for the annotations grips when editing. |