---
source: https://www.scichart.com/documentation/js/v4/2d-charts/builder-api/charts-serialization-deserialization
scraped_at: 2025-11-28T18:24:12.686913
---

# https://www.scichart.com/documentation/js/v4/2d-charts/builder-api/charts-serialization-deserialization

# Serialization and Deserialization of Charts

Pretty much everything in SciChart now has a `toJSON()`

method that will return the definition form of that object, usually as `{ type, options }`

. When you call **JSON.stringify()** on an object, `toJSON()`

will be called automatically.

By default, any data set on the chart will be included in the definition. If you want to exclude it, you need to call `toJSON()`

directly, which for the **SciChartSurface** and **renderableSeries** has an **excludeData** parameter. Then stringify the result.

`const definition = sciChartSurface.toJSON(true);`

const json = JSON.stringify(definition);

When handling incoming JSON, you may want to parse the string to a definition object, in order to combine it with something (usually data) before using it to build the chart. To do this you MUST use the chartReviver📘 on chartBuilder📘 to ensure that the types are correctly deserialized.

`import { chartBuilder } from "scichart";`

const definition = JSON.parse(json, chartBuilder.chartReviver);

const { sciChartSurface, wasmContext } = await chartBuilder.build2DChart(divElementId, definition);

All of the Builder API functions for building parts of charts can take JSON strings or a definition object.

Try this code and this JSON to see the output in SciChart.js

`import {`

chartBuilder,

ESeriesType,

EChart2DModifierType,

ISciChart2DDefinition

} from "scichart";

export async function drawAndSerializeChart(divElementId) {

const { sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

series: {

type: ESeriesType.LineSeries,

xyData: {

xValues: [1, 3, 4, 7, 9],

yValues: [10, 6, 7, 2, 16]

}

}

});

const definition = sciChartSurface.toJSON(true);

const json = JSON.stringify(definition);

console.log("json definition: ");

console.log(json);

}

export async function deserializeAndDrawChart(divElementId) {

const jsonDefinition = {

"surface": {

"canvasBorder": {

"color": "#00000000"

},

"layoutManager": {

"type": "Default"

},

"padding": {

"top": 10,

"right": 10,

"bottom": 10,

"left": 10

},

"theme": {

"type": "Dark"

},

"viewportBorder": {

"color": "#00000000"

}

},

"xAxes": [

{

"type": "NumericAxis",

"options": {

"autoRange": "Once",

"autoTicks": true,

"axisAlignment": "Bottom",

"axisBandsFill": "#20212333",

"axisBorder": {

"borderBottom": 0,

"borderLeft": 0,

"borderRight": 0,

"borderTop": 0,

"color": "#00000000",

"border": 0

},

"axisTitleStyle": {

"fontSize": 24,

"fontFamily": "Arial",

"color": "#C8C7C3FF",

"fontStyle": "normal",

"fontWeight": "normal",

"padding": {

"top": 6,

"right": 6,

"bottom": 6,

"left": 6

}

},

"drawLabels": true,

"drawMajorBands": true,

"drawMajorGridLines": true,

"drawMajorTickLines": true,

"drawMinorGridLines": true,

"drawMinorTickLines": true,

"flippedCoordinates": false,

"id": "DefaultAxisId",

"isInnerAxis": false,

"isVisible": true,

"labelStyle": {

"fontSize": 14,

"fontFamily": "Arial",

"color": "#A6A7ACFF",

"fontWeight": "normal",

"fontStyle": "normal",

"padding": {

"top": 1,

"right": 4,

"bottom": 1,

"left": 4

},

"alignment": "Auto"

},

"majorGridLineStyle": {

"strokeThickness": 1,

"color": "#AAAAAA37"

},

"majorTickLineStyle": {

"tickSize": 5,

"strokeThickness": 1,

"color": "#AAAAAA37"

},

"maxAutoTicks": 10,

"minorGridLineStyle": {

"strokeThickness": 1,

"color": "#77777719"

},

"minorTickLineStyle": {

"tickSize": 3,

"strokeThickness": 1,

"color": "#77777719"

},

"minorsPerMajor": 5

}

}

],

"yAxes": [

{

"type": "NumericAxis",

"options": {

"autoRange": "Once",

"autoTicks": true,

"axisAlignment": "Right",

"axisBandsFill": "#20212333",

"axisBorder": {

"borderBottom": 0,

"borderLeft": 0,

"borderRight": 0,

"borderTop": 0,

"color": "#00000000",

"border": 0

},

"axisTitleStyle": {

"fontSize": 24,

"fontFamily": "Arial",

"color": "#C8C7C3FF",

"fontStyle": "normal",

"fontWeight": "normal",

"padding": {

"top": 6,

"right": 6,

"bottom": 6,

"left": 6

}

},

"drawLabels": true,

"drawMajorBands": true,

"drawMajorGridLines": true,

"drawMajorTickLines": true,

"drawMinorGridLines": true,

"drawMinorTickLines": true,

"flippedCoordinates": false,

"id": "DefaultAxisId",

"isInnerAxis": false,

"isVisible": true,

"labelStyle": {

"fontSize": 14,

"fontFamily": "Arial",

"color": "#A6A7ACFF",

"fontWeight": "normal",

"fontStyle": "normal",

"padding": {

"top": 1,

"right": 4,

"bottom": 1,

"left": 4

},

"alignment": "Auto"

},

"majorGridLineStyle": {

"strokeThickness": 1,

"color": "#AAAAAA37"

},

"majorTickLineStyle": {

"tickSize": 5,

"strokeThickness": 1,

"color": "#AAAAAA37"

},

"maxAutoTicks": 10,

"minorGridLineStyle": {

"strokeThickness": 1,

"color": "#77777719"

},

"minorTickLineStyle": {

"tickSize": 3,

"strokeThickness": 1,

"color": "#77777719"

},

"minorsPerMajor": 5

}

}

],

"series": [

{

"type": "LineSeries",

"options": {

"id": "2a152f26-3248-474a-8040-203337f2f670",

"drawNaNAs": 1,

"isDigitalLine": false,

"isHovered": false,

"isSelected": false,

"isVisible": true,

"opacity": 1,

"stroke": "#C6E6FFFF",

"strokeThickness": 2,

"xAxisId": "DefaultAxisId",

"yAxisId": "DefaultAxisId"

},

"xyData": {

"containsNaN": true,

"dataIsSortedInX": true

}

}

],

"modifiers": [],

"annotations": []

};

const definition = JSON.parse(json, chartBuilder.chartReviver);

definition.modifiers = [{ type: EChart2DModifierType.Rollover }];

return chartBuilder.build2DChart(divElementId, definition);

}

You can generate JSON chart definitions as well using the SciChart.js library. For example if you wanted to define a chart definition on the server and send this over to a client as JSON it's possible to do this.

For more information and a workable example, try the Chart Serialization demo on our JavaScript Chart Examples