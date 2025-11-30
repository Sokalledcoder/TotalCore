---
source: https://www.scichart.com/documentation/js/v4/2d-charts/subcharts-api/sub-charts-positioning
scraped_at: 2025-11-28T18:24:52.607429
---

# https://www.scichart.com/documentation/js/v4/2d-charts/subcharts-api/sub-charts-positioning

# SubCharts Positioning

There are several modes that can be used to position a sub-surface, they are defined in the ECoordinateMode📘 enum.

By default, sub-surfaces use ECoordinateMode.Relative📘 for positioning. To change the coordinate mode use I2DSubSurfaceOptions.coordinateMode📘 or SciChartSubSurface.coordinateMode📘 property.

Note ECoordinateMode.DataValue📘 require axes to be present on the main surface and that they are specified as parent axes of the sub-surface.

Let's create a basic example to demonstrate this:

- TS
- Builder API (JSON Config)

`// Demonstrates how to use the Sub-Charts API to create child charts in a parent chart`

const {

SciChartSurface,

SciChartSubSurface,

NumericAxis,

FastLineRenderableSeries,

XyDataSeries,

SciChartJsNavyTheme,

Rect,

ECoordinateMode,

ESubSurfacePositionCoordinateMode,

ZoomPanModifier,

ZoomExtentsModifier,

MouseWheelZoomModifier,

EXyDirection,

NumberRange

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

// Function to add series to chart. This will be re-used for the parent and sub-charts

const addSeries = (sciChartSurface, stroke, x, y) => {

sciChartSurface.renderableSeries.add(

new FastLineRenderableSeries(wasmContext, {

stroke,

strokeThickness: 5,

dataSeries: new XyDataSeries(wasmContext, {

xValues: x,

yValues: y

}),

opacity: sciChartSurface.isSubSurface ? 0.5 : 1

})

);

};

// Create a parent (regular) SciChartSurface which will contain the sub-chart

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

// Create X,Y axis on the parent chart and programmatically zoom into part of the data

sciChartSurface.xAxes.add(

new NumericAxis(wasmContext, {

growBy: new NumberRange(0.1, 0.1)

})

);

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

growBy: new NumberRange(0.1, 0.1)

})

);

// Create a series on the parent chart

addSeries(sciChartSurface, "#FF6600", xValues, yValues);

addSeries(sciChartSurface, "#ae418d", xValues, yValues1);

addSeries(sciChartSurface, "#47bde6", xValues, yValues2);

// Add some interactivity to the parent chart

sciChartSurface.chartModifiers.add(new ZoomPanModifier({ xyDirection: EXyDirection.XDirection }));

sciChartSurface.chartModifiers.add(new MouseWheelZoomModifier({ xyDirection: EXyDirection.XDirection }));

sciChartSurface.chartModifiers.add(new ZoomExtentsModifier());

// Add a Sub-Charts to the main surface. This will display a rectangle showing the current zoomed in area on the parent chart

const subChart1 = SciChartSubSurface.createSubSurface(sciChartSurface, {

// Properties from I2DSubSurfaceOptions affect positioning and rendering of the subchart

position: new Rect(45, 0.2, 5, 0.2),

isTransparent: true,

isVisible: true,

coordinateMode: ESubSurfacePositionCoordinateMode.DataValue,

// However all properties from I2DSurfaceOptions are available

viewportBorder: { border: 3, color: "#77777777" },

background: "#333",

title: "Sub-chart Positioned at Data-Value",

titleStyle: { fontSize: 16, color: "#eeeeee77" }

});

// Add x,y axis to the subchart

subChart1.xAxes.add(new NumericAxis(wasmContext, { isVisible: false }));

subChart1.yAxes.add(new NumericAxis(wasmContext, { isVisible: false }));

addSeries(subChart1, "#FF6600", xValues, yValues);

addSeries(subChart1, "#ae418d", xValues, yValues1);

addSeries(subChart1, "#47bde6", xValues, yValues2);

// On the parent chart, programmatically zoom into a region

setTimeout(() => {

sciChartSurface.xAxes.get(0).animateVisibleRange(new NumberRange(30, 70), 1000);

sciChartSurface.yAxes.get(0).animateVisibleRange(new NumberRange(-0.4, 0.4), 1000);

}, 1000);

`// Demonstrates how to create a line chart with SciChart.js using the Builder API`

const {

chartBuilder,

ESeriesType,

EAxisType,

EThemeProviderType,

Rect,

ESubSurfacePositionCoordinateMode,

NumberRange,

EChart2DModifierType

} = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

// Main chart definition is here

xAxes: { type: EAxisType.NumericAxis },

yAxes: { type: EAxisType.NumericAxis },

series: [

{

type: ESeriesType.LineSeries,

xyData: {

xValues,

yValues: yValues1

},

options: {

stroke: "#0066FF",

strokeThickness: 5

}

}

],

modifiers: [

{ type: EChart2DModifierType.ZoomPan },

{ type: EChart2DModifierType.ZoomExtents },

{ type: EChart2DModifierType.MouseWheelZoom }

],

// Subchart definition is here

subCharts: [

{

surface: {

// Properties from I2DSubSurfaceOptions affect positioning and rendering of the subchart

position: new Rect(47, -0.2, 10, 0.2),

isTransparent: true,

isVisible: true,

coordinateMode: ESubSurfacePositionCoordinateMode.DataValue,

// However all properties from I2DSurfaceOptions are available

viewportBorder: { border: 3, color: "#77777777" },

background: "#333",

title: "2D Overview with Sub-Charts",

titleStyle: { fontSize: 16, color: "#eeeeee77" }

},

// Define the x,y axis on Subchart

xAxes: { type: EAxisType.NumericAxis, options: { isVisible: false } },

yAxes: { type: EAxisType.NumericAxis, options: { isVisible: false } },

// Define the series on Subchart

series: [

{

type: ESeriesType.LineSeries,

xyData: {

xValues,

yValues: yValues1

},

options: {

stroke: "#0066FF",

strokeThickness: 5

}

}

]

}

]

});

// On the parent chart, programmatically zoom into a region

setTimeout(() => {

sciChartSurface.xAxes.get(0).animateVisibleRange(new NumberRange(35, 65), 1000);

sciChartSurface.yAxes.get(0).animateVisibleRange(new NumberRange(-0.6, 0), 1000);

}, 1000);

This places a chart-within-a-chart at a specific DataValue.

## SubChart Positioning in Multi-Axis Scenarios

Next let's look at the case where we have a custom axis id or multiple axes on main surface.

Since positioning with ECoordinateMode.DataValue📘 depends on the axis visible ranges, we will have to specify which axis pair should be used for sub-surface position calculation.

To do this we can pass I2DSubSurfaceOptions.parentXAxisId📘 / I2DSubSurfaceOptions.parentYAxisId📘 via options or use SciChartSubSurface.parentXAxisId📘 / SciChartSubSurface.parentYAxisId📘 properties.

- TS
- Builder API (JSON Config)

`// Demonstrates how to use the Sub-Charts API to create child charts in a parent chart`

const {

SciChartSurface,

SciChartSubSurface,

NumericAxis,

FastLineRenderableSeries,

XyDataSeries,

SciChartJsNavyTheme,

Rect,

ECoordinateMode,

ESubSurfacePositionCoordinateMode,

ZoomPanModifier,

ZoomExtentsModifier,

MouseWheelZoomModifier,

NumberRange,

EAxisAlignment

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

// Function to add series to chart. This will be re-used for the parent and sub-charts

const addSeries = (sciChartSurface, stroke, x, y) => {

sciChartSurface.renderableSeries.add(

new FastLineRenderableSeries(wasmContext, {

stroke,

strokeThickness: 5,

dataSeries: new XyDataSeries(wasmContext, {

xValues: x,

yValues: y

}),

opacity: sciChartSurface.isSubSurface ? 0.5 : 1

})

);

};

// Create a parent (regular) SciChartSurface which will contain the sub-chart

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

// Create multiple X,Y axis on the parent chart and programmatically zoom into part of the data

sciChartSurface.xAxes.add(

new NumericAxis(wasmContext, {

growBy: new NumberRange(0.1, 0.1),

axisTitle: "XAxis Bottom"

})

);

sciChartSurface.xAxes.add(

new NumericAxis(wasmContext, {

id: "XAxisTop",

axisTitle: "XAxis Top",

axisAlignment: EAxisAlignment.Top

})

);

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

axisTitle: "YAxis Right",

growBy: new NumberRange(0.1, 0.1)

})

);

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

id: "YAxisLeft",

axisTitle: "YAxis Left",

axisAlignment: EAxisAlignment.Left

})

);

// Create a series on the parent chart

addSeries(sciChartSurface, "#FF6600", xValues, yValues);

addSeries(sciChartSurface, "#ae418d", xValues, yValues1);

addSeries(sciChartSurface, "#47bde6", xValues, yValues2);

// Add some interactivity to the parent chart

sciChartSurface.chartModifiers.add(new ZoomPanModifier());

sciChartSurface.chartModifiers.add(new MouseWheelZoomModifier());

sciChartSurface.chartModifiers.add(new ZoomExtentsModifier());

// Add a Sub-Charts to the main surface. This will display a rectangle showing the current zoomed in area on the parent chart

const subChart1 = SciChartSubSurface.createSubSurface(sciChartSurface, {

// Properties from I2DSubSurfaceOptions affect positioning and rendering of the subchart

position: new Rect(2, 8, 2, 2),

isTransparent: true,

isVisible: true,

coordinateMode: ESubSurfacePositionCoordinateMode.DataValue,

parentYAxisId: "YAxisLeft",

parentXAxisId: "XAxisTop",

// However all properties from I2DSurfaceOptions are available

viewportBorder: { border: 3, color: "#77777777" },

background: "#333",

title: "Sub-chart Positioned on Left/Top Axis",

titleStyle: { fontSize: 16, color: "#eeeeee77" }

});

// Add x,y axis to the subchart

subChart1.xAxes.add(new NumericAxis(wasmContext, { isVisible: false }));

subChart1.yAxes.add(new NumericAxis(wasmContext, { isVisible: false }));

addSeries(subChart1, "#FF6600", xValues, yValues);

addSeries(subChart1, "#ae418d", xValues, yValues1);

addSeries(subChart1, "#47bde6", xValues, yValues2);

// On the parent chart, programmatically zoom into a region

setTimeout(() => {

sciChartSurface.xAxes.get(0).animateVisibleRange(new NumberRange(30, 70), 1000);

sciChartSurface.yAxes.get(0).animateVisibleRange(new NumberRange(-0.4, 0.4), 1000);

}, 1000);

`// Demonstrates how to create a line chart with SciChart.js using the Builder API`

const {

chartBuilder,

ESeriesType,

EAxisType,

EThemeProviderType,

Rect,

ESubSurfacePositionCoordinateMode,

EAxisAlignment,

NumberRange,

EChart2DModifierType

} = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

// Main chart definition is here

xAxes: [

{ type: EAxisType.NumericAxis, options: { axisTitle: "XAxis Bottom" } },

{

type: EAxisType.NumericAxis,

options: {

id: "XAxisTop",

axisTitle: "XAxis Top",

axisAlignment: EAxisAlignment.Top

}

}

],

yAxes: [

{ type: EAxisType.NumericAxis, options: { axisTitle: "YAxis Right" } },

{

type: EAxisType.NumericAxis,

options: {

id: "YAxisLeft",

axisTitle: "YAxis Left",

axisAlignment: EAxisAlignment.Left

}

}

],

series: [

{

type: ESeriesType.LineSeries,

xyData: {

xValues,

yValues: yValues1

},

options: {

stroke: "#0066FF",

strokeThickness: 5

}

}

],

modifiers: [

{ type: EChart2DModifierType.ZoomPan },

{ type: EChart2DModifierType.ZoomExtents },

{ type: EChart2DModifierType.MouseWheelZoom }

],

// Subchart definition is here

subCharts: [

{

surface: {

// Properties from I2DSubSurfaceOptions affect positioning and rendering of the subchart

position: new Rect(2, 8, 2, 2),

isTransparent: true,

isVisible: true,

coordinateMode: ESubSurfacePositionCoordinateMode.DataValue,

parentYAxisId: "YAxisLeft",

parentXAxisId: "XAxisTop",

// However all properties from I2DSurfaceOptions are available

viewportBorder: { border: 3, color: "#77777777" },

background: "#333",

title: "Sub-chart Positioned on Left/Top Axis",

titleStyle: { fontSize: 16, color: "#eeeeee77" }

},

// Define the x,y axis on Subchart

xAxes: { type: EAxisType.NumericAxis, options: { isVisible: false } },

yAxes: { type: EAxisType.NumericAxis, options: { isVisible: false } },

// Define the series on Subchart

series: [

{

type: ESeriesType.LineSeries,

xyData: {

xValues,

yValues: yValues1

},

options: {

stroke: "#0066FF",

strokeThickness: 5

}

}

]

}

]

});

// On the parent chart, programmatically zoom into a region

setTimeout(() => {

sciChartSurface.xAxes.get(0).animateVisibleRange(new NumberRange(35, 65), 1000);

sciChartSurface.yAxes.get(0).animateVisibleRange(new NumberRange(-0.6, 0), 1000);

}, 1000);

This results in the following output:

## Updating SubChart Position

SciChart allows to change a sub-surface position dynamically using the SciChartSubSurface.subPosition��📘 property.

Let's demonstrate this by updating the coordinate mode and subPosition of the sub-chart from previous section

- TS
- Builder API (JSON Config)

`// Demonstrates how to use the Sub-Charts API to create child charts in a parent chart`

const {

SciChartSurface,

SciChartSubSurface,

NumericAxis,

FastLineRenderableSeries,

XyDataSeries,

SciChartJsNavyTheme,

Rect,

ECoordinateMode,

ESubSurfacePositionCoordinateMode,

ZoomPanModifier,

ZoomExtentsModifier,

MouseWheelZoomModifier,

NumberRange

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

// Function to add series to chart. This will be re-used for the parent and sub-charts

const addSeries = (sciChartSurface, stroke, x, y) => {

sciChartSurface.renderableSeries.add(

new FastLineRenderableSeries(wasmContext, {

stroke,

strokeThickness: 5,

dataSeries: new XyDataSeries(wasmContext, {

xValues: x,

yValues: y

}),

opacity: sciChartSurface.isSubSurface ? 0.5 : 1

})

);

};

// Create a parent (regular) SciChartSurface which will contain the sub-chart

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

// Create multiple X,Y axis on the parent chart and programmatically zoom into part of the data

sciChartSurface.xAxes.add(

new NumericAxis(wasmContext, {

growBy: new NumberRange(0.1, 0.1)

})

);

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

growBy: new NumberRange(0.1, 0.1)

})

);

// Create a series on the parent chart

addSeries(sciChartSurface, "#FF6600", xValues, yValues);

addSeries(sciChartSurface, "#ae418d", xValues, yValues1);

addSeries(sciChartSurface, "#47bde6", xValues, yValues2);

// Add some interactivity to the parent chart

sciChartSurface.chartModifiers.add(new ZoomPanModifier());

sciChartSurface.chartModifiers.add(new MouseWheelZoomModifier());

sciChartSurface.chartModifiers.add(new ZoomExtentsModifier());

// Add a Sub-Charts to the main surface. This will display a rectangle showing the current zoomed in area on the parent chart

const subChart1 = SciChartSubSurface.createSubSurface(sciChartSurface, {

// Properties from I2DSubSurfaceOptions affect positioning and rendering of the subchart

position: new Rect(0.1, 0.1, 0.1, 0.2),

isTransparent: true,

isVisible: true,

coordinateMode: ESubSurfacePositionCoordinateMode.Relative,

// However all properties from I2DSurfaceOptions are available

viewportBorder: { border: 3, color: "#77777777" },

background: "#333",

title: "Sub-chart Position with subPosition",

titleStyle: { fontSize: 16, color: "#eeeeee77" }

});

// Add x,y axis to the subchart

subChart1.xAxes.add(new NumericAxis(wasmContext, { isVisible: false }));

subChart1.yAxes.add(new NumericAxis(wasmContext, { isVisible: false }));

addSeries(subChart1, "#FF6600", xValues, yValues);

addSeries(subChart1, "#ae418d", xValues, yValues1);

addSeries(subChart1, "#47bde6", xValues, yValues2);

// On the parent chart, programmatically move the sub-chart to a new position

setTimeout(() => {

subChart1.subPosition = new Rect(0.75, 0.75, 0.1, 0.2);

}, 1000);

`// Demonstrates how to create a line chart with SciChart.js using the Builder API`

const {

chartBuilder,

ESeriesType,

EAxisType,

EThemeProviderType,

Rect,

ESubSurfacePositionCoordinateMode,

EChart2DModifierType

} = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

// Main chart definition is here

xAxes: [{ type: EAxisType.NumericAxis }],

yAxes: [{ type: EAxisType.NumericAxis }],

series: [

{

type: ESeriesType.LineSeries,

xyData: {

xValues,

yValues: yValues1

},

options: {

stroke: "#0066FF",

strokeThickness: 5

}

}

],

modifiers: [

{ type: EChart2DModifierType.ZoomPan },

{ type: EChart2DModifierType.ZoomExtents },

{ type: EChart2DModifierType.MouseWheelZoom }

],

// Subchart definition is here

subCharts: [

{

surface: {

// Properties from I2DSubSurfaceOptions affect positioning and rendering of the subchart

position: new Rect(0.1, 0.11, 0.1, 0.2),

isTransparent: true,

isVisible: true,

coordinateMode: ESubSurfacePositionCoordinateMode.Relative,

// However all properties from I2DSurfaceOptions are available

viewportBorder: { border: 3, color: "#77777777" },

background: "#333",

title: "Sub-chart Position with subPosition",

titleStyle: { fontSize: 16, color: "#eeeeee77" }

},

// Define the x,y axis on Subchart

xAxes: { type: EAxisType.NumericAxis, options: { isVisible: false } },

yAxes: { type: EAxisType.NumericAxis, options: { isVisible: false } },

// Define the series on Subchart

series: [

{

type: ESeriesType.LineSeries,

xyData: {

xValues,

yValues: yValues1

},

options: {

stroke: "#0066FF",

strokeThickness: 5

}

}

]

}

]

});

// On the parent chart, programmatically move the subchart with subPosition

setTimeout(() => {

sciChartSurface.subCharts.at(0).subPosition = new Rect(0.75, 0.75, 0.1, 0.2);

}, 1000);

This will move and update the SubChart position after 1-second (see the setTimeout call).