---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/SeriesPartialOptionsMap
scraped_at: 2025-12-01T14:31:41.615355
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/SeriesPartialOptionsMap

# Interface: SeriesPartialOptionsMap

Represents the type of partial options for each series type.

For example a bar series has options represented by BarSeriesPartialOptions.

## Properties

### Bar

The type of bar series partial options.

### Candlestick

Candlestick:`DeepPartial`

<`CandlestickStyleOptions`

&`SeriesOptionsCommon`

>

The type of candlestick series partial options.

### Area

Area:`DeepPartial`

<`AreaStyleOptions`

&`SeriesOptionsCommon`

>

The type of area series partial options.

### Baseline

Baseline:`DeepPartial`

<`BaselineStyleOptions`

&`SeriesOptionsCommon`

>

The type of baseline series partial options.

### Line

Line:`DeepPartial`

<`LineStyleOptions`

&`SeriesOptionsCommon`

>

The type of line series partial options.

### Histogram

Histogram:`DeepPartial`

<`HistogramStyleOptions`

&`SeriesOptionsCommon`

>

The type of histogram series partial options.

### Custom

Custom:`DeepPartial`

<`CustomStyleOptions`

&`SeriesOptionsCommon`

>

The type of a custom series partial options.