---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/CrosshairLineOptions
scraped_at: 2025-12-01T14:31:39.046235
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/CrosshairLineOptions

# Interface: CrosshairLineOptions

Structure describing a crosshair line (vertical or horizontal)

## Properties

### color

color:`string`

Crosshair line color.

#### Default Value

`'#758696'`

### width

width:`LineWidth`

Crosshair line width.

#### Default Value

`1`

### style

style:`LineStyle`

Crosshair line style.

#### Default Value

`{@link LineStyle.LargeDashed}`

### visible

visible:`boolean`

Display the crosshair line.

Note that disabling crosshair lines does not disable crosshair marker on Line and Area series.
It can be disabled by using `crosshairMarkerVisible`

option of a relevant series.

#### See

- LineStyleOptions.crosshairMarkerVisible
- AreaStyleOptions.crosshairMarkerVisible
- BaselineStyleOptions.crosshairMarkerVisible

#### Default Value

`true`

### labelVisible

labelVisible:`boolean`

Display the crosshair label on the relevant scale.

#### Default Value

`true`

### labelBackgroundColor

labelBackgroundColor:`string`

Crosshair label background color.

#### Default Value

`'#4c525e'`