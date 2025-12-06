---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/SeriesMarkerBar
scraped_at: 2025-12-01T14:31:41.370729
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/SeriesMarkerBar

# Interface: SeriesMarkerBar<TimeType>

Represents a series marker.

## Extends

`SeriesMarkerBase`

<`TimeType`

>

## Type parameters

• **TimeType**

## Properties

### position

position:`SeriesMarkerBarPosition`

The position of the marker.

#### Overrides

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

### price?

`optional`

price:`number`

The price value for exact Y-axis positioning.

Required when using SeriesMarkerPricePosition position type.