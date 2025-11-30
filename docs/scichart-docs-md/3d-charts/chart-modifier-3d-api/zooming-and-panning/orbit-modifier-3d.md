---
source: https://www.scichart.com/documentation/js/v4/3d-charts/chart-modifier-3d-api/zooming-and-panning/orbit-modifier-3d
scraped_at: 2025-11-28T18:24:55.704145
---

# https://www.scichart.com/documentation/js/v4/3d-charts/chart-modifier-3d-api/zooming-and-panning/orbit-modifier-3d

# Orbit Modifier 3D

Zooming and Panning a Chart in SciChart.js is achieved by moving the SciChart3DSurface.camera📘 to a new location.

The article "The SciChart3DSurface Camera" goes into detail how this camera class works and how to manipulate it programatically to achieve various views.

If you want to add simple panning of the camera to the chart then you can do so using our ChartModifiers API. The OrbitModifier3D📘 performs orbital motion of the camera giving the appearance of the chart rotating.

## Declaring an OrbitModifier3D

Declaring an OrbitModifier3D📘 is as simple as adding one to the SciChart3DSurface.chartModifiers📘 property. This can be done as a single modifier, or as part of a group.

- TS
- HTML
- CSS

// const { OrbitModifier3D, EExecuteOn } = SciChart;

// or for npm: import { OrbitModifier3D, EExecuteOn } from "scichart"

sciChart3DSurface.chartModifiers.add(

new OrbitModifier3D({

executeCondition: { button: EExecuteOn.MouseLeftButton }

})

);

`<div class="wrapper">`

<div id="scichart-root"></div>

<div class="titleWrapper">

<p class="title">SciChart.js 3D Chart Example</p>

<p class="subTitle">Drag the mouse to orbit the 3D chart</p>

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