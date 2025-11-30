---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-types/common-axis-base-type
scraped_at: 2025-11-28T18:24:08.037238
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-types/common-axis-base-type

# Common Axis Base Type and Options

Common Axis Base Type and Options

All the axis types in SciChart inherit from AxisCore📘 - a common type shared across both 2D and 3D Charts - and all 2D Axis inherit **AxisBase2D📘**.

The inheritance diagram for Axis in SciChart.js looks like this:

## Common Properties on an Axis

Common properties on an axis allow you to configure the following things:

- Showing/hiding and styling of Gridlines
- Showing/hiding and styling of labels
- Alignment of the axis
- Formatting of labels
- Getting / setting visibleRange or padding
- Getting / setting ID - used in multi-axis scenarios
- Styling border, background
- Setting axis title

The properties common to the **AxisBase2D** / **AxisCore** classes can be found in the TypeDoc API documentation📘.

## Specific Axis Types

The following sections go into further details for specific axis types, as well as giving code samples on how to configure and use each axis.

| Axis Type | Description |
|---|---|
NumericAxis | Value Axis / Numeric Types |
PolarNumericAxis | Value Axis / Numeric Types for Polar Charts |
DateTimeNumericAxis | Value Axis with additional features for Dates and Time formatting |
CategoryAxis | Category Axis - measures using index - Numeric Types or Dates |
PolarCategoryAxis | Category Axis for Polar Charts - measures using index - Numeric Types or Dates |
LogarithmicAxis | Logarithmic Axis supporting Base2, BaseE, Base10 with or without scientific notation |