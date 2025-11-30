---
source: https://www.scichart.com/documentation/js/v4/get-started/faqs/faq_hover_interactions
scraped_at: 2025-11-28T18:25:00.042698
---

# https://www.scichart.com/documentation/js/v4/get-started/faqs/faq_hover_interactions

# Hover and Click Interactions

In SciChart.js, you can implement both click and hover events on charts using several different approaches. Here are the main methods for detecting these interactions:

## Click Events on Charts

### Custom Chart Modifier for Click Detection

The most flexible approach is creating a CustomChartModifier that extends ChartModifierBase2D📘

`class SimpleChartModifier extends CustomChartModifier2D {`

readonly type = EChart2DModifierType.Custom;

modifierMouseDown(args: ModifierMouseArgs) {

super.modifierMouseDown(args);

statusLabel.text = `MouseDown at point ${args.mousePoint.x}, ${args.mousePoint.y}`;

}

modifierDoubleClick(args: ModifierMouseArgs) {

super.modifierDoubleClick(args);

statusLabel.text = `DoubleClick at point ${args.mousePoint.x}, ${args.mousePoint.y}`;

}

}

sciChartSurface.chartModifiers.add(new SimpleChartModifier());

### Series Selection Modifier

For built-in series click functionality, use the SeriesSelectionModifier📘

`const seriesSelectionModifier = new SeriesSelectionModifier({`

enableSelection: true,

onSelectionChanged: args => {

console.log("Series selected:", args.selectedSeries[0]);

}

});

sciChartSurface.chartModifiers.add(seriesSelectionModifier);

## Hover Events on Charts

### Hover Detection with Series Selection Modifier

Enable hover detection using the SeriesSelectionModifier📘

`const seriesSelectionModifier = new SeriesSelectionModifier({`

enableHover: true,

onHoverChanged: args => {

console.log("Series hovered:", args.hoveredSeries[0]);

}

});

sciChartSurface.chartModifiers.add(seriesSelectionModifier);

### Series-Level Hover Events

You can attach hover callbacks directly to RenderableSeries

`const lineSeries = new FastLineRenderableSeries(wasmContext, {`

strokeThickness: 3,

dataSeries: new XyDataSeries(wasmContext, {

xValues: xLineValues,

yValues: yLineValues,

dataSeriesName: "Line Series"

}),

onHoveredChanged: (sourceSeries, isHovered) => {

console.log(`Series ${sourceSeries.dataSeries.dataSeriesName} hovered: ${isHovered}`);

// Change appearance on hover

sourceSeries.strokeThickness = isHovered ? 6 : 3;

}

});

sciChartSurface.renderableSeries.add(lineSeries);

sciChartSurface.chartModifiers.add(

new SeriesSelectionModifier({

enableHover: true,

enableSelection: false // Set to false if you only want hover, not selection

})

);

### Custom Modifier for Advanced Hover Detection

For detecting hover on specific chart parts (axes, series, chart area), create a custom modifier

`const seriesSelectionModifier = new SeriesSelectionModifier({`

enableHover: true,

onHoverChanged: args => {

const hoveredSeries = args.hoveredSeries;

if (hoveredSeries && hoveredSeries.length > 0) {

// Get mouse coordinates from the chart surface

sciChartSurface.domCanvas2D.addEventListener(

"mousemove",

mouseEvent => {

const premultipliedX = mouseEvent.offsetX * DpiHelper.PIXEL_RATIO;

const premultipliedY = mouseEvent.offsetY * DpiHelper.PIXEL_RATIO;

hoveredSeries.forEach(series => {

const hitTestInfo = series.hitTestProvider.hitTest(premultipliedX, premultipliedY, 10);

if (hitTestInfo.isHit) {

console.log("Hovered data point:");

console.log("- Index:", hitTestInfo.dataSeriesIndex);

console.log(

"- Values:",

hitTestInfo.xValue,

hitTestInfo.yValue,

hitTestInfo.x1Value,

hitTestInfo.y1Value

);

statusLabel.text = `Hovered data point: Index: ${hitTestInfo.dataSeriesIndex}, Values: ${hitTestInfo.xValue} ${hitTestInfo.yValue} ${hitTestInfo.x1Value} ${hitTestInfo.y1Value}`;

}

});

},

{ once: true }

); // Use once to avoid multiple listeners

} else {

statusLabel.text = "";

}

}

});

sciChartSurface.chartModifiers.add(seriesSelectionModifier);

### Annotation Hover Events

For annotations, SciChart.js provides dedicated hover functionality

`// Create AnnotationHoverModifier to enable hover detection`

const annotationHoverModifier = new AnnotationHoverModifier({

enableHover: true,

targets: [boxAnnotation, secondBoxAnnotation], // Specify which annotations to monitor

hoverMode: EHoverMode.AbsoluteTopmost, // Only top annotation if overlapping

notifyOutEvent: true, // Fire events when mouse leaves annotation

notifyPositionUpdate: false, // Don't fire events on position updates within annotation

// Global hover callback for all targeted annotations

onHover: args => {

const { hoveredEntities, unhoveredEntities } = args;

// Change appearance of hovered annotations

hoveredEntities.forEach(annotation => {

console.log(annotation);

if (annotation instanceof BoxAnnotation) {

annotation.fill = "#34eb8c77"; // Semi-transparent green

annotation.stroke = "#34eb8c";

annotation.strokeThickness = 3;

}

console.log("Annotation became hovered:", annotation);

});

// Reset appearance of unhovered annotations

unhoveredEntities.forEach(annotation => {

if (annotation instanceof BoxAnnotation) {

annotation.fill = "#3d34eb77"; // Back to blue

annotation.stroke = "#3d34eb";

annotation.strokeThickness = 1;

}

console.log("Annotation became unhovered:", annotation);

});

}

});

// Add the hover modifier to enable the functionality

sciChartSurface.chartModifiers.add(annotationHoverModifier);

The ChartModifier API provides comprehensive mouse event handling including modifierMouseDown, modifierMouseUp, modifierMouseMove, modifierDoubleClick, and modifierMouseWheel methods for creating sophisticated chart interactions.