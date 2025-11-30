---
source: https://www.scichart.com/documentation/js/v4/2d-charts/surface/deploying-wasm
scraped_at: 2025-11-28T18:24:53.871921
---

# https://www.scichart.com/documentation/js/v4/2d-charts/surface/deploying-wasm

# Deploying Wasm (WebAssembly) with your app

If you receive an error message when running your app, you may not have deployed the Wasm (WebAssembly) or data files correctly. Below are some steps on how to resolve that.

**Error**: Could not load SciChart WebAssembly module. Check your build process and ensure that your scichart2d.wasm and scichart2d.js files are from the same version

### Option 1: Package Wasm & Data Files with Webpack (or similar)

In our tutorials and boilerplate examples we show you how to package the Wasm files to load them in a variety of JavaScript frameworks including React, Angular, Vue, Vite, Electron, Tauri, Svelte, Blazor, Next, Nuxt and more. Find the links to setting up a JavaScript project below:

| JS Project Framework | Boilerplate Project or Setup Instructions |
|---|---|
| npm / webpack | Tutorial - Setting up a project with Webpack |
| Vanilla Javascript CDN (no npm, webpack) | Tutorial - Including index.min.js and wasm files using CDN |
| Vanilla Javascript offline (no npm, webpack) | Tutorial - Including index.min.js and wasm files offline |
| React (scichart-react) | code sample |
| vue.js | code sample |
| svelte-vite | code sample |
| svelte-rollup | code sample |
| react-vite | code sample |
| nextjs | code sample |
| Nuxt.js | code sample |
| Angular | code sample |
| Angular (scichart-angular) | code sample |
| blazor via JS Interop | code sample |
| Electron | code sample |
| Tauri React Vite | code sample |
| Tauri Javascript Vite | code sample |
| Web components | code sample |

The above projects have been updated for SciChart.js v4, which has only a *.wasm file to serve. SciChart.js v3.x had *.wasm and *.data files. For older versions of SciChart, see the boilerplates folder in the dev 3.5 branch.

See more boilerplate examples for JavaScript frameworks at our Github repository: github.com/abtsoftware/scichart.js.examples under the Boilerplates folder

### Option 2: Load Wasm from URL with SciChartSurface.configure() or useWasmFromCDN()

The easiest way for SciChart.js to load WebAssembly and Data files are to load them from our CDN (see jsdelivr.com/package/npm/scichart). This method is particularly useful in projects or frameworks that don't have a package manager or module bundler.

To do load SciChart's Wasm and Data file from CDN, call SciChartSurface.configure()📘 once before any SciChartSurface is shown:

**Configure Wasm and Data File URLs**

`import { SciChartSurface, libraryVersion } from "scichart";`

// Load Wasm from URL

// This URL can be anything, but for example purposes we are loading from JSDelivr CDN

SciChartSurface.configure({

wasmUrl: `https://cdn.jsdelivr.net/npm/scichart@${libraryVersion}/_wasm/scichart2d.wasm`

});

We've packaged a helpful function that automatically loads the latest & correct version of SciChart's Wasm & Data files from CDN. To use this, instead of calling SciChartSurface.configure()📘 passing in a URL, call SciChartSurface.useWasmFromCDN()📘.

**Load Wasm from CDN**

`import { SciChartSurface } from "scichart";`

export async function initSciChart() {

// Call this once before any SciChartSurface is shown.

// This is equivalent to calling SciChartSurface.configure() with the CDN URL (JSDelivr)

SciChartSurface.useWasmFromCDN();

}

## Loading Wasm files offline

If your application must load wasm files offline (does not have an internet connection), you can download the files and serve them and use SciChartSurface.configure()📘 to fetch the local file.

To find out how to do this, see Tutorial 02 - Including index.min.js and WebAssembly Files offline.

## Loading Wasm for 3D Charts

The process for loading Wasm files for 3D Charts is exactly the same, except you must configure SciChart.js to load scichart3d.wasm.

This can be done via Webpack/npm or a bundlers, or by calling SciChart3DSurface.useWasmFromCDN()📘 or SciChart3DSurface.configure()📘 as before.

**Configure Wasm and Data File URLs**

`import { SciChartSurface } from "scichart";`

// Call this once before any SciChart3DSurface is shown to load wasm from CDN

SciChart3DSurface.useWasmFromCDN();

// Alternatively, if you want to host wasm files and serve them locally

// 1.) Ensure you are serving your wasm files

// 2.) Call to SciChart3DSurface.configure specifying the relative URL of the files

SciChart3DSurface.configure({

wasmUrl: `relative/path/to/scichart3d.wasm`

});