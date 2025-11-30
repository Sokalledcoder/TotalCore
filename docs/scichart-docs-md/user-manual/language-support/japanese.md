---
source: https://www.scichart.com/documentation/js/v4/user-manual/language-support/japanese
scraped_at: 2025-11-28T18:25:06.058521
---

# https://www.scichart.com/documentation/js/v4/user-manual/language-support/japanese

# SciChartは日本語をサポートしていますか？

はい、SciChartは日本語を完全にサポートしています。SciChartライブラリはUnicodeエンコーディングを使用しているため、日本語の文字（ひらがな、カタカナ、漢字）を含むすべてのUnicode文字セットを表示できます。

## Unicode文字サポート

SciChartは以下の理由で日本語文字を適切に処理できます：

-
完全なUnicodeサポート: UTF-8およびUTF-16エンコーディングに対応

-
国際化対応: 多言語テキストレンダリングエンジン内蔵

-
フォント互換性: システムフォントおよびWebフォントとの完全な互換性

## 2Dチャートでの日本語実装

基本的な日本語テキストの設定

SciChartDefaults.useNativeText = false;

// 2Dチャートで日本語タイトルとラベルを設定

const { wasmContext, sciChartSurface } = await SciChartSurface.create(divElementId, {

theme: new SciChartJsNavyTheme(),

title: "売上グラフ", // 日本語タイトル

titleStyle: {

fontSize: 30

}

});

// X軸の日本語ラベル

const xAxis = new NumericAxis(wasmContext, {

axisTitle: "月", // 日本語軸タイトル

growBy: new NumberRange(0.02, 0.02)

});

// Y軸の日本語ラベル

const yAxis = new NumericAxis(wasmContext, {

axisTitle: "売上（万円）", // 日本語軸タイトル

growBy: new NumberRange(0.01, 0.1)

});

sciChartSurface.xAxes.add(xAxis);

sciChartSurface.yAxes.add(yAxis);

const dataSeries = new XyDataSeries(wasmContext, {

dataSeriesName: "日本語シリーズ名"

});

dataSeries.appendRange([0, 1, 2, 3, 4, 5], [20, 22, 25, 28, 30, 27]);

const lineSeries = new FastLineRenderableSeries(wasmContext, {

dataSeries,

stroke: "#FF6600"

});

sciChartSurface.renderableSeries.add(lineSeries);

const textAnnotation = new TextAnnotation({

text: "重要なポイント：売上が急上昇", // 日本語注釈

x1: 4,

y1: 30,

fontSize: 14,

textColor: "#FF0000"

});

sciChartSurface.annotations.add(textAnnotation);

## 3Dチャートでの日本語実装

Scichart 3dで日本語文字を使用するには、この記事を参照してください。 - Native Text Api📘

## 重要な注意事項

-
エンコーディング: HTMLファイルとJavaScriptファイルはUTF-8エンコーディングで保存してください

-
ブラウザ互換性: すべての主要ブラウザで日本語表示がサポートされています

SciChartのUnicodeサポートにより、日本語を含む多言語チャートアプリケーションの開発が可能です。