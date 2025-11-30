---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-labels/axis-labels-faq
scraped_at: 2025-11-28T18:24:04.362099
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-labels/axis-labels-faq

# Axis Labels FAQs

## I would like no matter what always to show axis labels, they can overlap but should not hide

This scenario if often useful when we disable **autoTicks** and set **majorDelta** manually. This can be done by setting INumericAxisOptions.hideOverlappingLabels📘 option to `false`

.

`const { sciChartSurface, wasmContext } = await SciChartSurface.create("scichart-root");`

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

labelPrecision: 0,

autoTicks: false,

majorDelta: 2,

hideOverlappingLabels: false

})

);