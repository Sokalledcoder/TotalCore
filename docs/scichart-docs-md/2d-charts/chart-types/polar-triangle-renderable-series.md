---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/polar-triangle-renderable-series
scraped_at: 2025-11-28T18:24:42.713879
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/polar-triangle-renderable-series

# The Polar Triangle Series Type

The PolarTriangleRenderableSeries📘 creates triangle strips / lists or polyongs in a polar coordinate system, allowing for flexible data visualization in polar charts. This is useful for creating radar charts, polar area charts, or any custom triangular visualizations.

## Creating a Polar Triangle Series

To create a chart using PolarTriangleRenderableSeries📘 you can use use the following code.

- TS

`const radialYAxis = new PolarNumericAxis(wasmContext, {`

polarAxisMode: EPolarAxisMode.Radial

});

sciChartSurface.yAxes.add(radialYAxis);

const angularXAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Angular

});

sciChartSurface.xAxes.add(angularXAxis);

const trianglesX = [

[566.0, 551.0, 581.0],

[529.0, 514.0, 544.0],

[483.0, 468.0, 498.0],

[445.0, 430.0, 460.0],

[409.0, 394.0, 424.0],

[399.0, 384.0, 414.0],

[401.0, 386.0, 416.0],

[412.0, 397.0, 427.0],

[437.0, 422.0, 452.0],

[473.0, 458.0, 488.0],

[527.0, 512.0, 542.0],

[574.0, 559.0, 589.0]

].flat(); // xValues and yValues take an array of numbers, and we are using an array of arrays just for readability reasons

const trianglesY = [

[296.32, 270.34, 270.34],

[309.32, 283.34, 283.34],

[309.32, 283.34, 283.34],

[291.32, 265.34, 265.34],

[267.32, 241.34, 241.34],

[225.32, 199.34, 199.34],

[184.32, 158.34, 158.34],

[146.32, 120.34, 120.34],

[108.32, 82.34, 82.34],

[94.32, 68.34, 68.34],

[94.32, 68.34, 68.34],

[107.32, 81.34, 81.34]

].flat();

const triangle = new PolarTriangleRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, {

xValues: trianglesX,

yValues: trianglesY

}),

fill: "cornflowerblue",

opacity: 0.6,

drawMode: ETriangleSeriesDrawMode.List

});

sciChartSurface.renderableSeries.add(triangle);

## Polar Map Example

tip

The JavaScript Polar Map Example using the `PolarTriangleRenderableSeries`

can be found in the SciChart.Js Examples Suite > Polar Map Example on Github, or our live demo at scichart.com/demo.

Above: The JavaScript Polar Map Example example from the SciChart.js Demo