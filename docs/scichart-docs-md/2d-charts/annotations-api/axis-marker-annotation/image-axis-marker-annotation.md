---
source: https://www.scichart.com/documentation/js/v4/2d-charts/annotations-api/axis-marker-annotation/image-axis-marker-annotation
scraped_at: 2025-11-28T18:24:00.422204
---

# https://www.scichart.com/documentation/js/v4/2d-charts/annotations-api/axis-marker-annotation/image-axis-marker-annotation

# Image AxisMarkerAnnotation

SciChart.js allows to create **custom axis marker annotations** on axes. This is done by creating AxisMarkerAnnotation and passing an **image** option into the constructor.

`const htmlImageElement = await createImageAsync(imageUrl);`

const customAxisMarkerAnnotation = new AxisMarkerAnnotation({

y1: 5,

isEditable: true,

image: htmlImageElement,

});

The full example code is below:

- TS
- Builder API (JSON Config)

`const {`

AxisMarkerAnnotation,

NumericAxis,

SciChartSurface,

SciChartJsNavyTheme,

createImageAsync,

TextAnnotation,

EHorizontalAnchorPoint

} = SciChart;

// or for npm import { SciChartSurface, ... } from "scichart"

async function addAnnotationToChart(divElementId) {

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

const imageUrl = "https://www.scichart.com/demo/images/CustomMarkerImage.png";

const htmlImageElement = await createImageAsync(imageUrl);

// An AxisMarkerAnnotation at Y=5.2 showing an image

sciChartSurface.annotations.add(

new AxisMarkerAnnotation({

y1: 5.1,

isEditable: true,

image: htmlImageElement,

// Optional: Set imageWidth and imageHeight, else it will default to image size

imageWidth: 48,

imageHeight: 48

})

);

// Add a text annotation to explain

sciChartSurface.annotations.add(

new TextAnnotation({

x1: 9.5,

y1: 5.2,

horizontalAnchorPoint: EHorizontalAnchorPoint.Right,

fontSize: 16,

text: "Draggable Axis Marker with a custom image -->"

})

);

}

addAnnotationToChart("scichart-root");

`const { chartBuilder, EAnnotationType } = SciChart;`

// or for npm import { SciChartSurface, ... } from "scichart"

const imageUrl = "https://www.scichart.com/demo/images/CustomMarkerImage.png";

const htmlImageElement = await createImageAsync(imageUrl);

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

annotations: [

{

type: EAnnotationType.RenderContextAxisMarkerAnnotation,

options: {

y1: 5.1,

isEditable: true,

image: htmlImageElement,

// Optional: Set imageWidth and imageHeight, else it will default to image size

imageWidth: 48,

imageHeight: 48

}

}

]

});

In this example we are using createImageAsync()📘 helper function to create an htmlImageElement. This is then passed to AxisMarkerAnnotation.image📘 property. Optionally AxisMarkerAnnotation.imageWidth📘 and imageHeight📘 may be set.

Here's the output:

On the chart we can see a cloud-shaped custom axis label annotation. The annotation is draggable along the YAxis.