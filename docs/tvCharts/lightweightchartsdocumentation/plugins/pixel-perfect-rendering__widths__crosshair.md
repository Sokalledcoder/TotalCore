---
source: https://tradingview.github.io/lightweight-charts/docs/plugins/pixel-perfect-rendering/widths/crosshair
scraped_at: 2025-12-01T14:31:45.870969
---

# https://tradingview.github.io/lightweight-charts/docs/plugins/pixel-perfect-rendering/widths/crosshair

# Crosshair and Grid Line Width Calculations

tip

It is recommend that you first read the Pixel Perfect Rendering page.

The following functions can be used to get the calculated width that the library would use for a crosshair or grid line at a specific device pixel ratio.

`/**`

* Default grid / crosshair line width in Bitmap sizing

* @param horizontalPixelRatio - horizontal pixel ratio

* @returns default grid / crosshair line width in Bitmap sizing

*/

export function gridAndCrosshairBitmapWidth(

horizontalPixelRatio: number

): number {

return Math.max(1, Math.floor(horizontalPixelRatio));

}

/**

* Default grid / crosshair line width in Media sizing

* @param horizontalPixelRatio - horizontal pixel ratio

* @returns default grid / crosshair line width in Media sizing

*/

export function gridAndCrosshairMediaWidth(

horizontalPixelRatio: number

): number {

return (

gridAndCrosshairBitmapWidth(horizontalPixelRatio) / horizontalPixelRatio

);

}