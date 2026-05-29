import time

from Item import Item


class KnapsackSolver:
    """
    Knapsack 0/1 dengan Backtracking + Branch & Bound.

    Cara pakai:
        solver = KnapsackSolver(items, capacity)
        solver.solve()
        print(solver.best_profit, solver.best_items)
    """

    def __init__(self, items: list[Item], capacity: int):
        self.items = sorted(items, key=lambda x: x.ratio, reverse=True)
        self.capacity = capacity

        self.best_profit: int = 0
        self.best_items: list[int] = []
        self.node_count: int = 0
        self.elapsed_ms: float = 0.0

    # ── public ──────────────────────────────

    def solve(self) -> None:
        """Jalankan algoritma dan simpan hasilnya ke atribut instance."""
        self.best_profit = 0
        self.best_items = []
        self.node_count = 0

        start = time.perf_counter()
        self._backtrack(0, 0, 0, [])
        self.elapsed_ms = (time.perf_counter() - start) * 1_000

    # ── private ─────────────────────────────

    def _bound(self, index: int, weight: int, profit: int) -> float:
        """Upper-bound (fractional knapsack) dari posisi `index`."""
        if weight >= self.capacity:
            return 0.0

        bound_val = profit
        total_weight = weight

        for i in range(index, len(self.items)):
            item = self.items[i]
            if total_weight + item.weight <= self.capacity:
                total_weight += item.weight
                bound_val += item.profit
            else:
                remaining = self.capacity - total_weight
                bound_val += remaining * item.ratio
                break

        return bound_val

    def _backtrack(
        self, index: int, weight: int, profit: int, chosen: list[int]
    ) -> None:
        self.node_count += 1

        if profit > self.best_profit:
            self.best_profit = profit
            self.best_items = chosen[:]

        if index == len(self.items):
            return

        if self._bound(index, weight, profit) <= self.best_profit:
            return

        item = self.items[index]

        # Cabang kiri: ambil barang
        if weight + item.weight <= self.capacity:
            chosen.append(index)
            self._backtrack(
                index + 1, weight + item.weight, profit + item.profit, chosen
            )
            chosen.pop()

        # Cabang kanan: tidak ambil barang
        self._backtrack(index + 1, weight, profit, chosen)
