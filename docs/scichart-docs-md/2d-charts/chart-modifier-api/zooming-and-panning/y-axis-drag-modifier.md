---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/zooming-and-panning/y-axis-drag-modifier
scraped_at: 2025-11-28T18:24:20.345158
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/zooming-and-panning/y-axis-drag-modifier

# YAxisDragModifier

SciChart.js provides an zooming / panning behavior when dragging the Axis via the YAxisDragModifier📘, available out of the box.

Besides common features which are inherited from the ChartModifierBase class, the YAxisDragModifier📘 allows you to choose panning or scaling via the dragMode📘 property.

## Adding a YAxisDragModifier to a Chart

A YAxisDragModifier📘 can be added to the sciChartSurface.chartModifiers📘 collection to enable scaling or panning behavior. For example:

- TS
- Builder API (JSON Config)

`import { YAxisDragModifier, EDragMode } from "scichart";`

// Add YAxis Drag behavior

sciChartSurface.chartModifiers.add(

new YAxisDragModifier({

dragMode: EDragMode.Scaling,

})

);

`// Demonstrates how to configure the YAxisDrag Modifier in SciChart.js using the Builder API`

const { chartBuilder, EChart2DModifierType, EDragMode } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

modifiers: [

{

type: EChart2DModifierType.YAxisDrag,

options: {

dragMode: EDragMode.Scaling,

}

}

]

});

This results in the following behavior:

X and Y Axis Drag Modifier GIF