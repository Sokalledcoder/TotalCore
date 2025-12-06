---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/SeriesMarkerPrice
scraped_at: 2025-12-01T14:31:41.585867
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/SeriesMarkerPrice

# Interface: SeriesMarkerPrice<TimeType>

Represents a series marker.

## Extends

`SeriesMarkerBase`

<`TimeType`

>

## Type parameters

• **TimeType**

## Properties

### time

time:`TimeType`

The time of the marker.

#### Inherited from

### shape

shape:`SeriesMarkerShape`

The shape of the marker.

#### Inherited from

### color

color:`string`

The color of the marker.

#### Inherited from

### id?

`optional`

id:`string`

The ID of the marker.

#### Inherited from

### text?

`optional`

text:`string`

The optional text of the marker.

#### Inherited from

### size?

`optional`

size:`number`

The optional size of the marker.

#### Default Value

`1`

#### Inherited from

### position

position:`SeriesMarkerPricePosition`

The position of the marker.

#### Overrides

### price

price:`number`

The price value for exact Y-axis positioning.

Required when using SeriesMarkerPricePosition position type.