---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/zooming-and-panning/zoom-pan-modifier
scraped_at: 2025-11-28T18:24:20.932413
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/zooming-and-panning/zoom-pan-modifier

# ZoomPanModifier

SciChart.js provides an scrolling / panning behavior via the ZoomPanModifier📘, available out of the box.

As of SciChart.js v3.2, ZoomPanModifier📘 now inherits PinchZoomModifier📘, allowing you to configure zooming, panning and touch-to-zoom interaction via a single modifier.

All the properties for the PinchZoomModifier📘 may be set to control vertical/horizontal zooming, include/exclude axis from pinch zooming etc..

Besides common features which are inherited from the ChartModifierBase class, the ZoomPanModifier📘 allows to **restrict scrolling** to the horizontal or vertical direction only, via the xyDirection📘 property.

## Adding a ZoomPanModifier to a Chart

A ZoomPanModifier can be added to the sciChartSurface.chartModifiers📘 collection to enable panning behavior. For example:

- TS
- Builder API (JSON Config)

`const { ZoomPanModifier, EXyDirection } = SciChart;`

// or for npm: import { PinchZoomModifier } from "scichart";

// Add Zoom Pan and Pinch behaviour to the chart. All parameters are optional

sciChartSurface.chartModifiers.add(new ZoomPanModifier({

// Specifies Panning in X,Y direction or both

xyDirection: EXyDirection.XyDirection,

// Enables Pinch Zoom functionality

enableZoom: true,

// Optional parameters specify the amount of pinch zooming in X/Y Default is 0.005

horizontalGrowFactor: 0.005,

verticalGrowFactor: 0.005

// Optional parameters to include/exclude X/Y axis from zooming by axis.id

// If not specified, by default, all axis are included in zooming

// either use:

// excludedXAxisIds: ["XAxis1"],

// excludedYAxisIds: ["YAxis1"],

// or:

// includedXAxisIds: ["XAxis2"],

// includedYAxisIds: ["YAxis2"],

}));

`// Demonstrates how to configure the ZoomPanModifier in SciChart.js using the Builder API`

const { chartBuilder, EThemeProviderType, EAxisType, EChart2DModifierType, EXyDirection } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: { type: EAxisType.NumericAxis },

yAxes: { type: EAxisType.NumericAxis },

modifiers: [

{

type: EChart2DModifierType.ZoomPan,

options: {

// Specifies Panning in X,Y direction or both

xyDirection: EXyDirection.XyDirection,

// Enables Pinch Zoom functionality

enableZoom: true,

// Optional parameters specify the amount of pinch zooming in X/Y Default is 0.005

horizontalGrowFactor: 0.005,

verticalGrowFactor: 0.005

}

}

]

});

This results in the following behavior:

## Additional Properties

### Allow Panning in only one direction (X or Y)

Panning can be restricted to X or Y by setting the ZoomPanModifier.xyDirection📘 property.

### Allow Panning on only one X/Y axis

Panning can be restricted to a single X or Y axis by setting the ZoomPanModifier.xAxisId📘 or ZoomPanModifier.yAxisId📘 properties.

### Adjust Pinch Zooming / Scale Factor

The following is inherited from **PinchZoomModifier**

Horizontal and vertical pinch zoom scale factor can be adjusted via the following properties. The default value is set to `0.005`

.

### Include/Exclude Certain Axis from Pinch Zoom

The ZoomPanModifier allows you to include or exclude certain axis by axis.id from the pinch zoom operation.

By default all axis are included, to exclude one or more X or Y axis, set the following property:

- Exclude Axis

`// Exclude a specific axis from the pinch zoom operation`

zoomPanModifier.includeXAxis(axisXInstance, false);

zoomPanModifier.includeYAxis(axisYInstance, false);

// Include specific axis from the pinch zoom operation

zoomPanModifier.includeXAxis(axisXInstance, true);

zoomPanModifier.includeYAxis(axisYInstance, true);

// Reset flags

zoomPanModifier.includeAllAxes();

### Allow Pinch Zoom in only one direction

If you want to enable pinch zooming in only one direction, e.g. horizontal only, modify the ZoomPanModifier.verticalGrowFactor📘 to equal `0`

.