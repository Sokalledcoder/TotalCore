---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/LineStyleOptions
scraped_at: 2025-12-01T14:31:40.785722
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/LineStyleOptions

# Interface: LineStyleOptions

Represents style options for a line series.

## Properties

### color

color:`string`

Line color.

#### Default Value

`'#2196f3'`

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