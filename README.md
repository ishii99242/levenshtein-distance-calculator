# levenshtein-distance-calculator

A small, dependency-free Python library that computes the Levenshtein edit distance between two strings using a space-optimized Wagner-Fischer algorithm.

## Usage

```python
from levenshtein_distance_calculator import distance, normalized_distance

distance("kitten", "sitting")        # -> 3
normalized_distance("kitten", "sitting")  # -> 0.42857142857142855
```

Run the tests with:

```
PYTHONPATH=src python -m unittest discover -s tests
```

## Why this exists

The standard Wagner-Fischer algorithm builds a full (m+1) by (n+1) matrix, which is wasteful: only the previous row is needed to compute the current one. This implementation keeps two rolling rows of length `min(m, n) + 1`, reducing memory from O(m*n) to O(n) while preserving the O(m*n) time bound. The trade-off is that we cannot reconstruct an actual edit sequence afterwards — only the count is produced.

## Edge cases worth knowing

- Inputs are `str` only. Passing bytes or other types raises `TypeError`. If you need byte-level distance, decode your bytes to `str` first.
- Distance is measured in Unicode code points, so `"café"` and `"cafe"` differ by 1 (the precomposed `é` vs `e`). Combining marks count as separate code points.
- The shorter input is used as the column axis internally to keep buffers small, so `distance(a, b)` always equals `distance(b, a)`.
- `normalized_distance` divides by the length of the longer string and returns `0.0` when both strings are empty.

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

