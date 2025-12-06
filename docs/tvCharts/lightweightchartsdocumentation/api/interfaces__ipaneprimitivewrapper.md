---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/IPanePrimitiveWrapper
scraped_at: 2025-12-01T14:31:39.970738
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/IPanePrimitiveWrapper

# Interface: IPanePrimitiveWrapper<T, Options>

Interface for a pane primitive.

## Type parameters

• **T**

• **Options**

## Properties

### detach()

detach: () =>`void`

Detaches the plugin from the pane.

#### Returns

`void`

### getPane()

getPane: () =>`IPaneApi`

<`T`

>

Returns the current pane.

#### Returns

`IPaneApi`

<`T`

>

### applyOptions()?

`optional`

applyOptions: (`options`

) =>`void`

Applies options to the primitive.

#### Parameters

• **options**: `DeepPartial`

<`Options`

>

Options to apply. The options are deeply merged with the current options.

#### Returns

`void`