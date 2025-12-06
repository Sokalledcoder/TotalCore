---
source: https://tradingview.github.io/lightweight-charts/docs/plugins/pane-primitives
scraped_at: 2025-12-01T14:31:45.670619
---

# https://tradingview.github.io/lightweight-charts/docs/plugins/pane-primitives

# Pane Primitives

In addition to Series Primitives, the library now supports Pane Primitives. These are essentially the same as Series Primitives but are designed to draw on the pane of a chart rather than being associated with a specific series. Pane Primitives can be used for features like watermarks or other chart-wide annotations.

## Key Differences from Series Primitives

- Pane Primitives are attached to the chart pane rather than a specific series.
- They cannot draw on the price and time scales.
- They are ideal for chart-wide features that are not tied to a particular series.

## Adding a Pane Primitive

Pane Primitives can be added to a chart using the `attachPrimitive`

method on the `IPaneApi`

interface. Here's an example:

`const chart = createChart(document.getElementById('container'));`

const pane = chart.panes()[0]; // Get the first (main) pane

const myPanePrimitive = new MyCustomPanePrimitive();

pane.attachPrimitive(myPanePrimitive);

## Implementing a Pane Primitive

To create a Pane Primitive, you should implement the `IPanePrimitive`

interface. This interface is similar to `ISeriesPrimitive`

, but with some key differences:

- It doesn't include methods for drawing on price and time scales.
- The
`paneViews`

method is used to define what will be drawn on the chart pane.

Here's a basic example of a Pane Primitive implementation:

`class MyCustomPanePrimitive {`

paneViews() {

return [

{

renderer: {

draw: target => {

// Custom drawing logic here

},

},

},

];

}

// Other methods as needed...

}

For more details on implementing Pane Primitives, refer to the `IPanePrimitive`

interface documentation.