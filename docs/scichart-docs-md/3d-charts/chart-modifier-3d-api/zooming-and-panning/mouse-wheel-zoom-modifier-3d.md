---
source: https://www.scichart.com/documentation/js/v4/3d-charts/chart-modifier-3d-api/zooming-and-panning/mouse-wheel-zoom-modifier-3d
scraped_at: 2025-11-28T18:24:55.751067
---

# https://www.scichart.com/documentation/js/v4/3d-charts/chart-modifier-3d-api/zooming-and-panning/mouse-wheel-zoom-modifier-3d

# Mouse Wheel Zoom Modifier 3D

Zooming and Panning a Chart in SciChart.js is achieved by moving the SciChart3DSurface.camera📘 to a new location.

The article "The SciChart3DSurface Camera" goes into detail how this camera class works and how to manipulate it programatically to achieve various views.

If you want to add simple zooming in/out of the camera to the chart then you can do so using our ChartModifiers API. The MouseWheelZoomModifier3D📘 performs movement of the camera by adjusting the radius property, giving the appearance of the chart zooming.

## Declaring an MouseWheelZoomModifier3D

Declaring a MouseWheelZoomModifier3D📘 is as simple as adding one to the SciChart3DSurface.chartModifiers📘 property. This can be done as a single modifier, or as part of a group.

- TS
- HTML
- CSS

`// const { MouseWheelZoomModifier3D } = SciChart;`

// or for npm: import { MouseWheelZoomModifier3D } from "scichart"

sciChart3DSurface.chartModifiers.add(new MouseWheelZoomModifier3D());

`<div class="wrapper">`

<div id="scichart-root"></div>

<div class="titleWrapper">

<p class="title">SciChart.js 3D Chart Example</p>

<p class="subTitle">Use the Mouse Wheel to Zoom the 3D chart</p>

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