---
source: https://www.scichart.com/documentation/js/v4/2d-charts/miscellaneous-apis/glow-and-dro-shadow-shader-effects
scraped_at: 2025-11-28T18:24:46.314514
---

# https://www.scichart.com/documentation/js/v4/2d-charts/miscellaneous-apis/glow-and-dro-shadow-shader-effects

# Glow and DropShadow Shader Effects

SciChart.js features WebGL shader-based GlowEffect📘 and ShadowEffect📘 effects which may be added onto chart types throughout our library.

**Above**: WebGL GlowEffect added to the Real-time Ghosted Traces example

## Adding Glow Effects to Series

A glow shader effect can be added to series to give it an oscilloscope / VDU style effect.

`// GlowEffect example`

import { GlowEffect, Point, FastLineRenderableSeries } from "scichart";

sciChartSurface.renderableSeries.add(

new FastLineRenderableSeries(wasmContext, {

strokeThickness: 2,

stroke: "#FFFF00",

effect: new GlowEffect(wasmContext, {

range: 0,

intensity: 1,

color: "#333333",

offset: new Point(10, 10)

})

})

);

This results in the following (visible in the Vital Signs monitor example).

## Adding Shadow Effect to Series

Drop-shadow effects are also in development, and an example will be provided soon.