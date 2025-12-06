---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/AreaStyleOptions
scraped_at: 2025-12-01T14:31:38.595430
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/AreaStyleOptions

# Interface: AreaStyleOptions

Represents style options for an area series.

## Properties

### topColor

topColor:`string`

Color of the top part of the area.

#### Default Value

`'rgba( 46, 220, 135, 0.4)'`

### bottomColor

bottomColor:`string`

Color of the bottom part of the area.

#### Default Value

`'rgba( 40, 221, 100, 0)'`

### relativeGradient

relativeGradient:`boolean`

Gradient is relative to the base value and the currently visible range. If it is false, the gradient is relative to the top and bottom of the chart.

#### Default Value

`false`

### invertFilledArea

invertFilledArea:`boolean`

Invert the filled area. Fills the area above the line if set to true.

#### Default Value

`false`

### lineColor

lineColor:`string`

Line color.

#### Default Value

`'#33D778'`

### lineStyle

lineStyle:`LineStyle`

Line style.

#### Default Value

`{@link LineStyle.Solid}`

### lineWidth

lineWidth:`LineWidth`

Line width in pixels.

#### Default Value

`3`

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