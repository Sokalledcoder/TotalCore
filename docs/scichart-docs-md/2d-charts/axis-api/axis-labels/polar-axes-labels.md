---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-labels/polar-axes-labels
scraped_at: 2025-11-28T18:24:05.636997
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-labels/polar-axes-labels

# Polar Axis Labels

The Polar Axis Labels📘 API in SciChart.js provides functionality for customizing the appearance and behavior of labels on polar axes. This includes options for angular and radial axes, allowing developers to control label visibility, alignment, and formatting.

Above: The JavaScript Polar Column Chart example from the SciChart.js Demo.

## Key Properties

All of these properties are available on both the PolarNumericAxis📘 and PolarCategoryAxis📘 classes.

### 1. The PolarAxisBase.polarLabelMode📘

Defines how labels are displayed on the polar axis. The available modes are:

**EPolarLabelMode.Horizontal📘**: Labels are displayed horizontally, no matter the rotation, each label will be upright. This is useful for angular axes where you want labels to be readable regardless of their position.**EPolarLabelMode.Parallel📘**: Labels are displayed parallel to the axis, which means they will follow the curvature of the axis along their width.**EPolarLabelMode.Perpendicular📘**: Labels are displayed perpendicular to the axis, following the curvature of the axis along their height. This is useful for radial axes where you want labels to be oriented outward from the center.

### 2. The PolarAxisBase.isInnerAxis📘

Indicates whether the axis labels are drawn on the other side of the axis. For each type of polarAxisMode📘, this property achieves:

-
For the

**Angular**axis this is a lot more important, as it determines where the labels are drawn in relation to the last angular axis gridline (the biggest circle).`false`

: Labels are drawn**outside**the last angular axis gridline (biggest circle), further from the center.`true`

: Labels are drawn**inside**the last angular axis gridline, closer to the center.

-
The

**Radial**axis just draws the labels on the other side of the first radial gridline, but does not entail this much control over the layout.

### 3. The PolarAxisBase.labelProvider📘:

Provides the ability to modify / customize when and how the axis labels are formatted.

For the Polar Axes, we have created a special label provider, available out of the box, called RadianLabelProvider📘, which formats the labels in radians. Make sure to read the TSDoc indications📘 before using it, and observe how the errorTolerance📘 and maxDenominator📘 pair with AxisBase.autoTicks📘 and AxisBase.majorDelta📘 to determine the label values.

## Other Base Properties that are of interest for Polar Axes:

-
labelPostfix📘: A string that is appended to each label value.

- For angular axes, this is often set to
`°`

to indicate degrees. - For radial axes, it can be set to
`m`

,`km`

, or any other unit of measurement.

- For angular axes, this is often set to
-
drawMinorGridLines📘: A boolean that determines whether minor grid lines are drawn on the axis.

- For smaller polar charts, setting this to
`false`

can help improve readability by only keeping the major grid lines

- For smaller polar charts, setting this to
-
labelPrecision📘: A number that specifies the number of decimal places to display in the labels.

- By default, this is set to
`1`

, but if you work with degrees or just larger datasets, you may want to set it to`0`

to avoid showing decimal places in the labels.

- By default, this is set to