---
source: https://tradingview.github.io/lightweight-charts/docs/release-notes
scraped_at: 2025-12-01T14:31:46.054670
---

# https://tradingview.github.io/lightweight-charts/docs/release-notes

# Release Notes

## 5.0.9

**Enhancements**

- Added
`rightOffsetPixels`

option to`HorzScaleOptions`

, allowing margin space from the right side of the chart to be set in pixels. This option takes precedence over`rightOffset`

and ensures consistent pixel offset when using`fitContent`

on charts with different amounts of data. The pixel-based offset remains consistent during zoom operations. (PR #1957) - Added
`pop`

method to series API that removes a specified number of data points from the end of the series and returns the removed data. (PR #1949, fixes #1518, contributed by @tpunt) - Enhanced
`takeScreenshot`

method with two new optional parameters:`addTopLayer`

- includes top layer primitives in the screenshot (default: false)`includeCrosshair`

- includes the crosshair when`addTopLayer`

is enabled (default: false) (PR #1977)

- Added
`autoScale`

option to`SeriesMarkersOptions`

, allowing control over whether markers are included in the auto-scaling calculation of the price scale. When enabled (default: true), the chart will adjust its scale to ensure markers are fully visible. (PR #1940, contributed by @zbinlin) - Added
`base`

option to price format configuration as an alternative to`minMove`

. This helps avoid floating-point precision limitations when dealing with extremely small price movements. (PR #1952) - Enhanced plugin API with additional functionality:

**Bug Fixes**

- Fixed price scale visible range calculation when in logarithmic scale mode by properly converting the range from log space and handling precision issues with rounding. (PR #1965, contributed by @tpunt)

**Plugin & Indicator Examples**

- Added
*Dual Range Histogram Series*custom plugin example that visualizes paired positive and negative value ranges for each time point using a column-based display. (PR #1934) - Added
*Pretty Histogram*plugin example demonstrating non-standard histogram rendering. (PR #1930) - Added examples demonstrating how to implement indicators (studies) within Lightweight Charts. See the Analysis Indicators tutorial for more information. (PR #1915)

**Contributors**

We'd like to thank our external contributors for their valuable contributions to this release:

Changes since the last published version.

## 5.0.8

**Enhancements**

- Improved pane API with several new methods and options:
- Added
`addDefaultPane`

option to chart options, allowing creation of charts with no initial panes - Added
`addPane`

method to`IChartApi`

for programmatically adding panes - Added
`setPreserveEmptyPane`

and`preserveEmptyPane`

methods to control empty pane behavior - Added
`getStretchFactor`

and`setStretchFactor`

methods to control relative pane sizes - Added
`addCustomSeries`

and`addSeries`

methods to`IPaneApi`

for creating series directly on a specific pane - Updated
`getHTMLElement`

to return`null`

when a pane hasn't been created yet - These improvements provide greater flexibility when working with multi-pane charts (PR #1894, fixes #1898, #1896, #1872, #1907)

- Added
- Added additional price scale tick mark formatting capabilities:
- Added
`formatTickmarks`

method to`IPriceFormatter`

interface - Added
`tickmarksPriceFormatter`

and`tickmarksPercentageFormatter`

options to`LocalizationOptionsBase`

- Added
`tickmarksFormatter`

option to`PriceFormatCustom`

- These new formatters provide all tick mark values at once, allowing for context-aware formatting decisions such as determining the optimal precision level needed (PR #1903)

- Added

Changes since the last published version.

## 5.0.7

**Enhancements**

- Added price scale visible range control with new methods in
`IPriceScaleApi`

:`setVisibleRange(range)`

,`getVisibleRange()`

, and`setAutoScale(on)`

. These methods allow for programmatic control of the visible price range on a price scale. Also added`ensureEdgeTickMarksVisible`

option to`PriceScaleOptions`

, which ensures tick marks are always visible at the very top and bottom of the price scale, providing clear boundary indicators. These features are particularly useful for charts with zooming and panning disabled that are primarily for display purposes. (PR #1856) - Added control over the rendering stacking order of series markers through a new
`zOrder`

option in the series markers plugin. This enhancement provides greater flexibility in controlling marker visibility and layering in complex charts. (PR #1876).

Changes since the last published version.

## 5.0.6

**Enhancements**

- Implemented series order functionality, allowing control over the rendering order of series within a pane. Series with higher order values are rendered on top of those with lower values. Added two new methods to
`ISeriesApi`

:`seriesOrder()`

to get the current order index and`setSeriesOrder(order)`

to set a specific order. (PR #1868)

Changes since the last published version.

## 5.0.5

**Bug Fixes**

- Fixed an issue where the series marker plugin could throw an exception if the series data required for individual markers could not be found (such as when the data is cleared or changed via setData on the series). (PR #1845)

Changes since the last published version.

## 5.0.4

**Improvements**

- Fixed performance degradation when adding series markers to charts with large datasets (15,000+ data points) by optimizing marker calculations to only run when necessary. (PR #1835, fixes #1808)
- Added price-based positioning for series markers, allowing more precise control over marker placement. New position types include
`atPriceTop`

,`atPriceBottom`

, and`atPriceMiddle`

, which require a`price`

value to be specified. (PR #1826, thanks to @EranGrin) - Added
`MagnetOHLC`

to`CrosshairMode`

. This mode sticks the crosshair's horizontal line to the price value of a single-value series or to the open/high/low/close price of OHLC-based series. (PR #1831, thanks to @Jonney)

**Bug Fixes**

- Fixed an issue where the crosshair marker would be visible on the first data point when the chart is initially loaded, before any user interaction. This behavior has been reverted to match version 4, where the crosshair remains hidden until user interaction. (PR #1840)

Changes since the last published version.

## 5.0.3

**Bug Fixes**

- Fixed an issue where changing the price scale for one pane would impact all panes in multi-pane setups. Added pane index parameter to the price scale API to ensure changes only affect the intended pane. (PR #1821, fixes #1817)
- Fixed an issue where a cursorStyle defined in a primitive hit-test wouldn't be applied. Additionally improved cursor style handling to maintain the correct cursor when the mouse remains in the same position while price/time scales are adjusted. (PR #1823)

Changes since the last published version.

## 5.0.2

**Bug Fixes**

- Fixed an issue where the crosshair marker would remain visible after the mouse pointer has left the chart. (PR #1807)

Changes since the last published version.

## 5.0.0

Version 5.0.0 represents a significant milestone in the evolution of Lightweight Charts™, delivering on our commitment to keep the library truly "lightweight". Despite adding numerous new features, improvements, and fixes, we've managed to reduce the bundle size by up to 16%, bringing the base bundle size down to just 35kB. This remarkable reduction was achieved through enhanced tree-shaking capabilities, modernized architecture, and careful optimization of core features.

This release introduces highly requested features like multi-pane support and new chart types. It also modernizes the codebase and improves its architecture to set a foundation for future enhancements without compromising on size.

### Major Updates

#### Multi-Pane Support

One of our most requested features, multi-pane support is now available. It allows you to create complex chart layouts with multiple independent viewing areas. This enhancement enables sophisticated technical analysis setups and better visualization of related data series. Additional key benefits include:

- Full support for multiple panes within a single chart
- Independent scale and series management per pane
- Flexible pane sizing and arrangement options

See Panes for more information.

#### New Chart Types

**Yield Curve Charts**

- New specialized chart type for displaying yield curves
- Custom horizontal scale behavior with linear spacing
- Optimized whitespace handling

**Options Charts**

- Price-based horizontal scale support
- Specialized formatting and interaction handling
- Ideal for options chain visualization

See Chart types for more information about the Yield Curve Chart and Options Chart types.

#### Enhanced Color Support

- Expanded native support for sRGB-based colors (RGB, RGBA, hex, named colors, HSL)
- Support for expanded color gamuts like Display P3
- Ability to specify a custom color parser to add support for non-sRGB formats
- Reduced bundle size through browser-native color parsing

#### Architectural Improvements

- Watermark feature reimplemented as plugins (
`TextWatermark`

and`ImageWatermark`

) - Series Markers extracted as a plugin for better tree-shaking
- New Up/Down Markers Plugin for price change visualization
- Introduction of Pane Primitives for plugin attachment

### Breaking Changes

- New unified series creation API (see migration guide)
- Dropped CommonJS support and updated JS syntax version to ES2020
- Watermark functionality moved to plugins
- Series markers implementation changed to plugin system

### Enhancements

- Added relative gradient option for baseline and area series (
`relativeGradient`

) - New time scale option for maximum bar spacing (
`maxBarSpacing`

) - Added
`priceLines()`

method to`ISeriesApi`

interface - Enhanced watermark capabilities with multi-line text support
- Improved plugin system with Pane Primitives support
- Better tree-shaking capabilities for smaller bundle sizes

### Bug Fixes

- Fixed primitive detachment update issues (#1594)
- Various performance and rendering improvements

### Migration Guide

We've prepared a comprehensive migration guide to help you upgrade from v4 to v5. Key areas to note:

- Series Creation API changes
- Watermarks and Series Markers moving to separate plugins
- Plugin system updates

See the full migration guide: Migrating from v4 to v5

### Technical Notes

This release uses ES2020 syntax and no longer supports CommonJS. If you need to support older environments, you'll need to set up transpilation for the `lightweight-charts`

package in your build system using tools like Babel.

As always, we thank you for your support and help in making Lightweight Charts™ the best product on the financial web. We look forward to seeing what you build with these new capabilities!

You can always send us your feedback via GitHub. Happy trading!

Team TradingView

See changes since the last published version.

## 4.2.3

**Minor Improvements**

- Improve check for crosshair label visibility on the price scale. This improves upon previous work (#1743 in v4.2.2) by reducing the allocated space for the crosshair when it is enabled, but the label is disabled. (PR #1757)

**Bug Fixes**

- Added additional prototype pollution protection for internal merge helper function. (PR #1758)

Changes since the last published version.

## 4.2.2

**Minor Improvements**

- Improved price scale width calculation by not allocating space for crosshair labels when the crosshair is disabled. (PR #1743)

**Bug Fixes**

- Fixed calculations for
`fixLeftEdge`

and`fixRightEdge`

on the first render when both are true and data is added to an initially empty chart. Fixes issue #1356. (PR #1741)

Changes since the last published version.

## 4.2.1

**Bug Fixes**

- Fixed an issue where the series title part of a price scale label appeared blurry when using Firefox.

Changes since the last published version.

## 4.2.0

**Enhancements**

- Added new
`attributionLogo`

option to`LayoutOptions`

. This feature displays the TradingView attribution logo on the main chart pane by default, helping users meet the library's licensing requirements for attribution.- The TradingView attribution logo can be easily hidden by setting the
`attributionLogo`

option to`false`

in the chart's`layout`

option.

- The TradingView attribution logo can be easily hidden by setting the
- Improved data validation for
`OhlcData`

and`SingleValueData`

. Introduced`isFulfilledBarData`

for`OhlcData`

and`isFulfilledLineData`

for`SingleValueData`

, ensuring more accurate validation of data types. Contributed by @mozeryansky (PR #1579, fixes #1526).

Changes since the last published version.

## 4.1.7

**Enhancements**

- Further Refinement of the Price Scale Label Alignment (PR #1630)

Changes since the last published version.

## 4.1.6

**Enhancements**

- Improved Price Scale Label Alignment: Enhanced the alignment algorithm for price scale labels to ensure they do not move out of the viewport. This improves the visibility of price labels, particularly when they are near the edges of the scale. Fixes #1620 (PR #1621)

Changes since the last published version.

## 4.1.5

**Enhancements**

- Added
`IHorzScaleBehavior.shouldResetTickmarkLabels`

. (PR #1614)

Changes since the last published version.

## 4.1.4

**Bug Fixes**

- Fixed hoveredSeries being undefined during series removal and creation. (PR #1529, fixes #1406, fixes #1499)
- Fixed price label rendering artefact. (PR #1585, fixes #1584)
- Fixed an issue that prevented primitives with
`zOrder`

set to`top`

from drawing above the last price animation. (PR #1576) - Fixed possible ReDos. (PR #1536)
- Fixed marker positioning, which could cause a space between histogram and bottom of the chart. (PR #1538 & #1539, fixes #1382)

Changes since the last published version.

## 4.1.3

**Minor Improvements**

- Added option to disable bold labels in the time scale. (PR #1510)

**Bug Fixes**

- Fixed sub-pixel horizontal alignment of the crosshair marker and series markers. (PR #1505, fixes #1504)

Changes since the last published version.

## 4.1.2

**Bug Fixes**

- Fix for 'Total canvas memory use exceeds the maximum limit' error raised on iOS Safari. (PR #1485)

**Minor Improvements**

- Improved error messages for price scale margins. (PR #1489)

Changes since the last published version.

## 4.1.1

**Bug Fixes**

- Fixed
`shiftVisibleRangeOnNewBar`

behaviour for realtime updates to a series. Additionally, a new option`allowShiftVisibleRangeOnWhitespaceReplacement`

has been added if you wish to have the old 4.0 behaviour for when new data replaces existing whitespace. (PR #1444) - When disabling touch scrolling on the chart via either the
`vertTouchDrag`

or`horzTouchDrag`

setting in the`handleScroll`

options, any touch scroll events over the corresponding scale will now be ignored so the page can be scrolled. (PR #1445)

Changes since the last published version.

## 4.1.0

Version 4.1 of Lightweight Charts introduces exciting new features, including the introduction of Plugins, which provide developers the ability to extend the library's functionality. Additionally, this release includes enhancements to customize the horizontal scale and various minor improvements and bug fixes.

**Major Updates**

**Plugins**

Developers can now leverage the power of Plugins in Lightweight Charts. Two types of Plugins are supported - Custom Series and Drawing Primitives, offering the ability to define new series types and create custom visualizations, drawing tools, and annotations.

With the flexibility provided by these plugins, developers can create highly customizable charting applications for their users.

To get started with plugins, please refer to our Plugins Documentation for a better understanding of what is possible and how plugins work. You can also explore our collection of plugin examples (with a preview hosted here) for inspiration and guidance on implementing specific functionality.

To help you get started quickly, we have created an NPM package called create-lwc-plugin, which sets up a plugin project for you. This way, you can hit the ground running with your plugin development.

**Horizontal Scale Customization**

The horizontal scale is no longer restricted to only time-based values. The API has been extended to allow customization of the horizontal scale behavior, and enable uses cases like options chart where price values are displayed in the horizontal scale. The most common use-case would be to customise the tick marks behaviour.

The createChartEx function should be used instead of the usual `createChart`

function, and an instance of a class implementing IHorzScaleBehavior should be provided.

A simple example can be found in this test case: horizontal-price-scale.js

**Enhancements**

- Added point markers styling option for line-based series. (closes #365) Docs
- Added double click subscriber for the main chart pane. (closes #1385) Docs
- Added
`setCrosshairPosition`

API, allowing programmatic setting of the crosshair position. (fixes #1198, #1163, #438) Docs - Added an option to disable crosshair. Introduced the
`Hidden`

option in the`CrosshairMode`

setting. (closes #749, thanks to @luk707) - Allow overriding tick mark label length via the
`tickMarkMaxCharacterLength`

option. (closes #1396) Docs - Support for overriding the percentage formatter within the localization options. (fixes #1328, #1291) Docs
- Added
`paneSize`

getter to`IChartApi`

, returning the dimensions of the chart pane. (issue #1411) Docs - Added options to set minimum dimensions for the price and time scales. (closes #1062, related to #1163, #50) Docs, Docs

**Bug Fixes**

- Fixed chart layout when direction is set to RTL. (PR #1338)
- Fixed re-enabling of
`autoSize`

after disabling it. (PR #1274) - Corrected percentage mode and zero first value. (fixes #1386)
- Prevent chart shifting when new data replaces existing whitespace. (fixes #1201)

Thanks to our Contributors for this Release:

You can always send us your feedback via GitHub. We look forward to hearing from you! And as always, happy trading!

Team TradingView

See issues assigned to this version's milestone or changes since the last published version.

## 4.0.1

**Enhancements**

- Add the ability to specify font colour for the Priceline labels. #1274 #1287
- Ignore resize method if
`autoSize`

is active, and added API to check if active. #1301

**Bug fixes**

- Typo in customization guide. Thanks @UcheAzubuko. #1284
- Inability to immediately add markers when
`autoSize`

chart option is enabled. Thanks @victorbrambati. #1271 #1281 - First render when using
`autosize`

doesn't show the latest bars. Thanks @victorbrambati #1281. #1282 - Series rendering bug when outside of visible range. #1293 #1294
- Auto contrast text color for crosshair labels. #1309 #1310
- Hit box from the text of marker incorrectly shifted to the right. #1270 #1305

As always, we thank you for your support and help in making Lightweight Charts™ the best product on the financial web. And a big shout out to our hero contributors @victorbrambati, and @UcheAzubuko!

You can always send us your feedback via GitHub.

We look forward to hearing from you! And as always, happy trading! Team TradingView

See issues assigned to this version's milestone or changes since the last published version.

## 4.0.0

Long overdue as it’s been nearly 1 year since our last major update, but behold before all the changes that have happened over the last 12 months.

In total, more than 20 tickets have been addressed with one of the most important ones being **fancy-canvas** – the library we use to configure HTML canvas in Lightweight Charts™.

Please view the migration guide here: Migrating from v3 to v4.

**Breaking changes**

- Fancy-canvas 2 | #818
- Added support for ES module exports | #613
- We are now generating two more build types: esm, standalone & cjs
- Updated scales design | #606
- Changed scales look & feel according to the new design

- Add possibility to disable time axis ticks | #1043
- Added
`ticksVisible`

to`TimeScaleOptions`

, renamed`drawTicks`

to`ticksVisible`

in`PriceScaleOptions`

. - Custom price lines should be atop of the series | #684
- Price line to be added on top of any series - shout out to thanhlmm

- Remove deprecated code | #626
- Fix types inconsistency on API level with time | #470
- Add API to get chart values (data, markers, etc) | #414
- Added methods:
`ISeriesApi.markers`

`ISeriesApi.dataByIndex`

- Changed time types everywhere in the public API to
`Time`

- Added methods:

**Enhancements**

- Handle resize with ResizeObserver if it's exist in window | #71
- There was an issue when resizing the chart (such as rotating the screen of a phone/tablet).

- Add possibility to use default tick mark formatter implementation as a fallback | #1210
- Allow the custom tick mark formatter to return null so that it will use the default formatter for that specific mark.

- Add possibility to invert Area series filled area | #1115
- Adds invertFilledArea property to the AreaStyleOptions which when set to true will invert the filled area (draw above the line instead of below it).

- Documentation website improvements | #1001 #1002
- Provides a way to apply theme-based colors to a chart whenever the Docusaurus theme is changed.

- Add ability to draw parts of area with different colors | #1100
- Add a possibility to change line, top and bottom colors for the different parts of an area series

- Add possibility to change price axis text color | #1114
- Reset price and time scale double click options | #1118
- Distinguishing the reset between price & time scale vs having only one option

- Add curved lines | #506
- Add a new line type that draws curved lines between series points.

**Chores**

- Replace deprecated String.prototype.substr | #1048
- Shout out to CommanderRoot

**Bug fixes**

- Refactoring resize the chart | #367
- The chart is blank on printed page in Chromium | #873
- Chart was blank when printing

- Horizontal scroll animations improvements | #1136
- Fixes glitches when resetting the chart time scale while scrolling

- Draw series last price & price line labels on the top layer | #1046
- Fixes an issue where price line could be place over price scale labels

- Incorrect price line labels formatting | #1032
- When setting the price scale mode to anything than 'Normal' the price for PriceLine wasn't properly calculated.

- lockVisibleTimeRangeOnResize does not work with fixLeftEdge | #991
- The visible range is no longer changed after resizing the chart.

- Crosshair label text appears on the chart during initial render | #1255
- Small text artefacts from the crosshair no longer appear on the time axis before any interaction with the chart.

As always, we thank you for your support and help in making Lightweight Charts™ the best product on the financial web. And a big shout out to our hero contributors thanhlmm, CommanderRoot, samhainsamhainsamhain & colleague Nipheris! You can always send us your feedback via GitHub. We look forward to hearing from you! And as always, happy trading! Team TradingView

See issues assigned to this version's milestone or changes since the last published version.

## 3.8.0

We're happy to announce the next release of Lightweight Charts™ library. This release includes many improvements and bug fixes (as usual), but we are thrilled to say that from this version the library has its own documentation website that replaces the documentation in the repository. Check it out and share your feedback in this discussion thread.

**Enhancement**

- Documentation website (see #875, #918, #411, #919, #922, #983, #980, #1006)
- Quick tracking mode (see #830)
- Improved mouse behaviour on touch devices (like mouse connected to mobile phone/tablet) (see #106)
- Custom color for items of candlestick and line series (see #195)
- Labels might be cut off when disabling scale and scroll (#947)
- Add ability to disable visibility of price line line (see #969)

**Fixed**

- timeScale.fitContent is not working correctly (see #966)
- Delegate.unsubscribeAll method works in opposite way (see #995)
- Last price animation is active when no data added to the right (but to the left) (see #886)
- subscribeClick on mobile always get the last index of all the items (see #657)
- Incorrect crosshair position on scrolling by dragging by mouse (see #987)
- A painting slows down after a while with tons of updates (see #946)
- Bars disappear with devicePixelRatio less than 1 (see #982)
- There are no tick marks on the price axis (see #939)
- Disabling scrolling by disabled horzTouchDrag and vertTouchDrag options disables moving crosshair in tracking mode (see #434)
- Reducing precision doesn't update price scale width (see #550)
- Chart width is jumping on series change from area to candles (see #943)
- Log axis is not scaling on small number (see #874)
- Overlay series title is not rendered when no series use right price scale (see #926)
- scrollToPosition with big negative value and when no data breaks the chart (see #889)
- When rendering multiple charts with baseline series, baseValue of the last element is used on all charts series. (see #898)

Thanks to our contributors:

- @zaleGZL zale

See issues assigned to this version's milestone or changes since the last published version.

## 3.7.0

**Enhancement**

- The new baseline series chart (see #151)
- Documentation about time zones support (see #781)
- Added methods to get time axis size and subscribe on size change (see #853)
- Improved performance of setting/updating series data (see #418 and #838)
- Use lowerbound in TimeScale timeToIndex search (see #767)
- Add JSDoc comments for existing API docs (see #870)

**Fixed**

- Increased min price tick mark step up to 1e-14 (from 1e-9) (see #841)
- Fix typo in customization docs (see #844)
- Do not paint time axis if it not visible (see #865)
- Remove color customisation from settings.json (see #869)

Thanks to our contributors:

- @thanhlmm Thanh Le

See issues assigned to this version's milestone or changes since the last published version.

## 3.6.1

**Fixed**

- In v3.6.0 there was a typo in
`LasPriceAnimationMode`

const enum (`Last`

without`t`

), which was fixed in this release. The incorrect name is still available to import and could be used in your code so no breaking change so far (see e5133cb0c50fc557182aba4011e170aaf30a5b1a)

See changes since the last published version.

## 3.6.0

On this day 10 years ago, 10th September 2011, the very first version of the TradingView website was deployed. To celebrate 10th anniversary we're happy to announce the new version of lightweight-charts library v3.6.0 🎉🎉🎉

**Enhancement**

- Gradient chart background color (see #831)
- How to add buffer animation to price jump (see #567)
- Kinetic scroll (see #832)

**Fixed**

- Incorrect initial barSpacing when both fixRightEdge and fixLeftEdge are enabled (see #823)
- Time axis label get cut on the edge if a fix edge option is enabled (see #835)
- Price axis doesn't respect the width of crosshair label (see #834)
- Fixed both timescale edges make lockVisibleTimeRangeOnResize turn wrong (see #814)
`Error: Value is null`

error while set the data is container has 0x0 size (see #821)

Thanks to our contributors:

- @thanhlmm Thanh Le

See issues assigned to this version's milestone or changes since the last published version.

## 3.5.0

**A note about rendering order of series, which might be interpret as a bug or breaking change since this release**

This is not really a breaking change, but might be interpret like that. In #794 we've fixed the wrong order of series, thus now all series will be displayed in opposite order (they will be displayed in order of creating now; previously they were displayed in reversed order).

To fix that, just change the order of creating the series (thus instead of create series A, then series B create series B first and then series A) - see #812.

**Fixed**

- Screenshot output missing piece on bottom right (see #798)
- Overlapped line chart show wrong color order when hover (see #794)
- Price line label show on both axis (see #795)

Thanks to our contributors:

- @thanhlmm Thanh Le

See issues assigned to this version's milestone or changes since the last published version.

## 3.4.0

**Enhancement**

- Add option to fix right edge (see #218)
- Drop restriction for min bar spacing value (see #558)
- Round corners of the line-style plots (see #731)

**Fixed**

- AutoscaleProvider documentation error (see #773)
- Candlestick upColor and downColor is not changed on applyOptions (see #750)
- Cleared and reset data appears at visually different location (see #757)
- Remove unused internal method from SeriesApi (see #768)
- Removing data for the last series doesn't actually remove the data (see #752)
`to`

date of getVisibleRange contains partially visible data item and it's impossible to hover it (see #624)- series.priceFormatter().format(price) does not work (see #790)

See issues assigned to this version's milestone or changes since the last published version.

## 3.3.0

**Enhancement**

- Add type predicates for series type (see #670)
- Create Grid instance for every pane (see #382)
- Add possibility to chose crosshairMarker color, so it will be independent from line-series color (see #310)
- Implement option not to shift the time scale at all when data is added with
`setData`

(see #584)

**Fixed**

- Incorrect bar height when its value is more than chart's height (see #673)
- Disabling autoScale for non-visible series (see #687)

Thanks to our contributors:

- @dubroff
- @SuperPenguin Andree Yosua
- @mecm1993 Manuel Cepeda

See issues assigned to this version's milestone or changes since the last published version.

## 3.2.0

**Enhancement**

- Feat/gzip friendly colors (see #598)
- Add coordinateToLogical and logicalToCoordinate (see #587)
- Add API to show/hide series without removing it (see #471)
- Add run-time validation of inputs in debug mode (see #315)
- Pixel perfect renderers fixes (see #535)
- Add title option to createPriceLine (see #357)

**Fixed**

- Set rightOffset and scrollToPosition async as well as setVisibleRange (see #406)
- timeScale() changes visible range on setData() (see #549)
- Remove chart's size restriction or make it smaller (see #366)
- LineStyle.Dotted make no effect (see #572)
- If priceScaleId is empty string, invalid price scale api is returned (see #537)
- Incorrect Selection seen on long press in ios webview on chart (see #609)
- One-point line series is invisible (see #597)
- Empty price scale after creating series with the same price range (see #615)

**Infra and dev env**

- Compress artifacts in graphics tests in CI (see #145)
- Run tests against production build (see #503)
- Add test to check code usage coverage (see #495)
- Migrate from codechecks (see #356)
- Updated dev deps

Thanks to our contributors:

- Andree Yosua @SuperPenguin
- Christos @christose
- Shergin Rodion @beholderrk
- wenhoujx @wenhoujx

See issues assigned to this version's milestone or changes since the last published version.

## 3.1.5

It's a just re-published accidentally published 3.1.4 version, which didn't actually fix the issue #536.

Version 3.1.4 has been deprecated.

**Fixed**

- TypeError
`_internal_priceScale is not a function`

while getting series price scale (see #536)

See issues assigned to this version's milestone or changes since the last published version.

## 3.1.3

**Fixed**

`handleScroll`

and`handleScale`

options aren't applied (see #527)

See issues assigned to this version's milestone or changes since the last published version.

## 3.1.2

**Fixed**

- Crosshair doesn't work on touch devices (see #511)

See issues assigned to this version's milestone or changes since the last published version.

## 3.1.1

**Fixed**

- Fixed production build of 3.1 version (see #502 and 62aa93724e40fbb1b678d9b44655279a1df529c5)

See issues assigned to this version's milestone or changes since the last published version.

## 3.1.0

**Enhancement**

**Fixed**

- Added support for 'transparent' color (see #491)
- Refactor DataLayer/ChartApi (see #270)
- Remove series then scroll to right after not working (see #355)
- Scaling via mouse click and drag doesn't work if chart is inside shadow root (see #427)
- Applying watermark in setTimeout doesn't make an effect (see #485)
- Importing the library in server-side context caused
`ReferenceError`

(see #446)

**Undocumented breaking changes**

We know that some of users probably used some hacky-workarounds calling internal methods to achieve multi-pane support. In this release, to reduce size of the bundle we dropped out a code for pane's separator (which allows to resize panes).

As soon this workaround is undocumented and we don't support this feature yet - we don't bump a major version. But we think it's better to let you know that it has been changed.

**Development**

- Dropped support NodeJS < 12.18
- Migrated from TSLint to ESLint (see #314)
- Migrated from clean-publish to in-house script to clear package.json (see #474)

Thanks to our contributors:

- Meet Mangukiya @meetmangukiya
- NekitCorp @NekitCorp

See issues assigned to this version's milestone or changes since the last published version.

## 3.0.1

**Fixed**

- Correctly handle
`overlay: true`

in series options while create series to backward compat (see #475)

See issues assigned to this version's milestone or changes since the last published version.

## 3.0.0

**Breaking changes**

We have some breaking changes since the latest version due some features and API improvements:

- Methods
`subscribeVisibleTimeRangeChange`

and`unsubscribeVisibleTimeRangeChange`

has been moved from ChartApi to TimeScaleApi - Since 3.0 you can specify price axis you'd like to place the series on. The same for moving the series between price scales (see migration guide below)

See breaking changes doc with migration guide to migrate smoothly.

**Enhancement**

- Added ability to customize time scale tick marks formatter (see #226)
- Added ability to put text for series markers (see #207)
- Added ability to specify your own date formatter (see #368)
- Improved tick marks generation algorithm for the first point (see #387)
- Made inbound types weakly (outbound ones should be strict) (see #374)
- Removed non-exported const enum's JS code (see #432)
- Introduced ts-transformer-properties-rename instead of ts-transformer-minify-privates (see #436)

**Added**

- Add ability to override series' autoscale range (see #392)
- Add API to get price scale's width (see #452)
- Disabling/enabling scaling axis for both price and time (see #440)
- Get screen coordinate by a time point (see #435)
- Remove tick mark from price label (see #378)
- Support the second price axis (see #129)
- Visible time range should have bars count of the space from left/right (see #335)

**Fixed**

`series.setMarkers`

requires at least one data point (see #372)- Impossible to override the only width or height in constructor (see #353)
- Incorrect alignment of markers if series has gaps (see #464)
- Multiple series: error while trying to scroll the chart (see #373)
- Replace const enums with enums to let use them in projects with enabled isolatedModules option (see #375)

Thanks to our contributors:

- Ben Guidarelli @barnjamin
- gkaindl @gkaindl
- scrwdrv @scrwdrv
- Yusuf Sahin HAMZA @yusufsahinhamza

See issues assigned to this version's milestone or changes since the last published version.

## 2.0.0

**Breaking changes**

- Removed unused
`lineWidth`

property from`HistogramStyleOptions`

interface (it affects nothing, but could break your compilation) - Changed order of
`width`

and`height`

args in`resize`

method (#157) - Pattern for all non-solid (dotted, dashed, large dashed and sparse dotted) line styles was a bit changed (#274)

**Enhancement**

**Added**

- Disable all kinds of scrolls and touch with one option (#230)
- Added to the acceptable date formats (#296)
- Add option to show the "global" last value of the series instead of the last visible (#203)

**Fixed**

- Price line didn`t hightlight price (#273)
- CreatePriceLine not removed (#285)
- Crosshair line not visible when priceScale position set to none (#302)
- chart.resize parameter is inverted (#157)
- Removed unnecessary spacing from left/right (1 bar from each side) in
`fitContent`

(#345)

Thanks to our contributors:

- Andree Yosua @SuperPenguin
- kpaape @kpaape
- Matt Conway @mattsre

See issues assigned to this version’s milestone or changes since the last published version.

## 1.2.2

**Fixed**

- Bug while rendering few datasets with not equal timescale (#321)

## 1.2.1

**Added**

- Add custom price lines (#183)
- Migrate canvas-related logic to fancy-canvas library (#141)
- Add coordinateToPrice method to ISeriesApi (#171)

**Fixed**

- Scrolling by price is incorrect (#213)
- Histogram (volume) does not honor color setting (sometimes) (#233)
- Logarithmic scaling is applied to volume (#227)
- hoveredSeries in mouse events params is always undefined (#190)
`lineType`

option does not work for area/line series (#220)- Double clicking on time scale will reset fix left edge (#224)
- Series' marker does not aligned after autoscale (#212)
- Error on setData empty array for overlay histogram series (#267)
- Added some missing docs (#211 #193 #245)

See issues assigned to this version’s milestone or changes since the last published version.

## 1.1.0

**Added**

- Apply localization to specific series (#62)
- Series-based markers (#24)
- Reduced size of the library by using
`ts-transformer-minify-privates`

transformer (#98)

**Fixed**

- The chart can't start from the left (#144)
- OHLC charts render incorrect when
`value`

is provided (#165) - Price axis is not shown if series is created inside promise chain (#164)
- The line chart can't move to the left (#143)
- Lots of non-passive event listener warnings (#139)
- applyOptions of histogram series with color doesn't affect the data (#112)
- Price Axis Scaling Bug (#122)
- LineSeries is not displayed if starting x value is out of viewport (#116)
- Crosshair isn't updated when timescale is changed (#120)
- Pinch isn't prevented by long tap (#95)

Thanks to our contributors:

- zach @n8tb1t
- Chris Kaczor @krzkaczor

See issues assigned to this version’s milestone or changes since the last published version.

## 1.0.2

**Fixed**

- The histogram last bar not hide in chart (#133)

## 1.0.1

**Fixed**

- Setting the data to series fails after setting the data to histogram series with custom color (#110)

## 1.0.0

The first release.

The docs for this version are available here.