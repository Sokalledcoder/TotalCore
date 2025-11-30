---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/polar-modifiers/polar-mouse-wheel-zoom-modifier
scraped_at: 2025-11-28T18:24:17.243124
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/polar-modifiers/polar-mouse-wheel-zoom-modifier

# PolarMouseWheelZoomModifier

The PolarMouseWheelZoomModifier📘 is special a modifier that allows users to interact with the polar chart in 2 major ways:

## 1. Zooming in and out, using `EActionType.Zoom`

(default)

- TS
- Builder API (JSON Config)

`const { PolarMouseWheelZoomModifier, EActionType } = SciChart;`

// or for npm: import { PolarMouseWheelZoomModifier, EActionType } from "scichart";

// Add PolarMouseWheelZoomModifier behaviour to the chart

sciChartSurface.chartModifiers.add(

new PolarMouseWheelZoomModifier({

growFactor: 0.002,

zoomSize: false,

defaultActionType: EActionType.Zoom // DEFAULT value -> for zooming / scaling the polar chart

// defaultActionType: EActionType.Pan // secondary value -> pans / spins the polar chart

}),

);

`// Demonstrates how to configure the PolarMouseWheelZoomModifier in SciChart.js using the Builder API`

const {

chartBuilder,

EThemeProviderType,

EAxisType,

EChart2DModifierType,

EPolarAxisMode,

ESeriesType,

EActionType

} = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DPolarChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: {

type: EAxisType.PolarNumericAxis,

options: {

polarAxisMode: EPolarAxisMode.Angular

}

},

yAxes: {

type: EAxisType.PolarNumericAxis,

options: {

polarAxisMode: EPolarAxisMode.Radial

}

},

series: {

type: ESeriesType.PolarBandSeries,

options: {

strokeThickness: 3,

},

xyyData: {

xValues: Array.from({ length: 12 }, (_, i) => i),

yValues: Array.from({ length: 12 }, (_, i) => Math.sin(i * 0.2)),

y1Values: Array.from({ length: 12 }, (_, i) => Math.cos(i * 0.2))

}

},

modifiers: [

{

type: EChart2DModifierType.PolarMouseWheelZoom,

options: {

growFactor: 0.002,

zoomSize: false,

defaultActionType: EActionType.Zoom

}

}

]

});

This will result in the following behavior:

## 2. Panning / Spinning the chart, with `EActionType.Pan`

- TS

`const { PolarMouseWheelZoomModifier, EActionType } = SciChart;`

// or for npm: import { PolarMouseWheelZoomModifier, EActionType } from "scichart";

// Add PolarMouseWheelZoomModifier behaviour to the chart

sciChartSurface.chartModifiers.add(

new PolarMouseWheelZoomModifier({

growFactor: 0.002,

zoomSize: false,

defaultActionType: EActionType.Pan

}),

);

Which will result in this:

- use whichever configuration you prefer, depending on the desired interaction with the polar chart.