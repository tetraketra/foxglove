### 1. What is Foxglove? 🌷
Foxglove is an aesthetic and highly-configurable python-based terminal rendering support library with an accompanying custom frame definition language. Consider this a personalized alternative to [Urwid](https://urwid.org) with features customized to my use cases only.

### 2. What is Bouquet? 💐 
Bouquet is a plaintext custom frame definition language with support for variable sizing. Bouquet files ignore all standard English-language alphabetic characters `[a-z, A-Z]` except for `[AaBbCcLRUD]`, which are reserved for interpreter instructions. Bouquet intentionally requires all alphabetic characters to be inser
ted during runtime. The following characters have special meanings:
 - `A`|`a` and `B`|`b` define strictly-rectangular text frames.
   - `A`, `a`, `B`, and `b` do not connect to each other.
   - `AABBBAAA` will generate three independent numbered text frames.
   - `A` and `B` hard cut. Printing `Hello world!` to `AAAAAA` yields `Hello `.
   - `a` and `b` soft cut. Printing `Hello world!` to `aaaaaa` yields `Hel...` by default.
   - Multi-line frames text-wrap by default. This can be altered case-by-case in code.
 - `L`|`l` is an alternative to the `AaBb` format for a multi-line list region.
 - `X` is a smart division and expansion character. We call a line of Xs a "cut."
   - Cuts must be drawn in axis lines across the canvas. These may intersect and you may have multiple in the same axis.
   - Cuts reference the characters to their left/up to repeat the edge of a frame region to expand it to variable sizing.
   - If you don't want vertical resizing, don't have a horizontal cut.
   - Config in the form `X:Y:Z` can allow for biased expansion, handing out repeats in those proportions.
   - Expansions are Bouquet-only. They do not repeat printed text.
   - `⊨=X⫥` expands to `⊨===...=⫥`.

 All Bouquet files end in `.bqt`.
