---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-labels/custom-label-providers-dynamic-dates-on-zoom
scraped_at: 2025-11-28T18:24:04.456403
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-labels/custom-label-providers-dynamic-dates-on-zoom

# Custom LabelProviders: Dynamic Dates on Zoom

Customisation in SciChart.js can go a level deeper than built-in label formatting by creating a custom labelprovider class.

In this page we're going to show a worked example of how we can create a custom label provider to handle dynamic date formatting on zoom.

To create a custom labelprovider to handle dynamic dates, first a class which inherits one of the LabelProvider classes listed here and override formatLabel📘 or formatCursorLabel📘.

Inside the **formatLabel** function, **parentAxis.visibleRange** can be accessed to determine the visibleRange or zoom level of the axis.

Here we can provide some dynamic formatting of labels depending on the zoom level.

- TS

`const { DateLabelProvider } = SciChart;`

// A custom class which inherits DateLabelProvider for dynamic date/time formatting

// You can also inherit NumericLabelProvider for number formatting

class DynamicDateLabelProvider extends DateLabelProvider {

// Different thesholds of axis.visibleRange.max - min to trigger format changes

SECONDS_IN_DAY = 86400;

SECONDS_IN_HOUR = 60 * 60 * 6;

SECONDS_IN_MINUTE = 60 * 30;

constructor() {

super();

// Disable caching due to dynamic nature of the labels

this.useCache = false;

}

// Called for each label

// @ts-ignore TODO base class defines instance member as accessor

formatLabel(dataValue) {

const axisRange = this.parentAxis.visibleRange;

// assuming label dataValue is a unix timestamp / 1000 (attached to Date axis)

const unixTimeStamp = dataValue;

const date = new Date(unixTimeStamp * 1000);

const hours = date.getUTCHours();

const minutes = date.getUTCMinutes();

const seconds = date.getUTCSeconds();

const milliseconds = date.getUTCMilliseconds();

const hoursString = hours <= 9 ? `0${hours}` : hours.toString(10);

const minutesString = minutes <= 9 ? `0${minutes}` : minutes.toString(10);

const secondsString = seconds <= 9 ? `0${seconds}` : seconds.toString(10);

if (axisRange.max - axisRange.min < this.SECONDS_IN_MINUTE) {

// Format as 00m00s 000ms

const millisecondsString = `00` + milliseconds.toString(10);

return `${minutesString}m${secondsString}s ${millisecondsString}ms`;

} else if (axisRange.max - axisRange.min < this.SECONDS_IN_HOUR) {

// Format as HH:MM:SS

return `${hoursString}:${minutesString}:${secondsString}`;

} else if (axisRange.max - axisRange.min < this.SECONDS_IN_DAY) {

// Format as HH:MM

return `${hoursString}:${minutesString}`;

} else {

// Format as DD:MM:YY

return date.toLocaleDateString("en-GB", {

year: "2-digit",

month: "2-digit",

day: "2-digit"

});

}

}

// Called for each tooltip/cursor label

// @ts-ignore TODO base class defines instance member as accessor

formatCursorLabel(dataValue) {

return this.formatLabel(dataValue);

}

}

Next, apply the custom LabelProvider to an axis as follows:

- TS
- Builder API (JSON Config)

const minDate = new Date("2023-03-01");

const maxDate = new Date("2023-03-03");

const xAxis = new DateTimeNumericAxis(wasmContext, {

axisTitle: "X Axis with custom LabelProvider",

// Note see DateTimeNumericAxis docs about unix timestamps / 1000

visibleRange: new NumberRange(minDate.getTime() / 1000, maxDate.getTime() / 1000),

// Apply the custom labelprovider we created before

labelProvider: new DynamicDateLabelProvider()

});

sciChartSurface.xAxes.add(xAxis);

`const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {`

surface: { theme: { type: EThemeProviderType.Dark } },

xAxes: {

type: EAxisType.NumericAxis,

options: {

axisTitle: "X Axis with custom LabelProvider",

// Note see DateTimeNumericAxis docs about unix timestamps / 1000

visibleRange: new NumberRange(minDate.getTime() / 1000, maxDate.getTime() / 1000),

// Apply the custom labelprovider we created before

labelProvider: new DynamicDateLabelProvider()

}

},

yAxes: {

type: EAxisType.NumericAxis

},

modifiers: [{ type: EChart2DModifierType.MouseWheelZoom }]

});

This results in the following output:

- At default zoom level the format DD/MM/YYYY is chosen
- Zooming in and format changes to HH:mm
- Zooming further still and format changes to HH:mm:ss
- Once the axis range is less than a few minutes, label format changes to show minutes, seconds and milliseconds

Zoom IN on the above example using the mousewheel to see dynamic label formatting