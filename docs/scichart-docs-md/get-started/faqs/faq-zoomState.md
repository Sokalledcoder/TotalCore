---
source: https://www.scichart.com/documentation/js/v4/get-started/faqs/faq-zoomState
scraped_at: 2025-11-28T18:24:59.819059
---

# https://www.scichart.com/documentation/js/v4/get-started/faqs/faq-zoomState

# How to Detect If a User Is Zooming or Panning

## The sciChartSurface.zoomState Property

The sciChartSurface.zoomState📘 property allows us to detect if the chart has been zoomed or panned by the user, or if the chart is at extents of the data. You can take a look at the values of the EZoomState Enum here📘.

Here is example:

const statusLabel = new TextAnnotation({

x1: 0.1,

y1: 0.1,

opacity: 0.5,

fontSize: 22,

textColor: "white",

horizontalAnchorPoint: EHorizontalAnchorPoint.Left,

verticalAnchorPoint: EVerticalAnchorPoint.Bottom,

xCoordinateMode: ECoordinateMode.Relative,

yCoordinateMode: ECoordinateMode.Relative,

});

sciChartSurface.annotations.add(statusLabel);

sciChartSurface.rendered.subscribe(() => {

if (sciChartSurface.zoomState === EZoomState.UserZooming) {

statusLabel.text = "Chart has been zoomed or panned by the user"

} else if (sciChartSurface.zoomState === EZoomState.AtExtents) {

statusLabel.text = "Chart is at extents of the data"

}

})