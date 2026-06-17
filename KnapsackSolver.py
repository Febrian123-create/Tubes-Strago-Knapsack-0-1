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
        self.exploration_log: list[dict] = []

    # ── public ──────────────────────────────

    def solve(self) -> None:
        """Jalankan algoritma dan simpan hasilnya ke atribut instance."""
        self.best_profit = 0
        self.best_items = []
        self.node_count = 0
        self.exploration_log = []

        start = time.perf_counter()
        self._backtrack(0, 0, 0, [])
        self.elapsed_ms = (time.perf_counter() - start) * 1_000

    # ── private ─────────────────────────────

    def _bound(self, index: int, weight: int, profit: int) -> float:
        """Upper-bound (fractional knapsack) dari posisi `index`."""
        if weight >= self.capacity:
            return float(profit)

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
        self, index: int, weight: int, profit: int, chosen: list[int], action: str = "ROOT"
    ) -> None:
        self.node_count += 1

        is_leaf   = index == len(self.items)
        item_name = "LEAF" if is_leaf else self.items[index].name
        ub        = self._bound(index, weight, profit)
        pruned    = (not is_leaf) and (ub <= self.best_profit)

        self.exploration_log.append({
            "node_id":       self.node_count,
            "depth":         index,
            "item_name":     item_name,
            "weight_so_far": weight,
            "profit_so_far": profit,
            "upper_bound":   round(ub, 4),
            "pruned":        pruned,
            "action":        action,
        })

        if profit > self.best_profit:
            self.best_profit = profit
            self.best_items = chosen[:]

        if is_leaf or pruned:
            return

        item = self.items[index]

        if weight + item.weight <= self.capacity:
            chosen.append(index)
            self._backtrack(
                index + 1, weight + item.weight, profit + item.profit, chosen, action="INCLUDE"
            )
            chosen.pop()

        self._backtrack(index + 1, weight, profit, chosen, action="EXCLUDE")
