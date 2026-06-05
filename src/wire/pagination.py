"""Auto-paginating iterator over cursor-paginated list endpoints."""
from __future__ import annotations

from typing import Any, Callable, Iterator, List, Tuple


class ListIterator:
    """Lazily iterates all pages. `fetch(after, limit) -> (items, has_more)`.
    `id_of(item) -> str` yields the cursor for the next page."""

    def __init__(self, fetch: Callable[[str, int], Tuple[List[Any], bool]], id_of, limit: int = 0):
        self._fetch = fetch
        self._id_of = id_of
        self._limit = limit
        self._after = ""

    def __iter__(self) -> Iterator[Any]:
        while True:
            items, has_more = self._fetch(self._after, self._limit)
            if not items:
                return
            for it in items:
                self._after = self._id_of(it)
                yield it
            if not has_more:
                return
