---
source: https://www.scichart.com/documentation/js/v4/2d-charts/annotations-api/polar-pointer-annotation
scraped_at: 2025-11-28T18:24:03.154870
---

# https://www.scichart.com/documentation/js/v4/2d-charts/annotations-api/polar-pointer-annotation

# PolarPointerAnnotation

The PolarPointerAnnotation📘 creates a customizable SVG pointer for polar charts, ideal for gauges or radial indicators. It consists of 3 customizable elements: a pointer stick, center circle (optional), and arrowhead (also optional).

## Basic Usage

To create a PolarPointerAnnotation📘, you can use the following code snippet:

`// Demonstrates how to use PolarPointerAnnotation in SciChart.js`

const {

SciChartPolarSurface,

SciChartJsNavyTheme,

PolarNumericAxis,

EPolarAxisMode,

PolarPointerAnnotation,

ECoordinateMode,

EStrokeLineJoin

} = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await SciChartPolarSurface.create(divElementId, {

theme: new SciChartJsNavyTheme(),

});

// Create axes

sciChartSurface.xAxes.add(

new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Angular,

flippedCoordinates: true, // go clockwise

totalAngle: Math.PI, // 180 degrees

startAngle: 0,

})

);

sciChartSurface.yAxes.add(

new PolarNumericAxis(wasmContext, {

polarAxisMode: EPolarAxisMode.Radial,

})

);

const pointerExample = new PolarPointerAnnotation({

x1: Math.random() * 10, // pointer angle

y1: 10, // pointer length

xCoordinateMode: ECoordinateMode.DataValue,

yCoordinateMode: ECoordinateMode.DataValue,

isStrokeAboveCenter: true, // whether the pointer stick is above the center circle or not

pointerStyle: {

baseSize: 0.01, // slightly wider base than the pointer

fill: "#F00",

stroke: "#F00",

backExtensionSize: 0.2

},

// optional - arrowhead at the tip of the pointer

pointerArrowStyle: {

stroke: "#F00",

strokeWidth: 2,

fill: "#900",

height: 0.2,

width: 0.1,

headDepth: 0.8

},

// optional - circle at the base of the pointer

pointerCenterStyle: {

size: 0.12, // relative to the pointer height

fill: "#111",

},

strokeLineJoin: EStrokeLineJoin.Round,

});

sciChartSurface.annotations.add(pointerExample);

Resulting in the following output:

## Key Configuration Properties

### Core Properties

| Property | Type | Default | Description |
|---|---|---|---|
| x1 | number | 0 | Rotation angle (radians/data-value) |
| y1 | number | 0 | Pointer length (pixels/data-value) |
| xCoordinateMode | ECoordinateMode📘 | DataValue | Units for rotation angle |
| yCoordinateMode | ECoordinateMode📘 | DataValue | Units for pointer length |
| isStrokeAboveCenter | boolean | false | Z-order: pointer above/below center |

### Style Objects

The 3 main style objects control the appearance of the pointer's key pieces are the following:

| Property | Type | Description |
|---|---|---|
| pointerStyle | TPointerStyle📘 | Styling of the main stick of the pointer annotation. By default only this part will appear |
| pointerArrowStyle | TPointerArrowStyle📘 | Styles the arrowhead of the pointer annotation. To see the arrow end, you must set its `height` or `width` . |
| pointerCenterStyle | TPointerCenterStyle📘 | Styles the center circle of the pointer annotation. To see the center circle, you must set its `size` . |

### How the style objects work in the PolarPointerAnnotation📘:

The **arrowhead** of the pointer does not appear by default. Set pointerArrowStyle📘's width & height to see it.

`const arrowheadPointer = new PolarPointerAnnotation({`

// .....

pointerArrowStyle: {

width: 0.1,

height: 0.16,

stroke: "#222",

fill: "#fff",

headDepth: 0.8

},

});

In simlar fashion, the **base circle** only appears if the pointerCenterStyle📘 option is defined.

`const centerCirclePointer = new PolarPointerAnnotation({`

// .....

pointerCenterStyle: {

size: 0.1,

fill: "#EEE"

}

});

In the case you want a **stick-less** pointer annotation, this can be achieved by doing this:

`const stickLessPointer = new PolarPointerAnnotation({`

// .....

pointerStyle: { // Hide the pointer stick

baseSize: 0,

stroke: "none"

},

pointerArrowStyle: { // make the arrowhead visible so a pointer entity still exists

// .....

width: 0.1,

height: 0.16,

stroke: "#222",

}

});

## Advanced Customization

Override SVG generation methods for full control:

`// Define a pointer annotation`

const customPointer = new PolarPointerAnnotation({

x1: Math.random() * 6 + 2,

y1: 10, // pointer length

xCoordinateMode: ECoordinateMode.DataValue,

yCoordinateMode: ECoordinateMode.DataValue,

pointerStyle: {

baseSize: 0.05, // relative to the pointer length

fill: "#195",

stroke: "#195",

},

// optional - arrowhead at the tip of the pointer

pointerArrowStyle: {

stroke: "#195",

fill: "#132",

height: 0.2,

width: 0.1,

headDepth: 0.8,

},

// optional - circle at the base of the pointer

pointerCenterStyle: {

size: 0.05, // relative to the pointer length

fill: "#132",

stroke: "#195",

},

strokeLineJoin: EStrokeLineJoin.Round,

});

// You can override:

// 1. the Stick (pointer) path

customPointer.getPointerStickSvg = (pointerLength, pointerWidth, backExtensionSize) => {

const size = pointerLength * 2;

const halfStrokeWidth = Math.max(customPointer.pointerStyle.strokeWidth ?? 1.5, 0);

return `<path stroke-linejoin=${customPointer.strokeLineJoin}

d="

M${size - halfStrokeWidth} ${pointerLength}

L${pointerLength - pointerLength * backExtensionSize} ${pointerLength - pointerWidth / 2}

l0 ${pointerWidth}

L${size - halfStrokeWidth} ${pointerLength}Z

"

fill="${customPointer.pointerStyle.fill}"

stroke="${customPointer.pointerStyle.stroke}"

stroke-width="${customPointer.pointerStyle.strokeWidth}"

/>`;

}

// 2. Center path

customPointer.getPointerCenterSvg = (pointerLength, centerSize) => {

return `<rect

x="${pointerLength - centerSize / 2}"

y="${pointerLength - centerSize / 2}"

width=${centerSize}

height=${centerSize}

rx=${centerSize / 2}

ry=${centerSize / 2}

stroke=${customPointer.pointerCenterStyle.stroke}

stroke-width=${customPointer.pointerCenterStyle.strokeWidth}

fill=${customPointer.pointerCenterStyle.fill}

/>`;

}

// 3. The arrowhead path

customPointer.getPointerArrowSvg = (pointerLength, height, width, headDepth) => {

const size = 2 * pointerLength;

const halfStrokeWidth = Math.max(customPointer.pointerArrowStyle.strokeWidth ?? 1.5, 0);

return `<path

stroke="${customPointer.pointerArrowStyle.stroke}"

stroke-width="${customPointer.pointerArrowStyle.strokeWidth}"

fill="${customPointer.pointerArrowStyle.fill}"

stroke-linejoin=${customPointer.strokeLineJoin}

d="

M${size - height / 2 - halfStrokeWidth} ${pointerLength - width / 2}

l${height / 2} ${width / 2}

l-${height / 2} ${width / 2}

${headDepth === 0

? ""

: `l${((1 - headDepth) * height) / 2} ${-width / 2}Z`

}

"

/>`;

}

// The above methods are the default implementations, but you can override them if you want to

This produces the following output:

The PolarPointerAnnotation📘 plays a crucial role within a Gauge Chart