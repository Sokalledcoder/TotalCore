---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/CustomData
scraped_at: 2025-12-01T14:31:39.142093
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/CustomData

# Interface: CustomData<HorzScaleItem>

Base structure describing a single item of data for a custom series.

This type allows for any properties to be defined within the interface. It is recommended that you extend this interface with the required data structure.

## Extends

`CustomSeriesWhitespaceData`

<`HorzScaleItem`

>

## Type parameters

• **HorzScaleItem** = `Time`

## Properties

### color?

`optional`

color:`string`

If defined then this color will be used for the price line and price scale line for this specific data item of the custom series.

### time

time:`HorzScaleItem`

The time of the data.

#### Inherited from

`CustomSeriesWhitespaceData`

. `time`

### customValues?

`optional`

customValues:`Record`

<`string`

,`unknown`

>

Additional custom values which will be ignored by the library, but could be used by plugins.