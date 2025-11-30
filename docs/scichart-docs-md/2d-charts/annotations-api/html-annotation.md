---
source: https://www.scichart.com/documentation/js/v4/2d-charts/annotations-api/html-annotation
scraped_at: 2025-11-28T18:24:01.486849
---

# https://www.scichart.com/documentation/js/v4/2d-charts/annotations-api/html-annotation

# HTML Annotations

Here we will describe how to use the HTML-based annotations feature of SciChart.JS and its advantages.

**Live Example**:

## Description

### General Annotation Layer Types Overview

The surface of the SciChart.JS chart consists of several layers in DOM tree.
These are a combination of `canvas`

, `div`

, and `svg`

nodes.

The annotations could be divided by the node type where they are rendered.

-
Native "Render Context" Annotations - rendered using WebGl and displayed on the canvas layer. Some examples are:

-
HTML Annotations - rendered as a

`div`

element placed within a DOM layer. For example: -
SVG Annotations - rendered as an SVG element on one of the SVG layers. For example:

We refer to HTML and SVG Annotations as "DOM Annotations" since they share some similar logic and the same rendering principles. Thus, the common base class is DomAnnotation📘.

There are isDomAnnotation📘 and isSvgAnnotation📘 properties on an annotation.

So, the significant difference between DOM Annotations and Native Annotations is that each DOM Annotation instance is added as a separate node to the DOM tree

There might be multiple of layers of the same type to allow drawing DOM Annotations above or below the WebGl-drawn chart elements on the canvas.

## CustomHtmlAnnotation

The HtmlCustomAnnotation📘 provides a basic functionality of an annotation and renders a `div`

element on a chart at a specified position.
And exposes a reference to this element via HtmlCustomAnnotation.htmlElement📘.

The use case for this annotation is rendering arbitrary HTML content within a chart. This provides a great flexibility by allowing to apply standard JS APIs to work with the content and styling it with CSS.

So one can use the `htmlElement`

reference and append content to it.

Example:

`// A CustomHtmlAnnotation which contains an HTML input element`

const customHtmlAnnotation = new HtmlCustomAnnotation({

xCoordinateMode: ECoordinateMode.DataValue,

yCoordinateMode: ECoordinateMode.DataValue,

x1: 2,

y1: 7,

xCoordShift: 0,

yCoordShift: 0

});

customHtmlAnnotation.htmlElement.classList.add("styledCustomAnnotation");

customHtmlAnnotation.htmlElement.innerHTML = `

<label for="colorSelect">Choose a color:</label>

<select id="colorSelect" name="colorSelect">

<option value="red" style="background-color: red; color: white;">Red</option>

<option value="green" style="background-color: green; color: white;">Green</option>

<option value="blue" style="background-color: blue; color: white;">Blue</option>

<option value="yellow" style="background-color: yellow; color: black;">Yellow</option>

<option value="purple" style="background-color: purple; color: white;">Purple</option>

</select>`;

sciChartSurface.annotations.add(customHtmlAnnotation);

Where the relevant CSS is:

`.styledCustomAnnotation {`

pointer-events: all;

background-color: grey;

padding: 4px;

}

This approach also allows the content to be rendered by UI frameworks. For more examples, check the our demo website. #TODO reference HTML Annotations Demo

## HtmlTextAnnotation

The HtmlTextAnnotation📘 extends the `CustomHtmlAnnotation`

by providing a simple interface for adding textual annotations to a chart.

In the form of constructor options: IHtmlTextAnnotationOptions📘 and instance properties:

**HtmlTextAnnotation.text****HtmlTextAnnotation.textContainerStyle**

Example:

`// A HtmlTextAnnotation which is resized on zoom and bound to data value coordinates`

const textAnnotation = new HtmlTextAnnotation({

xCoordinateMode: ECoordinateMode.DataValue,

yCoordinateMode: ECoordinateMode.DataValue,

x1: 4,

y1: 5,

x2: 7,

xCoordShift: 0,

yCoordShift: 0,

text: "This annotation has X coordinates bound to data values. Try zooming or panning",

// style object with CSSStyleDeclaration format. Supports camel-cased property names.

// https://developer.mozilla.org/en-US/docs/Web/API/CSSStyleDeclaration

textContainerStyle: {

padding: "4px",

fontSize: "1.5em",

color: "white",

background: "linear-gradient(135deg, #1f1c2c, #928dab)",

border: "1px dotted black",

borderRadius: "15px",

textOverflow: "ellipsis",

overflow: "hidden"

}

});

sciChartSurface.annotations.add(textAnnotation);

## Positioning and Sizing

Similar to other annotation types, `CustomHtmlAnnotation`

and `HtmlTextAnnotation`

could be positioned via
`x1`

and `y1`

properties.
Additionally, you can provide optional `x2`

and `y2`

values to bind the annotation size to specific coordinates.
These annotations also support different coordinate modes defined in ECoordinateMode.
xCoordinateMode, yCoordinateMode

So, for example, with the correct combination of the coordinates, coordinate modes, and CSS styles, you can achieve either a static size annotation or make it responsive to the visible range (zoom level), or the chart size. And apply other cool features that are available in CSS.

## Performance considerations

This API is made to provide better annotation flexibility, a simple and familiar setup in a browser environment. However, depending on a use case you may find the Render Context annotations have a better performance compared to DOM Annotations. So consider trying them out first, and if you can't achieve the desired result, switch to Dom Annotations.

As an example:
`NativeTextAnnotation`

s have a great performance and support features as background, multiline text, rotation, etc...
But, if you need more advanced features, consider whether the `HtmlTextAnnotation`

or `TextAnnotation`

(based on SVG) fits better.