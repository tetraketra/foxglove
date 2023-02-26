### 1. What is Foxglove? 🌷
Foxglove is an aesthetic and highly-configurable python-based terminal rendering support library with an accompanying custom frame definition language. Consider this a personalized alternative to [Urwid](https://urwid.org) with features customized to my use cases only.

### 2. What is Bouquet? 💐 
`.bqt` is a plaintext custom frame definition language with support for variable sizing. Bouquet files ignore all standard English-language alphabetic characters `[a-zA-Z]` except for `[AaBbCcLRUD]`, which are reserved for interpreter instructions. Bouquet intentionally requires _all_ alphabetic characters to be inserted during runtime using `.format()`. The following characters have special meanings:
 - `A`|`a` and `B`|`b` define strictly-rectangular text regions.
   - `A`, `a`, `B`, and `b` do not connect to each other.
   - `AABBBAAA` will generate three independent numbered text frames.
   - `A` and `B` hard cut. Printing `Hello world!` to `AAAAAA` yields `Hello `.
   - `a` and `b` soft cut. Printing `Hello world!` to `aaaaaa` yields `Hel...`.
   - Multi-line regions text-wrap by default.
 - `L`|`l` is an alternative to the `AaBb` format for a multi-line list region.
 - `X` is a smart division and expansion character. We call a line of Xs a "cut."
   - Cuts must be drawn in axis lines across the canvas. These may intersect and you may have multiple in the same axis.
   - Cuts reference the characters to their left/up to repeat the edge of a frame region to expand it to variable sizing.
   - If you don't want vertical resizing, don't have a horizontal cut.
   - Config in the form `X:Y:Z` can allow for biased expansion, handing out repeats in those proportions.
   - Expansions are Bouquet-only. They do not repeat printed text.
   - `╔═X╝` expands to `╔═══...═╝`.
