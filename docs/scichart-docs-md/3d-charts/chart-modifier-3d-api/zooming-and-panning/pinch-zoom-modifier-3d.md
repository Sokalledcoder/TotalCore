---
source: https://www.scichart.com/documentation/js/v4/3d-charts/chart-modifier-3d-api/zooming-and-panning/pinch-zoom-modifier-3d
scraped_at: 2025-11-28T18:24:56.016980
---

# https://www.scichart.com/documentation/js/v4/3d-charts/chart-modifier-3d-api/zooming-and-panning/pinch-zoom-modifier-3d

# Pinch Zoom Modifier 3D

Zooming and Panning a Chart in SciChart.js is achieved by moving the SciChart3DSurface.camera📘 to a new location.

The article "The SciChart3DSurface Camera" goes into detail how this camera class works and how to manipulate it programatically to achieve various views.

If you want to add simple Pinch Zooming via Touch to the chart then you can do so using our ChartModifiers API. The PinchZoomModifier3D📘 was added to SciChart.js v3.2 and performs adjustment of the camera radius giving the appearance of the chart zooming.

## Declaring an PinchZoomModifier3D

Declaring a PinchZoomModifier3D📘 is as simple as adding one to the SciChart3DSurface.chartModifiers📘 property. This can be done as a single modifier, or as part of a group.

- TS
- HTML
- CSS

`// const { OrbitModifier3D, PinchZoomModifier3D, MouseWheelZoomModifier3D, ResetCamera3DModifier } = SciChart;`

// or for npm: import { OrbitModifier3D, PinchZoomModifier3D, MouseWheelZoomModifier3D, ResetCamera3DModifier } from "scichart"

// Add multiple behaviours including pinch-zoom to the chart

sciChart3DSurface.chartModifiers.add(

new PinchZoomModifier3D(),

new OrbitModifier3D(),

new MouseWheelZoomModifier3D(),

new ResetCamera3DModifier()

);

`<div class="wrapper">`

<div id="scichart-root"></div>

<div class="titleWrapper">

<p class="title">SciChart.js 3D Chart Example</p>

<p class="subTitle">Use Touch to zoom and pan the chart</p>

<p class="subTitle">Pinch zoom is enabled via PinchZoomModifier3D</p>

</div>

<div id="debug-camera">

<!-- Debug output from camera will be put here -->

</div>

</div>

`body {`

margin: 0;

font-family: Arial;

}

.wrapper {

width: 100%;

height: 100vh;

position: relative;

}

#scichart-root {

width: 100%;

height: 100%;

position: relative;

}

.titleWrapper {

position: absolute;

width: 100%;

top: 35%;

text-align: center;

pointer-events: none;

color: #ffffff77;

}

.title {

font-size: 20px;

}

.subTitle {

font-size: 16px;

}

#debug-camera {

pointer-events: none;

position: absolute;

left: 10px;

top: 10px;

color: #ffffff;

background: #00000077;

padding: 10px;

font-size: 13px;

}

This results in the following behaviour added to the chart.