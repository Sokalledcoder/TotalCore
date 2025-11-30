---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/misc/polar-pixel-and-data-coordinates
scraped_at: 2025-11-28T18:24:09.595723
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/misc/polar-pixel-and-data-coordinates

# Axis APIs – Convert Polar Pixel to Data Coordinates

SciChart.js provides a dedicated API for transforming between polar pixel coordinates and data coordinates, enabling advanced annotations, hit-testing, and custom rendering on polar charts.

## Understanding Polar Coordinates in SciChart.js

In polar charts, coordinates are defined by an **angle** (θ) and a **radius** (r) from the chart's center, while Cartesian coordinates are defined by (x, y) positions.

### Where Polar Pixel Coordinates Are Measured From

**Origin**: The center of the polar chart (not the top-left corner as in Cartesian charts).**Angle**: Measured from the axis' start angle, increasing in the direction set by the chart configuration.**Radius**: Measured outward from the center.

All conversions are relative to the **series area** (viewRect) of the chart.

## Converting Polar Data to Cartesian (Pixel) Coordinates

To convert polar data (angle, radius) to Cartesian (pixel) coordinates for rendering or hit-testing, use the annotationHelpers.convertPolarToCartesian()📘 function:

**Parameters:**

`angularAxis`

: The polar angular axis instance.`usePixelRatio`

: Whether to apply device pixel ratio scaling.`wasmContext`

: The WebAssembly context for SciChart.`coordinateMode`

: Indicates if the angle/radius are in pixels, data values, or relative units.`angle`

: The angle in radians`radius`

: The radius in data units

## Usage Example

Convert a data-value angle and radius to pixel coordinates for rendering an annotation:

`const angularAxis = sciChartSurface.xAxes.get(0) as PolarAxisBase;`

const angle = 1.57; // Radians, for example

const radius = 100; // Data units

const { x, y } = convertPolarToCartesian(

angularAxis,

true, // usePixelRatio

wasmContext,

ECoordinateMode.DataValue,

angle,

radius

);

// (x, y) are now pixel coordinates relative to the series area (viewRect)

## Practical Applications

**Hit-Testing**: To determine if a mouse event hits a data point or annotation, convert the event's pixel coordinates to polar data coordinates and compare.**Custom Rendering**: Any custom drawing on a polar chart surface should use this conversion to ensure correct placement.

## Hit-Testing in Polar Charts

When hit-testing, convert the mouse (x, y) pixel coordinates to polar coordinates, then compare with data points.

For reference, here is our actual implementation of a hit-test provider for the PolarLineRenderableSeries📘:

`import { `

BaseHitTestProvider,

PolarLineRenderableSeries,

PolarAxisBase,

Point,

HitTestInfo,

XyDataSeries,

hitTestHelpers,

annotationHelpers,

ECoordinateMode,

calcDistance, calcDistanceFromLine,

PolarDataPointHitTestProvider,

DpiHelper

} from "scichart";

const DEFAULT_RADIUS = 10;

/**

* Hit-test provider for {@link PolarLineRenderableSeries}. See base class {@link BaseHitTestProvider} for further info

*/

export class PolarLineSeriesHitTestProvider extends PolarDataPointHitTestProvider {

/** @inheritDoc */

public hitTest(x: number, y: number, hitTestRadius: number = DEFAULT_RADIUS): HitTestInfo {

// convert to polar and add necessary offset

const hitTestPoint = this.getTranslatedHitTestPoint(x, y);

if (!hitTestPoint) {

return HitTestInfo.empty();

}

const { xCoordinateCalculator, yCoordinateCalculator, isVerticalChart } = this.currentRenderPassData;

const xHitCoord = hitTestPoint.x;

const yHitCoord = hitTestPoint.y;

const dataSeries = this.parentSeries.dataSeries as XyDataSeries;

if (!dataSeries) {

return HitTestInfo.empty();

}

const xNativeValues = dataSeries.getNativeXValues();

const yNativeValues = dataSeries.getNativeYValues();

const xPolarAxis = this.parentSeries.xAxis as PolarAxisBase;

const getCartesianCoordsFn = (index$: number): Point => {

const x = xNativeValues.get(index$);

const y = yNativeValues.get(index$);

const xCoord = xCoordinateCalculator.getCoordinate(x);

const yCoord = yCoordinateCalculator.getCoordinate(y);

const angle = isVerticalChart ? yCoord : xCoord;

const radius = isVerticalChart ? xCoord : yCoord;

const res = annotationHelpers.convertPolarToCartesian(

xPolarAxis,

false,

this.webAssemblyContext,

ECoordinateMode.Pixel,

angle * DpiHelper.PIXEL_RATIO,

radius

);

return new Point(res.x, res.y);

};

let minDistance = Number.MAX_VALUE;

let minDistanceIndex1 = -1;

let minDistanceIndex2 = -1;

const updateMinDistFn = (dist$: number, ind1$: number, ind2$: number = -1) => {

if (dist$ < minDistance) {

minDistance = dist$;

minDistanceIndex1 = ind1$;

minDistanceIndex2 = ind2$;

}

};

if (dataSeries.count() > 0) {

let point1Coords = getCartesianCoordsFn(0);

let distanceToPoint1 = calcDistance(xHitCoord, yHitCoord, point1Coords.x, point1Coords.y);

updateMinDistFn(distanceToPoint1, 0);

for (let i = 1; i < dataSeries.count(); i++) {

const point2Coords = getCartesianCoordsFn(i);

const lineSegmentLength = calcDistance(point1Coords.x, point1Coords.y, point2Coords.x, point2Coords.y);

const distanceToPoint2 = calcDistance(xHitCoord, yHitCoord, point2Coords.x, point2Coords.y);

updateMinDistFn(distanceToPoint2, i);

const isHitPointInLineSegmentVicinity =

distanceToPoint1 < lineSegmentLength && distanceToPoint2 < lineSegmentLength;

if (isHitPointInLineSegmentVicinity) {

const distanceToLine = calcDistanceFromLine(

xHitCoord,

yHitCoord,

point1Coords.x,

point1Coords.y,

point2Coords.x,

point2Coords.y

);

if (distanceToLine < minDistance) {

if (distanceToPoint1 < distanceToPoint2) {

updateMinDistFn(distanceToLine, i - 1, i);

} else {

updateMinDistFn(distanceToLine, i, i - 1);

}

}

}

point1Coords = point2Coords;

distanceToPoint1 = distanceToPoint2;

}

}

const polarHitTestPoint = xPolarAxis.reverseTransform(hitTestPoint.x, hitTestPoint.y);

const hitTestInfo = hitTestHelpers.createHitTestInfo(

this.parentSeries,

xCoordinateCalculator,

yCoordinateCalculator,

isVerticalChart,

dataSeries,

xNativeValues,

yNativeValues,

polarHitTestPoint.x,

polarHitTestPoint.y,

minDistanceIndex1,

hitTestRadius

);

hitTestInfo.isHit = minDistance < hitTestRadius;

return hitTestInfo;

}

}

The inverse function of `convertPolarToCartesian()`

is reverseTransform()📘, which converts from cartesian to polar coordinates.