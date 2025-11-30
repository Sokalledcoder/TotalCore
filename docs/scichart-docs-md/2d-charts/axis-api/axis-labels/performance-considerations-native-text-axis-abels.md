---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-labels/performance-considerations-native-text-axis-abels
scraped_at: 2025-11-28T18:24:05.388578
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-labels/performance-considerations-native-text-axis-abels

# Native Text Axis Labels

In version SciChart 4.0 rendering axis labels defaults to using a native text api. This uses our in-house WebGL text rendering engine and offers performance benefits in situations where you have many axes with many labels. Rotated and multiline support is better with native text than with standard text, but there are also some important limitations you need to be aware of.

## Disabling Native Text Labels

If you are using any custom fonts in your axes, then you can disable native text as the default for all axes by doing the following once at the start of your app:

`// Enable native text`

import { SciChartDefaults } from "scichart";

SciChartDefaults.useNativeText = false;

You can control it for a particular axis by setting the useNativeText option when creating the axis, or by setting the axis.labelProvider.useNativeText📘 property.

To use any font other than Arial you will need ensure that font is available on your server (as fontname.ttf), or registered using sciChartSurface.registerFont()📘 if coming from a remote url. See Native Text Font Loading for more details.

All the normal options in labelStyle📘 are supported except for **fontStyle** and **fontWeight**.

The example below creates axes using both native and standard text.

- TS
- Builder API (JSON Config)

`// Demonstrates native text vs. standard text in SciChart.js`

const {

SciChartSurface,

NumericAxis,

SciChartJsNavyTheme,

EAxisAlignment,

ELabelAlignment,

SciChartDefaults,

Thickness

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

// Use Native text for all axes by default

SciChartDefaults.useNativeText = true;

const labelStyle = {

fontFamily: "Default",

fontSize: 14,

color: "white",

padding: new Thickness(0, 0, 0, 0),

alignment: ELabelAlignment.Auto

};

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

// Enable native text for a specific axis

sciChartSurface.xAxes.add(

new NumericAxis(wasmContext, {

useNativeText: true,

// Most style options are supported

// fontStyle and FontWeight are not supported for native text

labelStyle,

axisTitle: "Native X",

backgroundColor: "#50C7E011"

}),

new NumericAxis(wasmContext, {

// Disable native text for a specfic axis

useNativeText: false,

axisAlignment: EAxisAlignment.Top,

// Same style for comparison

labelStyle,

axisTitle: "Normal X",

backgroundColor: "#50C7E011"

})

);

sciChartSurface.yAxes.add(

// Native text with default values

new NumericAxis(wasmContext, { axisTitle: "Native Y", labelStyle, backgroundColor: "#50C7E011" }),

// Normal text with default values

new NumericAxis(wasmContext, {

labelStyle,

useNativeText: false,

axisAlignment: EAxisAlignment.Left,

axisTitle: "Normal Y",

backgroundColor: "#50C7E011"

})

);

`// Demonstrates native text vs. standard text in SciChart.js using the Builder API`

const { chartBuilder, SciChartDefaults, EAxisAlignment, ELabelAlignment, EAxisType, Thickness } = SciChart;

// or, for npm, import { chartBuilder, ... } from "scichart"

// Use Native text for all axes by default

SciChartDefaults.useNativeText = true;

const labelStyle = {

fontFamily: "Default",

fontSize: 14,

color: "white",

padding: new Thickness(0, 0, 0, 0),

alignment: ELabelAlignment.Auto

};

const { sciChartSurface, wasmContext } = await chartBuilder.build2DChart(divElementId, {

xAxes: [

{

type: EAxisType.NumericAxis,

options: {

useNativeText: true,

// Most style options are supported

// fontStyle and FontWeight are not supported for native text

labelStyle,

axisTitle: "Native X",

backgroundColor: "#50C7E011"

}

},

{

type: EAxisType.NumericAxis,

options: {

// Disable native text for a specfic axis

useNativeText: false,

axisAlignment: EAxisAlignment.Top,

// Same style for comparison

labelStyle,

axisTitle: "Normal X",

backgroundColor: "#50C7E011"

}

}

],

yAxes: [

{

// Native text with default values

type: EAxisType.NumericAxis,

options: { axisTitle: "Native Y", labelStyle, backgroundColor: "#50C7E011" }

},

{

type: EAxisType.NumericAxis,

// Normal text with default values

options: {

labelStyle,

useNativeText: false,

axisAlignment: EAxisAlignment.Left,

axisTitle: "Normal Y",

backgroundColor: "#50C7E011"

}

}

]

});

This results in the following output:

## Rotated and Multiline Native Text Labels

The standard axis labels supported rotation, but the positioning is poor for angles outside the 0 to 90 range. With native text labels, this is fixed. Note that rotation is a property on the labelProvider, not the axis itself.

When using angles that are not a multiple of 90, you probably want to set **hideOverlappingLabels: false** as the overlap is calculated using the bounding rectangle of the text.

Multiline labels are supported simply by using newline characters (\n) in the label text. lineSpacing is a property on the labelProvider. The alignment property on labelStyle also affects the alignment for multiple lines.

Note: for more info about Text and MultiLine labels see this article. For rotation of labels see this article.

#### See Also

Axis Label Formatting - TextLabelProvider

Axis Label Formatting - Custom LabelProviders