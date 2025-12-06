---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/TouchMouseEventData
scraped_at: 2025-12-01T14:31:42.096056
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/TouchMouseEventData

# Interface: TouchMouseEventData

The TouchMouseEventData interface represents events that occur due to the user interacting with a pointing device (such as a mouse). See MouseEvent

## Properties

### clientX

`readonly`

clientX:`Coordinate`

The X coordinate of the mouse pointer in local (DOM content) coordinates.

### clientY

`readonly`

clientY:`Coordinate`

The Y coordinate of the mouse pointer in local (DOM content) coordinates.

### pageX

`readonly`

pageX:`Coordinate`

The X coordinate of the mouse pointer relative to the whole document.

### pageY

`readonly`

pageY:`Coordinate`

The Y coordinate of the mouse pointer relative to the whole document.

### screenX

`readonly`

screenX:`Coordinate`

The X coordinate of the mouse pointer in global (screen) coordinates.

### screenY

`readonly`

screenY:`Coordinate`

The Y coordinate of the mouse pointer in global (screen) coordinates.

### localX

`readonly`

localX:`Coordinate`

The X coordinate of the mouse pointer relative to the chart / price axis / time axis canvas element.

### localY

`readonly`

localY:`Coordinate`

The Y coordinate of the mouse pointer relative to the chart / price axis / time axis canvas element.

### ctrlKey

`readonly`

ctrlKey:`boolean`

Returns a boolean value that is true if the Ctrl key was active when the key event was generated.

### altKey

`readonly`

altKey:`boolean`

Returns a boolean value that is true if the Alt (Option or ⌥ on macOS) key was active when the key event was generated.

### shiftKey

`readonly`

shiftKey:`boolean`

Returns a boolean value that is true if the Shift key was active when the key event was generated.

### metaKey

`readonly`

metaKey:`boolean`

Returns a boolean value that is true if the Meta key (on Mac keyboards, the ⌘ Command key; on Windows keyboards, the Windows key (⊞)) was active when the key event was generated.