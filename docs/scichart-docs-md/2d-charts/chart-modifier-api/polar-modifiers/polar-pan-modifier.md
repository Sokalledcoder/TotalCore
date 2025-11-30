---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/polar-modifiers/polar-pan-modifier
scraped_at: 2025-11-28T18:24:17.045036
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/polar-modifiers/polar-pan-modifier

# PolarPanModifier

The PolarPanModifier📘 is a modifier that allows users to pan (drag) the polar chart. This modifier is useful for enhancing the user experience by providing an intuitive way to navigate through the chart data.

tip

You can set the primaryPanMode📘 to `EPolarPanModifierPanMode.Cartesian`

to pan the chart in Cartesian coordinates, or keep it to either `EPolarPanModifierPanMode.PolarStartAngle`

or `EPolarPanModifierPanMode.PolarVisibleRange`

to pan the chart in polar coordinates.

- TS
- Builder API (JSON Config)

`const { PolarPanModifier, EPolarPanModifierPanMode } = SciChart;`

// or for npm: import { PolarPanModifier } from "scichart";

// Add PolarPanModifier behaviour to the chart

sciChartSurface.chartModifiers.add(

new PolarPanModifier({

primaryPanMode: EPolarPanModifierPanMode.PolarVisibleRange,

secondaryPanMode: EPolarPanModifierPanMode.Cartesian,

secondaryExecuteCondition: {

key: SciChart.EModifierMouseArgKey.Ctrl

}

}),

);

`// Demonstrates how to configure the PolarPanModifier in SciChart.js using the Builder API`

const {

chartBuilder,

EThemeProviderType,

EAxisType,

EChart2DModifierType,

EActionType,

EPolarAxisMode

} = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DPolarChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: {

type: EAxisType.PolarNumericAxis,

options: { polarAxisMode: EPolarAxisMode.Angular }

},

yAxes: {

type: EAxisType.PolarNumericAxis,

options: { polarAxisMode: EPolarAxisMode.Radial }

},

modifiers: [

{

type: EChart2DModifierType.PolarPan,

options: {

growFactor: 0.002,

zoomSize: false,

}

}

]

});

This results in the following behavior: