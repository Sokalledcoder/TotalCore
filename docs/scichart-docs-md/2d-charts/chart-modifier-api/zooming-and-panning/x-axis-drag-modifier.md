---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/zooming-and-panning/x-axis-drag-modifier
scraped_at: 2025-11-28T18:24:20.228189
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/zooming-and-panning/x-axis-drag-modifier

# XAxisDragModifier

SciChart.js provides an zooming / panning behavior when dragging the Axis via the XAxisDragModifier📘, available out of the box.

Besides common features which are inherited from the ChartModifierBase class, the XAxisDragModifier📘 allows you to choose panning or scaling via the dragMode📘 property.

## Adding a XAxisDragModifier to a Chart

A XAxisDragModifier📘 can be added to the sciChartSurface.chartModifiers📘 collection to enable scaling or panning behavior. For example:

- TS
- Builder API (JSON Config)

`import { XAxisDragModifier, EDragMode } from "scichart";`

// Add XAxis Drag behavior

sciChartSurface.chartModifiers.add(

new XAxisDragModifier({

dragMode: EDragMode.Scaling,

})

);

`// Demonstrates how to configure the XAxisDrag Modifier in SciChart.js using the Builder API`

const { chartBuilder, EChart2DModifierType, EDragMode } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

modifiers: [

{

type: EChart2DModifierType.XAxisDrag,

options: {

dragMode: EDragMode.Scaling,

}

}

]

});

This results in the following behavior:

X and Y Axis Drag Modifier GIF