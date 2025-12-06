---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/BaselineStyleOptions
scraped_at: 2025-12-01T14:31:38.834428
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/BaselineStyleOptions

# Interface: BaselineStyleOptions

Represents style options for a baseline series.

## Properties

### baseValue

baseValue:`BaseValuePrice`

Base value of the series.

#### Default Value

`{ type: 'price', price: 0 }`

### relativeGradient

relativeGradient:`boolean`

Gradient is relative to the base value and the currently visible range. If it is false, the gradient is relative to the top and bottom of the chart.

#### Default Value

`false`

### topFillColor1

topFillColor1:`string`

The first color of the top area.

#### Default Value

`'rgba(38, 166, 154, 0.28)'`

### topFillColor2

topFillColor2:`string`

The second color of the top area.

#### Default Value

`'rgba(38, 166, 154, 0.05)'`

### topLineColor

topLineColor:`string`

The line color of the top area.

#### Default Value

`'rgba(38, 166, 154, 1)'`

### bottomFillColor1

bottomFillColor1:`string`

The first color of the bottom area.

#### Default Value

`'rgba(239, 83, 80, 0.05)'`

### bottomFillColor2

bottomFillColor2:`string`

The second color of the bottom area.

#### Default Value

`'rgba(239, 83, 80, 0.28)'`

### bottomLineColor

bottomLineColor:`string`

The line color of the bottom area.

#### Default Value

`'rgba(239, 83, 80, 1)'`

### lineWidth

lineWidth:`LineWidth`

Line width.

#### Default Value

`3`

### lineStyle

lineStyle:`LineStyle`

Line style.

#### Default Value

`{@link LineStyle.Solid}`

### lineType

lineType:`LineType`

Line type.

#### Default Value

`{@link LineType.Simple}`

### lineVisible

lineVisible:`boolean`

Show series line.

#### Default Value

`true`

### pointMarkersVisible

pointMarkersVisible:`boolean`

Show circle markers on each point.

#### Default Value

`false`

### pointMarkersRadius?

`optional`

pointMarkersRadius:`number`

Circle markers radius in pixels.

#### Default Value

`undefined`

### crosshairMarkerVisible

crosshairMarkerVisible:`boolean`

Show the crosshair marker.

#### Default Value

`true`

### crosshairMarkerRadius

crosshairMarkerRadius:`number`

Crosshair marker radius in pixels.

#### Default Value

`4`

### crosshairMarkerBorderColor

crosshairMarkerBorderColor:`string`

Crosshair marker border color. An empty string falls back to the color of the series under the crosshair.

#### Default Value

`''`

### crosshairMarkerBackgroundColor

crosshairMarkerBackgroundColor:`string`

The crosshair marker background color. An empty string falls back to the color of the series under the crosshair.

#### Default Value

`''`

### crosshairMarkerBorderWidth

crosshairMarkerBorderWidth:`number`

Crosshair marker border width in pixels.

#### Default Value

`2`

### lastPriceAnimation

lastPriceAnimation:`LastPriceAnimationMode`

Last price animation mode.

#### Default Value

`{@link LastPriceAnimationMode.Disabled}`