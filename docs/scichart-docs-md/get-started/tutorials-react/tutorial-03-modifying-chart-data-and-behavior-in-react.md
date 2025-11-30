---
source: https://www.scichart.com/documentation/js/v4/get-started/tutorials-react/tutorial-03-modifying-chart-data-and-behavior-in-react
scraped_at: 2025-11-28T18:25:04.621246
---

# https://www.scichart.com/documentation/js/v4/get-started/tutorials-react/tutorial-03-modifying-chart-data-and-behavior-in-react

# Tutorial 03 - Modifying Chart Data and Behavior in React

In this tutorial we will show how to modify the ** initChart** callback in

**scichart-react**to pass properties, functions, or data back into

**onInit**. This allows you to connect chart behavior to other UI elements in your React application, such as buttons or controls, to manipulate chart data or modify chart state.

The previous tutorial Tutorial 01 - Understanding the scichart-react boilerplate should be used as a reference for project setup. Copy the boilerplate to a new folder or project from: Boilerplates/scichart-react.

## Accessing & Controlling the Chart via Nested Components

We will modify **App.jsx** to replace `chartConfig`

with an **initChart** function. This function initializes the chart and returns additional functions to control it. These are accessible through **initResult**, which can be used in **onInit** or via **SciChartSurfaceContext**.

### initChart Function

`import {`

SciChartJsNavyTheme,

SciChartSurface,

NumericAxis,

SplineMountainRenderableSeries,

CursorModifier,

XyDataSeries,

} from "scichart";

import React, { useContext } from "react";

import { SciChartReact, SciChartSurfaceContext } from "scichart-react";

export const initChart = async (rootElement) => {

const { sciChartSurface, wasmContext } = await SciChartSurface.create(

rootElement,

{ theme: new SciChartJsNavyTheme() }

);

sciChartSurface.xAxes.add(new NumericAxis(wasmContext));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext));

const xValues = [0,1,2,3,4,5,6,7,8,9];

const yValues = [1,4,7,3,7,6,7,4,2,5];

const mountainSeries = new SplineMountainRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues }),

fill: "SteelBlue",

stroke: "White",

strokeThickness: 4,

opacity: 0.4,

});

sciChartSurface.renderableSeries.add(mountainSeries);

const cursor = new CursorModifier({

showTooltip: true,

showYLine: true,

showXLine: true,

showAxisLabels: true,

crosshairStroke: "White",

crosshairStrokeDashArray: [5, 5],

});

cursor.isEnabled = false;

sciChartSurface.chartModifiers.add(cursor);

const addData = () => {

const x = xValues.length;

const y = Math.random() * 10;

xValues.push(x);

yValues.push(y);

mountainSeries.dataSeries.append(x, y);

sciChartSurface.zoomExtents(500);

};

const enableTooltip = (enable) => { cursor.isEnabled = enable; };

const getTooltipEnabled = () => cursor.isEnabled;

return { sciChartSurface, addData, enableTooltip, getTooltipEnabled };

};

### Nested Components in App.jsx

`import React, { useContext } from "react";`

import { SciChartReact, SciChartSurfaceContext } from "scichart-react";

import { initChart } from "./initChart";

const AddDataButton = () => {

const initResult = useContext(SciChartSurfaceContext);

return <input type="button" value="Add Data" onClick={() => initResult.addData()} />;

};

const EnableTooltipButton = () => {

const initResult = useContext(SciChartSurfaceContext);

const handleClick = () => {

const tooltipEnabled = initResult.getTooltipEnabled();

initResult.enableTooltip(!tooltipEnabled);

};

return <input type="button" value="Toggle Tooltip" onClick={handleClick} />;

};

function App() {

return (

<div className="App">

<header className="App-header">

<h1><SciChartReact/> with custom chart controls</h1>

</header>

<SciChartReact initChart={initChart} style={{ maxWidth: 900, height: 600 }}>

<div style={{ display: "flex", justifyContent: "center" }}>

<AddDataButton />

<EnableTooltipButton />

</div>

</SciChartReact>

</div>

);

}

export default App;

## Accessing the Chart via Non-Nested Components

To access the chart from buttons or UI components outside the `<SciChartReact />`

element, you can store **initResult** in React state and share it via Context.

### initChart.js (with modifiers)

`import {`

SciChartJsNavyTheme,

SciChartSurface,

NumericAxis,

SplineMountainRenderableSeries,

RubberBandXyZoomModifier,

ZoomPanModifier,

RolloverModifier,

XyDataSeries,

EllipsePointMarker,

ZoomExtentsModifier,

MouseWheelZoomModifier,

} from "scichart";

export const initChart = async (rootElement) => {

const { sciChartSurface, wasmContext } = await SciChartSurface.create(rootElement, { theme: new SciChartJsNavyTheme() });

sciChartSurface.xAxes.add(new NumericAxis(wasmContext, { axisTitle: "X Axis" }));

sciChartSurface.yAxes.add(new NumericAxis(wasmContext, { axisTitle: "Y Axis" }));

const xValues = [0,1,2,3,4,5,6,7,8,9];

const yValues = [1,4,7,3,7,6,7,4,2,5];

const mountainSeries = new SplineMountainRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { dataSeriesName: "Mountain Series", xValues, yValues }),

fill: "SteelBlue",

stroke: "White",

strokeThickness: 4,

opacity: 0.4,

pointMarker: new EllipsePointMarker(wasmContext, { width: 7, height: 7, fill: "White", strokeThickness: 0 }),

});

mountainSeries.rolloverModifierProps.tooltipTextColor = "#fff";

mountainSeries.rolloverModifierProps.tooltipColor = "SteelBlue";

mountainSeries.tooltipLabelX = "X";

mountainSeries.tooltipLabelY = "Y";

sciChartSurface.renderableSeries.add(mountainSeries);

const rolloverModifier = new RolloverModifier({ rolloverLineStroke: "LightSteelBlue", snapToDataPoint: true });

const rubberBandZoomModifier = new RubberBandXyZoomModifier({ stroke: "#FFFFFF77", fill: "#FFFFFF33", strokeThickness: 1 });

const zoomPanModifier = new ZoomPanModifier();

const zoomExtentsModifier = new ZoomExtentsModifier();

const mouseWheelZoomModifier = new MouseWheelZoomModifier();

rolloverModifier.isEnabled = false;

zoomPanModifier.isEnabled = false;

rubberBandZoomModifier.isEnabled = true;

sciChartSurface.chartModifiers.add(rolloverModifier, rubberBandZoomModifier, zoomPanModifier, zoomExtentsModifier, mouseWheelZoomModifier);

return { sciChartSurface, rolloverModifier, zoomPanModifier, rubberBandZoomModifier };

};

### App.jsx with Toolbar & Context

`import React, { useState } from "react";`

import { SciChartReact } from "scichart-react";

import { ToggleButton } from "./ToggleButton";

import { ChartContext } from "./ChartContext";

import { initChart } from "./initChart";

import "./styles.css";

function App() {

const [chartState, setChartState] = useState(null);

return (

<ChartContext.Provider value={{ chartState, setChartState }}>

<div className="App">

<header className="App-header">

<h1><SciChartReact/> with custom chart controls</h1>

</header>

<div style={{ display: "flex", justifyContent: "left", backgroundColor: "lightgrey", padding: "10px" }}>

<ToggleButton label="Zoom" modifierKey="rubberBandZoomModifier" />

<ToggleButton label="Pan" modifierKey="zoomPanModifier" />

<ToggleButton label="Tooltip" modifierKey="rolloverModifier" />

<button onClick={() => chartState?.sciChartSurface?.zoomExtents(500)} className="normal-button">Zoom to Fit</button>

</div>

<SciChartReact initChart={initChart} onInit={setChartState} style={{ maxWidth: 900, height: 600 }} />

</div>

</ChartContext.Provider>

);

}

export default App;

### ToggleButton.jsx

`import React, { useContext } from "react";`

import { ChartContext } from "./ChartContext";

import "./styles.css";

export const ToggleButton = ({ label, modifierKey }) => {

const { chartState, setChartState } = useContext(ChartContext);

const handleClick = () => {

if (!chartState) return;

const { sciChartSurface, ...modifiers } = chartState;

Object.values(modifiers).forEach((modifier) => modifier.isEnabled = false);

modifiers[modifierKey].isEnabled = true;

setChartState({ ...chartState });

};

return (

<button onClick={handleClick} className={`toggle-button ${chartState?.[modifierKey]?.isEnabled ? "active" : ""}`}>

{label}

</button>

);

};

### ChartContext.jsx

`import { createContext } from "react";`

export const ChartContext = createContext(null);

### Styles (styles.css)

`.toggle-button {`

background-color: #e0e0e0;

color: #333;

border: none;

padding: 8px 16px;

border-radius: 2px;

cursor: pointer;

font-size: 14px;

font-weight: bold;

box-shadow: 0 1px 3px rgba(0,0,0,0.2);

transition: background 0.2s, color 0.2s, box-shadow 0.2s;

}

.toggle-button.active {

background-color: #007aff;

color: white;

box-shadow: 0 2px 5px rgba(0,122,255,0.5);

}

.normal-button {

background-color: #e0e0e0;

color: #333;

border: none;

padding: 8px 16px;

border-radius: 2px;

cursor: pointer;

font-size: 14px;

font-weight: bold;

box-shadow: 0 2px 5px rgba(0,0,0,0.2);

}

.normal-button:hover {

background-color: #55aaff;

}

To load this CSS, install `style-loader`

and `css-loader`

and update **webpack.config.js**:

`npm install --save-dev style-loader css-loader`

Add the rule:

`{`

test: /\.css$/,

use: ["style-loader", "css-loader"],

}

Full source code is available on GitHub: Tutorials/React/Tutorial_03b_Controlling_Chart_Behaviour_With_Toolbar