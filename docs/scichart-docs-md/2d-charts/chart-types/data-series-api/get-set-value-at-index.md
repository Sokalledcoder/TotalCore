---
source: https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/data-series-api/get-set-value-at-index
scraped_at: 2025-11-28T18:24:25.186247
---

# https://www.scichart.com/documentation/js/v4/2d-charts/chart-types/data-series-api/get-set-value-at-index

# Accessing DataSeries xValues, yValues and count (size)

## How to access DataSeries xValues, yValues

You can access `xValues`

, `yValues`

on a `DataSeries`

by getting the internal WebAssembly native arrays via dataSeries.getNativeXValues()📘 and dataSeries.getNativeYValues()📘 functions.

These functions return the x & y values as `SCRTDoubleVector`

: a webassembly buffer type which stores underlying data as `Float64`

array in the wasm heap.

### Accessing DataSeries data via getNativeXValues() / getNativeYValues().get(i)

Accessing dataSeries xValues, yValues can be done via the `dataSeries.getNativeXValues()`

, `dataSeries.getNativeYValues()`

functions.
These return an `SCRTDoubleVector`

type which allows you to get a value at index via `dataSeries.getNativeXValues().get(i)`

.

Below find a simple example of accessing dataSeries x/y values point by point:

- Ts

`// Example: Accessing X, Y Values from DataSeries using getNativeXValues, getNativeYValues`

const xyDataSeries = new XyDataSeries(wasmContext);

xyDataSeries.appendRange([1, 2, 3], [10, 20, 30]);

// Get xValues from the dataSeries

const xValues = xyDataSeries.getNativeXValues();

// Get yValues from the dataSeries

const yValues = xyDataSeries.getNativeYValues();

for (let i = 0; i < xyDataSeries.count(); i++) {

// Note, this method of point by point access using .get(i) is slow

// faster methods exist below using the helper functions `vectorToArrayViewF64` and `vectorToArray`

console.log(`index=${i}, xy = ${xValues.get(i)}, ${yValues.get(i)}`);

}

// Will output to console

// index=0, xy=1, 10

// index=1, xy=2, 20

// index=2, xy=3, 30

point by point access to the DataSeries via this method is slow when you're dealing with millions of points. If you need to do bulk operations, it's better to read the entire vector out to JavaScript array first (see how)

### What is the SCRTDoubleVector type returned by getNativeXValues()?

dataSeries.getNativeXValues()📘 and dataSeries.getNativeYValues()📘 allow you to access the dataSeries xValues, yValues.

These both return type `SCRTDoubleVector`

. This is a type declared in webassembly which maps to a `Float64`

array on the wasm heap.

The example above shows how you can access data point by point using the `SCRTDoubleVector.get(i)`

function:

`export declare class SCRTDoubleVector {`

push_back(_dNewValue: number): void;

resize(_iNewSize: number, _dInitialValue: number): void;

resizeFast(_iNewSize: number): void;

reserve(_iCount: number): void;

clear(): void;

size(): number;

capacity(): number;

get(_iIndex: number): number; // Access value at index (i)

set(_iIndex: number, _dValue: number): void;

insertAt(_iIndex: number, _dValue: number): void;

removeAt(_iIndex: number): void;

removeRange(_iIndex: number, _iCount: number): void;

dataPtr(_iOffset: number): number; // returns a pointer to the wasm heap for this vector

delete(): void;

}

The above type declaration for `SCRTDoubleVector`

is included for information purposes only.

It's not recommended to use `SCRTDoubleVector.push_back`

, `resize`

, `clear`

, `insertAt`

, `removeAt`

or `delete`

.
Instead, use the `append`

`update`

`insert`

`remove`

`clear`

and `delete`

functions directly on XyDataSeries📘 and related dataSeries types,
as this will manage internal state as well as memory.

## Accessing DataSeries Count (length) and Capacity

The length, size or count or a `dataSeries`

can be accessed via the dataSeries.count()📘 function. Here is an example:

- TS

`// Example: get count (length, size) of dataSeries`

const count = 1_000_000;

const xValues: number[] = Array.from(Array(count).keys());

const yValues: number[] = Array.from(Array(count).keys());

const series = new XyDataSeries(wasmContext, {

xValues,

yValues

});

console.log(`dataSeries count: ${series.count()}`);

// Outputs: "dataSeries count: 1,000,000"

The capacity of a `dataSeries`

can be get/set via the dataSeries.capacity📘 property. This sets the size of the underlying memory buffers allowing you to pre-allocate memory in demanding applications.

For example, if you plan to call `dataSeries.append()`

or `.appendRange()`

many times up to a capacity of 1,000,000, you can pre-allocate the memory now by setting the `capacity`

:

- TS

`// Example: setting the capacity of a dataseries to preallocate memory`

const series = new XyDataSeries(wasmContext);

series.capacity = 1000000; // pre-allocates 1,000,000 values for X,Y

console.log(`dataSeries count: ${series.count()}`);

console.log(`dataSeries capacity: ${series.capacity}`);

// Outputs: "dataSeries count: 0"

// "dataSeries capacity: 1,000,000"

## Reading DataSeries xValues, yValues as a Float64Array View

As the `dataSeries.getNativeXValues()`

, `dataSeries.getNativeYValues()`

functions return the xValues and yValues as webassembly Float64 memory buffers (type `SCRTDoubleVector`

), you can't operate on these like normal JavaScript arrays.

However, it is possible to create a view on the dataSeries xValues, yValues as a JS array (`Float64Array`

) for further manipulation, read-back of dataSeries values or otherwise.

The following helper function `vectorToArrayViewF64()`

(added in version 4.0.873) will convert a `SCRTDoubleVector`

(Float64 webassembly memory buffer)
into a `Float64Array`

(JavaScript typed 64-bit array). This operation is super-fast and will allow you to read back values from a `dataSeries`

into JavaScript arrays with little overhead.

Here's an example of how to use it to get a JavaScript array view of `dataSeries`

x,y values:

- TS

`// vectorToArrayViewF64() (returns Float64Array) allows access to dataSeries xValues, yValues`

// by creating a view onto webassembly memory

const count = 1_000_000;

const xValues: number[] = Array.from(Array(count).keys());

const yValues: number[] = Array.from(Array(count).keys());

// Create an XyDataSeries with 1,000,000 xValues, yValues

const dataSeries = new XyDataSeries(wasmContext, {

xValues,

yValues

});

// Create a view into the data (maps dataSeries xValues, yValues onto a JavaScript Float64Array)

const startGet = performance.now();

const f64XValues: Float64Array = vectorToArrayViewF64(dataSeries.getNativeXValues(), wasmContext);

const f64YValues: Float64Array = vectorToArrayViewF64(dataSeries.getNativeYValues(), wasmContext);

console.log(`vectorToArrayViewF64 get: ${(performance.now() - startGet).toFixed(3)}ms`);

// Operate on these as normal JS arrays

const startIterate = performance.now();

// Check values

let test = 0;

for (let i = 0; i < count; i++) {

test += f64XValues[i];

test += f64YValues[i];

}

console.log(`vectorToArrayViewF64 iterate: ${(performance.now() - startIterate).toFixed(3)}ms`);

// Output to console:

// vectorToArrayViewF64 get: 0.072ms

// vectorToArrayViewF64 iterate: 2.747ms

Note, the returned `Float64Array`

is a **view** onto the wasm memory, **not a copy**. Updating this `Float64Array`

view will update the dataSeries data and vice-versa.

This method of creating a `Float64Array`

view onto the webassembly data is **much faster** than `getNativeXValues().get(i)`

`getNativeYValues().get(i)`

and can be used to read back dataSeries `xValues`

`yValues`

into JavaScript efficiently.

Since the `Float64Array`

is a **view** onto the webassembly memory, note that you should re-map this view every time you use it. If the underlying dataSeries size is changed, the wasm memory may be moved (`.dataPtr(0)`

will change), then you run
the risk of getting strange errors like `TypeError: Cannot perform %TypedArray%.prototype.set on a detached ArrayBuffer`

.

It's best to use this operation to **read/write** values from a dataSeries where you need fast access, but don't keep the `Float64Array`

view instance for longer than needed (use once for an operation then discard). For passing JS array copies around your app, use `vectorToArray()`

which provides a safer deep-copy.

For write operations, it's recommended to use the `append`

`update`

`insert`

`remove`

`clear`

and `delete`

functions directly on XyDataSeries📘 and related dataSeries types
unless you absolutely know what you're doing!

## Copying DataSeries xValues, yValues to JavaScript number[] array

If you want to go a step further, you can convert a `Float64Array`

to a JavaScript array (e.g. `number[]`

) and perform a deep-copy of dataSeries data into JavaScript Arrays.
This operation involves a copy and is slower, but you can also be assured that the underlying data won't change.
It's also the most compatible with JavaScript frameworks and other parts of your code.

The `vectorToArray()`

helper function (added in version 4.0.873) can be used to perform a deep-copy of dataSeries data (xValues, yValues).

- TS

`// vectorToArray() (returns number[]) performs a deep-copy of a scichart webassembly vector`

// allowing for safer read-only access to dataseries data

const count = 1_000_000;

const xValues = Array.from(Array(count).keys());

const yValues = Array.from(Array(count).keys());

// Create an XyDataSeries with 1,000,000 xValues, yValues

const dataSeries = new XyDataSeries(wasmContext, {

xValues,

yValues

});

const startGet = performance.now();

// vectorToArray creates first a Float64Array view onto dataSeries xValues, yValues

// then uses Array.from(typedArrayView) to copy to JS Array

const jsXValues: number[] = vectorToArray(dataSeries.getNativeXValues(), wasmContext);

const jsYValues: number[] = vectorToArray(dataSeries.getNativeYValues(), wasmContext);

console.log(`vectorToArray deepCopy: ${(performance.now() - startGet).toFixed(3)}ms`);

// Operate on these as normal JS arrays

const startIterate = performance.now();

// Check values

let test = 0;

for (let i = 0; i < count; i++) {

test += jsXValues[i];

test += jsYValues[i];

}

console.log(`vectorToArray iterate: ${(performance.now() - startIterate).toFixed(3)}ms`);

// Output to console:

// vectorToArray deepCopy: 62ms

// vectorToArray iterate: 2ms

This operation involves a deep copy of dataSeries data and is safer, but will introduce some extra latency depending on the size of the dataSeries data.

## Fast copy one XyDataSeries to another

Using the utility function `vectorToArrayViewF64()`

we discussed above, it's possible to fast copy an entire `XyDataSeries`

to another.
Use this in the case where you want to duplicate (copy) data from one DataSeries to another.

- Given a source
`dataSeries`

with`count()`

- Create a destination
`dataSeries`

- set
`destination.capacity = source.count()`

**important**to avoid detached ArrayBuffer errors - Use the
`vectorToArrayViewF64()`

helper function declared above to get`Float64Array`

views into the source xValues, yValues - call
`destination.appendRange()`

using these array views

- TS

`const count = 1_000_000;`

const xValues: number[] = Array.from(Array(count).keys());

const yValues: number[] = Array.from(Array(count).keys());

const startCreate = performance.now();

// Create a src series and fill with values

const seriesSrc = new XyDataSeries(wasmContext, {

xValues,

yValues

});

console.log(`time to fill a dataSeries 1M points: ${(performance.now() - startCreate).toFixed(3)}ms`);

const startCopy = performance.now();

// Create a dest series and ensure the capacity (memory size) before calling

// vectorToArrayView. This will avoid potential "Cannot perform %TypedArray%.prototype.set on a detached ArrayBuffer"

// error as any resizes of memory might move other memory locations

const seriesDest = new XyDataSeries(wasmContext);

seriesDest.capacity = seriesSrc.count();

// Fast copy xValues, yValues from one dataSeries to another

console.time("Time to deep copy an entire dataSeries");

seriesDest.appendRange(

vectorToArrayViewF64(seriesSrc.getNativeXValues(), wasmContext),

vectorToArrayViewF64(seriesSrc.getNativeYValues(), wasmContext)

);

console.log(`time to deep copy a dataSeries 1M points: ${(performance.now() - startCopy).toFixed(3)}ms`);

// Console output

// Time to fill a dataSeries 1M points: 11.762ms

// Time to deep copy a dataSeries 1M points: 13.861ms

The time to deep copy `dataSeries`

data from one series to another using `vectorToArrayViewF64()`

is comparable to the time to create the `dataSeries`

in the first place.

This method can be used if you need to create copies (clones) of dataSeries in your js application.

## Performance Table of different dataSeries readback methods

Here's a performance table of the various methods to get, set, read, copy dataSeries xValues yValues into JS Arrays. Performance will vary from system to system, but the following can be used as a guide to assess the impact of using different

| Method | Time (ms) | Note |
|---|---|---|
Read 1M points with `getNativeXValues().get(i)` | 400ms | point-by-point iteration is slow and should be avoided |
Read 1M points with `vectorToArray()` | 62ms | performs a deep-copy of xValues, yValues into number[] array |
Read 1M points with `vectorToArrayViewF64()` | 4ms | returns an unsafe array view. Used for v. fast read/write access with caveats |
| create new 1M point dataSeries | 11ms | creation of a new dataSeries with pre-allocated arrays |
deep copy 1M point dataSeries using `vectorToArrayViewF64()` | 13ms | fast deep-copy of dataSeries data to another dataSeries |

## Examples of Dynamic Updates

There are a number of worked examples of how to apply dynamic updates to the chart over at the page DataSeries Realtime Updates.