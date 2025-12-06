---
source: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ISeriesPrimitiveAxisView
scraped_at: 2025-12-01T14:31:40.335614
---

# https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ISeriesPrimitiveAxisView

# Interface: ISeriesPrimitiveAxisView

This interface represents a label on the price or time axis

## Methods

### coordinate()

coordinate():`number`

The desired coordinate for the label. Note that the label will be automatically moved to prevent overlapping with other labels. If you would like the label to be drawn at the
exact coordinate under all circumstances then rather use `fixedCoordinate`

.
For a price axis the value returned will represent the vertical distance (pixels) from the top. For a time axis the value will represent the horizontal distance from the left.

#### Returns

`number`

coordinate. distance from top for price axis, or distance from left for time axis.

### fixedCoordinate()?

`optional`

fixedCoordinate():`number`

fixed coordinate of the label. A label with a fixed coordinate value will always be drawn at the specified coordinate and will appear above any 'unfixed' labels. If you supply
a fixed coordinate then you should return a large negative number for `coordinate`

so that the automatic placement of unfixed labels doesn't leave a blank space for this label.
For a price axis the value returned will represent the vertical distance (pixels) from the top. For a time axis the value will represent the horizontal distance from the left.

#### Returns

`number`

coordinate. distance from top for price axis, or distance from left for time axis.

### text()

text():`string`

#### Returns

`string`

text of the label

### textColor()

textColor():`string`

#### Returns

`string`

text color of the label

### backColor()

backColor():`string`

#### Returns

`string`

background color of the label

### visible()?

`optional`

visible():`boolean`

#### Returns

`boolean`

whether the label should be visible (default: `true`

)

### tickVisible()?

`optional`

tickVisible():`boolean`

#### Returns

`boolean`

whether the tick mark line should be visible (default: `true`

)