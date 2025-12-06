---
source: https://tradingview.github.io/lightweight-charts/docs/api/functions/defaultHorzScaleBehavior
scraped_at: 2025-12-01T14:31:38.254774
---

# https://tradingview.github.io/lightweight-charts/docs/api/functions/defaultHorzScaleBehavior

# Function: defaultHorzScaleBehavior()

defaultHorzScaleBehavior(): () =>`IHorzScaleBehavior`

<`Time`

>

Provides the default implementation of the horizontal scale (time-based) that can be used as a base for extending the horizontal scale with custom behavior. This allows for the introduction of custom functionality without re-implementing the entire IHorzScaleBehavior<Time> interface.

For further details, refer to the createChartEx chart constructor method.

## Returns

`Function`

An uninitialized class implementing the IHorzScaleBehavior<Time> interface