---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-labels/custom-label-providers-readable-numbers
scraped_at: 2025-11-28T18:24:04.631251
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-labels/custom-label-providers-readable-numbers

# Custom LabelProviders: Readable Numbers

Customisation in SciChart.js can go a level deeper than built-in label formatting by creating a custom labelprovider class.

In this page we're going to show a worked example of how we can create a custom label provider to handle formatting of numbers with thousands/millions commas, or to format large numbers such as 1,000 as 1K, 1,000,000 as 1M and 1,000,000,000 as 1Bn

To create a custom labelprovider to handle dynamic dates, first a class which inherits one of the LabelProvider classes listed here and override formatLabel📘 or formatCursorLabel📘.

Inside the **formatLabel** function, determine which formatting to apply based on properties and format the label value.

In this example below, we show two ways to format large numeric values in SciChart.js.

### Method 1: K,M,B,T formatting

Large numbers are formatted as follows:

- 1,000 = 1K
- 1,000,000 = 1M
- 1,000,000,000 = 1B
- 1,000,000,000,000 = 1T

Label prefix and postfix, decimal places are supported by passing ILabel2DOptions📘 to the constructor of **CustomNumericLabelProvider**, which in turn passes to the base class constructor NumericLabelProvider📘.

### Method 2: Comma formatting

Large numbers are formatted as follows:

- 1000 => 1,000
- 1000000 => 1,000,000
- 1000000000 => 1,000,000,000

etc...

- TS

`const { NumericLabelProvider } = SciChart;`

// A custom class which inherits NumericLabelProvider for advanced numeric formatting

// You can also inherit DateLabelProvider for date formatting

class CustomNumericLabelProvider extends NumericLabelProvider {

customFormat = "Commas"; // Options are "Default", "Commas" and "KMBT"

// Options accepts values from ILabel2DOptions or 'customFormat' e.g.

// { customFormat: "Commas", labelPrefix: "$", labelPrecision: 2 } or { customFormat: "KMBT" }

constructor(options) {

super(options);

this.customFormat = options?.customFormat ?? "Commas";

}

// Called for each label

// @ts-ignore TODO base class defines instance member as accessor

formatLabel(dataValue) {

if (this.customFormat === "Default") {

return super.formatLabel(dataValue);

} else if (this.customFormat === "Commas") {

// Format numbers using the default format, but with commas e.g. 1,000,000

return this.formatNumberWithCommas(dataValue);

} else if (this.customFormat === "KMBT") {

// Format large numbers with K, M, B abbreviations e.g. 1.5M

return this.formatNumberKMBT(dataValue);

}

return "";

}

// Called for each tooltip/cursor label

// @ts-ignore TODO base class defines instance member as accessor

formatCursorLabel(dataValue) {

return this.formatLabel(dataValue);

}

// Formats a label with commas e.g. 1000000 becomes 1,000,000

formatNumberWithCommas(dataValue) {

const labelValue = super.formatLabel(dataValue);

const commasRegex = /\B(?=(\d{3})+(?!\d))/g;

const output = labelValue.replace(commasRegex, ",");

// Log what happened for educational purposes

console.log(`formatNumberWithCommas: ${dataValue} => ${labelValue} => ${output}`);

return output;

}

// Returns a number formatted as K, M, B, T for thousands, millions, billions, trillions

formatNumberKMBT(dataValue) {

// formatLabel applies decimal, significant figure formatting and adds prefix, postfix

let originalLabel = super.formatLabel(dataValue);

let result = originalLabel;

// Now we need to inject K, M, B, T into the label before the postfix

// e.g. formatLabel(1000000) with prefix="$", postfix="USD" = "$1000000 USD" => "$1M USD"

if (dataValue >= 1_000_000_000_000) {

result = super.formatLabel(dataValue / 1_000_000_000_000).replace(this.postfix, "T" + this.postfix);

} else if (dataValue >= 1_000_000_000) {

result = super.formatLabel(dataValue / 1_000_000_000).replace(this.postfix, "B" + this.postfix);

} else if (dataValue >= 1_000_000) {

result = super.formatLabel(dataValue / 1_000_000).replace(this.postfix, "M" + this.postfix);

} else if (dataValue >= 1_000) {

result = super.formatLabel(dataValue / 1_000).replace(this.postfix, "K" + this.postfix);

}

// Log what happened for educational purposes

console.log(`formatNumberKMBT: ${dataValue} => ${originalLabel} => ${result}`);

return result;

}

}

### Applying the Custom LabelProvider to an Axis

Next, apply the custom LabelProvider to an axis as follows:

- TS
- Builder API (JSON Config)

// Apply the custom labelprovider we created before to different axis

sciChartSurface.yAxes.add(

new LogarithmicAxis(wasmContext, {

axisTitle: "Y Axis with K,M,B,T abbreviations",

// Enable K,M,B,T abbreviations for large labels

labelProvider: new CustomNumericLabelProvider({

customFormat: "KMBT",

labelPrefix: "$",

labelPostfix: " USD",

labelPrecision: 2,

labelFormat: ENumericFormat.SignificantFigures

}),

visibleRange: new NumberRange(1, 1e12)

})

);

sciChartSurface.xAxes.add(

new NumericAxis(wasmContext, {

axisTitle: "X Axis with comma separators",

// Enable comma formatting for large labels

labelProvider: new CustomNumericLabelProvider({ customFormat: "Commas", labelPrecision: 1 }),

visibleRange: new NumberRange(0, 1e10)

})

);

`const { wasmContext, sciChartSurface } = await chartBuilder.build2DChart(divElementId, {`

surface: { theme: { type: EThemeProviderType.Dark } },

yAxes: {

type: EAxisType.LogarithmicAxis,

options: {

axisTitle: "Y Axis with K,M,B,T abbreviations",

// Enable K,M,B,T abbreviations for large labels

labelProvider: new CustomNumericLabelProvider({

customFormat: "KMBT",

labelPrefix: "$",

labelPostfix: " USD",

labelPrecision: 2,

labelFormat: ENumericFormat.SignificantFigures

}),

visibleRange: new NumberRange(1, 1e12)

}

},

xAxes: {

type: EAxisType.NumericAxis,

options: {

axisTitle: "X Axis with comma separators",

// Enable comma formatting for large labels

labelProvider: new CustomNumericLabelProvider({ customFormat: "Commas", labelPrecision: 1 }),

visibleRange: new NumberRange(0, 1e10)

}

},

modifiers: [{ type: EChart2DModifierType.MouseWheelZoom }, { type: EChart2DModifierType.ZoomPan }]

});

This results in the following output:

- When the property formatOptions = "Default", default numeric formatting is chosen
- When the property formatOptions = "Commas", numbers are formatted with comma separators, e.g. 1,000,000
- When the property formatOptions = "KMBT", large numbers are formatted as 1k, 1M, 1B

The above example showcases how to apply custom or complex formatting to labels in SciChart.js.

Any formatting (dynamic or static) that you can think of can be applied using the LabelProvider API.

Custom labelproviders can then be set on individual X,Y axis of any type.