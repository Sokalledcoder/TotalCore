# Volume footprint charts: a complete guide

#### Important notes on interpretation
When interpreting alert results for Volume Footprints, keep in mind that this study is repainting by design.In real time, the chart may use one intrabar data source (e.g., 1T) for calculations, while the same bar may later be recalculated using a less granular interval (e.g., 1S) as more historical data becomes available.This means that the appearance of imbalances — and therefore alert triggers — can differ slightly between real-time execution and historical review.
In addition, when using Row size = ATR, the chart automatically derives the number of Ticks per row from the current ATR value. For consistent comparison between alert signals and chart visuals, it is recommended to manually set Ticks per row to the same value and to configure alerts with manual row sizing whenever possible.
For more information about repainting behavior and how it may affect script calculations, see article about [Repainting](https://www.tradingview.com/support/solutions/43000478429/)

#### Settings
Customization options for the volume footprint chart are available from the chart settings, which you can access from the gear button in the toolbar above the chart.

#### Candles
The settings in the "Candles" section are identical to those for a regular candlestick chart. From this section, you can configure the appearance of the candlesticks.

#### Volume footprint

#### Row size
Controls how the chart will determine the size of each footprint row (level). There are two options to choose from:
- The "Auto" option specifies that the chart will calculate the size automatically based on the data's latest normalized Average True Range (ATR) value. It uses the formula: 0.2 * NormalizedATR / MinimumTick. The chart recalculates the size when selecting the "Volume footprint" chart type or changing the symbol or timeframe. When using this option, the input below specifies the length of the ATR calculation
- The "Manual" option specifies that the chart will utilize the number of ticks specified in the "Ticks per row" input below

#### ATR length
Specifies the smoothing length for the Average True Range used to calculate the number of ticks per footprint row when the "Row size" input uses the "Auto" option.

#### Ticks per Row
Specifies the number of ticks per footprint row when the "Row size" input uses the "Manual" option.

#### Display
Specifies the display type of the chart. In Cluster mode, all cells have the same width. In Profile mode, the width of each cell is proportional to the trading volume at that level, offering a clearer, more dynamic representation.

#### Type
Defines the display mode of the footprints on the chart. Four options are available:
- The "Buy and Sell" option (default) displays seller volume across levels to the left of each candle and buyer volume to the right
- The "Delta" option will display one column to the right of each bar that shows the volume delta (i.e., the difference between buyer and seller volume) for each level
- The "Total" option will display one column to the right of each bar that shows the total volume at each price level
- The "Ladder" option will highlight with color the highest volume at each price level

#### Apply gradient to background
If enabled, the color of the background of each footprint level will differ based on its volume compared to the volume at other levels. The chart uses the following algorithm to calculate the gradient colors:
1. Determine the maximum and minimum volume
2. Calculate the volume range, i.e., the difference between the maximum and minimum volume value
3. Subtract the minimum volume from the current level's volume
4. Calculate the ratio of the value obtained in step 3 to the volume range obtained in step 2
5. Use the ratio from step 4 to select a color from the available options:Select the first color if the ratio is less than 0.25Select the second color if the ratio is greater than or equal to 0.25 and less than 0.5Select the third color if the ratio is greater than or equal to 0.5 and less than 0.75Select the fourth color if the ratio is greater than or equal to 0.75
6. Select the first color if the ratio is less than 0.25
7. Select the second color if the ratio is greater than or equal to 0.25 and less than 0.5
8. Select the third color if the ratio is greater than or equal to 0.5 and less than 0.75
9. Select the fourth color if the ratio is greater than or equal to 0.75