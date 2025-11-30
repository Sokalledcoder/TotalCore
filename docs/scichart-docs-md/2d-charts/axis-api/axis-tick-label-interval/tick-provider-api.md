---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-tick-label-interval/tick-provider-api
scraped_at: 2025-11-28T18:24:07.856546
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-tick-label-interval/tick-provider-api

# The TickProvider API

If you want to have absolute control over the gridlines, labels and minor gridline spacing in SciChart.js, you can use the **TickProvider API**.

Every axis implementation has an axisCore.tickProvider📘 property. This accepts a class which inherits TickProvider📘. Several classes are built-in such as NumericTickProvider📘 and LogarithmicTickProvider📘 which SciChart uses internally.

The inheritance diagram for TickProviders in SciChart.js looks like this:

You can create your own TickProvider if you want to have absolute control over the axis gridlines and label spacing. This API allows you to create some pretty advanced customisations with SciChart.js that are hard to achieve otherwise.

## Example 1: Our NumericTickProvider

Below here how our NumericTickProvider📘 is implemented. This code is shared for example purposes so you can see the inner workings of this class. **For a worked example, scroll down**.

In the code below:

- The method getMajorTicks()📘 returns an array of values where you want to place major gridlines and labels.
- The method getMinorTicks()📘 returns an array of values where you want to place minor gridlines.

Both arrays are in data-coordinates, not pixels. E.g. if your Chart has data between 0..10 then you want to set major gridlines at 2,4,6,8 then return [2, 4, 6, 8] as an array from getMajorTicks.

- NumericTickProvider source code v4.0

`export class NumericTickProvider extends TickProvider {`

private readonly minDeltaValue: number = 1e-13;

private webAssemblyContext: TSciChart | TSciChart3D;

/**

* Creates an instance of a NumericTickProvider

* @param webAssemblyContext The {@link TSciChart | SciChart 2D WebAssembly Context} or {@link TSciChart | SciChart 3D WebAssembly Context}

* containing native methods and access to our WebGL2 WebAssembly Rendering Engine

*/

constructor(webAssemblyContext: TSciChart | TSciChart3D) {

super();

this.webAssemblyContext = webAssemblyContext;

}

/**

* @inheritDoc

*/

public getMinorTicks(minorDelta: number, majorDelta: number, visibleRange: NumberRange): number[] {

const deltaRange = new NumberRange(minorDelta, majorDelta);

const tickRange = visibleRange;

if (!this.isParamsValid(tickRange, deltaRange)) {

return [];

}

return this.calculateTicks(tickRange, deltaRange.min, deltaRange.max);

}

/**

* @inheritDoc

*/

public getMajorTicks(minorDelta: number, majorDelta: number, visibleRange: NumberRange): number[] {

const deltaRange = new NumberRange(minorDelta, majorDelta);

const tickRange = visibleRange;

if (!this.isParamsValid(tickRange, deltaRange)) {

return [];

}

return this.calculateTicks(tickRange, deltaRange.max, deltaRange.max);

}

/**

* @summary Performs sanity checks to see if parameters are valid.

* @description If this method returns false, then we should not process or compute major/minor gridlines, but instead should

* return empty array ```[]``` in {@link getMajorTicks} / {@link getMinorTicks}

* @param visibleRange The current {@link AxisCore.visibleRange} which is the minimum / maximum range visible on the Axis.

* @param deltaRange The current {@link AxisCore.minorDelta} and {@link AxisCore.majorDelta} which is the difference between minor

* and major gridlines requested by the {@link AxisCore | Axis}

*/

protected isParamsValid(visibleRange: NumberRange, deltaRange: NumberRange): boolean {

Guard.notNull(visibleRange, "visibleRange");

Guard.notNull(deltaRange, "deltaRange");

return (

isRealNumber(visibleRange.min) && isRealNumber(visibleRange.max) && deltaRange.min > 0 && deltaRange.max > 0

);

}

/**

* @summary Performs the Numeric tick calculation

* @param visibleRange The current {@link AxisCore.visibleRange} which is the minimum / maximum range visible on the Axis.

* @param delta The delta we are calculating for (could be major or minor delta)

* @param majorDelta The current {@link AxisCore.majorDelta} which is the difference between major

* gridlines requested by the {@link AxisCore | Axis}

*/

protected calculateTicks(visibleRange: NumberRange, delta: number, majorDelta: number): number[] {

const results: number[] = [];

const min = visibleRange.min;

const max = visibleRange.max;

const calcMajorTicks = delta === majorDelta;

const numberUtil = this.webAssemblyContext.NumberUtil;

// Skip the divisiblity check here as it can return true if the min is within epsilon of being divisible,

// but false for min + delta, leading to only one tick being output.

let current = numberUtil.RoundUp(min, delta);

const start = current;

let tickCount = 0;

while (current <= max) {

// TRUE if major ticks are calculated && Current is divisible by MajorDelta

// or if minor ticks are calculated && Current is NOT divisible by MajorDelta

if (!(numberUtil.IsDivisibleBy(current, majorDelta) !== calcMajorTicks)) {

results.push(current);

}

current = start + ++tickCount * delta;

}

return results;

}

}

## Example 2: Custom TickProvider

Below we've included a worked example of a custom tickprovider. This is a very simplistic implementation that returns hard-coded spacings for major & minor gridlines. However, it could be easily customised to behave dynamically based on the minorDelta, majorDelta and visibleRange passed into the getMajorTicks/getMinorTicks functions.

First, create the TickProvider class and implement getMajorTicks/getMinorTicks:

- TS

`const { NumericTickProvider } = SciChart;`

// or, for npm, import { NumericTickProvider, ... } from "scichart"

// Custom TickProvider implementation

//

class CustomTickProvider extends NumericTickProvider {

constructor(wasmContext) {

super(wasmContext);

}

// returns an array of minor gridline positions in data space

// Called once per draw. Can be dynamic

getMinorTicks(minorDelta, majorDelta, visibleRange) {

// Todo here: calculate your tick spacing based on axis minorDelta, majorDelta and visibleRange

// Note we do not return major ticks here, so minor ticks exclude the majors

return [

0.2, 0.4, 0.6, 0.8, 1.2, 1.4, 1.6, 1.8, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.2, 4.4, 4.6, 4.8,

5.0, 5.2, 5.4, 5.6, 5.8, 6.0, 6.2, 6.4, 6.6, 6.8, 7.0, 7.2, 7.4, 7.6, 7.8, 8.2, 8.4, 8.6, 8.8, 9.0, 9.2,

9.4, 9.6, 9.8

];

}

// returns an array of major gridline positions in data space

// Called once per draw. Can be dynamic

getMajorTicks(minorDelta, majorDelta, visibleRange) {

// Todo here: calculate your tick spacing based on axis minorDelta, majorDelta and visibleRange

// Note we return the major tick intervals and label intervals here

return [0, 1, 2, 4, 8];

}

}

Then, apply the TickProvider to an axis like this:

- TS
- Builder API (JSON Config)

`// Demonstrates how to apply a custom tickprovider in SciChart.js`

const { SciChartSurface, NumericAxis, SciChartJsNavyTheme } = SciChart;

// or, for npm, import { SciChartSurface, ... } from "scichart"

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme()

});

// Adjust major/minor gridline style to make it clearer for the demo

const styleOptions = {

majorGridLineStyle: { color: "#50C7E077" },

minorGridLineStyle: { color: "#50C7E033" }

};

// Create an XAxis on the bottom

const xAxis = new NumericAxis(wasmContext, {

...styleOptions,

axisTitle: "Custom TickProvider - unequally spaced gridlines"

});

// Apply the tickProvider

xAxis.tickProvider = new CustomTickProvider(wasmContext);

// Add the xAxis to the chart

sciChartSurface.xAxes.add(xAxis);

// TODO You can also apply a tickprovider in constructor options

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

// tickProvider: new CustomTickProvider(wasmContext),

...styleOptions

})

);

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: {

type: EAxisType.NumericAxis,

options: {

axisTitle: "Custom TickProvider - unequally spaced gridlines"

}

},

yAxes: {

type: EAxisType.NumericAxis,

options: {

axisTitle: "Y Axis"

}

}

});

// Tickproviders must be applied after the fact using the Builder API

sciChartSurface.xAxes.get(0).tickProvider = new CustomTickProvider(wasmContext);

This results in an uneven spacing of ticklines or gridlines in SciChart which looks like this:

You can customize TickProviders further and even return dynamic arrays. For example, if you wanted to ensure an equally sized grid independent of zoom level, or to dynamically change the number of gridlines on screen, you can do it with the TickProvider API.