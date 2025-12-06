---
source: https://tradingview.github.io/lightweight-charts/docs/api/functions/createTextWatermark
scraped_at: 2025-12-01T14:31:38.302943
---

# https://tradingview.github.io/lightweight-charts/docs/api/functions/createTextWatermark

# Function: createTextWatermark()

createTextWatermark<`T`

>(`pane`

,`options`

):`ITextWatermarkPluginApi`

<`T`

>

Creates an image watermark.

## Type parameters

• **T**

## Parameters

• **pane**: `IPaneApi`

<`T`

>

Target pane.

• **options**: `DeepPartial`

<`TextWatermarkOptions`

>

Watermark options.

## Returns

Image watermark wrapper.

## Example

`import { createTextWatermark } from 'lightweight-charts';`

const firstPane = chart.panes()[0];

const textWatermark = createTextWatermark(firstPane, {

horzAlign: 'center',

vertAlign: 'center',

lines: [

{

text: 'Hello',

color: 'rgba(255,0,0,0.5)',

fontSize: 100,

fontStyle: 'bold',

},

{

text: 'This is a text watermark',

color: 'rgba(0,0,255,0.5)',

fontSize: 50,

fontStyle: 'italic',

fontFamily: 'monospace',

},

],

});

// to change options

textWatermark.applyOptions({ horzAlign: 'left' });

// to remove watermark from the pane

textWatermark.detach();