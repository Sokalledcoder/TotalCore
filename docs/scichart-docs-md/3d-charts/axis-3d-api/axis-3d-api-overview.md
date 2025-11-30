---
source: https://www.scichart.com/documentation/js/v4/3d-charts/axis-3d-api/axis-3d-api-overview
scraped_at: 2025-11-28T18:24:54.076680
---

# https://www.scichart.com/documentation/js/v4/3d-charts/axis-3d-api/axis-3d-api-overview

# Axis3D APIs Overview

SciChart.js 3D shares the same AxisCore📘 as SciChart.js 2D. Many features such as **Text Formatting**, **Autorange** (zooming to fit) and **Styling** **are** **shared**. For your convenience, some of the documentation has been duplicated here, with some referring to other sections of the user manual.

The Axis Types in SciChart all inherit from AxisCore📘 and 3D axis inherit AxisBase3D📘. Below you can find an inheritance diagram. In the next section we're going to go over the main properties, types and what you can do with SciChart.js 3D Axis.

### The AxisCore Type

AxisCore📘 properties and methods can be seen at the TypeDoc documentation📘.

Some important properties to note: autoRange📘, textFormatting📘, majorGridLineStyle📘 and properties like drawLabels📘, drawMajorGridLines📘 etc... We're going to explain more on how to use these later.

### The AxisBase3D Type

AxisBase3D📘 inherits AxisCore and has some additional properties specific to 3D charts. These include:

- axisPlaneBackgroundFill📘
- backgroundColor📘
- labelDepthTestEnabled📘
- negativeSideClipping📘
- planeBorderColor📘
- planeBorderThickness📘
- positiveSideClipping📘
- tickLabelAlignment📘
- tickLabelsOffset📘
- titleOffset📘

## Basic Examples of how to declare an Axis

For a super-simple primer with code sample on how to declare an axis in SciChart.js 3D, see the article Numeric and Date Axis in SciChart3D.

## Axis 3D APIs

Below are the key things you can do with the axis in SciChart.js 3D and where to find more information.

### Axis 3D Text (Label) Formatting

All Axis in SciChart use the labelProviders to format text for the axis labels and cursor (tooltip) labels.

Background information can be found found at the Axis LabelProvider API Overview.

Specific example code for formatting 3D Axis text labels can be found in the article Axis3D Text (Label) Formatting).

### Axis 3D AutoRanging & Setting VisibleRange

AxisBase3D📘 derived Types also have auto-ranging behaviour as per the 2D axis types. The axis.autoRange📘 property defines how the axis will autorange when data is changed.

The axis.visibleRange📘 property allows you to set or get the min, max on the axis.

axis.growBy📘 allows you to set padding on the visibleRange.

axis.visibleRangeChanged📘 is an event or callback which fires when the range is updated.

For more info see:

- Axis Ranging - AutoRanging
- Axis Ranging - Setting and Getting VisibleRange
- Axis Ranging - Listen to VisibleRange Changes

**NOTE**: In a 3D Axis, AutoRanging means ‘given a fixed size of Axis in 3D world coordinates, change the VisibleRange Max/Min to fit the data’.

Dynamically positioning the camera to view all of the 3D Chart would require updating the camera position, target. See the article on Camera 3D for more information.

### Axis 3D Tick / Label Frequency

In SciChart.js, the ticks are small marks around the chart on an axis. They Also define the spacing of Gridlines, Axis Labels and Axis Bands.

AxisBase3D tick intervals can be changed using the same APIs as SciChart 2D. For further information see Axis 3D Gridline and Label Spacing.

### Axis 3D Element Styling

For styling gridlines, labels and titles, the rules in SciChart.js 3D are the same as 2D charts.

There are some addditional elements on the 3D chart which can be styled, such as the axis walls. For more info see the article on Styling Gridlines, Labels and Elements.