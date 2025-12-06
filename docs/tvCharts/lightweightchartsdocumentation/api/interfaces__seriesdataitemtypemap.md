---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/SeriesDataItemTypeMap
scraped_at: 2025-12-01T14:31:41.481166
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/SeriesDataItemTypeMap

# Interface: SeriesDataItemTypeMap<HorzScaleItem>

Represents the type of data that a series contains.

For example a bar series contains BarData or WhitespaceData.

## Type parameters

• **HorzScaleItem** = `Time`

## Properties

### Bar

Bar:`WhitespaceData`

<`HorzScaleItem`

> |`BarData`

<`HorzScaleItem`

>

The types of bar series data.

### Candlestick

Candlestick:`WhitespaceData`

<`HorzScaleItem`

> |`CandlestickData`

<`HorzScaleItem`

>

The types of candlestick series data.

### Area

Area:`AreaData`

<`HorzScaleItem`

> |`WhitespaceData`

<`HorzScaleItem`

>

The types of area series data.

### Baseline

Baseline:`WhitespaceData`

<`HorzScaleItem`

> |`BaselineData`

<`HorzScaleItem`

>

The types of baseline series data.

### Line

Line:`WhitespaceData`

<`HorzScaleItem`

> |`LineData`

<`HorzScaleItem`

>

The types of line series data.

### Histogram

Histogram:`WhitespaceData`

<`HorzScaleItem`

> |`HistogramData`

<`HorzScaleItem`

>

The types of histogram series data.

### Custom

Custom:`CustomData`

<`HorzScaleItem`

> |`CustomSeriesWhitespaceData`

<`HorzScaleItem`

>

The base types of an custom series data.