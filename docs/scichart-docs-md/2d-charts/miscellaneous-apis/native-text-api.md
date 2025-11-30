---
source: https://www.scichart.com/documentation/js/v4/2d-charts/miscellaneous-apis/native-text-api
scraped_at: 2025-11-28T18:24:46.692869
---

# https://www.scichart.com/documentation/js/v4/2d-charts/miscellaneous-apis/native-text-api

# Native Text Api

The Native Text api is new in SciChart v3. It uses industry standard font libraries compiled into webassembly to render text directly using webGL, supporting all types of fonts including right to left text, shaped fonts such as Arabic and Chinese. This first version of the api is not complete and we welcome your feedback to shape it going forward.

## Font Loading

Only Arial is included in the webassembly data as standard. Other fonts must either be hosted on your server, or registered if coming from a remote location. In either case, fonts are only downloaded once, and are then cached in the browser (in indexdb).

### Hosting fonts on your server

If you simply specify a font other than arial for native axis labels, dataLabels or NativeTextAnnotation, SciChart will look for a file with that name .ttf on your server. For example, the following annotation will cause SciChart to request /jokerman.ttf

`// Hosted font`

const nativeTextHostedFont = new NativeTextAnnotation({

x1: 1,

y1: 1,

font: "jokerman",

text: "This text uses a hosted font",

fontSize: 18

});

To serve fonts using webpack dev server you need a rule for .ttf files which specifies the correct mimetype, and you need to copy the font file itself to the root of the output location:

`// webpack.config.js`

const path = require("path");

const CopyPlugin = require("copy-webpack-plugin");

const webpack = require("webpack");

module.exports = {

mode: "development",

entry: "./src/index.js",

module: {

rules: [

// Serve .ttf files

{

test: /\.ttf$/,

use: {

loader: "url-loader",

options: { mimetype: "application/font-ttf" }

}

}

]

},

resolve: {

extensions: [".js"]

},

output: {

filename: "bundle.js",

path: path.resolve(__dirname, "build")

},

plugins: [

new CopyPlugin({

patterns: [

{ from: "src/index.html", to: "" },

// Copy the font to the root of the output location

{ from: "src/jokerman.ttf", to: "" },

{ from: "node_modules/scichart/_wasm/scichart2d.data", to: "" },

{ from: "node_modules/scichart/_wasm/scichart2d.wasm", to: "" }

]

}),

]

};

### Registering Remote Fonts

Use `sciChartSurface.registerFont`

to provide a remote url to load a font file from. Note that this requires a sciChartSurface instance - it is not a static method. The method returns a promise which resolves once the file is downloaded. If you do not await this method, the text will render using Arial until the font is available. There is a timeout (set by SciChartDefaults.nativeFontTimeout, default 2000ms) after which SciChart will fall back to Arial and stop trying to load the custom font. You might need to increase this if you need to load fonts over a slow connection, but in general it is better to await the registerFont method.

There is currently a limitation in that the font fetching from webassembly will not follow a http 302 redirection, so you need to pass the url to the actual file. For instance, when downloading from github, https://github.com/google/fonts/blob/main/ofl/braahone/BraahOne-Regular.ttf redirects to https://raw.githubusercontent.com/google/fonts/main/ofl/braahone/BraahOne-Regular.ttf so you need to use the githubusercontent.com link.

`// Registering a font`

await sciChartSurface.registerFont(

"braahone",

"https://raw.githubusercontent.com/google/fonts/main/ofl/braahone/BraahOne-Regular.ttf"

);

const nativeTextRemote = new NativeTextAnnotation({

x1: 3,

y1: 7,

text: "This text uses a font from the internet",

fontFamily: "braahone",

fontSize: 24

});

## Native Text API

The following sections describe some of the native text api methods and concepts which you may need if you want to develop custom annotations, dataLabels or series using native text. In summary, using the native text api goes like this:

- Call renderContext.getFont to get a font instance. Fonts are cached and shared within webassembly, so there is no need to cache them in JS.
- If necessary call getTextBounds and pass it to font.CalculateStringBounds to get information on the size of your text so you can adjust drawing coordinates.
- Call font.DrawString, or font.DrawStringAdvanced

### getFont

getFont is a method on webGLRenderContext2D which is passed to the drawing methods (eg to RenderContextAnnotationBase.drawWithContext) as renderContext. If you plan to use rotation or scaling, set the advanced parameter true. Requesting an advanced font actually means SciChart will generate a Signed Distance Field font which gives much better rendering for rotated and scaled text, and in the future will allow for more advanced text effects. However, if you don't need this, normal fonts use less memory and are slightly faster to first frame.

There is no need to call font.Begin() - this is done by getFont. Set the drawEarly parameter true if you are planning to call font.End() early so other elements can draw over the text. This is not stricly required, but it causes SciChart to give you a separate font instance so you don't mess with other text that might be drawing with the same font.

Do not call nativeContext.AquireFont directly. There is no need to delete the font to free memory.

### TextBounds

Call getTextBounds from scichart/Charting/Visuals/Helpers/NativeObject, to get a TSRTextBounds instance. Each call to this method returns the same cached instance. Do not call delete on it.

Call font.CalculateStringBounds which populates the TSRTextBounds with the size of your desired text. The image below shows how the properties on textBounds relate to the text. Text is anchored at the left on the baseline. The origin is top, left (for consistency with canvas coordinates) so to have the text anchored at the top, you need to add textBounds.GetLineBounds(0).m_fHeight to your y coordinate.

For multi line text, m_fHeight is the height of the entire text block, but text is still anchored at the baseline of the first line.

### Drawing Text

Call font.DrawString, or font.DrawStringAdvanced. DrawString is just text, colour, x, y whereas DrawStringAdvanced also allows you to specify rotation, multiline alignment and spacing.The only difference is the options available. You do not have to have created the font with advanced: true to use DrawStringAdvanced if you are just doing multiline, but for rotated text you will get much nicer rendering with advanced: true.

Note that text is not actually drawn immediately. This happens when font.End() is called.

SciChart automatically calls font.End on all fonts at the end of the render cycle. If you want the native text to draw earlier so other chart elements can draw over it, you can call font.End yourself, but for optimum performance you want to do this as little as possible.

### Rotation

To get a rotation vector use the following code:

`// Rotation vector`

import { getVector4 } from "scichart"

const rotationVector = getVector4(

webAssemblyContext2D,

rotationCenterX,

rotationCenterY,

rotationInRadians,

0

);

Like textBounds this returns a single shared instance so you do not need to delete it.

### Scaling

You can adjust the size of text by calling font.SetScale, which will multiply the font size by the value you set. This only applies to subsequent DrawString/DrawStringAdvanced calls.

#### See Also

##### Axis Labels

Performance Considerations - Native Text Axis Labels