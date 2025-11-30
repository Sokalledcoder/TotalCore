---
source: https://www.scichart.com/documentation/js/v4/3d-charts/chart-modifier-3d-api/zooming-and-panning/reset-camera-modifier-3d
scraped_at: 2025-11-28T18:24:56.061841
---

# https://www.scichart.com/documentation/js/v4/3d-charts/chart-modifier-3d-api/zooming-and-panning/reset-camera-modifier-3d

# Reset Camera Modifier 3D

Zooming and Panning a Chart in SciChart.js is achieved by moving the SciChart3DSurface.camera📘 to a new location.

The article "The SciChart3DSurface Camera" goes into detail how this camera class works and how to manipulate it programatically to achieve various views.

If you add any zooming or panning to the chart you might want to reset the viewport to it's original state. You can do this with the ResetCamera3DModifier📘.

How this modifier works:

- When the ResetCamera3DModifier📘 is attached to the chart, it saves the current camera📘 state.
- An optional destination object of type TCameraState📘 may be set to override this state.
- When you double click on the chart, the ResetCamera3DModifier📘 animates the camera position to the initial camera state.

## Declaring an ResetCameraModifier3D

Declaring a ResetCamera3DModifier📘 is as simple as adding one to the SciChart3DSurface.chartModifiers📘 property. This can be done as a single modifier, or as part of a group.

- TS
- HTML
- CSS

`// const { ResetCamera3DModifier } = SciChart;`

// or for npm: import { ResetCameraModifier3D } from "scichart"

sciChart3DSurface.chartModifiers.add(

new ResetCamera3DModifier ({

// Optional properties. If these are not set,

// the ResetCameraModifier3D grabs initial state from the SciChart3DSurface.camera

isAnimated: true,

animationDuration: 2000,

// Camera will animate to this position on double click (or initial position if not set)

destination: {

radius: 450,

pitch: 30,

yaw: 45,

}

}),

);

`<div class="wrapper">`

<div id="scichart-root"></div>

<div class="titleWrapper">

<p class="title">SciChart.js 3D Chart Example</p>

<p class="subTitle">Double Click the chart to reset Camera State</p>

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

If you double click by the left mouse button you will notice how the camera resets.