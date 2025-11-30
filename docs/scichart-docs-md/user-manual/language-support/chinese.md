---
source: https://www.scichart.com/documentation/js/v4/user-manual/language-support/chinese
scraped_at: 2025-11-28T18:25:05.600512
---

# https://www.scichart.com/documentation/js/v4/user-manual/language-support/chinese

# SciChart 是否支持中文

SciChart JS 完全支持中文字符显示，因为它基于 Unicode 字符编码系统构建。作为一个现代的 JavaScript 图表库，SciChart 能够正确渲染和显示各种语言的字符，包括中文简体、繁体以及其他 Unicode 字符集。

## Unicode 支持原理

SciChart JS 利用浏览器的原生 Unicode 支持来处理多语言文本渲染。由于现代浏览器都遵循 Unicode 标准，SciChart 可以无缝地显示中文字符，无需额外的配置或插件。

## 2D 图表中的中文字符实现

以下代码示例展示了如何在 SciChart 2D 图表中使用中文标签和文本：

SciChartDefaults.useNativeText = false;

// 创建 SciChart 表面

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme(),

title: "每日温度变化趋势图",

titleStyle: {

fontSize: 30,

},

});

// 配置带中文标签的 X 轴

const xAxis = new NumericAxis(wasmContext, {

axisTitle: "时间（小时）",

growBy: new NumberRange(0.02, 0.02),

});

// 配置带中文标签的 Y 轴

const yAxis = new NumericAxis(wasmContext, {

axisTitle: "温度（摄氏度）",

growBy: new NumberRange(0.01, 0.1),

});

// 添加轴到图表

sciChartSurface.xAxes.add(xAxis);

sciChartSurface.yAxes.add(yAxis);

// 创建数据系列

const dataSeries = new XyDataSeries(wasmContext, {

dataSeriesName: "北京温度数据"

});

// 添加数据点

dataSeries.appendRange([0, 1, 2, 3, 4, 5], [20, 22, 25, 28, 30, 27]);

// 创建线系列

const lineSeries = new FastLineRenderableSeries(wasmContext, {

dataSeries,

stroke: "#FF6600"

});

// 添加系列到图表

sciChartSurface.renderableSeries.add(lineSeries);

## 文本注释和标签

SciChart 还支持在图表上添加中文文本注释：

// 创建中文文本注释

const textAnnotation = new TextAnnotation({

text: "最高温度点",

x1: 4,

y1: 30,

fontSize: 14,

textColor: "#FF0000"

});

// 添加注释到图表

sciChartSurface.annotations.add(textAnnotation);

## 3D 图表中的中文字符实现

要在 Scichart 3d 中使用中文字符，请参阅本文 - Native Text Api📘

## 最佳实践建议

-
字体选择：使用系统默认的中文字体，如 Microsoft YaHei（微软雅黑）或 SimHei（黑体）

-
编码设置：确保 HTML 页面使用 UTF-8 编码

-
字体大小：根据图表大小调整合适的字体大小，确保中文字符清晰可读

-
浏览器兼容性：测试不同浏览器中的中文显示效果

通过以上配置和代码示例，您可以在 SciChart JS 应用程序中完美地显示和使用中文字符，创建本地化的图表界面。