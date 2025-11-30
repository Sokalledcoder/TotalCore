---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-labels/rotating-axis-labels
scraped_at: 2025-11-28T18:24:05.897959
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-labels/rotating-axis-labels

# Rotating Axis Labels

SciChart.js supports rotation of labels for all 2D axis types and LabelProviders. This lets you display longer labels, or pack more labels onto an x axis.

To use rotated labels on a chart, or vertical labels, use this code:

- TS
- Builder API (JSON Config)

`const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {`

theme: new SciChartJsNavyTheme()

});

const xAxis = new NumericAxis(wasmContext, {

axisTitle: "X Axis / 90 Degree Rotation",

visibleRange: new NumberRange(1e6, 2e6),

labelFormat: ENumericFormat.Decimal,

labelPrecision: 4,

// Allow more labels for the demo

maxAutoTicks: 30,

// Rotation is in degrees clockwise. Negative numbers are OK

rotation: 90,

// Turn off minor gridlines, since majors are now closer together

drawMinorGridLines: false

});

// Add the xAxis to the chart

sciChartSurface.xAxes.add(xAxis);

// Creating a NumericAxis as a YAxis on the left

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

axisTitle: "Y Axis, -25 Degree Rotation",

rotation: -25,

labelFormat: ENumericFormat.Decimal,

labelPrecision: 4

})

);

`// If you want to show an Axis with rotated labels. Using a numeric axis for example`

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: {

type: EAxisType.NumericAxis,

options: {

axisTitle: "X Axis / 90 Degree Rotation",

visibleRange: new NumberRange(1e6, 2e6),

labelFormat: ENumericFormat.Decimal,

labelPrecision: 4,

// Allow more labels for the demo

maxAutoTicks: 30,

// Rotation is in degrees clockwise. Negative numbers are OK

rotation: 90,

// Turn off minor gridlines, since majors are now closer together

drawMinorGridLines: false

}

},

yAxes: {

type: EAxisType.NumericAxis,

options: {

axisTitle: "Y Axis, Numeric",

rotation: 25,

labelFormat: ENumericFormat.Decimal,

labelPrecision: 4

}

}

});

This results in the following output:

For an example of using rotation with text labels see the Multiline and Rotated Text Labels demo in our examples suite.

### Further notes on Label Culling & Spacing

An axis with rotated labels obeys other rules of axis tick spacing and label culling. Take a look at the section on Gridline and Label Spacing (Interval) for some more information how this works.

When working with rotated labels that are not horizontal or vertical, it may be necessary to turn off axis.axisRenderer.hideOverlappingLabels📘 as the bounding box of a partially rotated label is much larger than the text itself.This property may also be set via the axis constructor option hideOverlappingLabels📘.

To do this, use the following code:

`// hideOverlappingLabels Example`

// Either

const xAxis = new NumericAxis(wasmContext, {

// Allow labels to overlap

hideOverlappingLabels : false

});

// Or

const xAxis = new NumericAxis(wasmContext);

// Allow rotated labels to overlap

xAxis.axisRenderer.hideOverlappingLabels = false;