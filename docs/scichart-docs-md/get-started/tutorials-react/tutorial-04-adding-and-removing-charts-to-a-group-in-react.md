---
source: https://www.scichart.com/documentation/js/v4/get-started/tutorials-react/tutorial-04-adding-and-removing-charts-to-a-group-in-react
scraped_at: 2025-11-28T18:25:05.534146
---

# https://www.scichart.com/documentation/js/v4/get-started/tutorials-react/tutorial-04-adding-and-removing-charts-to-a-group-in-react

# Tutorial 04 - Adding & Removing Charts To a Group in React

In the previous tutorials we showed you how to use `<SciChartReact/>`

`onInit`

and React State / Contexts to control chart data and chart state via buttons hosted in your app.

In this tutorial, we're going to show how to **dynamically add and remove chart panels** from a `<SciChartGroup/>`

— a React component in **scichart-react** which allows you to host several charts together in a group and synchronize zooming, panning, and axis sizes to create dynamic linked dashboards using SciChart.js.

## Before We Begin

As a basis for this tutorial, use Tutorial 01 - Understanding the scichart-react boilerplate for the initial project setup.

Copy the boilerplate to a new folder or project. You can get the code from here: 👉 Boilerplates/scichart-react

## Step 1: Simplify the App Component

Let’s roll back some changes from the previous tutorial.
We want our **App.jsx** to be simpler, removing `ToggleButton`

, `<SciChartReact/>`

, and `ChartContext`

.

### App.jsx

`import React from "react";`

import "./styles.css";

function App() {

return (

<div className="App">

<header className="App-header">

<h1><SciChartReact/> with custom chart controls</h1>

</header>

<div

style={{

display: "flex",

justifyContent: "left",

backgroundColor: "lightgrey",

padding: "10px",

}}

>

{/* TODO: Add chart controls here */}

</div>

{/* TODO: Add SciChartReact here */}

</div>

);

}

export default App;

## Step 2: Creating a `<SciChartGroup/>`

We will now create a `<SciChartGroup/>`

which can host one or more `<SciChartReact/>`

components to make a dashboard or group of charts.

Import the necessary components:

`import { SciChartGroup, SciChartReact } from "scichart-react";`

Then replace `{/* TODO: Add SciChartReact here */}`

with a `<SciChartGroup/>`

element containing two `<SciChartReact/>`

components.

Each chart will be initialized with a simple `initChart`

function.

### App.jsx

`import React from "react";`

import "./styles.css";

import { SciChartGroup, SciChartReact } from "scichart-react";

import { SciChartSurface, NumericAxis, SciChartJsNavyTheme } from "scichart";

const simpleChart = async (divElement, chartId) => {

const { sciChartSurface, wasmContext } = await SciChartSurface.create(

divElement,

{

title: `Chart ${chartId}`,

titleStyle: { fontSize: 28 },

theme: new SciChartJsNavyTheme(),

}

);

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { axisTitle: "X Axis" }));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { axisTitle: "Y Axis" }));

return { sciChartSurface };

};

function App() {

return (

<div className="App">

<header className="App-header">

<h1><SciChartReact/> chart groups</h1>

</header>

<div

style={{

display: "flex",

justifyContent: "left",

backgroundColor: "lightgrey",

padding: "10px",

}}

>

{/* TODO: Add chart controls here */}

</div>

<div style={{ height: "600px" }}>

<SciChartGroup>

<SciChartReact initChart={(div) => simpleChart(div, 0)} style={{ height: "50%" }} />

<SciChartReact initChart={(div) => simpleChart(div, 1)} style={{ height: "50%" }} />

</SciChartGroup>

</div>

</div>

);

}

export default App;

If you run the app now, you should see the following output:

💡 Note:

`<SciChartGroup/>`

is a non-visual React component. To control the overall size, wrap it in a`<div>`

and set the height/width on that container. Individual`<SciChartReact/>`

elements can use relative sizes like`"50%"`

.

## Step 3: Dynamically Adding / Removing Charts

Next, let’s make this example **dynamic** by adding toolbar buttons to **Add** and **Remove** charts.
We’ll do this by modifying React state and re-rendering `<SciChartReact/>`

components within the `<SciChartGroup/>`

.

Start by importing `useState`

:

`import React, { useState } from "react";`

Then create an initial state and functions to add/remove charts.

### App.jsx

`function App() {`

const [charts, setCharts] = useState([0, 1]); // Initialize with 2 charts

const addChart = () => {

setCharts([...charts, charts.length]);

};

const removeChart = () => {

if (charts.length > 0) {

setCharts(charts.slice(0, -1));

}

};

## Step 4: Mapping Charts from State

We now map over the `charts`

array to create one `<SciChartReact/>`

per item.
The height of each chart will be dynamically adjusted based on how many charts exist, ensuring the total group height remains fixed at 600px.

### Final App.jsx

`import React, { useState } from "react";`

import "./styles.css";

import { SciChartGroup, SciChartReact } from "scichart-react";

import { SciChartSurface, NumericAxis, SciChartJsNavyTheme } from "scichart";

const simpleChart = async (divElement, chartId) => {

const { sciChartSurface, wasmContext } = await SciChartSurface.create(

divElement,

{

title: `Chart ${chartId}`,

titleStyle: { fontSize: 16 },

theme: new SciChartJsNavyTheme(),

}

);

sciChartSurface.xAxes.add(

new NumericAxis(wasmContext, {

axisTitle: "X Axis",

axisTitleStyle: { fontSize: 12 },

})

);

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

axisTitle: "Y Axis",

axisTitleStyle: { fontSize: 12 },

})

);

return { sciChartSurface };

};

function App() {

const [charts, setCharts] = useState([0, 1]); // Start with 2 charts

const addChart = () => {

setCharts([...charts, charts.length]);

};

const removeChart = () => {

if (charts.length > 0) {

setCharts(charts.slice(0, -1));

}

};

return (

<div className="App">

<header className="App-header">

<h1><SciChartReact/> chart groups</h1>

</header>

<div

style={{

display: "flex",

justifyContent: "left",

backgroundColor: "lightgrey",

padding: "10px",

}}

>

<button onClick={addChart} style={{ margin: "0 10px" }}>

Add Chart

</button>

<button onClick={removeChart} style={{ margin: "0 10px" }}>

Remove Chart

</button>

</div>

<div style={{ height: "600px" }}>

<SciChartGroup>

{charts.map((chartId) => (

<SciChartReact

key={chartId}

initChart={(div) => simpleChart(div, chartId)}

style={{ height: `${100 / charts.length}%` }}

/>

))}

</SciChartGroup>

</div>

</div>

);

}

export default App;

## Output

Now go ahead and run the app. You should see:

You can dynamically add or remove charts — each one synchronizes with the group layout.

## Full Source Code

You can find the full example here: 👉 Tutorials/React/Tutorial_04_Adding_Removing_Syncing_Charts