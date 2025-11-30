Right, so I want to create some form of a pipeline. I already have it for Pinescript, but the general idea is research strategies, create them in Python, and then being able to backtest them fast. Like the whole pipeline itself should be frictionless. So research my knowledge base and the internet and everything, find trading strategies based on whatever criteria I ask, then quickly implement that strategy into Python, and then test the strategy works, actually it's functioning, and when that's established, we do a backtest based on whatever data we have. Yeah, so that's the workflow. I want it in Python. I have means to get data and stuff, so that's not part of the research I want you to do. It's mostly to search if there's an existing framework we can use, what's the common way of doing these things. Backtesting needs to be robust, like able to do several, not just test the trades, like being able to do tweak parameters on its own, et cetera. I want a more complex backtesting system than what you get in TradingView, for example. All right, do a thorough search, and we'll take it from there.

Got you — you basically want a *research → Python strategy → “is this even doing what I think?” → heavy-duty backtest + auto tuning* pipeline, not a toy TradingView backtester.

Here’s what the ecosystem looks like and what stack I’d recommend building on top of.

---

## 1\. The pipeline you’re describing (in Python terms)

Ignoring data ingestion (you said you’ve got that):

1. **Research layer**
	- You (and me) brainstorm strategies / rules / ideas.
	- These get written as **pure functions** on OHLCV / factor data:  
		`signals = strategy_fn(data, params)` → entry/exit arrays, position sizing rules, etc.
2. **Backtest engine**
	- Takes `prices + signals + execution assumptions` → trades, PnL, equity curve, metrics.
	- Needs to support:
		- Multi-asset portfolios
		- Realistic costs, slippage, position sizing
		- Multiple parameter sets in one run
		- Walk-forward / multiple time periods
3. **Optimization / sweeps**
	- Something that can:
		- Run grid / random / Bayesian search over params
		- Call the backtester as an objective function
		- Return best params + diagnostics
4. **Reporting / sanity checks**
	- Tear sheets, drawdowns, trade distributions, per-symbol metrics, etc.
	- Check that things aren’t obviously overfit.

The core question is: *what engine(s) give us the least friction for steps 2–4?*

---

## 2\. Main Python backtesting frameworks (what they’re good/bad at)

### 2.1 VectorBT

**What it is**

VectorBT is a quant/backtesting library built entirely on pandas/NumPy and accelerated with Numba; it represents strategies as big arrays and can test “many thousands of strategies in seconds.” [VectorBT](https://vectorbt.dev/)

Key bits:

- Fully vectorized + Numba-compiled engine.
- Multi-asset, multi-parameter, multi-period backtests in one shot using multi-index columns. [VectorBT](https://vectorbt.dev/)
- Has a `Portfolio` module that builds equity curves from signal arrays (`from_signals`, `from_orders`, etc.). [VectorBT](https://vectorbt.dev/)
- Can split time into many sub-periods and backtest them all at once (`range_split`) – basically built-in walk-forward grid. [VectorBT](https://vectorbt.dev/)

**Pros**

- **Stupid fast**: it’s commonly cited as one of the fastest Python backtesting libs, especially when scanning thousands of parameter combinations. [Marketcalls +2 Composer +2](https://www.marketcalls.in/python/mastering-vectorbt-backtesting-and-optimization-part-1-python-tutorial.html?utm_source=chatgpt.com)
- Perfect for your “tweak params on its own” requirement: you pass arrays of parameter values, and it broadcasts them into a joint backtest. [VectorBT](https://vectorbt.dev/)
- Native multi-asset & multi-parameter dimensions.

**Cons**

- Learning curve is higher than TradingView-style OOP engines; you think more in terms of arrays than “on\_bar()”.
- Free version is “maintained but not the main focus”; new features are largely going into VectorBT PRO. [greyhoundanalytics.com](https://greyhoundanalytics.com/blog/vectorbt-vs-backtrader/)

**Fit for you**

- Very strong candidate for the *core backtest + param sweep engine* in your pipeline.

### 2.2 PyBroker

**What it is**

PyBroker is a newer framework focused on algorithmic trading with ML, with a fast Numpy+Numba engine and multi-instrument support. [PyBroker](https://www.pybroker.com/?utm_source=chatgpt.com)

Key features:

- Super-fast engine (NumPy + Numba) similar spirit to vectorbt.
- Multi-instrument strategies, walk-forward analysis (built-in), and bootstrapped performance metrics. [PyBroker](https://www.pybroker.com/?utm_source=chatgpt.com)
- Designed to integrate “trading rules + ML models” and run them over many symbols. [PyBroker](https://www.pybroker.com/?utm_source=chatgpt.com)

**Pros**

- More “batteries included” around ML and walk-forward testing.
- Built-in randomized bootstrapping for more robust metrics. [PyBroker](https://www.pybroker.com/?utm_source=chatgpt.com)

**Cons**

- Newer / smaller ecosystem compared to Backtrader / vectorbt.
- Less community content/tutorials than the older libs.

**Fit for you**

- Really nice if you expect to go heavy into ML strategies and want walk-forward + robust metrics without wiring them yourself.

### 2.3 Backtesting.py

Backtesting.py is a lightweight, user-friendly framework built on pandas/NumPy with a simple `Strategy` class API. [kernc.github.io](https://kernc.github.io/backtesting.py/)

- Supports both vectorized and event-based styles and has a **built-in optimizer** (SAMBO) that generates heatmaps over many parameter combos. [kernc.github.io +1](https://kernc.github.io/backtesting.py/)
- Plays nicely with TA-Lib, pandas-ta, etc. [kernc.github.io](https://kernc.github.io/backtesting.py/)

**Pros**

- Very quick to prototype, small API surface.
- One-liner optimization over parameters (great for “does this thing even work?” tests). [kernc.github.io](https://kernc.github.io/backtesting.py/)

**Cons**

- Official docs and community note: currently single-asset; multi-asset support is limited. [Interactive Brokers](https://www.interactivebrokers.com/campus/ibkr-quant-news/backtesting-py-an-introductory-guide-to-backtesting-with-python/?utm_source=chatgpt.com)
- Less suited to complex portfolio-level stuff than vectorbt/QSTrader.

**Fit for you**

- Ideal as a **sanity-check / unit-test engine** for a new strategy where you want TradingView-like OOP semantics but more control.
- For the full multi-asset + large parameter grid dream, vectorbt/PyBroker win.

### 2.4 Backtrader

Backtrader is the classic heavy-duty Python engine: event-driven, feature-rich, supports backtesting **and live trading**. [backtrader.com +2 algotrading101.com +2](https://www.backtrader.com/)

- Has deep support for multiple data feeds, commission schemes, slippage, multi-timeframe data, analyzers, and even IB/Oanda live trading. [backtrader.com +1](https://www.backtrader.com/)

**Pros**

- Very mature and widely used; tons of docs, blog posts, and examples. [backtrader.com +1](https://www.backtrader.com/)
- Feels familiar if you’re used to “strategy class with on\_bar logic” from platforms like Tradestation / older-school quant platforms. [greyhoundanalytics.com](https://greyhoundanalytics.com/blog/vectorbt-vs-backtrader/)

**Cons**

- Slower when you want to run *huge* parameter grids. [greyhoundanalytics.com](https://greyhoundanalytics.com/blog/vectorbt-vs-backtrader/)
- Core project is basically in maintenance; community forks exist, but not lots of new features. [greyhoundanalytics.com](https://greyhoundanalytics.com/blog/vectorbt-vs-backtrader/)

**Fit for you**

- Amazing if you want a *production-grade event-driven engine*, or eventually live trading.
- For “brute-force thousands of parameter combos”, it’s not as comfy as vectorbt/PyBroker.

### 2.5 QSTrader

QSTrader is explicitly focused on **institutional-style portfolio backtesting** (long/short equities & ETFs, daily or lower frequency). [quantstart.com +2 GitHub +2](https://www.quantstart.com/qstrader/introduction/)

- Separates alpha models, portfolio construction, broker/accounting, and risk reporting. [quantstart.com](https://www.quantstart.com/qstrader/introduction/)
- Strong on portfolio-level mechanics, cashflows, and rebalancing schedules.

**Pros**

- Serious portfolio construction & risk management framework out of the box. [quantstart.com](https://www.quantstart.com/qstrader/introduction/)

**Cons**

- Less geared toward intraday / HFT / very high-frequency parameters sweeps.
- More structure (modules, schedules) than you might want for ultra-fast iteration.

**Fit for you**

- Great reference for **architecture** if you want your pipeline to look like a real quant shop.
- Might be overkill for your first iteration unless you’re specifically doing daily/monthly cross-asset portfolios.

### 2.6 Freqtrade (crypto-focused, but useful reference)

Freqtrade is a crypto bot framework with backtesting, **Hyperopt-based parameter optimization**, and live trading. [botcrypto | le blog +4 freqtrade.io +4 freqtrade.io +4](https://www.freqtrade.io/en/stable/backtesting/?utm_source=chatgpt.com)

- You define strategies, then run backtests + Hyperopt to automatically tune stop-loss, ROI tables, indicator params, etc. [freqtrade.io +1](https://www.freqtrade.io/en/stable/hyperopt/?utm_source=chatgpt.com)

**Fit for you**

- Might be overkill as your main engine, but it’s a *great design template* for how to integrate a backtester with an automatic hyperparameter optimizer.

---

## 3\. Hyperparameter optimization layer

Regardless of which backtester you choose, you’ll want an optimization framework on top.

### 3.1 Optuna (top pick)

Optuna is a general-purpose hyperparameter optimization framework (Bayesian/TPE, pruning, multi-objective, distributed, etc.). [Wikipedia +4 Optuna +4 optuna.readthedocs.io +4](https://optuna.org/?utm_source=chatgpt.com)

- You define an `objective(trial)` function that:
	- samples parameter values (`trial.suggest_float/int/...`)
	- runs a backtest with those params
	- returns Sharpe, CAGR, whatever metric you want to maximize/minimize.

That’s a plug-and-play way to bolt **smart** search (not just brute-force grids) onto vectorbt, PyBroker, Backtrader, etc.

### 3.2 Hyperopt / others

- **Hyperopt**: widely used in trading (Freqtrade uses it as their optimizer). [freqtrade.io +1](https://www.freqtrade.io/en/stable/hyperopt/?utm_source=chatgpt.com)
- Others like Mango, Nevergrad, etc. exist, but Optuna is currently one of the most actively developed and well-documented. [arXiv +1](https://arxiv.org/abs/2005.11394?utm_source=chatgpt.com)

Given your use case, I’d just standardize on **Optuna** and treat the backtester as a black box the optimizer calls.

---

## 4\. Recommended stack for your pipeline

If we optimize for **speed**, **frictionless iteration**, and **multi-asset + param sweeps**, I’d suggest this:

### Core choices

- **Primary engine:**
	- **VectorBT** for large-scale parameter sweeps and multi-asset portfolios. [VectorBT +2 greyhoundanalytics.com +2](https://vectorbt.dev/)
- **Secondary / “unit test” engine:**
	- **Backtesting.py** for quick, readable “does this logic behave like my PineScript idea?” tests. [kernc.github.io +1](https://kernc.github.io/backtesting.py/)
- **Optional ML-heavy engine:**
	- **PyBroker** if/when you want built-in walk-forward analysis and ML model integration while still being vectorized. [PyBroker](https://www.pybroker.com/?utm_source=chatgpt.com)
- **Optimizer:**
	- Optuna on top of whichever engine we use. [Optuna +1](https://optuna.org/?utm_source=chatgpt.com)
- **Metrics / reporting:**
	- VectorBT’s performance metrics (has returns metrics and integration with QuantStats-style adapters). [VectorBT](https://vectorbt.dev/)
	- Or external libs like `empyrical` / `quantstats` for Sharpe/Sortino, drawdowns, etc. (common practice; general background).

### How this would feel in practice

For each new strategy:

1. **Research step**  
	You describe the idea (or PineScript version), I help convert it into a Python `signal_fn(data, params)`.
2. **Quick correctness check (Backtesting.py)**
	- Plug `signal_fn` into a tiny wrapper Strategy in Backtesting.py.
	- Verify:
		- Entry/exit timing matches expectations on a small dataset.
		- Basic stats look sane.
	- Cheap way to catch logical bugs before heavy sweeps.
3. **High-throughput backtesting (VectorBT / PyBroker)**
	- Express the same logic in vectorbt-style:
		- indicators as vectors
		- entries/exits as boolean arrays
	- Pass **arrays of parameter values** to run a huge grid in one go (e.g. all MA fast/slow combos across 50 tickers × several time ranges). [VectorBT +1](https://vectorbt.dev/)
4. **Automatic hyperparameter optimization (Optuna)**
	- Define an objective that:
		- Runs either a vectorbt or PyBroker backtest internally
		- Returns a composite score (e.g. Sharpe minus penalty for max DD).
	- Let Optuna explore the space and log trials + best params. [Optuna +2 optuna.readthedocs.io +2](https://optuna.org/?utm_source=chatgpt.com)
5. **Robustness checks**
	- Use vectorbt’s time-splitting / multi-period backtesting to see how parameters perform across different regimes. [VectorBT +1](https://vectorbt.dev/)
	- Optionally do more advanced stuff like combinatorial cross-validation (CCV) for parameters, which is specifically recommended as a robust anti-overfitting approach in trading backtests. [Medium](https://medium.com/%40alexdemachev/finding-optimal-hyperparameters-for-a-trading-strategy-with-combinatorial-cross-validation-3fd241d613fc?utm_source=chatgpt.com)

---

## 5\. How this beats TradingView-style backtesting

Compared to TradingView’s built-in backtester, this stack gives you:

- **Full control over assumptions**: custom slippage, commissions, corporate actions, multi-asset portfolios, rebalancing rules, etc. (especially via vectorbt or QSTrader-style architecture). [VectorBT +1](https://vectorbt.dev/)
- **Massive param sweeps**: thousands of parameter combinations in one shot instead of manually adjusting PineScript inputs. [VectorBT +2 greyhoundanalytics.com +2](https://vectorbt.dev/)
- **Proper optimization**: Optuna/Hyperopt rather than “change inputs by hand and eyeball equity curves.” [Optuna +2 freqtrade.io +2](https://optuna.org/?utm_source=chatgpt.com)
- **Portfolio/risk focus**: easy to build portfolio-level strategies, not just one-chart, single-symbol toys. [quantstart.com +2 PyBroker +2](https://www.quantstart.com/qstrader/introduction/)

---

## 6\. Concrete next move

To keep this practical and not just library tourism, I’d propose:

1. **Standardize on:**
	- vectorbt (+ possibly PyBroker) as the “big gun” engine,
	- Backtesting.py as the quick sanity checker,
	- Optuna as the optimizer.
2. **Next step together:**  
	Design a **minimal common interface** like:
	- `def generate_signals(data_df, params) -> (entries, exits, size)`
	- Hook that into Backtesting.py and vectorbt in two thin adapters.

From there, we can start with one of your existing PineScript strategies, port it into this interface in Python, and wire it through this stack end-to-end (including a basic Optuna optimization loop). Once that skeleton is in place, dropping in new strategies becomes almost mechanical.

Branched from [Python strategy pipeline](https://chatgpt.com/c/69205aca-4510-832b-94dd-95ac8d18dea0)

All right. I don't really want VectorDVD due to the pro version support being mostly there. So, I'm thinking of having as a primary engine backtesting.py with PyBroker as my machine learning heavy engine. And then having Optuna as the open manager, I don't see any other option to be honest. And as for the metrics and reporting, I'm not really sure. Isn't PyBroker backtesting.py already offering these things? I'm not sure why do I need it. Anyway, let's dive deeper into those and see how we can combine them. There is an existing backend and frontend that has some other features. So, we're going to put things there and integrate it. So, let's keep it generalized. Like don't consider things like if we're starting from scratch or stuff, right? Like we already have our databases, etc. I'm just more considering deeper research to see if there's anything else I need to consider. Anyway, think hard, be thorough.

Nice, that stack makes a lot of sense:

- **Primary engine:**`backtesting.py`
- **ML-heavy / multi-asset / walkforward engine:**`PyBroker`
- **Optimizer:**`Optuna`
- **Existing infra:** DB + backend + frontend already there

Let’s zoom in on what each piece actually gives you, what’s missing, and how to glue them together without painting yourself into a corner.

---

## 1\. What backtesting.py really gives you

### 1.1 Features & metrics

`Backtest.run()` in backtesting.py returns a `Stats` object that already includes a *lot* of metrics out of the box: CAGR, annualized vol, Sharpe, Sortino, Calmar, max drawdown, win rate, profit factor, SQN, Kelly, trade stats, etc. [kernc.github.io +1](https://kernc.github.io/backtesting.py/)

So for a single-instrument, single-run sanity check, you honestly don’t need any extra metrics library.

You also have:

- **Order model:** market/limit/stop, SL/TP, fraction-of-equity sizing, etc. [kernc.github.io +1](https://kernc.github.io/backtesting.py/doc/backtesting/backtesting.html)
- **Strategy types:** classic `Strategy`, `SignalStrategy` (vector-ish entry/exit signals), `TrailingStrategy` with automatic ATR-based trailing stops. [algotrading101.com](https://algotrading101.com/learn/backtesting-py-guide/)

### 1.2 Built-in grid search

`Backtest.optimize` can already do parameter optimization over grids and rank by any metric, with:

- Default ranking metric = **SQN** (System Quality Number). [Medium](https://blog.poloxue.com/strategy-parameter-optimization-with-backtesting-py-3fb2f024c0b9)
- `maximize` argument lets you target any built-in metric, e.g. `"Sharpe Ratio"` or `"Max. Drawdown [%]"`. [Medium +1](https://blog.poloxue.com/strategy-parameter-optimization-with-backtesting-py-3fb2f024c0b9)
- You can supply **your own objective**: a function that maps the stats dict to a scalar. [Medium](https://blog.poloxue.com/strategy-parameter-optimization-with-backtesting-py-3fb2f024c0b9)
- Option to get a heatmap of results (`return_heatmap=True` + `plot_heatmaps`) to see parameter surfaces. [Medium](https://blog.poloxue.com/strategy-parameter-optimization-with-backtesting-py-3fb2f024c0b9)

So backtesting.py already covers “small/medium parameter grid + metric ranking + visualization” quite nicely.

### 1.3 Limitations you should keep in mind

This matters for architecture decisions:

- **Mostly single-instrument per Backtest instance.** You *can* hack pairs/relative strategies by feeding custom dataframes, but it’s not a natural portfolio/multi-asset engine. [algotrading101.com](https://algotrading101.com/learn/backtesting-py-guide/)
- Execution is **“on next bar”**, so SL/TP and entries are approximated at bar-to-bar level; for granular intraday behavior or tick-level microstructure you’ll hit limitations. [algotrading101.com +1](https://algotrading101.com/learn/backtesting-py-guide/)
- Project is stable but not super fast-moving; some articles point out dev has slowed and there’s no live-trading support. [Medium](https://medium.com/%40timemoneycode/mastering-python-backtesting-for-trading-strategies-1f7df773fdf5?utm_source=chatgpt.com)

Given all that, using it as:

> “Readable, simple primary engine + quick correctness + smaller grid optimization”

is perfectly aligned with what it’s good at.

---

## 2\. What PyBroker brings to the table

PyBroker is essentially your **“serious research / ML / portfolio” engine**.

### 2.1 Engine + multi-asset

Key design bits:

- Fast backtesting engine built on NumPy + Numba with multi-instrument support. [Reddit +3 PyBroker +3 PyBroker +3](https://www.pybroker.com/?utm_source=chatgpt.com)
- You register:
	- **rules/models** (`pybroker.model`, execution functions)
	- a `Strategy` with tickers, timeframe, and execution callbacks
	- then run `backtest()` or `walkforward()`.

Example in docs: run walkforward over AAPL/MSFT 1m data in 5 windows. [PyBroker +1](https://www.pybroker.com/)

### 2.2 Walkforward + bootstrapped metrics

This is the big one:

- **Walkforward analysis**: splits history into multiple train/test windows and simulates retraining + forward trading. That’s baked into `strategy.walkforward(...)`. [PyPI +3 PyBroker +3 Medium +3](https://www.pybroker.com/en/latest/notebooks/6.%20Training%20a%20Model.html?utm_source=chatgpt.com)
- **Bootstrap metrics**: it lets you compute performance metrics using resampling of returns, and gives you **confidence intervals** for stuff like Sharpe and Profit Factor. [PyBroker +2 PyBroker +2](https://www.pybroker.com/en/latest/notebooks/3.%20Evaluating%20with%20Bootstrap%20Metrics.html)

Their notebook shows metrics like trade count, total PnL, max drawdown, Sharpe, Sortino, profit factor, ulcer index, etc., plus bootstrapped CIs for Sharpe and profit factor. [PyBroker +1](https://www.pybroker.com/en/latest/notebooks/3.%20Evaluating%20with%20Bootstrap%20Metrics.html)

So yes: PyBroker already does “fancier stats” than you usually get out of the box, including robustness checks.

### 2.3 ML-centric design

PyBroker is intentionally built around ML:

- You define a `train_fn` that gets train/test data per symbol and returns a trained model + columns to use. [PyBroker +2 PyBroker +2](https://www.pybroker.com/en/latest/notebooks/6.%20Training%20a%20Model.html)
- You register that with `pybroker.model(...)`.
- During walkforward, it automatically retrains per window and uses model predictions in your execution callback.

So your heavy ML research stays here, not in backtesting.py land.

---

## 3\. Do you need extra metrics/reporting libs?

Short answer: **No, strictly you don’t “need” them**. Between:

- `Stats` from backtesting.py with a big table of performance and trade-level stats [kernc.github.io +1](https://kernc.github.io/backtesting.py/)
- PyBroker’s metrics + bootstrapping + walkforward results [PyBroker +4 PyBroker +4 PyPI +4](https://www.pybroker.com/en/latest/notebooks/3.%20Evaluating%20with%20Bootstrap%20Metrics.html)

you can make solid decisions.

But there *are* reasons to have a separate **metrics/analytics layer**, not tied to either engine:

### 3.1 Reasons to keep metrics as a separate layer

1. **Unification across engines**  
	You want to be able to compare:
	- Strategy A backtested in backtesting.py,
	- Strategy B in PyBroker,
	- Strategy C maybe later in some other engine,
	all in one dashboard. Having metrics logic separate (e.g. something that just takes a returns series + trades table) solves that.
2. **Richer analytics than each engine exposes**  
	Backtesting.py and PyBroker give a lot, but dedicated analytics libs like **QuantStats** add:
	- Benchmark comparison (alpha, beta, correlation, R²). [Medium](https://medium.com/%40elvis.thierry/analyze-risk-and-performance-with-quantstats-a-comprehensive-framework-for-portfolio-evaluation-633fd7e86693)
	- Rolling Sharpe/Sortino, monthly return heatmaps, detailed drawdown reports. [quantscience.io +3 GitHub +3 Medium +3](https://github.com/ranaroussi/quantstats)
	- One-shot tear sheets as HTML, which you can either embed in your UI or just pillage for ideas. [GitHub +2 slingacademy.com +2](https://github.com/ranaroussi/quantstats)
3. **Frontend flexibility**  
	You already have a frontend. You probably don’t want to just iframe whatever the library spits out. Better to:
	- Treat engines as **“returns/trades generators”**
	- Treat analytics as **“metrics computation”**
	- Treat your frontend as **“view layer only”**.
4. **Future-proofing**  
	If backtesting.py or PyBroker change their metrics APIs, or you add a custom engine, your UI and databases stay stable as long as your metrics layer contract stays stable.

### 3.2 Practical compromise

You don’t need to go full quantstats cult:

- Use **engine-native metrics** (backtesting.py’s `Stats`, PyBroker’s `result.metrics` / `result.bootstrap`) internally for quick checks. [kernc.github.io +1](https://kernc.github.io/backtesting.py/)
- Have a **thin analytics layer** that:
	- Accepts: `returns_series`, `benchmark_returns`, `trades_table`, maybe `cash_flow`.
	- Computes extra metrics via QuantStats or your own functions.
	- Normalizes engine-specific names (e.g. both engines map into your canonical “Sharpe”, “MaxDrawdownPct”, etc).

QuantStats is just a very convenient implementation detail there. It gives you stats, plots, and reports modules that can be called programmatically. [GitHub +2 Medium +2](https://github.com/ranaroussi/quantstats)

---

## 4\. How to combine backtesting.py + PyBroker + Optuna

Given you’ve already got DB + backend + frontend, I’d think of the three libs as **plug-in engines behind your own interface**.

### 4.1 Define your own “engine adapter” interface

Example of your internal contract (pseudo-code, not fussed about exact types):

Then you implement:

- `BacktestingPyAdapter(EngineAdapter)`
- `PyBrokerAdapter(EngineAdapter)`

Each adapter:

- Knows how to pull data from your DB and format it into the shape the library expects.
- Runs the backtest via that library.
- Converts the output (`Stats` or PyBroker `result`) into your `BacktestResult`.

Your frontend & Optuna only talk to `EngineAdapter` / `BacktestResult`, not to the libraries directly.

### 4.2 Using backtesting.py inside the adapter

Rough shape:

The point is: you strip it down to a generic format early.

### 4.3 Using PyBroker inside the adapter

Similar pattern:

Again, you normalize ASAP.

### 4.4 Optuna integration on top

Optuna doesn’t care what engine you use; it just cares about the objective function. That’s its whole thing – “framework agnostic.” [ijsred.com +4 Optuna +4 ogsiji.hashnode.dev +4](https://optuna.org/?utm_source=chatgpt.com)

So you can define:

Then:

- For quick idea checking, you might still use `Backtest.optimize(...)` with its built-in SQN + heatmap features. [Medium +1](https://blog.poloxue.com/strategy-parameter-optimization-with-backtesting-py-3fb2f024c0b9)
- For **serious** search (especially with ML + walkforward + cross-validation), you standardize on Optuna + your adapters. There’s even a Substack post explicitly pairing Optuna + PyBroker for trading strategy hyperparameter optimization. [piotrpomorski.substack.com +2 Medium +2](https://piotrpomorski.substack.com/p/hyperparameter-optimisation-with?utm_source=chatgpt.com)

---

## 5\. Extra things worth thinking about (since you already have infra)

Because you’re not starting from scratch, these are the things that tend to bite later:

### 5.1 Data contracts, not just data

- Enforce a **schema** for what a “dataset” is to a backtest:
	- timezone normalized,
	- no forward-filled future info,
	- fields: at least `open/high/low/close/volume`, maybe extra factor columns.
- PyBroker supports creating custom data sources; that’s how you’d hook it cleanly to your DB instead of letting it pull from Alpaca/Yahoo. [PyBroker +1](https://www.pybroker.com/)

### 5.2 Portfolio & multi-asset behavior

- For **single-symbol intraday logic**, backtesting.py is fine.
- For **multi-symbol ranking / rotational / portfolio rebalancing**, PyBroker is the better fit (it has docs for ranking & position sizing, rebalancing, rotational trading). [PyBroker +3 PyBroker +3 PyBroker +3](https://www.pybroker.com/)
- Make sure your interface allows “strategy acts on N symbols with shared capital” even if backtesting.py implementation is more limited there.

### 5.3 Overfitting protection

Tools you already get:

- Backtesting.py heatmaps and custom `maximize` functions let you penalize weird parameter regions (#trades too small, low exposure, etc.). [Medium +1](https://blog.poloxue.com/strategy-parameter-optimization-with-backtesting-py-3fb2f024c0b9)
- PyBroker’s **walkforward** & **bootstrap metrics** give you a built-in notion of out-of-sample performance and statistical significance. [Hacker News +4 PyBroker +4 Medium +4](https://www.pybroker.com/en/latest/notebooks/6.%20Training%20a%20Model.html?utm_source=chatgpt.com)
- Optuna lets you do:
	- nested CV (different time splits),
	- custom objective that averages metrics across multiple periods,
	- pruning for obviously-bad parameter sets. [Optuna +2 ogsiji.hashnode.dev +2](https://optuna.org/?utm_source=chatgpt.com)

Architecture-wise: treat “cross-validation & walkforward” as **config** your engine adapter knows how to perform, not something hardcoded per strategy.

### 5.4 Metrics storage & reproducibility

Since you’ve got a backend & DB:

- Store **raw returns series and trades**, plus:
	- engine name + version,
	- library versions (backtesting.py / PyBroker / numpy/numba/etc),
	- param dict,
	- data snapshot ID / query hash.

That way, when PyBroker ships a new version (it’s rapidly evolving; releases throughout 2024–2025) [PyPI](https://pypi.org/project/lib-pybroker/1.0.2/) you can re-run key experiments and compare.

For Optuna specifically, you can either use its built-in RDB storage or roll your own mapping into your DB; there are integration examples with experiment trackers like Neptune for logging trials + plots. [ijsred.com +3 docs-legacy.neptune.ai +3 Optuna +3](https://docs-legacy.neptune.ai/integrations/optuna/?utm_source=chatgpt.com)

---

## 6\. TL;DR design call

- Your **engine choices** (backtesting.py + PyBroker + Optuna) are totally reasonable and give you a fully open-source stack that covers:
	- human-readable strategy prototyping + quick grid search (backtesting.py),
	- multi-asset ML-heavy and robust evaluation (PyBroker),
	- serious hyperparameter search (Optuna).
- You *can* rely solely on their built-in metrics, but:
	- A thin **metrics/analytics layer** (possibly powered by QuantStats) gives you:
		- unified metrics across engines,
		- better portfolio/benchmark analysis,
		- clean separation between engines and UI. [GitHub +2 Medium +2](https://github.com/ranaroussi/quantstats)
- The key architectural move is to wrap both libraries behind a **common adapter interface** that:
	- takes your DB refs and strategy IDs,
	- returns standardized `BacktestResult`,
	- lets Optuna and your frontend treat them as interchangeable engines.

Once that skeleton exists, you basically just throw new strategies at it and decide which engine to run them on based on how complex the idea is and whether it’s ML-heavy or not.