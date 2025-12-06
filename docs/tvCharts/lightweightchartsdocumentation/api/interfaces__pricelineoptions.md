---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/PriceLineOptions
scraped_at: 2025-12-01T14:31:41.241159
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/PriceLineOptions

# Interface: PriceLineOptions

Represents a price line options.

## Properties

### id?

`optional`

id:`string`

The optional ID of this price line.

### price

price:`number`

Price line's value.

#### Default Value

`0`

### color

color:`string`

Price line's color.

#### Default Value

`''`

### lineWidth

lineWidth:`LineWidth`

Price line's width in pixels.

#### Default Value

`1`

### lineStyle

lineStyle:`LineStyle`

Price line's style.

#### Default Value

`{@link LineStyle.Solid}`

### lineVisible

lineVisible:`boolean`

Display line.

#### Default Value

`true`

### axisLabelVisible

axisLabelVisible:`boolean`

Display the current price value in on the price scale.

#### Default Value

`true`

### title

title:`string`

Price line's on the chart pane.

#### Default Value

`''`

### axisLabelColor

axisLabelColor:`string`

Background color for the axis label. Will default to the price line color if unspecified.

#### Default Value

`''`

### axisLabelTextColor

axisLabelTextColor:`string`

Text color for the axis label.

#### Default Value

`''`