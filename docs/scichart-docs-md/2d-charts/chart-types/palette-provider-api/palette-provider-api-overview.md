---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/palette-provider-api/palette-provider-api-overview
scraped_at: 2025-11-28T18:24:36.971709
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/palette-provider-api/palette-provider-api-overview

# PaletteProvider API Overview

SciChart.js features the ability to change color of series on a point-by-point basis, using the PaletteProvider feature.

Many series types support PaletteProvider, including:

- Line Series (FastLineRenderableSeries)
- Mountain Series (FastMountainRenderableSeriers)
- Band Series (FastBandRenderableSeries)
- Bubble Series (FastBubbleRenderableSeries)
- Candlestick Series (FastCandlestickRenderableSeries)
- OHLC Series (FastOhlcRenderableSeries)
- Column Series (FastColumnRenderableSeries)
- Scatter Series (XyScatterRenderableSeries)
- Polar Band Series (PolarBandRenderableSeries)
- Polar Column Series (PolarColumnRenderableSeries)
- Polar Line Series (PolarLineRenderableSeries)
- Polar Mountain Series (PolarMountainRenderableSeries)
- Polar Scatter Series (PolarXyScatterRenderableSeries)

## What is the PaletteProvider API?

The PaletteProvider API allows you to achieve per data-point colouring or styling. Here is a quick example below. The following pages have further worked examples for each series type.

The PaletteProvider API is a powerful extension in SciChart.js which allows you to colour line segments, scatter points, candles/columns or mountain chart segments based on a programatic rule.

## Some common Use-cases for the PaletteProvider

Some common use-cases for the PaletteProvider API include:

- Changing colour of a line series when value exceeds a threshold.
- Colouring candlesticks based on volume
- Changing the Fill of a time-based Histogram based on day of the week
- Highlighting important Scatter or Bubble points based on additional data.

Use this API any time you want to change the colour, fill or scatter-point colours programmatically on a per-datapoint basis.

## Enabling the PaletteProvider

To enable the paletting feature, you need to create a class which conforms to the IStrokePaletteProvider📘, IFillPaletteProvider📘 or IPointMarkerPaletteProvider📘 interfaces and assign a new instance of the class to the IRenderableSeries.paletteProvider📘 property.

The following articles in this section show you how to do this for each series type:

- Per-point Colouring of Line Segments
- Per-point Colouring of Mountain Segments
- Per-Point Colouring of Band Segments
- Per-Point Colouring of Bubble Charts
- Per-Point Colouring of Candlestick / OHLC Charts
- Per-Point Colouring of Scatter Charts (or PointMarkers)
- Per-Point Colouring of Column Charts
- Per-Point Colouring of Impulse Charts
- Per-Point Coloring for Rectangle Series
- Per-Point Coloring for Line Segment Series
- Per-Point Coloring for Triangle Series
- Per-Point Coloring for Polar Band Series
- Per-Point Coloring for Polar Column Series
- Per-Point Coloring for Polar Line Series