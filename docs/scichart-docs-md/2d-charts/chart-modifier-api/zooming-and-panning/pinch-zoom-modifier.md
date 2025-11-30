---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/zooming-and-panning/pinch-zoom-modifier
scraped_at: 2025-11-28T18:24:20.310070
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/zooming-and-panning/pinch-zoom-modifier

# PinchZoomModifier

SciChart.js provides Pinch zooming on touch devices via the PinchZoomModifier📘 type.

As of SciChart.js v3.2, **ZoomPanModifier** now inherits **PinchZoomModifier**, allowing you to configure zooming, panning and touch-to-zoom interaction via a single modifier.

## Adding a PinchZoomModifier to a Chart

A **PinchZoomModifier** may be added to the sciChartSurface.chartModifiers📘 colletion to enable pinch to zoom behaviour. For example:

- TS
- Builder API (JSON Config)

`// Demonstrates how to configure PinchZoomModifier SciChart.js`

const { SciChartSurface, NumericAxis, PinchZoomModifier } = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId);

// Create an X and Y Axis

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

const pinchZoomModifier = new PinchZoomModifier({

horizontalGrowFactor: 0.001,

verticalGrowFactor: 0.001,

excludedXAxisIds: ["xAxis2"],

includedYAxisIds: ["yAxis1"]

});

sciChartSurface.chartModifiers.add(pinchZoomModifier);

`// Demonstrates how to configure a PinchZoom Modifier in SciChart.js using the Builder API`

const { chartBuilder, EChart2DModifierType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

modifiers: [

{

type: EChart2DModifierType.PinchZoom,

options: {

horizontalGrowFactor: 0.001,

verticalGrowFactor: 0.001,

excludedXAxisIds: ["xAxis2"],

includedYAxisIds: ["yAxis1"]

}

}

]

});

This results in the following output

## Additional Properties

### Adjust Zooming / Scale Factor

Horizontal and vertical zoom scale factor can be adjusted via the following properties:

The default value for both is set to `0.005`

.

### Allow Pinch Zoom in only one direction

If you want to enable pinch zooming in only one direction, e.g. horizontal only, modify the **PinchZoomModifier.verticalGrowFactor** to equal `0`

.

### Include/Exclude Certain Axis from Pinch Zoom

The PinchZoomModifier allows you to include or exclude certain axis by axis.id from the zoom operation.

By default all axis are included, to exclude one or more X or Y axis, set the following property:

- Exclude Axis

`// Exclude a specific axis from the pinch zoom operation`

pinchZoomModifier.includeXAxis(axisXInstance, false);

pinchZoomModifier.includeYAxis(axisYInstance, false);

// Include specific axis from the pinch zoom operation

pinchZoomModifier.includeXAxis(axisXInstance, true);

pinchZoomModifier.includeYAxis(axisYInstance, true);

// Reset flags

pinchZoomModifier.includeAllAxes();

### Allow Pinch Zoom in only one direction

If you want to enable pinch zooming in only one direction, e.g. horizontal only, modify the **PinchZoomModifier.verticalGrowFactor** to equal `0`

.