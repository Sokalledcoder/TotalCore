---
source: https://tradingview.github.io/lightweight-charts/docs/api/enumerations/PriceScaleMode
scraped_at: 2025-12-01T14:31:38.069902
---

# https://tradingview.github.io/lightweight-charts/docs/api/enumerations/PriceScaleMode

# Enumeration: PriceScaleMode

Represents the price scale mode.

## Enumeration Members

### Normal

Normal:`0`

Price scale shows prices. Price range changes linearly.

### Logarithmic

Logarithmic:`1`

Price scale shows prices. Price range changes logarithmically.

### Percentage

Percentage:`2`

Price scale shows percentage values according the first visible value of the price scale. The first visible value is 0% in this mode.

### IndexedTo100

IndexedTo100:`3`

The same as percentage mode, but the first value is moved to 100.