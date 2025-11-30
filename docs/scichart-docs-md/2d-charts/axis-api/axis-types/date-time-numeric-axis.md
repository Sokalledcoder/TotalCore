---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-types/date-time-numeric-axis
scraped_at: 2025-11-28T18:24:08.438240
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-types/date-time-numeric-axis

# The DateTimeNumericAxis

The DateTimeNumericAxis📘 is a Value axis (subclass of NumericAxis📘) and has some extra formatting options and features for handling date formatting.

Learn more about the commonalities between axis here.

## Create and Configure a DateTimeNumericAxis

Dates in SciChart.js are treated as Linux timestamps divided by 1000 (to get seconds from milliseconds). e.g. to create a DateTimeNumericAxis in SciChart.js, use the following code:

- TS
- Builder API (JSON Config)

`const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {`

theme: new SciChartJsNavyTheme()

});

// If you want to show an XAxis with dates between 1st March 2023 and 10th March 2023

const minDate = new Date("2023-03-01");

const maxDate = new Date("2023-03-10");

// Create the axis. SmartDateLabelProvider is automatically applied to labelProvider property

const xAxis = new DateTimeNumericAxis(wasmContext, {

axisTitle: "X Axis / DateTime",

// We need to specify some visibleRange to see these two dates

// SciChart.js expects linux timestamp / 1000

visibleRange: new NumberRange(minDate.getTime() / 1000, maxDate.getTime() / 1000)

});

// Add the xAxis to the chart

sciChartSurface.xAxes.add(xAxis);

// Creating a NumericAxis as a YAxis on the left

sciChartSurface.yAxes.add(

new NumericAxis(wasmContext, {

axisTitle: "Y Axis, Numeric",

axisAlignment: EAxisAlignment.Left

})

);

// Add a series to the chart with X-data as dates using unix Timestamp / 1000

//

const xValues = [];

const yValues = [];

let startDate = minDate.getTime() / 1000;

for (let i = 0; i <= 10; i++) {

xValues.push(startDate);

yValues.push(Math.random() * 0.1 + (i > 0 ? yValues[i - 1] : 0));

startDate += 86400; // number of seconds in a day

}

sciChartSurface.renderableSeries.add(

new FastLineRenderableSeries(wasmContext, {

dataSeries: new XyDataSeries(wasmContext, { xValues, yValues }),

strokeThickness: 3,

stroke: "#50C7E0"

})

);

// Note console log out xValues to see they are unix timestamps / 1000

console.log("xValues: " + xValues);

`// If you want to show an XAxis with dates between 1st March 2023 and 10th March 2023`

const minDate = new Date("2023-03-01");

const maxDate = new Date("2023-03-10");

// Create data for the chart with X-data as dates using unix Timestamp / 1000

const xValues = [];

const yValues = [];

let startDate = minDate.getTime() / 1000;

for (let i = 0; i <= 10; i++) {

xValues.push(startDate);

yValues.push(Math.random() * 0.1 + (i > 0 ? yValues[i - 1] : 0));

startDate += 86400; // number of seconds in a day

}

const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: {

type: EAxisType.DateTimeNumericAxis,

options: {

axisTitle: "X Axis / DateTime",

// We need to specify some visibleRange to see these two dates

// SciChart.js expects linux timestamp / 1000

visibleRange: new NumberRange(minDate.getTime() / 1000, maxDate.getTime() / 1000)

}

},

yAxes: {

type: EAxisType.NumericAxis,

options: {

axisTitle: "Y Axis, Left, default formatting",

axisAlignment: EAxisAlignment.Left

}

},

series: [

{

type: ESeriesType.LineSeries,

options: {

strokeThickness: 3,

stroke: "#50C7E0"

},

xyData: { xValues, yValues }

}

]

});

This results in the following output:

Two fundamental differences of DateTimeNumericAxis and NumericAxis are that a SmartDateLabelProvider📘 is applied to the labelProvider property and DateTimeDeltaCalculator📘 is applied to the deltaCalculator property. This allows for more intuitive date formatting & handling when zooming the chart. Try it!

## Date / Label Formatting Options

### Configuring Default behaviour with the SmartDateLabelProvider

You'll notice above the Date formatting is quite intuitive out of the box, and dynamically changes on zoom. The more zoomed in you are, the finer grained the date labels e.g. Month/Day becomes Day/Hour, and Day/Hour becomes Hour/Minute. This behaviour is provided by the SmartDateLabelProvider📘 which is assigned to the Axis.LabelProvider📘 property by default.

This behaviour is pretty fixed, however some options of the SmartDateLabelProvider📘 are below:

The properties on SmartDateLabelProvider can be found in the TypeDoc API documentation📘.

### Further customising the DateTimeNumericAxis Label Output

There isn't much option at the moment for customising the DateTimeNumericAxis📘 label formatting when using the default SmartDateLabelProvider📘, however, it is possible to substitute the simpler DateLabelProvider📘 which doesn't have dynamic updating labels on zoom, and to specify your own formats.

It is also possible to create a custom labelprovider class and have complete control over axis label output. More on that in the Custom Label Providers documentation page.

Here's a quick example:

- TS
- Builder API (JSON Config)

`// If you want to show an XAxis with custom label formats`

const minDate = new Date("2023-03-01");

const maxDate = new Date("2023-03-03");

// Create the axis. SmartDateLabelProvider is automatically applied to labelProvider property

const xAxis = new DateTimeNumericAxis(wasmContext, {

axisTitle: "X Axis / DateTime",

visibleRange: new NumberRange(minDate.getTime() / 1000, maxDate.getTime() / 1000),

// Specify a DateLabelProvider with format to override the built-in behaviour

labelProvider: new DateLabelProvider({ labelFormat: ENumericFormat.Date_DDMMYYYY })

});

// When zoomed in to less than one day, switch the date format

xAxis.visibleRangeChanged.subscribe(arg => {

const SECONDS_IN_DAY = 86400;

const SECONDS_IN_HOUR = 3600;

if (arg.visibleRange.max - arg.visibleRange.min < SECONDS_IN_HOUR) {

xAxis.labelProvider.numericFormat = ENumericFormat.Date_HHMMSS;

} else if (arg.visibleRange.max - arg.visibleRange.min < SECONDS_IN_DAY) {

xAxis.labelProvider.numericFormat = ENumericFormat.Date_HHMM;

} else {

xAxis.labelProvider.numericFormat = ENumericFormat.Date_DDMMYYYY;

}

});

// Note other options include overriding labelProvider.formatLabel,

// or custom labelproviders

// Add the xAxis to the chart

sciChartSurface.xAxes.add(xAxis);

`// If you want to show an XAxis with dates and dynamic label formats`

const minDate = new Date("2023-03-01");

const maxDate = new Date("2023-03-03");

const { sciChartSurface, wasmContext } = await chartBuilder.build2DChart(divElementId, {

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: {

type: EAxisType.DateTimeNumericAxis,

options: {

axisTitle: "X Axis / DateTime",

// We need to specify some visibleRange to see these two dates

// SciChart.js expects linux timestamp / 1000

visibleRange: new NumberRange(minDate.getTime() / 1000, maxDate.getTime() / 1000),

labelProvider: {

type: ELabelProviderType.Date,

options: {

labelFormat: ENumericFormat.Date_DDMMYYYY

}

}

}

},

yAxes: {

type: EAxisType.NumericAxis,

options: {

axisTitle: "Y Axis, Left, default formatting",

axisAlignment: EAxisAlignment.Left

}

},

modifiers: [{ type: EChart2DModifierType.MouseWheelZoom }]

});

const xAxis = sciChartSurface.xAxes.get(0);

// When zoomed in to less than one day, switch the date format

xAxis.visibleRangeChanged.subscribe(arg => {

const SECONDS_IN_DAY = 86400;

const SECONDS_IN_HOUR = 3600;

if (arg.visibleRange.max - arg.visibleRange.min < SECONDS_IN_HOUR) {

xAxis.labelProvider.numericFormat = ENumericFormat.Date_HHMMSS;

} else if (arg.visibleRange.max - arg.visibleRange.min < SECONDS_IN_DAY) {

xAxis.labelProvider.numericFormat = ENumericFormat.Date_HHMM;

} else {

xAxis.labelProvider.numericFormat = ENumericFormat.Date_DDMMYYYY;

}

});

This code example above shows how you can swap the default SmartDateLabelProvider📘 on the DateTimeNumericAxis📘 for a simpler DateLabelProvider📘, then subscribe to axis.visibleRangeChanged to dynamically change the labelformat.

This results in the following output:

Other options are available, such as implementing a custom LabelProvider. Overriding LabelProvider.formatLabel📘 and formatCursorLabel allows for complete control over axis labels.