---
source: https://tradingview.github.io/lightweight-charts/docs/api/type-aliases/Nominal
scraped_at: 2025-12-01T14:31:43.676821
---

# https://tradingview.github.io/lightweight-charts/docs/api/type-aliases/Nominal

# Type alias: Nominal<T, Name>

Nominal<`T`

,`Name`

>:`T`

&`object`

This is the generic type useful for declaring a nominal type, which does not structurally matches with the base type and the other types declared over the same base type

## Examples

`type Index = Nominal<number, 'Index'>;`

// let i: Index = 42; // this fails to compile

let i: Index = 42 as Index; // OK

`type TagName = Nominal<string, 'TagName'>;`

## Type declaration

### [species]

[species]:`Name`

The 'name' or species of the nominal.

## Type parameters

• **T**

• **Name** *extends* `string`