---
source: https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-labels/image-labels
scraped_at: 2025-11-28T18:24:04.857354
---

# https://www.scichart.com/documentation/js/v4/2d-charts/axis-api/axis-labels/image-labels

# Image Labels

In additional to all the label formatting options by SciChart.js, it is possible to go further and override the LabelProvider.getLabelTexture()📘 function which converts the label text that is produced by LabelProvider.formatLabel()📘 into a texture that can be drawn by WebGL. This gives you total control over the appearance of your labels so that you can use images, complex text, or a combination.

The code below is taken from our online Image Labels example. The key part is to pass an HtmlImageElement to TextureManager.createTextureFromImage()📘. Everything else here is about mapping the data to the images.

Setting `useNativeText: false`

on axis is needed for images to appear.

- TS

`const { sciChartSurface, wasmContext } = await SciChartSurface.create(divElementId, {`

theme: new SciChartJsNavyTheme()

});

const xAxis = new NumericAxis(wasmContext, {

// Ensure there can be 1 label per item in the dataset.

maxAutoTicks: 15,

axisTitle: "Mobile phone manufacturer",

// We need the data value as plain text

labelFormat: ENumericFormat.NoFormat,

useNativeText: false // need to be set to "false" to show images

});

const images = [

"https://www.scichart.com/demo/images/apple.png",

"https://www.scichart.com/demo/images/samsung.png",

"https://www.scichart.com/demo/images/xiaomi.png",

"https://www.scichart.com/demo/images/huawei.png",

"https://www.scichart.com/demo/images/oppo.png",

"https://www.scichart.com/demo/images/vivo.png",

"https://www.scichart.com/demo/images/realme.png",

"https://www.scichart.com/demo/images/motorola.png",

"https://www.scichart.com/demo/images/question.png",

"https://www.scichart.com/demo/images/lg.png",

"https://www.scichart.com/demo/images/oneplus.png",

"https://www.scichart.com/demo/images/tecno.png",

"https://www.scichart.com/demo/images/infinix.png",

"https://www.scichart.com/demo/images/google.png",

"https://www.scichart.com/demo/images/nokia.png"

];

// SciChart utility function to create HtmlImage elements from urls

const promises = images.map(image => createImageAsync(image));

const res = await Promise.allSettled(promises);

// Override labelProvider.getLabelTexture() to return an image

const getLabelTexture = (labelText, textureManager, labelStyle) => {

const index = parseInt(labelText);

if (!isNaN(index)) {

if (res[index].status === "fulfilled") {

const emoji = res[index].value;

return textureManager.createTextureFromImage(emoji, 40, 40);

} else {

console.warn(`image ${images[index]} not found`);

}

}

return textureManager.createTextTexture([labelText], labelStyle);

};

xAxis.labelProvider.getLabelTexture = getLabelTexture;

// If using asyncLabels = true, override this as well

xAxis.labelProvider.getLabelTextureAsync = (labelText, textureManager, labelStyle) =>

Promise.resolve(getLabelTexture(labelText, textureManager, labelStyle));

// Disable shared cache for this provider, otherwise other axes might pick up the emoji textures

xAxis.labelProvider.useSharedCache = false;

sciChartSurface.xAxes.add(xAxis);

This results in the following output:

Textures created this way are automatically cached for performance, and disposed of (deleted) when the chart is deleted.

Normally, the size of the texture returned is used as the width and height for layout purposes. Depending on the shape of your images, you may also want to override the **getLabelWidth** and **getLabelHeight** methods on LabelProviderBase2D📘.

For an example of how to do this with TypeScript, React and npm / webpack to import images, see our Image Labels example, part of the SciChart Demo.