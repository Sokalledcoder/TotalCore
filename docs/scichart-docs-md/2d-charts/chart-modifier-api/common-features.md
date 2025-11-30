---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/common-features
scraped_at: 2025-11-28T18:24:14.107634
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-modifier-api/common-features

# Common ChartModifiers Features

All the ChartModifiers provided by SciChart.js implement the IChartModifierBase interface📘 and derive from the ChartModifierBase📘 class. These provide a powerful API which gives the full access to internals of a chart, axes, series, annotations, mouse, touch events and more.

Please refer to the What is a ChartModifier article for the complete list of all the Chart Modifiers available out of the box in SciChart.

## Common Features of Chart Modifiers

### ChartModifierBase type

The ChartModifierBase type📘 has the following public API.

Refer to our TypeDoc Documentation📘 for up to date and commented / annotated functions and properties available on this type.

Feature | Description |
|---|---|
| .parentSurface📘 | A property to get the parent SciChartSurface📘 when the modifier is attached. |
| .isEnabled📘 | A property which determines if the current modifier is enabled or not. |
| .isAttached📘 | When true, the modifier is attached to a parent SciChartSurface📘. |
| .receiveHandledEvents📘 | When true, the modifier will receive all events even if that event is marked as handled by a previous modifier. When false (default), the modifier will not receive events if they are handled. |
| .executeCondition📘 | The primary action execute condition that modifier should respond to (see below). |
| .secondaryExecuteCondition📘 | The secondary action execute condition that modifier should respond to (see below). |
| .modifierGroup📘 | Specifies a string ID to group modifiers. When one receives a mouse event, all modifiers in the same group receive the event. |
| onAttach()📘 | Called when the modifier is attached to a SciChartSurface📘. |
| onParentSurfaceRendered()📘 | Called when the parent SciChartSurface📘 is rendered. |
| modifierMouseDown()📘 | Called when a mouse or touch-down event occurs on the parent SciChartSurface📘. |
| modifierMouseMove()📘 | Called when a mouse or touch-move event occurs on the parent SciChartSurface📘. |
| modifierMouseUp()📘 | Called when a mouse or touch-up event occurs on the parent SciChartSurface📘. |
| modifierMouseWheel()📘 | Called when a mouse wheel event occurs on the parent SciChartSurface📘. |
| modifierDoubleClick()📘 | Called when a mouse or touch double-click event occurs on the parent SciChartSurface📘. |
| modifierMouseEnter()📘 | Called when a mouse-enter event occurs on the parent SciChartSurface📘. |
| modifierMouseLeave()📘 | Called when a mouse-leave event occurs on the parent SciChartSurface📘. |

### Execute Conditions

Chart modifiers can be configured to respond to specific mouse and keyboard combinations using `executeCondition`

and `secondaryExecuteCondition`

properties. These conditions determine when the modifier should activate.

Each condition can specify:

- A mouse button (
`button`

) from`EExecuteOn`

enum (e.g., MouseLeftButton, MouseMiddleButton, MouseRightButton) - A keyboard modifier key (
`key`

) from`EModifierMouseArgKey`

enum (Shift, Ctrl, Alt, or None)

**Available Mouse Buttons:**

`enum EExecuteOn {`

MouseLeftButton = 0, // Primary mouse button

MouseMiddleButton = 1, // Middle mouse button/wheel

MouseRightButton = 2, // Secondary mouse button

BrowserBackButton = 3, // Browser back button

BrowserForwardButton = 4 // Browser forward button

}

**Available Modifier Keys:**

`enum EModifierMouseArgKey {`

None = 0, // No modifier key

Shift = 1, // Shift key

Ctrl = 2, // Control key

Alt = 4 // Alt/Option key

}

**Common Usage Patterns:**

**Basic mouse button activation:**

`// Activate on right mouse button only`

new RubberBandXyZoomModifier({

executeCondition: { button: EExecuteOn.MouseRightButton }

})

**Keyboard modifier combinations:**

`// Require Ctrl+Left mouse button`

new ZoomPanModifier({

executeCondition: {

button: EExecuteOn.MouseLeftButton,

key: EModifierMouseArgKey.Ctrl

}

})

**Different primary and secondary actions:**

`// Primary: Left mouse drag`

// Secondary: Right mouse drag with Shift key

new CursorModifier({

executeCondition: { button: EExecuteOn.MouseLeftButton },

secondaryExecuteCondition: {

button: EExecuteOn.MouseRightButton,

key: EModifierMouseArgKey.Shift

}

})

**Browser navigation buttons:**

`// Use browser back/forward buttons for navigation`

new CustomModifier({

executeCondition: { button: EExecuteOn.BrowserBackButton },

secondaryExecuteCondition: { button: EExecuteOn.BrowserForwardButton }

})

**Multiple modifier combinations:**

`// Complex combination example`

new TooltipModifier({

executeCondition: {

button: EExecuteOn.MouseMiddleButton,

key: EModifierMouseArgKey.Alt | EModifierMouseArgKey.Ctrl

}

})

**Important Notes:**

- The
`executeCondition`

is the primary activation trigger - The
`secondaryExecuteCondition`

provides an alternative activation method - Modifier keys can be combined using bitwise OR (e.g.,
`Ctrl|Shift`

) - When no condition is specified, most modifiers default to left mouse button with no modifiers
- The
`EExecuteOn`

enum values correspond to standard mouse button indices (0=left, 1=middle, 2=right)

**Advanced Example: Custom Interaction Scheme**

`sciChartSurface.chartModifiers.add(`

// Zoom with Ctrl+Left drag

new RubberBandXyZoomModifier({

executeCondition: {

button: EExecuteOn.MouseLeftButton,

key: EModifierMouseArgKey.Ctrl

}

}),

// Pan with Middle mouse drag

new ZoomPanModifier({

executeCondition: { button: EExecuteOn.MouseMiddleButton }

}),

// Show tooltips on Alt+Right click

new CursorModifier({

executeCondition: {

button: EExecuteOn.MouseRightButton,

key: EModifierMouseArgKey.Alt

}

})

);

This configuration creates a sophisticated interaction model where:

- Ctrl+Left drag performs rectangular zoom
- Middle mouse drag pans the chart
- Alt+Right click shows cursor tooltips
- All other interactions remain available for other modifiers

### Series Interaction

Chart modifiers can interact with specific series through these methods:

Method | Description |
|---|---|
| onAttachSeries()📘 | Called when a renderable series is attached to the chart |
| onDetachSeries()📘 | Called when a renderable series is detached from the chart |
| includeSeries()📘 | Controls whether a series should be included in the modifier's behavior |

### Including/Excluding Series

The `includeSeries()`

method is particularly important for modifiers that display legends or tooltips (like `CursorModifier`

, `LegendModifier`

, `RolloverModifier`

, etc.). It allows you to control which series should be included in the modifier's behavior.

Example usage:

`// Include a specific series in the modifier`

modifier.includeSeries(mySeries, true);

// Exclude a series from the modifier

modifier.includeSeries(mySeries, false);

When a series is included/excluded, the modifier will update its internal state (e.g., update tooltip content or legend items) if it's currently attached to a chart.

### ChartModifierBase2D Type

The ChartModifierBase2D📘 type provides a base class for all modifiers on 2D SciChartSurfaces and 2D SciChartPolarSurfaces. Use this type when creating custom modifiers for 2D Charts.

### ChartModifierBase3D Type

The ChartModifierBase3D📘 type provides a base class for all modifiers on **SciChart3DSurfaces**. Use this type when creating custom modifiers for 3D Charts.