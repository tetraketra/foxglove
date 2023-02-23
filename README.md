### 1. What is Foxglove?
Foxglove is an aesthetic and highly-configurable python-based terminal rendering support library with an accompanying custom frame definition language. Consider this a personalized alternative to [Urwid](https://urwid.org) with features customized to my use cases only.

### 2. What is Bouquet? 
Bouquet is a plaintext custom frame definition language with support for variable sizing. Bouqet files ignore all standard English-language alphabetic characters `[a-z, A-Z]` except for `AaBbLRUD`, which are reserved for interpreter instructions. Bouquet intentionally requires all alphabetic characters to be inserted during runtime. The following characters have special meanings:
 - `A`, `a`, `B`, and `b` define strictly-rectangular text frames. 
   - `A`|`a` and `B`|`b` do not connect to each other. This allows for adjacent text frames.
   - `A` and `B` hard cut. Printing `Hello world!` to `AAAAAA` yields `Hello `.
   - `a` and `b` soft cut. Printing `Hello world!` to `aaaaaa` yields `Hel...` by default.
   - `AABBBAAA` will generate three independent and numbered text frames. 
   - Multi-line frames text-wrap by default.
 - `L`, `R`, `U`, and `D` define single-character repetitions for expanding frames to variable widths.
   - Expansions are Bouqet-only. They do not repeat printed text.
   - `⊨=L⫥` can expand to `⊨===...=⫥`. 
   - `⊨=R⫥` would instead expand to `⊨=⫥⫥⫥...⫥`.
 All Bouqet files end in `.bqt`.
