---
source: https://www.scichart.com/documentation/js/v4/3d-charts/axis-3d-api/axis-3d-gridline-and-label-spacing-interval
scraped_at: 2025-11-28T18:24:54.352629
---

# https://www.scichart.com/documentation/js/v4/3d-charts/axis-3d-api/axis-3d-gridline-and-label-spacing-interval

# Axis3D Gridline and Label Spacing (Interval)

Axis 3D Gridline and Label Spacing obeys the same rules as SciChart 2D. Here are the key principles.

- Each axis has a axisCore.MajorDelta📘 and axisCore.MinorDelta📘, which specify the interval of major gridlines / labels and minor gridlines respectively. These are normally calculated automatically. They can be set manually along with axis.autoTicks📘 = false to achieve user-defined intervals.
- You can also set hints such as axis.maxAutoTicks📘 or axis.minorsPerMajor📘 to adjust the number of gridlines using the automatic built-in intervals.
- Or, if you want fine-grained control over gridline spacing and to apply custom or dynamic rules, you can create a TickProvider plugin to do it

Background reading: Read the Axis Ticks - Gridline and Label Spacing and the advanced article Axis Ticks - Programmatic Gridline Spacing to learn more about this powerful API.

## Simple Example of spacing Gridlines

Here is a code sample that demonstrates the three ways to space gridlines.

### Automatic Spacing

Automatic gridline and label spacing (default) can be adjusted by setting the axis.maxAutoTicks📘 and axis.minorsPerMajor📘 properties.

- TS

`// Define the X Axis with automatic spacing, and optional hint to set the max`

// number of gridlines, labels and minor gridlines

sciChart3DSurface.xAxis = new NumericAxis3D(wasmContext, {

axisTitle: "X [Automatic Spacing]",

visibleRange: new NumberRange(0, 10),

autoTicks: true, // default value is true. Major/Minor Deltas are calculated automatically

maxAutoTicks: 5, // Hint: 5 major gridlines and labels

minorsPerMajor: 4 // Exact: 4 minor gridlines per major gridline

});

### Manual Spacing

To manually specify gridline and label intervals, set axis.autoTicks📘 = false then set axisCore.MajorDelta📘 and axisCore.MinorDelta📘.

- TS

`sciChart3DSurface.yAxis = new NumericAxis3D(wasmContext, {`

axisTitle: "Y [Manual Spacing]",

visibleRange: new NumberRange(0, 10),

autoTicks: false, // Major/Minor Deltas are specified manually

majorDelta: 5,

minorDelta: 1

});

### Custom Spacing

Finally, to specify custom spacing or irregular spacing, you can create a class which inherits from NumericTickProvider and attach to the axis like this.

- TS

`// Custom TickProvider implementation`

//

class CustomTickProvider extends NumericTickProvider {

constructor(wasmContext) {

super(wasmContext);

}

// returns an array of minor gridline positions in data space

// Called once per draw. Can be dynamic

getMinorTicks(minorDelta, majorDelta, visibleRange) {

// Todo here: calculate your tick spacing based on axis minorDelta, majorDelta and visibleRange

// Note we do not return major ticks here, so minor ticks exclude the majors

return [

0.2, 0.4, 0.6, 0.8, 1.2, 1.4, 1.6, 1.8, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.2, 4.4, 4.6, 4.8,

5.0, 5.2, 5.4, 5.6, 5.8, 6.0, 6.2, 6.4, 6.6, 6.8, 7.0, 7.2, 7.4, 7.6, 7.8, 8.2, 8.4, 8.6, 8.8, 9.0, 9.2,

9.4, 9.6, 9.8

];

}

// returns an array of major gridline positions in data space

// Called once per draw. Can be dynamic

getMajorTicks(minorDelta, majorDelta, visibleRange) {

// Todo here: calculate your tick spacing based on axis minorDelta, majorDelta and visibleRange

// Note we return the major tick intervals and label intervals here

return [0, 1, 2, 4, 8];

}

}

// Create the X-Axis

sciChart3DSurface.zAxis = new NumericAxis3D(wasmContext, {

axisTitle: "Z [Custom Spacing]",

visibleRange: new NumberRange(0, 10)

});

// Apply the tick provider

sciChart3DSurface.zAxis.tickProvider = new CustomTickProvider(wasmContext);

Putting this all together, we've created an example to show you all three spacing methods in one 3D chart.