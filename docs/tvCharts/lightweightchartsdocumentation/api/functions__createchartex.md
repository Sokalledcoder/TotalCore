---
source: https://tradingview.github.io/lightweight-charts/docs/api/functions/createChartEx
scraped_at: 2025-12-01T14:31:38.085610
---

# https://tradingview.github.io/lightweight-charts/docs/api/functions/createChartEx

# Function: createChartEx()

createChartEx<`HorzScaleItem`

,`THorzScaleBehavior`

>(`container`

,`horzScaleBehavior`

,`options`

?):`IChartApiBase`

<`HorzScaleItem`

>

This function is the main entry point of the Lightweight Charting Library. If you are using time values for the horizontal scale then it is recommended that you rather use the createChart function.

## Type parameters

• **HorzScaleItem**

type of points on the horizontal scale

• **THorzScaleBehavior** *extends* `IHorzScaleBehavior`

<`HorzScaleItem`

>

type of horizontal axis strategy that encapsulate all the specific behaviors of the horizontal scale type

## Parameters

• **container**: `string`

| `HTMLElement`

ID of HTML element or element itself

• **horzScaleBehavior**: `THorzScaleBehavior`

Horizontal scale behavior

• **options?**: `DeepPartial`

<`ReturnType`

<`THorzScaleBehavior`

[`"options"`

]>>

Any subset of options to be applied at start.

## Returns

`IChartApiBase`

<`HorzScaleItem`

>

An interface to the created chart