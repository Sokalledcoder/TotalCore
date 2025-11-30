---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/data-point-labels/data-label-skip-modes-and-culling
scraped_at: 2025-11-28T18:24:23.891674
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/data-point-labels/data-label-skip-modes-and-culling

# DataLabel SkipModes and Culling

DataLabels allow per data-point text labels to be drawn on series, or arbitrary text labels at x,y positions on the chart.

You can see several datalabel examples on the SciChart.js demo:

- The Line Chart example
- The Column Chart example
- The PaletteProvider example
- The DataLabels demo
- The Stacked Column Chart demo
- The Population Pyramid demo

Explore these for some rich examples of how to use this API.

## Labels for Many Points

SciChart's native text rendering means that it can potentially draw tens of thousands of labels relatively fast, but in practise with many points there is no point drawing so many labels that they become unreadable. SciChart has a number of options for dealing with this. If you really want to show all labels even if they overlap, set skipMode📘 to EDataLabelSkipMode.ShowAll📘

### Hide overlapping labels

The default for the skipMode📘 property is EDataLabelSkipMode.SkipIfOverlapPrevious📘. This means a label will not be drawn if it would overlap the bounds of the previous label. This means that even if you have 1000 points on a line series, you will only see a few dozen non-overlpping labels (depending on the shape of your data).

The downside of this is that SciChart has to calculate the text, size and position of every label, and then throw most of them away, which is potentially inefficient. Also, it is often unclear which points on the line are actually being labeled. The alternative to this is to calculate less labels (use skipNumber📘) or to not draw labels at all if there are too many to display (use pointGapThreshold📘 or pointCountThreshold📘).

skipMode📘 also has a EDataLabelSkipMode.SkipIfOverlapNext📘 option. This is useful if you have labels of significantly varying lengths, as it means long labels tend to be skipped in favour of shorter ones.

### Improve performance with many points using skipNumber

Setting skipNumber📘 greater than 0 will make SciChart skip that many points between each label it generates. The number of labels generated is therefore pointCount / ( skipNumber + 1). You will see performance warnings in the console if more than 80% of labels were skipped.

### Showing Labels Past a Threshold

The alternative is to only show labels when the chart is sufficiently zoomed in so that there are a sensible number of labels to display, or room to show them.

#### pointGapThreshold

If your labels are a consistent size and your data is evenly spaced and does not have large y variation (ie it is smooth, not jagged), then setting pointGapThreshold📘 to around 1 will cause labels to appear only when there is room to show them. pointGapThreshold📘 is the gap between the first points divided by the size of the first label, so 1 means the spacing between points is equal to the label size. Values less than 1 will cause labels to be drawn sooner, but they may overlap. Values greater than 1 mean that you will need to zoom in more, but labels are less likely to overlap.

#### pointCountThreshold

If your data is unevenly spaced, is jagged, or your label text has significant variation in width, then pointCountThreshold📘 may give more predictable results. It is simply the number of points in view, below which labels will be drawn. skipMode📘 and skipNumber📘 still apply when these threshold options are set.

#### Custom thresholds

If you don't like either of those options, you can write your own threshold by overriding the shouldGenerate📘 function on dataLabelProvider📘. This receives a DataLabelState📘 which will return values for the first label. If shouldGenerate📘 returns true, labels will be generated. If false, they will not. Below is the standard implementation of shouldGenerate.

`public shouldGenerate(state: DataLabelState): boolean {`

if (state.pointCount > this.pointCountThresholdProperty) return false;

const firstlabel = this.getText(state);

const bounds = getTextBounds(this.webAssemblyContext);

state.font.CalculateStringBounds(firstlabel ?? "", bounds, this.style?.lineSpacing ?? 2);

return state.pointGap > bounds.m_fWidth * this.pointGapThreshold;

}