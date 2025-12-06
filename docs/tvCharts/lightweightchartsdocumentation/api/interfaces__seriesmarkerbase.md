---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/SeriesMarkerBase
scraped_at: 2025-12-01T14:31:41.636196
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/SeriesMarkerBase

# Interface: SeriesMarkerBase<TimeType>

Represents a series marker.

## Extended by

## Type parameters

• **TimeType**

## Properties

### time

time:`TimeType`

The time of the marker.

### position

position:`SeriesMarkerPosition`

The position of the marker.

### shape

shape:`SeriesMarkerShape`

The shape of the marker.

### color

color:`string`

The color of the marker.

### id?

`optional`

id:`string`

The ID of the marker.

### text?

`optional`

text:`string`

The optional text of the marker.

### size?

`optional`

size:`number`

The optional size of the marker.

#### Default Value

`1`

### price?

`optional`

price:`number`

The price value for exact Y-axis positioning.

Required when using SeriesMarkerPricePosition position type.