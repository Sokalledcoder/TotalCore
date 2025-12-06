---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/IPriceLine
scraped_at: 2025-12-01T14:31:40.021874
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/IPriceLine

# Interface: IPriceLine

Represents the interface for interacting with price lines.

## Methods

### applyOptions()

applyOptions(`options`

):`void`

Apply options to the price line.

#### Parameters

• **options**: `Partial`

<`PriceLineOptions`

>

Any subset of options.

#### Returns

`void`

#### Example

`priceLine.applyOptions({`

price: 90.0,

color: 'red',

lineWidth: 3,

lineStyle: LightweightCharts.LineStyle.Dashed,

axisLabelVisible: false,

title: 'P/L 600',

});

### options()

options():`Readonly`

<`PriceLineOptions`

>

Get the currently applied options.

#### Returns

`Readonly`

<`PriceLineOptions`

>