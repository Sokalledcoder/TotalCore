---
source: https://www.scichart.com/documentation/js/v4/2d-charts/subcharts-api/polar-and-cartesian-sub-charts
scraped_at: 2025-11-28T18:24:51.652688
---

# https://www.scichart.com/documentation/js/v4/2d-charts/subcharts-api/polar-and-cartesian-sub-charts

# Combining Polar and Cartesian Charts

It is possible to combine both Polar and Cartesian chart. You will find the example below.

- TS

`import {`

EAxisAlignment,

EColor,

ESubSurfacePositionCoordinateMode,

EllipsePointMarker,

EPolarAxisMode,

FastLineRenderableSeries,

I2DSubSurfaceOptions,

MouseWheelZoomModifier,

NumericAxis,

PolarLineRenderableSeries,

PolarMouseWheelZoomModifier,

PolarNumericAxis,

PolarZoomExtentsModifier,

Rect,

SciChartPolarSubSurface,

SciChartSubSurface,

SciChartSurface,

XyDataSeries,

ZoomExtentsModifier

} from "scichart";

async function polarAndCartesianSubCharts(divElementId: string) {

const { sciChartSurface, wasmContext } = await SciChartSurface.create(divElementId, {

title: "Cartesian Root Chart"

});

sciChartSurface.renderNativeAxisLabelsImmediately = true;

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

// Add Cartesian SubChart

const cartesianSubChartOptions: I2DSubSurfaceOptions = {

isTransparent: false,

id: "subChart-1",

coordinateMode: ESubSurfacePositionCoordinateMode.Relative,

position: new Rect(0, 0.5, 0.5, 0.5),

title: "Sub Chart 1"

};

const cartesianSubChart = SciChartSubSurface.createSubSurface(sciChartSurface, cartesianSubChartOptions);

cartesianSubChart.xAxes.add(new NumericAxis(wasmContext));

cartesianSubChart.yAxes.add(new NumericAxis(wasmContext));

cartesianSubChart.renderableSeries.add(

new FastLineRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: [1, 2, 3],

yValues: [1, 2, 3]

})

})

);

cartesianSubChart.chartModifiers.add(new MouseWheelZoomModifier());

cartesianSubChart.chartModifiers.add(new ZoomExtentsModifier());

// Add Polar SubChart

const polarSubChartOptions: I2DSubSurfaceOptions = {

isTransparent: false,

id: "subChart-2",

coordinateMode: ESubSurfacePositionCoordinateMode.Relative,

position: new Rect(0.5, 0.5, 0.5, 0.5),

title: "Sub Chart 2"

};

const polarSubChart = SciChartPolarSubSurface.createSubSurface(sciChartSurface, polarSubChartOptions);

const dataSeries = new XyDataSeries(wasmContext, {

xValues: [0, 1, 3, 4, 5, 6, 7],

yValues: [1, 2, 3, 4, 4, 6, 7]

});

const angularXAxis = new PolarNumericAxis(wasmContext, {

axisAlignment: EAxisAlignment.Top,

polarAxisMode: EPolarAxisMode.Angular,

majorGridLineStyle: { strokeThickness: 1, color: "AAAAAA22" }

});

polarSubChart.xAxes.add(angularXAxis);

const radialYAxis = new PolarNumericAxis(wasmContext, {

axisAlignment: EAxisAlignment.Right,

polarAxisMode: EPolarAxisMode.Radial,

labelPrecision: 0,

drawMinorGridLines: false,

majorGridLineStyle: { strokeThickness: 1, color: "AAAAAAAA" }

});

polarSubChart.yAxes.add(radialYAxis);

const polarlineSeries = new PolarLineRenderableSeries(wasmContext, {

stroke: EColor.Orange,

pointMarker: new EllipsePointMarker(wasmContext, { height: 10, width: 10 }),

dataSeries,

strokeThickness: 3

});

polarSubChart.renderableSeries.add(polarlineSeries);

polarSubChart.chartModifiers.add(new PolarMouseWheelZoomModifier());

polarSubChart.chartModifiers.add(new PolarZoomExtentsModifier());

return sciChartSurface;

}

polarAndCartesianSubCharts("scichart-root");

First we create the root chart. It could be either Cartesian📘 or Polar📘. In our example we are using the Cartesian one.

Next we create a Cartesian SubChart by using SciChartSubSurface.createSubSurface()📘 static method.

Finally we add a Polar SubChart by using SciChartSubSurface.createSubSurface()📘.

This gives us a parent chart and two sub-charts each taking 1/4 of the parent chart area, with Cartesian sub-chart at the bottom-left and Polar sub-chart at the bottom-right.

If you do mouse wheel or double click on a sub-chart you will see that they are fully interactive. This is thank to MouseWheelZoomModifier📘, ZoomExtentsModifier📘, PolarMouseWheelZoomModifier📘 and PolarZoomExtentsModifier📘 chart modifiers.

If you need information on positioning or transparency please refer these documents SubChart Positioning and SubChart Surface Transparency.