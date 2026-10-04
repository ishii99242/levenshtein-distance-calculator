"""Levenshtein edit distance via a space-optimized Wagner-Fischer.

The classic Wagner-Fischer algorithm fills an (m+1) x (n+1) matrix. We only
ever need two rows at a time (the current and previous row), so we keep two
1-D buffers of length n+1 instead. This drops memory from O(m*n) to O(n)
while keeping the O(m*n) time bound.

Design decisions:
- Inputs are str only. Accepting bytes would force an encoding/character-set
  policy; callers who want byte-level distance can decode to str themselves.
- We use ord() comparisons rather than direct char equality. On CPython this
  is marginally faster and makes the intent (code-point identity) explicit,
  which matters because Python strings are sequences of Unicode code points,
  not bytes.
- We canonicalise argument order so the shorter string indexes the rows and
  the longer one indexes the columns. This keeps the row buffers as small as
  possible given the two inputs.
"""

from __future__ import annotations


def distance(s1: str, s2: str) -> int:
    """Return the Levenshtein edit distance between two strings.

    The distance is the minimum number of single-character insertions,
    deletions, or substitutions required to turn ``s1`` into ``s2``.

    Raises TypeError if either argument is not a str.
    """
    if not isinstance(s1, str) or not isinstance(s2, str):
        raise TypeError("distance() requires two str arguments")

    # Keep the shorter string as the column axis to minimise buffer width.
    if len(s1) < len(s2):
        s1, s2 = s2, s1

    m = len(s1)
    n = len(s2)

    # Trivial cases: one side empty means distance is the other side's length.
    if n == 0:
        return m

    # Previous row starts as 0..n (cost of turning an empty prefix of s1
    # into each prefix of s2 by pure insertion).
    previous = list(range(n + 1))
    current = [0] * (n + 1)

    for i in range(1, m + 1):
        current[0] = i  # deleting i characters from s1 to match empty s2
        c1 = ord(s1[i - 1])
        for j in range(1, n + 1):
            cost = 0 if c1 == ord(s2[j - 1]) else 1
            current[j] = min(
                previous[j] + 1,        # deletion from s1
                current[j - 1] + 1,     # insertion into s1
                previous[j - 1] + cost, # substitution (or match)
            )
        previous, current = current, previous

    return previous[n]


def normalized_distance(s1: str, s2: str) -> float:
    """Return distance(s1, s2) divided by the length of the longer string.

    The result is in [0.0, 1.0], where 0.0 means identical and 1.0 means
    no characters in common (including the case where both strings are
    empty, which we define to return 0.0 because the strings are equal).

    We divide by the longer length rather than the average because that
    gives an intuitive 1.0 ceiling: two completely disjoint strings are
    maximally different. Dividing by the shorter length would exceed 1.0
    in asymmetric cases, which is harder to reason about.
    """
    if not isinstance(s1, str) or not isinstance(s2, str):
        raise TypeError("normalized_distance() requires two str arguments")

    if not s1 and not s2:
        return 0.0

    d = distance(s1, s2)
    return d / max(len(s1), len(s2))
