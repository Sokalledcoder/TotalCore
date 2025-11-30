---
source: https://www.scichart.com/documentation/js/v4/2d-charts/subcharts-api/subcharts-api-overview
scraped_at: 2025-11-28T18:24:52.971135
---

# https://www.scichart.com/documentation/js/v4/2d-charts/subcharts-api/subcharts-api-overview

# What is the SubCharts API?

The SubCharts API allows to place 1..N child SciChartSurfaces📘 within a parent chart (Charts within charts). It is possible to have multiple sub-charts within the main SciChartSurface.

## What is the Benefit of the SubCharts API?

SubCharts is an extremely powerful API that allows you to create dashboards or chart groups that share a single SciChartSurface, single WebGL canvas and engine instance.

- With the SubCharts API you can
**create a single chart with several nested chart panels**, enabling you to create components of single dashboards with one SciChartSurface parent that you can re-use throughout your app. - It's possible to
**dynamically position and resize SubCharts**on the main SciChartSurface, so you could create**dynamic multi-panel charts**such as in the financial industry or industrial process monitoring industry. **SubCharts are a huge performance boost**when many charts are used. For example, 100 charts created using SciChartSurface.create() will be far slower than 100 charts added to a single SciChartSurfaces using SubCharts.

It's possible with SubCharts to create very dashboards and re-usable multi-chart configurations, multi-chart groups while maintaining very high performance due to the WebGL canvas & context sharing nature of this API.

SubCharts API could be applied to display separate charts simultaneously on a single root element. The API allows to set a position, size , and styling of a sub-chart. Additionally it is possible to add custom HTML elements to the chart, which would be positioned accordingly to the chart layout flow.

## Overview of the SubCharts API

A sub-chart is represented by the SciChartSubSurface📘 class, which inherits SciChartSurface📘. Similarly to SciChartSurface📘 it has its own Axes, Modifiers, Renderable Series and Annotations.

You can add a sub-chart to a SciChartSurface by calling SciChartSubSurface.createSubSurface()📘. This returns a SciChartSubSurface📘 instance.

- SciChartSubSurface.createSubSurface()

`SciChartSubSurface.createSubSurface(parentSurface: ISciChartSurface, options?: I2DSubSurfaceOptions): SciChartSubSurface`

Parent sciChartSurface📘 must be passed, in addition I2DSubSurfaceOptions📘 may be passed to createSubSurface📘.

This interface has the following properties:

- I2DSubSurfaceOptions interface

`export interface I2DSubSurfaceOptions extends I2DSurfaceOptions {`

surfaceType?: ESciChartSurfaceType;

/**

* A rectangle defining the position and size of a subchart.

* If {@link coordinateMode} is Relative (the default) then the values give the size as a proportion of the parent div, and all properties must be between 0 and 1 inclusive.

* If {@link coordinateMode} is DataValue, values will be converted to coordinates using {@link parentXAxisId} and {@link parentYAxisId}. Subchart will be clpped to the parent SeriesViewRect

* Can only be set if this is a subChart. See {@link addSubChart}

*/

position?: TSubSurfacePosition;

/** An id or div element that will wrap the subchart. This can contain top, left, bottom and right section divs. The chart will shrink to fit the sections */

subChartContainerId?: string | HTMLDivElement;

/** Whether other surfaces, including the parent, will be visible underneath this surface */

isTransparent?: boolean;

/** Sets if the subchart is visible, allowing you to hide a subchart without removing it from the parent surface */

isVisible?: boolean;

/**

* Gets or sets the {@link TSubSurfaceCoordinateMode} used when calculating the actual position based on the {@link subPosition}.

* @default Relative

*/

coordinateMode?: TSubSurfaceCoordinateMode;

/**

* Sets the AxisId used to determing which X Axis should be used when calculating the actual position based on the {@link subPosition}

* if {@link coordinateMode} is DataValue

*/

parentXAxisId?: string;

/**

* Sets the AxisId used to determing which Y Axis should be used when calculating the actual position based on the {@link subPosition}

* if {@link coordinateMode} is DataValue

*/

parentYAxisId?: string;

/**

* Gets or sets scale property for all sections

*/

sectionScale?: number;

The return value of createSubSurface📘 is a SciChartSubSurface class. This inherits SciChartSurface but has additional properties, which can be found below.

- ISciChartSubSurface interface

`interface ISciChartSubSurface extends ISciChartSurface {`

/**

* The {@link HTMLDivElement} which is the dom sub-chart root

*/

readonly subChartContainer: HTMLDivElement;

/**

* The parent {@link ISciChartSurface}, if this is a subChart

*/

readonly parentSurface: ISciChartSurface;

/**

* Gets the adjusted padding between the SciChartSurface and its inner elements, in order top, right, bottom, left

* Defines a resulting padding accordingly to DPI scaling.

*/

readonly adjustedPadding: Thickness;

offset: Thickness | undefined;

topSectionClass: string;

leftSectionClass: string;

bottomSectionClass: string;

rightSectionClass: string;

/**

* Gets or Sets whether other surfaces, including the parent, will be visible underneath this surface

*/

isTransparent: boolean;

/**

* Gets or sets the {@link TSubSurfaceCoordinateMode} used when calculating the actual position based on the {@link subPosition}

*/

coordinateMode: TSubSurfaceCoordinateMode;

/**

* Gets or sets the parent chart AxisId used to determine which X Axis should be used when calculating the actual position based on the {@link subPosition}

* if {@link coordinateMode} is DataValue

*/

parentXAxisId: string;

/**

* Gets or sets the parent chart AxisId used to determine which Y Axis should be used when calculating the actual position based on the {@link subPosition}

* if {@link coordinateMode} is DataValue

*/

parentYAxisId: string;

/**

* A rectangle defining the position and size of a subchart.

* If {@link coordinateMode} is Relative (the default) then the values give the size as a proportion of the parent div, and all properties must be between 0 and 1 inclusive.

* If {@link coordinateMode} is DataValue, values will be converted to coordinates using {@link parentXAxisId} and {@link parentYAxisId}. Subchart will be clpped to the parent SeriesViewRect

* Can only be set if this is a subChart.

*/

subPosition: TSubSurfacePosition;

/**

* Gets or sets if the subchart is visible, allowing you to hide a subchart without removing it from the parent surface

*/

isVisible: boolean;

/**

* Gets or sets scale property for all sections

* It is necessary if the scale transformation is being used for html areas around the subchart

* For example, style = { width: "50%", transform: scale(2), transformOrigin: 'left top' }

*/

sectionScale: number;

/**

* Used internally

*/

backgroundFillBrushCache: BrushCache;

/**

* Recalculate the position of the subChart. Call if you update the size of html elements in the wrapper

*/

updateSubLayout(isDrawing?: boolean): void;

/**

* Gets the sub-chart container

*/

getSubChartContainer(): HTMLDivElement;

/** Gets the sub-chart rect on the parent surface. Defines the viewport size of the sub-surface.

* TThis rect is a subset of the {@link SciChartSubSurface.subPosition} considering the SubChart Wrapper content areas

*/

getSubChartRect(): Rect;

toJSON(excludeData: boolean): ISubChartDefinition;

}

## Basic Subchart Example (Charts within Charts)

Let's demonstrate a simple setup, where we define a sub-chart on a surface. For this we will start from defining a surface with some axes on it. On the surface we will create a sub-chart on a specified area.

- Subcharts

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

BoxAnnotation,

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

sciChartSurface.chartModifiers.add(new ZoomPanModifier());

sciChartSurface.chartModifiers.add(new MouseWheelZoomModifier());

sciChartSurface.chartModifiers.add(new ZoomExtentsModifier());

// Add a Sub-Charts to the main surface. This will display a rectangle showing the current zoomed in area on the parent chart

const subChart1 = SciChartSubSurface.createSubSurface(sciChartSurface, {

// Properties from I2DSubSurfaceOptions affect positioning and rendering of the subchart

position: new Rect(0.02, 0.02, 0.4, 0.4),

isTransparent: false,

isVisible: true,

coordinateMode: ESubSurfacePositionCoordinateMode.Relative,

// However all properties from I2DSurfaceOptions are available

viewportBorder: { border: 3, color: "#77777777" },

background: "#333",

title: "2D Overview with Sub-Charts",

titleStyle: { fontSize: 16, color: "#eeeeee77" }

});

// Add x,y axis to the subchart

subChart1.xAxes.add(new NumericAxis(wasmContext, { isVisible: false }));

subChart1.yAxes.add(new NumericAxis(wasmContext, { isVisible: false }));

addSeries(subChart1, "#FF6600", xValues, yValues);

addSeries(subChart1, "#ae418d", xValues, yValues1);

addSeries(subChart1, "#47bde6", xValues, yValues2);

// Add a BoxAnnotation to the SubChart

const boxAnnotation = new BoxAnnotation({

fill: "#FF660033",

stroke: "#FF6600",

strokeThickness: 2,

opacity: 0.5

});

subChart1.annotations.add(boxAnnotation);

// On parent chart zoom, pan, update the box annotation on the subchart

sciChartSurface.xAxes.get(0).visibleRangeChanged.subscribe(args => {

boxAnnotation.x1 = args.visibleRange.min;

boxAnnotation.x2 = args.visibleRange.max;

});

sciChartSurface.yAxes.get(0).visibleRangeChanged.subscribe(args => {

boxAnnotation.y1 = args.visibleRange.min;

boxAnnotation.y2 = args.visibleRange.max;

});

// On the parent chart, programmatically zoom into a region

setTimeout(() => {

sciChartSurface.xAxes.get(0).animateVisibleRange(new NumberRange(30, 70), 1000);

sciChartSurface.yAxes.get(0).animateVisibleRange(new NumberRange(-0.4, 0.4), 1000);

}, 1000);

In the example above we create a SciChartSurface📘 as normal and add some series to it. Then, we call createSubSurface📘 function, which contains a position property. The property defines a structure for specifying coordinates and sizes of a sub-chart. By default, the coordinates and size are treated as ratio values in range from 0 to 1, with a canvas viewport used as a base.

Next, we add some series to both the parent SciChartSurface📘 and the SciChartSubSurface📘. We subscribe to visibleRangeChanged📘 on the parent SciChartSurface x, y axis and use that to update a BoxAnnotation📘 in the SciChartSubSurface📘.

By creating this example, we have created a 2D viewport overview using the Sub-charts API, placing a child SciChartSubSurface📘 inside a parent SciChartSurface📘, and subscribed to interactivity on the parent chart. The Sub-chart shows all the data and where you have zoomed in on the parent chart, allowing you to get a view into your current position (zoom level and range) on the chart.

Try zooming the example with mouse-drag, panning, mousewheel and double-click to reset zoom to see the effect on the BoxAnnotation in the SciChartSubSurface.

## SubCharts with the Builder API

It is also possible to create a sub-chart via Builder API. For this pass an array of ISubChartDefinition📘 via ISciChart2DDefinition.subCharts📘 property.

For example, the following snippet will give us the same result as Basic Example setup:

- Subcharts builder API

`// Demonstrates how to create a line chart with SciChart.js using the Builder API`

const {

chartBuilder,

ESeriesType,

EAxisType,

EThemeProviderType,

Rect,

ECoordinateMode,

EAnnotationType,

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

position: new Rect(0.02, 0.02, 0.4, 0.4),

isTransparent: false,

isVisible: true,

coordinateMode: SciChart.ESubSurfacePositionCoordinateMode.Relative,

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

],

annotations: [

{

type: EAnnotationType.RenderContextBoxAnnotation,

options: {

fill: "#FF660033",

stroke: "#FF6600",

strokeThickness: 2,

opacity: 0.5

}

}

]

}

]

});

// On parent chart zoom, pan, update the box annotation on the subchart

const subChartBoxAnnotation = sciChartSurface.subCharts.at(0).annotations.get(0);

sciChartSurface.xAxes.get(0).visibleRangeChanged.subscribe(args => {

subChartBoxAnnotation.x1 = args.visibleRange.min;

subChartBoxAnnotation.x2 = args.visibleRange.max;

});

sciChartSurface.yAxes.get(0).visibleRangeChanged.subscribe(args => {

subChartBoxAnnotation.y1 = args.visibleRange.min;

subChartBoxAnnotation.y2 = args.visibleRange.max;

});

// On the parent chart, programmatically zoom into a region

setTimeout(() => {

sciChartSurface.xAxes.get(0).animateVisibleRange(new NumberRange(30, 70), 1000);

sciChartSurface.yAxes.get(0).animateVisibleRange(new NumberRange(-0.4, 0.4), 1000);

}, 1000);

The Builder API demo of SubCharts works very similarly to the javascript-API version. A SubChart is declared via the subCharts📘 property of the chart ISciChart2DDefinition📘, and axis, series, interactions can be added to it as before. You can access the SubChart and any of it's created properties via the SciChartSurface.subCharts📘 property.

## Other ways to set SubChart position

The subPosition📘 property supports 3 formats of coordinates:

`TXywhCoordinates: {x, y, width, height}`

`TLtrbCoordinates: {left, top, right, bottom}`

`TEdgeCoordinates: {x1, y1, x2, y2}`

Each of the coordinates could be assigned to use different coordinate modes.

- TS
- JS

`const subChart1 = SciChartSubSurface.createSubSurface(sciChartSurface, {`

position: { x: 0.1, y: 0.1, width: 0.4, height: 0.3 },

isTransparent: false,

coordinateMode: ESubSurfacePositionCoordinateMode.Relative,

title: "SubChart 1",

titleStyle

});

subChart1.xAxes.add(new NumericAxis(wasmContext));

subChart1.yAxes.add(new NumericAxis(wasmContext));

const subChart2 = SciChartSubSurface.createSubSurface(sciChartSurface, {

position: { left: 600, right: 900, top: 100, bottom: 300 },

isTransparent: false,

coordinateMode: [ESubSurfacePositionCoordinateMode.Pixel, ESubSurfacePositionCoordinateMode.Pixel],

title: "SubChart 2",

titleStyle

});

subChart2.xAxes.add(new NumericAxis(wasmContext));

subChart2.yAxes.add(new NumericAxis(wasmContext));

const subChart3 = SciChartSubSurface.createSubSurface(sciChartSurface, {

position: { x1: 6, x2: 9, y1: 6, y2: 2 },

isTransparent: false,

coordinateMode: [

ESubSurfacePositionCoordinateMode.DataValue,

ESubSurfacePositionCoordinateMode.DataValue,

ESubSurfacePositionCoordinateMode.DataValue,

ESubSurfacePositionCoordinateMode.DataValue

],

title: "SubChart 3",

titleStyle

});

subChart3.xAxes.add(new NumericAxis(wasmContext));

subChart3.yAxes.add(new NumericAxis(wasmContext));

`const subChart1 = SciChartSubSurface.createSubSurface(sciChartSurface, {`

position: { x: 0.1, y: 0.1, width: 0.4, height: 0.3 },

isTransparent: false,

coordinateMode: ESubSurfacePositionCoordinateMode.Relative,

title: "SubChart 1",

titleStyle

});

subChart1.xAxes.add(new NumericAxis(wasmContext));

subChart1.yAxes.add(new NumericAxis(wasmContext));

const subChart2 = SciChartSubSurface.createSubSurface(sciChartSurface, {

position: { left: 600, right: 900, top: 100, bottom: 300 },

isTransparent: false,

coordinateMode: [ESubSurfacePositionCoordinateMode.Pixel, ESubSurfacePositionCoordinateMode.Pixel],

title: "SubChart 2",

titleStyle

});

subChart2.xAxes.add(new NumericAxis(wasmContext));

subChart2.yAxes.add(new NumericAxis(wasmContext));

const subChart3 = SciChartSubSurface.createSubSurface(sciChartSurface, {

position: { x1: 6, x2: 9, y1: 6, y2: 2 },

isTransparent: false,

coordinateMode: [

ESubSurfacePositionCoordinateMode.DataValue,

ESubSurfacePositionCoordinateMode.DataValue,

ESubSurfacePositionCoordinateMode.DataValue,

ESubSurfacePositionCoordinateMode.DataValue

],

title: "SubChart 3",

titleStyle

});

subChart3.xAxes.add(new NumericAxis(wasmContext));

subChart3.yAxes.add(new NumericAxis(wasmContext));