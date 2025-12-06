---
source: https://tradingview.github.io/lightweight-charts/docs/price-scale
scraped_at: 2025-12-01T14:31:46.069634
---

# https://tradingview.github.io/lightweight-charts/docs/price-scale

# Price scale

Price Scale (or price axis) is a vertical scale that mostly maps prices to coordinates and vice versa. The rules of converting depend on a price scale mode, a height of the chart and visible part of the data.

By default, chart has 2 predefined price scales: `left`

and `right`

, and an unlimited number of overlay scales.

Only `left`

and `right`

price scales could be displayed on the chart, all overlay scales are hidden.

If you want to change `left`

price scale, you need to use `leftPriceScale`

option, to change `right`

price scale use `rightPriceScale`

, to change default options for an overlay price scale use `overlayPriceScales`

option.

Alternatively, you can use `IChartApi.priceScale`

method to get an API object of any price scale or `ISeriesApi.priceScale`

to get an API object of series' price scale (the price scale that the series is attached to).

## Creating a price scale

By default a chart has only 2 price scales: `left`

and `right`

.

If you want to create an overlay price scale, you can simply assign `priceScaleId`

option to a series (note that a value should be differ from `left`

and `right`

) and a chart will automatically create an overlay price scale with provided ID.
If a price scale with such ID already exists then a series will be attached to this existing price scale.
Further you can use provided price scale ID to get its corresponding API object via `IChartApi.priceScale`

method.

## Removing a price scale

The default price scales (`left`

and `right`

) cannot be removed, you can only hide them by setting `visible`

option to `false`

.

An overlay price scale exists while there is at least 1 series attached to this price scale. Thus, to remove an overlay price scale remove all series attached to this price scale.