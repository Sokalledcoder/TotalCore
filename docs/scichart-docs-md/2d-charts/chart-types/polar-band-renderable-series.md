---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/polar-band-renderable-series
scraped_at: 2025-11-28T18:24:40.474917
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/polar-band-renderable-series

# The Polar Band Series Type

The PolarBandRenderableSeries📘 creates a band or area between two polar curves, displaying the relationship between two sets of yValues on a polar coordinate system.

The JavaScript Polar Band Chart can be found in the SciChart.Js Examples Suite > Polar Band Chart on Github, or our live demo at scichart.com/demo.

Some of IPolarBandRenderableSeriesOptions📘's key properties include:

- dataSeries📘 - The XyyDataSeries📘 containing
`xValues`

,`yValues`

, and`y1Values`

arrays. - fill📘 - Fill color where Y is greater than Y1
- fillY1📘 - Fill color where Y1 is greater than Y
- stroke📘 - Stroke color for the Y line
- strokeY1📘 - Stroke color for the Y1 line
- strokeThickness📘 - Thickness of the stroke lines
- interpolateLine📘 - When true, line segments draw as arcs instead of straight lines
- scaleGradientToYRange📘 - Controls gradient scaling behavior for radial axis
- fillLinearGradient📘 - Linear gradient params where Y is greater than Y1
- fillLinearGradientY1📘 - Linear gradient params where Y1 is greater than Y
- paletteProvider📘 - Custom coloring provider for dynamic styling

## Examples

### Basic Polar Band Series

`const { sciChartSurface, wasmContext } = await SciChartPolarSurface.create(divElementId, {`

theme: new SciChartJsNavyTheme()

});

const angularXAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Angular,

visibleRange: new NumberRange(0, 8),

drawMinorGridLines: false

});

sciChartSurface.xAxes.add(angularXAxis);

const radialYAxis = new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Radial,

drawMinorGridLines: false,

labelPrecision: 0,

autoTicks: false,

majorDelta: 1,

innerRadius: 0.2

});

sciChartSurface.yAxes.add(radialYAxis);

// Define the polar band series

const baiscBand = new PolarBandRenderableSeries(wasmContext, {

dataSeries: new XyyDataSeries(wasmContext, {

xValues: [0, 1, 3, 4, 5, 6],

yValues: [1, 2, 3, 4, 5, 6],

y1Values: [6, 5, 1, 5, 4, 2]

}),

stroke: "rgba(200,200,30,1)", // yellow

fill: "rgba(200,200,30,0.3)", // thin yellow

strokeY1: "rgba(200,120,160,1)", // pink

fillY1: "rgba(200,120,160,0.3)", // thin pink

strokeThickness: 4,

interpolateLine: false

});

sciChartSurface.renderableSeries.add(baiscBand);

In the code above:

- 2 Polar Band Series instances are created and added to the
`sciChartSurface.renderableSeries`

collection. - We set the stroke📘, strokeY1📘 for the yValues and y1Values respectively, and then fill📘 and fillY1📘, for when
`Y > Y1`

and vice versa. - We assign an XyyDataSeries📘 which stores X, Y and Y1 value arrays.

### Gradient Fills in Polar Band Series

To use Gradient Fills with a PolarBandRenderableSeries📘, you need to set the fillLinearGradient📘 & fillLinearGradientY1📘 properties with a GradientParams📘 object: a type which defines gradients by a number of TGradientStop📘 objects inside an array and a start and end Point📘.

`const gradientBand = new PolarBandRenderableSeries(wasmContext, {`

dataSeries: new XyyDataSeries(wasmContext, {

xValues: [0, 1, 2, 3, 4, 5],

yValues: [7, 4, 1, 5, 6, 7],

y1Values: [2, 5, 7, 3, 8, 2]

}),

stroke: "white",

strokeY1: "white",

strokeThickness: 2,

fillLinearGradient: new GradientParams(new Point(0, 0), new Point(0, 1), [

{ color: "#FF9999", offset: 0 },

{ color: "#FF2222", offset: 1 }

]),

// This one is for gradient where Y1 values are greater than Y2 values

fillLinearGradientY1: new GradientParams(new Point(0, 0), new Point(0, 1), [

{ color: "#2222FF", offset: 0 },

{ color: "#9999FF", offset: 1 }

]),

interpolateLine: true,

scaleGradientToYRange: false // set to true to have global gradient depending on Y axis range

});

sciChartSurface.renderableSeries.add(gradientBand);

In the code above:

- We create a GradientParams📘 object with 2 gradient stops, and set the start and end points of the gradient.
- We set scaleGradientToYRange📘 to
`true`

to make the gradient scale to the Y range of the data for each band segment. - The interpolateLine📘 flag is set to
`true`

to make the band wrap around the angular axes in a circular fashion.

### PaletteProvider for Polar Band Series

By extending DefaultPaletteProvider📘 you can create a custom palette for your Polar Band Series, to achieve dynamic coloring based on data values. See more about this topic here Palette Provider API - Polar Band Series.