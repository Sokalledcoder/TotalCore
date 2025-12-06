---
source: https://tradingview.github.io/lightweight-charts/docs/api/functions/createImageWatermark
scraped_at: 2025-12-01T14:31:38.172275
---

# https://tradingview.github.io/lightweight-charts/docs/api/functions/createImageWatermark

# Function: createImageWatermark()

createImageWatermark<`T`

>(`pane`

,`imageUrl`

,`options`

):`IImageWatermarkPluginApi`

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

• **imageUrl**: `string`

Image URL.

• **options**: `DeepPartial`

<`ImageWatermarkOptions`

>

Watermark options.

## Returns

Image watermark wrapper.

## Example

`import { createImageWatermark } from 'lightweight-charts';`

const firstPane = chart.panes()[0];

const imageWatermark = createImageWatermark(firstPane, '/images/my-image.png', {

alpha: 0.5,

padding: 20,

});

// to change options

imageWatermark.applyOptions({ padding: 10 });

// to remove watermark from the pane

imageWatermark.detach();