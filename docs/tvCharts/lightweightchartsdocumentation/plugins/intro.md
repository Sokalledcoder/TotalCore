---
source: https://tradingview.github.io/lightweight-charts/docs/plugins/intro
scraped_at: 2025-12-01T14:31:45.571358
---

# https://tradingview.github.io/lightweight-charts/docs/plugins/intro

# Plugins

Plugins allow you to extend the library's functionality and render custom elements, such as new series, drawing tools, indicators, and watermarks.

You can create plugins of the following types:

- Custom series — define new types of series.
- Primitives — define custom visualizations, drawing tools, and chart annotations that can be attached to an existing series (series primitives) or chart pane (pane primitives).

- Use the create-lwc-plugin npm package to quickly scaffold a project for your custom plugin.
- Explore the Plugin Examples Demo page that hosts interactive examples of heatmaps, alerts, watermarks, and tooltips implemented with plugins. You can find the code of these examples in the
`plugin-examples`

folder in the Lightweight Charts™ repository.

## Custom series

Custom series allow you to define new types of series with custom data structures and rendering logic. For implementation details, refer to the Custom Series Types article.

Use the `addCustomSeries`

method to add a custom series to the chart.
Then, you can manage it through the same API available for built-in series.
For example, call the `setData`

method to populate the series with data.

`class MyCustomSeries {`

/* Class implementing the ICustomSeriesPaneView interface */

}

// Create an instantiated custom series

const customSeriesInstance = new MyCustomSeries();

const chart = createChart(document.getElementById('container'));

const myCustomSeries = chart.addCustomSeries(customSeriesInstance, {

// Options for MyCustomSeries

customOption: 10,

});

const data = [

{ time: 1642425322, value: 123, customValue: 456 },

/* ... more data */

];

myCustomSeries.setData(data);

## Primitives

Primitives allow you to define custom visualizations, drawing tools, and chart annotations. You can render them at different levels in the visual stack to create complex, layered compositions.

### Series primitives

Series primitives are attached to a specific series and can render on the main pane, price and time scales. For implementation details, refer to the Series Primitives article.

Use the `attachPrimitive`

method to add a primitive to the chart and attach it to the series.

`class MyCustomPrimitive {`

/* Class implementing the ISeriesPrimitive interface */

}

// Create an instantiated series primitive

const myCustomPrimitive = new MyCustomPrimitive();

const chart = createChart(document.getElementById('container'));

const lineSeries = chart.addSeries(LineSeries);

const data = [

{ time: 1642425322, value: 123 },

/* ... more data */

];

// Attach the primitive to the series

lineSeries.attachPrimitive(myCustomPrimitive);

### Pane primitives

Pane primitives are attached to a chart pane rather than a specific series. You can use them to create chart-wide annotations and features like watermarks. For implementation details, refer to the Pane Primitives article.

Note that pane primitives cannot render on the price or time scale.

Use the `attachPrimitive`

method to add a primitive to the chart and attach it to the pane.

`class MyCustomPanePrimitive {`

/* Class implementing the IPanePrimitive interface */

}

// Create an instantiated pane primitive

const myCustomPanePrimitive = new MyCustomPanePrimitive();

const chart = createChart(document.getElementById('container'));

// Get the main pane

const mainPane = chart.panes()[0];

// Attach the primitive to the pane

mainPane.attachPrimitive(myCustomPanePrimitive);