---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/multi-axis-and-layout/central-axis-layout
scraped_at: 2025-11-28T18:24:10.053318
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/multi-axis-and-layout/central-axis-layout

# Central Axis Layout

Placing Axis in the center the chart, like an oscilloscope or spectrum analyzer is possible with SciChart.js.

To do this, use the CentralAxesLayoutManager📘 applied to the SciChartSurface.LayoutManager📘 property.

Here's a code sample:

- TS
- Builder API (JSON Config)

`// Demonstrates how to configure a central axis in SciChart.js`

const { SciChartSurface, NumericAxis, SciChartJsNavyTheme, CentralAxesLayoutManager } = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

// Apply the CentralAxesLayoutManager to the SciChartSurface

sciChartSurface.layoutManager = new CentralAxesLayoutManager();

// Add an X, Y Axis

sciChartSurface.xAxes.add(

new NumericAxis(wasmContext, {

// To allow easier visualisation of axis position

backgroundColor: "#50C7E022",

axisBorder: {

borderTop: 1,

color: "#50C7E0"

}

})

);

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

// To allow easier visualisation of axis position

backgroundColor: "#F4842022",

axisBorder: {

borderRight: 1,

color: "#F48420"

}

})

);

`// Demonstrates how to configure a central axis in SciChart.js using the Builder API`

const { chartBuilder, EThemeProviderType, EAxisType, ELayoutManagerType } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: {

theme: { type: EThemeProviderType.Dark },

layoutManager: { type: ELayoutManagerType.CentralAxes }

},

xAxes: {

type: EAxisType.NumericAxis,

options: {

// To allow easier visualisation of axis position

backgroundColor: "#50C7E022",

axisBorder: {

borderTop: 1,

color: "#50C7E0"

}

}

},

yAxes: {

type: EAxisType.NumericAxis,

options: {

// To allow easier visualisation of axis position

backgroundColor: "#F4842022",

axisBorder: {

borderRight: 1,

color: "#F48420"

}

}

}

});

This results in the following output:

## Configure the Position of Central Axis

CentralAxesLayoutManager📘 has some options you can use to configure the position of the horizontal and vertical axes.

The following code places an YAxis inside the chart at X=3 and an XAxis inside the chart at Y=100 pixels.

tip

Options available in the EInnerAxisPlacementCoordinateMode📘 enum include: DataValue, Pixel, or Relative, which allows placement of an axis at a fraction of the viewport from 0..1.

- TS
- Builder API (JSON Config)

`// Apply the CentralAxesLayoutManager to the SciChartSurface`

sciChartSurface.layoutManager = new CentralAxesLayoutManager({

horizontalAxisPositionCoordinateMode: EInnerAxisPlacementCoordinateMode.DataValue,

verticalAxisPositionCoordinateMode: EInnerAxisPlacementCoordinateMode.Pixel,

horizontalAxisPosition: 3,

verticalAxisPosition: 100

});

// Continue to add your X,Y axis as before

`const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {`

surface: {

theme: { type: EThemeProviderType.Dark },

layoutManager: {

type: ELayoutManagerType.CentralAxes,

options: {

horizontalAxisPositionCoordinateMode: EInnerAxisPlacementCoordinateMode.DataValue,

verticalAxisPositionCoordinateMode: EInnerAxisPlacementCoordinateMode.Pixel,

horizontalAxisPosition: 3,

verticalAxisPosition: 100

}

}

},

// etc...

This results in the following output: