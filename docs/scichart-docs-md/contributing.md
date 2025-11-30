---
source: https://www.scichart.com/documentation/js/v4/contributing
scraped_at: 2025-11-28T18:24:59.021283
---

# https://www.scichart.com/documentation/js/v4/contributing

# SciChart.js Docs Contributing Guide

## Mark document status

This are documentations statuses

If no icon - document is up to date, most of the documents will have this status.

⚠️ - existing document needs update, this icon means that the document is not up to date and requires correction

🆕 - for newly added items we can use this icon, to make it obvious. Or we can use text alternative `[NEW]`

🔄 - this icon is not used any more.

⭕ - this icon is not used any more.

✅ - this icon is not used any more.

## Use TypeScript

Use TypeScript where it is possible.

Create a `demo.ts`

file and run snippets compiler in watch mode ` npm run compileSnippets:watch`

it will watch for changes and generate `demo.js`

file.

In the documentation always reference the ts file, for example:

`ts showLineNumbers file=./PaletteProvider/demo.ts start=region_A_start end=region_A_end`

If after changing `demo.ts`

file the code snippet does not update, delete and insert it again.

## Create Search friendly titles

Create titles friendly for the site Search. The title h1, h2, h3 can be created using one, two or three hash symbols (#, ##, ###). The docusaurus uses these title for the search autocomplete. Therefore, give titles wisely to have a useful search. For example, in order to see PolarBandRenderableSeries in the search, I've created a h2 title with

`## Create PolarBandRenderableSeries`

## Decorate TypeDoc links and reference v4

This is v4 TypeDoc - https://www.scichart.com/documentation/js/v4/typedoc

In order to make all TypeDoc links distinct decorate the link with book icon `:blue_book:`

, this is an example of SciChartSurface class typedoc link

## Reference scichart.com/demo

Use this link to reference scichart demo app - https://www.scichart.com/demo/react

## Do not reference DocumentX documents

Reference pages within the docusaurus and make sure the links are not broken. The broken links show up in the build console. Do not reference old DocumentX documents.

## Use kebab-case notation for docs

- It is recommended to
**create a separate folder for each document**and to put`index.md`

or`index.mdx`

file inside. Having a separate folder is preferable because often documentation contains doc-snippets and it is nice to have them in the same folder. - In order to have nice URLs it is recommended to create folder names in a
**kebab-case notation**like`my-folder-name`

.

## Use limited formatting styles

Stick to the limited set of formatting styles.

TODO: add more formatting example

**Tip Example**

Info about the properties and functions available can be found at the TypeDoc API Documentation for SciChart📘.

**Info Example**

The default layers are defined in EDefaultRenderLayer📘.

**Note Example**

The order may differ depending on some configuration specifics.

**Warning**

**Error**: Could not load SciChart WebAssembly module. Check your build process and ensure that your scichart2d.wasm, scichart2d.data and scichart2d.js files are from the same version

**Quotation Example**

For more information about Chart Modifier types in SciChart, head over to the ChartModifier API documentation or see our Examples.

**Mermaid class diagram example**

**Insert Chart iFrame from scichart.com/demo**

**Insert Live CodePen snippet**

`<LiveDocSnippet maxWidth={"100%"} name="./Basic/demo" htmlPath="./Basic/demo.html" cssPath="./Basic/demo.css" />`

The variant with div element with id="result" useful to output something.

`<LiveDocSnippet maxWidth={"100%"} name="demo" htmlType="WithResult" />`

600 px width

`<LiveDocSnippet name="demoGapDifferentStyle" />`

**Code block**

`<CodeSnippetBlock labels={["TS", "Builder API (JSON Config)"]}>`

```ts showLineNumbers file=./2d-charts/annotations-api/line-annotation/Basic/demo.ts start=region_A_start end=region_A_end

```

```ts showLineNumbers file=./2d-charts/annotations-api/line-annotation/Basic/demo.ts start=region_B_start end=region_B_end

```

</CodeSnippetBlock>