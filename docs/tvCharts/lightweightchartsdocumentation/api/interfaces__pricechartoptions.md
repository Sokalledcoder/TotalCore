---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/PriceChartOptions
scraped_at: 2025-12-01T14:31:41.155365
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/PriceChartOptions

# Interface: PriceChartOptions

Configuration options specific to price-based charts. Extends the base chart options and includes localization settings for price formatting.

## Extends

`ChartOptionsImpl`

<`number`

>

## Properties

### width

width:`number`

Width of the chart in pixels

#### Default Value

If `0`

(default) or none value provided, then a size of the widget will be calculated based its container's size.

#### Inherited from

### height

height:`number`

Height of the chart in pixels

#### Default Value

If `0`

(default) or none value provided, then a size of the widget will be calculated based its container's size.

#### Inherited from

### autoSize

autoSize:`boolean`

Setting this flag to `true`

will make the chart watch the chart container's size and automatically resize the chart to fit its container whenever the size changes.

This feature requires `ResizeObserver`

class to be available in the global scope.
Note that calling code is responsible for providing a polyfill if required. If the global scope does not have `ResizeObserver`

, a warning will appear and the flag will be ignored.

Please pay attention that `autoSize`

option and explicit sizes options `width`

and `height`

don't conflict with one another.
If you specify `autoSize`

flag, then `width`

and `height`

options will be ignored unless `ResizeObserver`

has failed. If it fails then the values will be used as fallback.

The flag `autoSize`

could also be set with and unset with `applyOptions`

function.

`const chart = LightweightCharts.createChart(document.body, {`

autoSize: true,

});

#### Inherited from

### layout

layout:`LayoutOptions`

Layout options

#### Inherited from

### leftPriceScale

leftPriceScale:`PriceScaleOptions`

Left price scale options

#### Inherited from

`ChartOptionsImpl`

. `leftPriceScale`

### rightPriceScale

rightPriceScale:`PriceScaleOptions`

Right price scale options

#### Inherited from

`ChartOptionsImpl`

. `rightPriceScale`

### overlayPriceScales

overlayPriceScales:`OverlayPriceScaleOptions`

Overlay price scale options

#### Inherited from

`ChartOptionsImpl`

. `overlayPriceScales`

### timeScale

timeScale:`HorzScaleOptions`

Time scale options

#### Inherited from

### crosshair

crosshair:`CrosshairOptions`

The crosshair shows the intersection of the price and time scale values at any point on the chart.

#### Inherited from

### grid

grid:`GridOptions`

A grid is represented in the chart background as a vertical and horizontal lines drawn at the levels of visible marks of price and the time scales.

#### Inherited from

### handleScroll

handleScroll:`boolean`

|`HandleScrollOptions`

Scroll options, or a boolean flag that enables/disables scrolling

#### Inherited from

`ChartOptionsImpl`

. `handleScroll`

### handleScale

handleScale:`boolean`

|`HandleScaleOptions`

Scale options, or a boolean flag that enables/disables scaling

#### Inherited from

`ChartOptionsImpl`

. `handleScale`

### kineticScroll

kineticScroll:`KineticScrollOptions`

Kinetic scroll options

#### Inherited from

`ChartOptionsImpl`

. `kineticScroll`

### trackingMode

trackingMode:`TrackingModeOptions`

Represent options for the tracking mode's behavior.

Mobile users will not have the ability to see the values/dates like they do on desktop. To see it, they should enter the tracking mode. The tracking mode will deactivate the scrolling and make it possible to check values and dates.

#### Inherited from

`ChartOptionsImpl`

. `trackingMode`

### addDefaultPane

addDefaultPane:`boolean`

Whether to add a default pane to the chart Disable this option when you want to create a chart with no panes and add them manually

#### Default Value

`true`

#### Inherited from

`ChartOptionsImpl`

. `addDefaultPane`

### localization

localization:`PriceChartLocalizationOptions`

Localization options for formatting price values and other chart elements.