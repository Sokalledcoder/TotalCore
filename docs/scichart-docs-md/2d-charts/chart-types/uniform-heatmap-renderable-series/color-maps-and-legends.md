---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/uniform-heatmap-renderable-series/color-maps-and-legends
scraped_at: 2025-11-28T18:24:46.055008
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/uniform-heatmap-renderable-series/color-maps-and-legends

# Heatmap ColorMaps and Legends

## Converting Data-Values to Colors (Defining a Color Map)

Conversion of data value into color is defined by the property UniformHeatmapRenderableSeries.colorMap📘. The ColorMap is type HeatmapColorPalette📘. You can define a custom Color Palette in JavaScript as follows:

- TS

`// Create a Heatmap RenderableSeries with the color map. ColorMap.minimum/maximum defines the values in`

// HeatmapDataSeries which correspond to gradient stops at 0..1

const heatmapSeries = new UniformHeatmapRenderableSeries(wasmContext, {

dataSeries: heatmapDataSeries,

useLinearTextureFiltering: false,

fillValuesOutOfRange: true,

colorMap: new HeatmapColorMap({

minimum: 0,

maximum: 200,

gradientStops: [

{ offset: 1, color: "#EC0F6C" },

{ offset: 0.9, color: "#F48420" },

{ offset: 0.7, color: "#DC7969" },

{ offset: 0.5, color: "#67BDAF" },

{ offset: 0.3, color: "#50C7E0" },

{ offset: 0.2, color: "#264B9377" }, // Start to fade out the transparency here

{ offset: 0, color: "Transparent" } // Set the zero value as Transparent. Corresponds to zValue <= minimum

]

})

});

sciChartSurface.renderableSeries.add(heatmapSeries);

What this means:

- The GradientStop at
`Offset = 0`

with`Color = "Transparent"`

corresponds to the HeatmapColorMap.minimum📘 value of`0`

- The GradientStop at
`Offset = 1`

with`Color = "#EC0F6C"`

corresponds to HeatmapColorMap.maximum📘 value of`200`

. - Data within this range will be blended according to the gradient stops between
`0`

and`1`

- Data outside this range will be clamped to the minimum or maximum colors in the HeatmapColorMap📘

### Defining how Data-values outside of ColorMap range are drawn

By default, when defining a HeatmapColorMap📘 any values that fall outside the range are clipped to the edges of the colormap. e.g. in the above example data falling outside of the range `0-200`

is clipped to color `"#000000"`

and `"#EC0F6C"`

respectively.

There is also a fillValuesOutOfRange📘 property which defines how the values outside the range are treated. Either clamped to the min/max color or drawn as transparent.

## Heatmap Legends

A heatmap legend may be generated with the HeatmapLegend📘 class. It is placed in a element just like a SciChartSurface. It will expand to fit the parent div.

The constructor accepts IHeatmapLegendOptions📘 which lets you specify theme, colorMap and yAxisOptions. This allows configuration of the appearance of the heatmap legend. See these are the TypeDoc documentation📘 for this type.

Here's a full code sample below.

- TS

`const { HeatmapLegend, SciChartJsNavyTheme } = SciChart;`

const { heatmapLegend, wasmContext } = await HeatmapLegend.create(divElementId, {

theme: {

...new SciChartJsNavyTheme(),

sciChartBackground: "#14233CBB",

loadingAnimationBackground: "#14233CBB"

},

yAxisOptions: {

axisBorder: {

borderLeft: 1,

color: "#FFFFFF77"

},

majorTickLineStyle: {

color: "White",

tickSize: 6,

strokeThickness: 1

},

minorTickLineStyle: {

color: "White",

tickSize: 3,

strokeThickness: 1

}

},

colorMap: {

minimum: 0,

maximum: 200,

gradientStops: [

{ offset: 1, color: "#EC0F6C" },

{ offset: 0.9, color: "#F48420" },

{ offset: 0.7, color: "#DC7969" },

{ offset: 0.5, color: "#67BDAF" },

{ offset: 0.3, color: "#50C7E0" },

{ offset: 0.2, color: "#264B9377" }, // Start to fade out the transparency here

{ offset: 0, color: "Transparent" } // Set the zero value as Transparent. Corresponds to zValue <= minimum

]

}

});

### Defining the ColorMap on the HeatmapLegend control

ColorMaps obey similar rules to Heatmap series (see above).

### Styling the Axis on the HeatmapLegend control

yAxisOptions is type IAxisBase2dOptions📘. This is the same type that is passed to an Axis in SciChart.

To Style the HeatmapLegend is very similar to styling an axis in SciChart. See more at the page Axis Styling.

## Updating ColorMaps Dynamically

HeatmapColorMaps📘 can be updated dynamically by changing their properties. All the properties such as minimum, maximum, gradientStops are fully reactive and when set, the chart will redraw.

Below we've created a demo to show how to update HeatmapColorMap.gradientStops📘 dynamically by adding interactivity to the HeatmapLegend📘.

- TS

`// .. Assuming SciChartSurface, UniformHeatmapDataSeries already created`

// Create a colormap

const colorMap = new HeatmapColorMap({

minimum: 0,

maximum: 200,

gradientStops: [

{ offset: 1, color: "#EC0F6C" },

{ offset: 0.9, color: "#F48420" },

{ offset: 0.7, color: "#DC7969" },

{ offset: 0.5, color: "#67BDAF" },

{ offset: 0.3, color: "#50C7E0" },

{ offset: 0.2, color: "#264B9377" },

{ offset: 0, color: "Transparent" }

]

});

// Create a Heatmap RenderableSeries with the color map

sciChartSurface.renderableSeries.add(

new UniformHeatmapRenderableSeries(wasmContext, {

dataSeries: heatmapDataSeries,

useLinearTextureFiltering: false,

fillValuesOutOfRange: true,

colorMap

})

);

// Create the heatmapLegend with the same colorMap

const { heatmapLegend } = await HeatmapLegend.create(divElementIdLegend, {

theme: {

...new SciChartJsNavyTheme(),

sciChartBackground: "#14233CBB",

loadingAnimationBackground: "#14233CBB"

},

colorMap

});

// The HeatmapLegend is implemented using a SciChartSurface, You can access the inner chart

const legendSciChartSurface = heatmapLegend.innerSciChartSurface.sciChartSurface;

// Create an AxisMarkerAnnotation and subscribe to onDrag

const axisAnnotation = new AxisMarkerAnnotation({

y1: colorMap.maximum * 0.9,

isEditable: true,

onDrag: args => {

// First step: prevent dragging outside the min/max

if (axisAnnotation.y1 > 200) axisAnnotation.y1 = 200;

if (axisAnnotation.y1 < 0) axisAnnotation.y1 = 0;

// On-drag, update the gradient stops and re-assign. The Chart automatically redraws

const gradientStops = [

{ offset: 1, color: "#EC0F6C" },

{ offset: axisAnnotation.y1 / 200, color: "#F48420" },

{ offset: 0.7, color: "#DC7969" },

{ offset: 0.5, color: "#67BDAF" },

{ offset: 0.3, color: "#50C7E0" },

{ offset: 0.2, color: "#264B9377" },

{ offset: 0, color: "Transparent" }

];

colorMap.gradientStops = gradientStops;

}

});

// Add it to the legend's SciChartSurface

legendSciChartSurface.annotations.add(axisAnnotation);

The HeatmapLegend📘 is implemented internally using a SciChartSurface. You can access the surface via the innerSciChartSurface📘 property. After that, you can configure the axis, series, annotations just like you would any other SciChartSurface.