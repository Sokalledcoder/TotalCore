---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-api-overview
scraped_at: 2025-11-28T18:24:03.868610
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-api-overview

# Axis API Overview

SciChart.js has a rich and configurable axis API. We believe you won't find a JavaScript Chart in the world with as many options for axis as SciChart!

This page we're going to give you an overview of what the Axis APIs can do and then show you where to look next for more detail.

# What can SciChart.js Do with Axis?

Heres a quick list of what SciChart.js can do with axis configuration, and where to go next.

## Many Axis Types

There are several axis types in SciChart.js. Although they all differ in types of data values that can be rendered, the most fundamental difference is in their behavior.

By that, the axes can be divided into two groups, Category and Value axis types.

The axis types provided by SciChart.js are listed below:

Here's the content formatted as a two-column Markdown table:

| Axis Type | Description |
|---|---|
NumericAxis | Value Axis / Numeric Types |
PolarNumericAxis | Value Axis / Numeric Types for Polar Charts |
DateTimeNumericAxis | Value Axis with additional features for Dates and Time formatting |
CategoryAxis | Category Axis - measures using index - Numeric Types or Dates |
PolarCategoryAxis | Category Axis for Polar Charts - measures using index - Numeric Types or Dates |
LogarithmicAxis | Logarithmic Axis supporting Base2, BaseE, Base10 with or without scientific notation |
Text / String Axis | Use LabelProviders to format axis labels as text |

To learn more about the axis types, click one of the article links in the table above.

## Axis Layout (Multiple Axis, Axis Alignment)

### Q: Is it easier to render axes and layouts with SciChart compared to competitors?

Yes, with SciChart.js, many axis configurations are possible, these are covered in detail in What Axis Configuration Options and Axis Layout Options does SciChart.js Support?

For an overview of axis layout options, see the documentation links below:

- Aligning Axis on the Left, Right
- Adding a Secondary Axis
- Adding Multiple X and Y Axis
- Rotating a chart 90 degrees (Vertical charts)
- Drawing Series behind axis
- Placing axis in the centre of a chart, or inside a chart surface
- Vertically Stacking Axis - to create complex layouts
- Horizontally Stacking Axis - more complex layouts
- Advanced Custom Axis Layout via the Layout Provider API

To learn more about the axis layout options see the pages in the list above.

## Axis Label Configuration

SciChart.js has a number of label APIs, including:

- Formatting labels the easy way (using built-in flags)
- Formatting labels - using custom code (fine grained label format)
- Having a text axis e.g. "Apples" "Pears" "Oranges" not 1, 2, 3
- Turning native (WebGL) text labels on or off
- Spacing gridlines and labels the easy way
- Spacing gridlines and labels - using custom code (fine grained control)
- Rotating Labels / Multiline Labels / Image Labels
- Label Style, Alignment, Positioning

To learn more about the axis labelling options see Axis Label Formatting and related pages

## Axis Ranging and Scaling

It's possible to programmatically control axis ranging, scaling and auto-fitting of data.

- AutoRange (auto fitting of data)
- Setting/Getting range programatically
- Listening to axis range changes (callbacks on zoom)

To learn more about the axis labelling options see Axis Label Formatting and related pages

Zooming and panning of Axis (such as mouse-drag, or mousewheel zoom) is handled by the ChartModifiers. See sections in the ChartModifier API for more details.

## Axis Styling

Finally, SciChart.js supports Axis styling, including:

- Styling of Gridlines, Labels, Titles and Bands
- Styling of Axis Borders and Background
- Showing or Hiding of Axis parts
- Styling of Polar Axes

To learn more about the axis styling options see Axis Styling and related pages