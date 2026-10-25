"""
Stock Market Range Analysis using Segment Trees

Includes:
- ADT formal definitions (Insertion, Deletion, Updation, Selection/Query)
- Implementation of a Segment Tree that stores (sum, min, max) in each node
- Helper methods: build, update (point), insert (append), delete (remove index),
  query_sum, query_min, query_max, query_volatility, query_average
- CLI menu for interactive testing and a sample usage at bottom.

Notes:
- For simplicity `insert` and `delete` are implemented by rebuilding the tree
  (O(n)). In real-time systems an implicit/dynamic segment tree or Fenwick tree
  variants may be preferred depending on operations.
- Indices shown to the user are 1-based (day 1..n). Internally 0-based.

"""

from dataclasses import dataclass
from typing import List, Tuple
import math


# -----------------------
# ADT Specifications
# -----------------------
# ADT: StockPrices
# Domain: sequences (array) of non-negative real numbers representing daily closing prices.
# Operations:
#  - build(prices: List[float]) -> constructs the ADT from initial array. (O(n))
#  - query_sum(L: int, R: int) -> float  # Sum of prices in range [L,R] (1-based inclusive). (O(log n))
#  - query_min(L: int, R: int) -> float  # Minimum price in range [L,R]. (O(log n))
#  - query_max(L: int, R: int) -> float  # Maximum price in range [L,R]. (O(log n))
#  - query_average(L: int, R: int) -> float  # Average price in [L,R]. (O(log n))
#  - update(index: int, value: float) -> void  # Update single day's price. (O(log n))
#  - insert(value: float) -> void  # Append a new day price. (O(n) -- rebuild)
#  - delete(index: int) -> void  # Remove a day's price. (O(n) -- rebuild)
#  - display() -> void  # Print the current prices array.
#
# Implementation notes: The segment tree stores tuples (sum, min, max) in each node.
# For min and max identity values, we use +inf and -inf respectively.


@dataclass
class Node:
    s: float  # sum
    mn: float  # min
    mx: float  # max


class StockSegmentTree:
    def __init__(self, prices: List[float]):
        self.n = len(prices)
        self.prices = prices[:]  # keep a copy
        if self.n == 0:
            # support empty tree
            self.size = 0
            self.tree = []
        else:
            # size of segment tree array: 4*n is safe
            self.size = 4 * self.n
            self.tree = [Node(0.0, math.inf, -math.inf) for _ in range(self.size)]
            self._build(1, 0, self.n - 1)

    # --------------------
    # Internal builder
    # --------------------
    def _build(self, idx: int, l: int, r: int) -> None:
        if l == r:
            v = float(self.prices[l])
            self.tree[idx] = Node(v, v, v)
            return
        mid = (l + r) // 2
        self._build(idx * 2, l, mid)
        self._build(idx * 2 + 1, mid + 1, r)
        left = self.tree[idx * 2]
        right = self.tree[idx * 2 + 1]
        self.tree[idx] = Node(left.s + right.s, min(left.mn, right.mn), max(left.mx, right.mx))

    # --------------------
    # Point update (1-based index exposed)
    # --------------------
    def update(self, day: int, value: float) -> None:
        if self.n == 0:
            raise IndexError("No elements in the structure. Use insert to add elements.")
        i = day - 1
        if i < 0 or i >= self.n:
            raise IndexError("Day index out of range")
        self._update(1, 0, self.n - 1, i, float(value))
        self.prices[i] = float(value)

    def _update(self, idx: int, l: int, r: int, pos: int, value: float) -> None:
        if l == r:
            self.tree[idx] = Node(value, value, value)
            return
        mid = (l + r) // 2
        if pos <= mid:
            self._update(idx * 2, l, mid, pos, value)
        else:
            self._update(idx * 2 + 1, mid + 1, r, pos, value)
        left = self.tree[idx * 2]
        right = self.tree[idx * 2 + 1]
        self.tree[idx] = Node(left.s + right.s, min(left.mn, right.mn), max(left.mx, right.mx))

    # --------------------
    # Range queries (1-based inclusive)
    # Each returns a Node-like tuple for convenience
    # --------------------
    def query_sum(self, L: int, R: int) -> float:
        node = self._query(1, 0, self.n - 1, L - 1, R - 1)
        return node.s

    def query_min(self, L: int, R: int) -> float:
        node = self._query(1, 0, self.n - 1, L - 1, R - 1)
        return node.mn

    def query_max(self, L: int, R: int) -> float:
        node = self._query(1, 0, self.n - 1, L - 1, R - 1)
        return node.mx

    def query_average(self, L: int, R: int) -> float:
        total = self.query_sum(L, R)
        cnt = (R - L + 1)
        return total / cnt if cnt > 0 else 0.0

    def query_volatility(self, L: int, R: int) -> float:
        # volatility defined as max - min in the range
        return self.query_max(L, R) - self.query_min(L, R)

    def _query(self, idx: int, l: int, r: int, ql: int, qr: int) -> Node:
        # fully outside
        if qr < l or ql > r:
            return Node(0.0, math.inf, -math.inf)
        # fully inside
        if ql <= l and r <= qr:
            return self.tree[idx]
        mid = (l + r) // 2
        left = self._query(idx * 2, l, mid, ql, qr)
        right = self._query(idx * 2 + 1, mid + 1, r, ql, qr)
        return Node(left.s + right.s, min(left.mn, right.mn), max(left.mx, right.mx))

    # --------------------
    # Insert (append) - implemented by rebuilding (O(n))
    # --------------------
    def insert(self, value: float) -> None:
        self.prices.append(float(value))
        self.n = len(self.prices)
        self.size = 4 * self.n if self.n > 0 else 0
        self.tree = [Node(0.0, math.inf, -math.inf) for _ in range(self.size)]
        if self.n > 0:
            self._build(1, 0, self.n - 1)

    # --------------------
    # Delete at day index (1-based) - O(n) rebuild
    # --------------------
    def delete(self, day: int) -> None:
        i = day - 1
        if i < 0 or i >= self.n:
            raise IndexError("Day index out of range")
        self.prices.pop(i)
        self.n = len(self.prices)
        if self.n == 0:
            self.tree = []
            self.size = 0
            return
        self.size = 4 * self.n
        self.tree = [Node(0.0, math.inf, -math.inf) for _ in range(self.size)]
        self._build(1, 0, self.n - 1)

    # --------------------
    # Utility
    # --------------------
    def display(self) -> None:
        print("Current prices (day:price):")
        for i, p in enumerate(self.prices, start=1):
            print(f"Day {i}: {p}")


# --------------------
# Sample interactive CLI
# --------------------

def sample_run():
    print("Stock Market Range Analysis - Segment Tree Implementation")
    print("Enter initial prices separated by space (or leave blank for empty):")
    line = input().strip()
    prices = []
    if line:
        try:
            prices = [float(x) for x in line.split()]
        except ValueError:
            print("Invalid numbers. Starting with empty list.")
            prices = []
    tree = StockSegmentTree(prices)

    menu = '''\nChoose operation:
1. Display prices
2. Query Max price in range
3. Query Min price in range
4. Query Sum in range
5. Query Average in range
6. Query Volatility (max-min) in range
7. Update price for a day
8. Insert (append) new day price
9. Delete a day
10. Exit
''' 
    while True:
        print(menu)
        choice = input("Choice: ").strip()
        if choice == '10':
            print("Exiting. Goodbye!")
            break
        if choice == '1':
            tree.display()

        elif choice in {'2','3','4','5','6'}:
            try:
                L = int(input("Enter L (start day, 1-based): "))
                R = int(input("Enter R (end day, 1-based): "))
            except ValueError:
                print("Invalid input. Provide integer day indices.")
                continue
            if tree.n == 0:
                print("No data available.")
                continue
            if L < 1 or R > tree.n or L > R:
                print(f"Invalid range. Valid days: 1 to {tree.n}")
                continue
            if choice == '2':
                print(f"Max price in range [{L},{R}] = {tree.query_max(L, R)}")
            elif choice == '3':
                print(f"Min price in range [{L},{R}] = {tree.query_min(L, R)}")
            elif choice == '4':
                print(f"Sum of prices in range [{L},{R}] = {tree.query_sum(L, R)}")
            elif choice == '5':
                print(f"Average price in range [{L},{R}] = {tree.query_average(L, R)}")
            elif choice == '6':
                print(f"Volatility in range [{L},{R}] = {tree.query_volatility(L, R)}")

        elif choice == '7':
            try:
                d = int(input("Day index to update (1-based): "))
                val = float(input("New price: "))
            except ValueError:
                print("Invalid input.")
                continue
            try:
                tree.update(d, val)
                print("Update successful.")
            except IndexError as e:
                print(e)

        elif choice == '8':
            try:
                val = float(input("New day price to append: "))
            except ValueError:
                print("Invalid input.")
                continue
            tree.insert(val)
            print("Inserted.")

        elif choice == '9':
            try:
                d = int(input("Day index to delete (1-based): "))
            except ValueError:
                print("Invalid input.")
                continue
            try:
                tree.delete(d)
                print("Deleted.")
            except IndexError as e:
                print(e)

        else:
            print("Unknown choice. Try again.")


if __name__ == '__main__':
    sample_run()