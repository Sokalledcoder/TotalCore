---
source: https://www.scichart.com/documentation/js/v4/3d-charts/scichart-3d-basics/scichart-3d-surface-create-and-create-single
scraped_at: 2025-11-28T18:24:58.997840
---

# https://www.scichart.com/documentation/js/v4/3d-charts/scichart-3d-basics/scichart-3d-surface-create-and-create-single

# SciChart3DSurface.create() vs. createSingle()

Instantiating a new SciChart3DSurface📘 chart is accomplished with the SciChart3DSurface.create()📘 function. We have some variations on this function which can be used in different scenarios. We'll go through these as well as WebAssembly (wasm) file loading below.

## SciChart3DSurface.create()

The first function to create a 3D chart in SciChart.js is simply SciChart3DSurface.create()📘. This is an **asynchronous static function** which places a SciChart3DSurface (a single chart with X, Y, Z axis and one to many series) into the HTML Dom. It will also load WebAssembly files and initialise our 3D WebGL engine for the first chart load.

- SciChart3DSurface.create()

`import { SciChart3DSurface } from "scichart";`

async function initSciChart1() {

// Assumes a div in your HTML <div id="scichart-div-id"></div>

const { sciChart3DSurface, wasmContext } = await SciChart3DSurface.create("scichart-div-id");

// Now manipulate the sciChart3DSurface, adding axis, series and more

// When you exit the page and no longer want the chart to draw, call .delete() to free memory

sciChart3DSurface.delete();

}

SciChart3DSurface.create()📘 **uses a single, shared WebGL context for all chart surfaces on the screen**. This bypasses the maximum number of WebGL contexts and you can have 10, 20, 30 or even 100 charts on an HTML page. The only limit is performance of the browser in rendering the chart surfaces. **For a higher performance solution which uses one WebGL context per chart, see** SciChart3DSurface.createSingle()📘

**Ensure that you await SciChart3DSurface.create().** The return type is an object containing SciChart3DSurface and its wasmContext (WebAssembly Context) which must be passed to other chart parts on this SciChart3DSurface.

## SciChart3DSurface.createSingle()

SciChart3DSurface.createSingle()📘 is also an asynchronous static function which places a SciChart3DSurface into the DOM. However, this variation forces one WebGL context per chart. This can improve performance in multi-chart scenarios but you must obey the WebGL Context Limits per browser. More on this in our Performance Tips article.

- SciChart3DSurface.createSingle()

`import { SciChart3DSurface } from "scichart";`

async function initSciChart2() {

// Assumes a div in your HTML <div id="scichart-div-id"></div>

const { sciChart3DSurface, wasmContext } = await SciChart3DSurface.createSingle("scichart-div-id");

// Now manipulate the sciChart3DSurface, adding axis, series and more

// When you exit the page and no longer want the chart to draw, call .delete() to free memory

sciChart3DSurface.delete();

}

### Resolving Wasm errors on load

If you get an error when loading a SciChart3DSurface as follows:

Could not load SciChart WebAssembly module. Check your build process and ensure that your scichart3d.wasm and scichart3d.js files are from the same version

If so, find out how to resolve this at the page Deploying Wasm and Data files.