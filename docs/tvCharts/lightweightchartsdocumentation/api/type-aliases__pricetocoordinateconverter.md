---
source: https://tradingview.github.io/lightweight-charts/docs/api/type-aliases/PriceToCoordinateConverter
scraped_at: 2025-12-01T14:31:43.844924
---

# https://tradingview.github.io/lightweight-charts/docs/api/type-aliases/PriceToCoordinateConverter

# Type alias: PriceToCoordinateConverter()

PriceToCoordinateConverter: (`price`

) =>`Coordinate`

|`null`

Converter function for changing prices into vertical coordinate values.

This is provided as a convenience function since the series original data will most likely be defined in price values, and the renderer needs to draw with coordinates. This returns the same values as directly using the series' priceToCoordinate method.

## Parameters

• **price**: `number`

## Returns

`Coordinate`

| `null`