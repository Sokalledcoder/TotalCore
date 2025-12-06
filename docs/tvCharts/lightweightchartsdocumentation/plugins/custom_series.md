---
source: https://tradingview.github.io/lightweight-charts/docs/plugins/custom_series
scraped_at: 2025-12-01T14:31:45.586789
---

# https://tradingview.github.io/lightweight-charts/docs/plugins/custom_series

# Custom Series Types

Custom series allow developers to create new types of series with their own data structures, and rendering logic (implemented using CanvasRenderingContext2D methods). These custom series extend the current capabilities of our built-in series, providing a consistent API which mirrors the built-in chart types.

These series are expected to have a uniform width for each data point, which
ensures that the chart maintains a consistent look and feel across all series
types. The only restriction on the data structure is that it should extend the
`CustomData`

interface (have a valid time
property for each data point).

## Defining a Custom Series

A custom series should implement the
`ICustomSeriesPaneView`

interface.
The interface defines the basic functionality and structure required for
creating a custom series view.

It includes the following methods and properties:

### Renderer

- ICustomSeriesPaneView property:
`renderer`

This method should return a renderer which implements the
`ICustomSeriesPaneRenderer`

interface and is used to draw the series data on the main chart pane.

The `draw`

method of the
renderer is evoked whenever the chart needs to draw the series.

The `PriceToCoordinateConverter`

provided as the 2nd argument to the draw method is a convenience function for
changing prices into vertical coordinate values. It is provided since the
series' original data will most likely be defined in price values, and the
renderer needs to draw with coordinates. The values returned by the converter
will be defined in mediaSize (unscaled by `devicePixelRatio`

).

`CanvasRenderingTarget2D`

provided within the `draw`

function is explained in
more detail on the Canvas Rendering Target page.

### Update

- ICustomSeriesPaneView property:
`update`

This method will be called with the latest data for the renderer to use during the next paint.

The update method is evoked with two parameters: `data`

(discussed below), and
`seriesOptions`

. seriesOptions is a reference to the currently applied options
for the series

The `PaneRendererCustomData`

interface provides the data that can be used within the renderer for drawing the
series data. It includes the following properties:

`bars`

: List of all the series' items and their x coordinates. See`CustomBarItemData`

for more details`barSpacing`

: Spacing between consecutive bars.`visibleRange`

: The current visible range of items on the chart.

### Price Value Builder

- ICustomSeriesPaneView property:
`priceValueBuilder`

A function for interpreting the custom series data and returning an array of numbers representing the prices values for the item, specifically the equivalent highest, lowest, and current price values for the data item.

These price values are used by the chart to determine the auto-scaling (to ensure the items are in view) and the crosshair and price line positions. The largest and smallest values in the array will be used to specify the visible range of the painted item, and the last value will be used for the crosshair and price line position.

### Whitespace

- ICustomSeriesPaneView property:
`isWhitespace`

A function used by the library to determine which data points provided by the
user should be considered Whitespace. The method should return `true`

when the
data point is Whitespace. Data points which are whitespace data won't be provided to
the renderer, or the `priceValueBuilder`

.

### Default Options

- ICustomSeriesPaneView property:
`defaultOptions`

The default options to be used for the series. The user can override these
values using the options argument in
`addCustomSeries`

, or via the
`applyOptions`

method on the
`ISeriesAPI`

.

### Destroy

- ICustomSeriesPaneView property:
`destroy`

This method will be evoked when the series has been removed from the chart. This method should be used to clean up any objects, references, and other items that could potentially cause memory leaks.

This method should contain all the necessary code to clean up the object before it is removed from memory. This includes removing any event listeners or timers that are attached to the object, removing any references to other objects, and resetting any values or properties that were modified during the lifetime of the object.