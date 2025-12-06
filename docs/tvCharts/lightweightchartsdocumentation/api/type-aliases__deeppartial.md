---
source: https://tradingview.github.io/lightweight-charts/docs/api/type-aliases/DeepPartial
scraped_at: 2025-12-01T14:31:43.037410
---

# https://tradingview.github.io/lightweight-charts/docs/api/type-aliases/DeepPartial

# Type alias: DeepPartial<T>

DeepPartial<`T`

>:`{ [P in keyof T]?: T[P] extends (infer U)[] ? DeepPartial<U>[] : T[P] extends readonly (infer X)[] ? readonly DeepPartial<X>[] : DeepPartial<T[P]> }`

Represents a type `T`

where every property is optional.

## Type parameters

• **T**