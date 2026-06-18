from Item import Item
from KnapsackSolver import KnapsackSolver


class KnapsackCLI:
    """Menangani semua interaksi terminal: input, output, dan formatting."""

    _SEP_WIDE = "=" * 62
    _SEP_THIN = "-" * 62

    # ── input ───────────────────────────────

    def read_items_and_capacity(self) -> tuple[list[Item], int]:
        print(f"\n{self._SEP_WIDE}")
        print("  KNAPSACK 0/1 - Backtracking + Branch & Bound")
        print(self._SEP_WIDE)

        n = self._read_min_int("  Jumlah barang (minimal 1): ", 1)
        items = []

        for i in range(1, n + 1):
            print(f"\n  Barang {i}:")
            name = input("    Nama   : ").strip() or f"Barang{i}"
            weight = self._read_positive_int("    Berat  : ")
            profit = self._read_positive_int("    Profit : ")
            items.append(Item(i, name, weight, profit))

        print()
        capacity = self._read_min_int("  Kapasitas knapsack W (minimal 1): ", 1)
        print()
        return items, capacity

    # ── output ──────────────────────────────

    def print_sorted_items(self, items: list[Item]) -> None:
        print(self._SEP_WIDE)
        print("  DAFTAR BARANG  (diurutkan: rasio profit/berat desc)")
        print(self._SEP_THIN)
        print(f"  {'ID':<4}  {'Nama':<14}  {'Berat':>6}  {'Profit':>7}  {'Rasio':>7}")
        print(f"  {'-'*4}  {'-'*14}  {'-'*6}  {'-'*7}  {'-'*7}")
        for item in items:
            print(
                f"  {item.id:<4}  {item.name:<14}  "
                f"{item.weight:>6}  {item.profit:>7}  {item.ratio:>7.2f}"
            )
        print(self._SEP_WIDE)

    def print_solution(self, solver: KnapsackSolver) -> None:
        print(self._SEP_WIDE)
        print("  SOLUSI OPTIMAL")
        print(self._SEP_THIN)

        if not solver.best_items:
            print("  Tidak ada barang yang dapat dimasukkan.")
            print(self._SEP_WIDE)
            return

        print(f"  {'ID':<4}  {'Nama':<14}  {'Berat':>6}  {'Profit':>7}")
        print(f"  {'-'*4}  {'-'*14}  {'-'*6}  {'-'*7}")

        total_weight = total_profit = 0
        for idx in solver.best_items:
            item = solver.items[idx]
            print(
                f"  {item.id:<4}  {item.name:<14}  "
                f"{item.weight:>6}  {item.profit:>7}"
            )
            total_weight += item.weight
            total_profit += item.profit

        print(f"  {'':>4}  {'-'*14}  {'-'*6}  {'-'*7}")
        print(f"  {'':>4}  {'TOTAL':<14}  {total_weight:>6}  {total_profit:>7}")
        print(
            f"\n  Sisa kapasitas: {solver.capacity - total_weight} / {solver.capacity}"
        )
        print(self._SEP_WIDE)

    def print_statistics(self, solver: KnapsackSolver) -> None:
        print("  STATISTIK")
        print(self._SEP_THIN)
        print(f"  Jumlah node dikunjungi  : {solver.node_count:,}")
        print(f"  Waktu eksekusi          : {solver.elapsed_ms:.3f} ms")
        print(self._SEP_WIDE)

    # ── helpers ─────────────────────────────

    @staticmethod
    def _read_positive_int(prompt: str) -> int:
        while True:
            try:
                value = int(input(prompt))
                if value > 0:
                    return value
                print("  [!] Nilai harus bilangan bulat positif (> 0).")
            except ValueError:
                print("  [!] Input tidak valid. Masukkan bilangan bulat.")

    @staticmethod
    def _read_min_int(prompt: str, minimum: int) -> int:
        while True:
            try:
                value = int(input(prompt))
                if value >= minimum:
                    return value
                print(f"  [!] Nilai harus minimal {minimum}.")
            except ValueError:
                print("  [!] Input tidak valid. Masukkan bilangan bulat.")
if __name__ == "__main__":
    cli = KnapsackCLI()
    
    # 1. Baca input dari terminal
    items, capacity = cli.read_items_and_capacity()
    
    # 2. Inisialisasi Solver dan selesaikan
    solver = KnapsackSolver(items, capacity)
    solver.solve()
    
    # 3. Tampilkan hasil ke terminal
    cli.print_sorted_items(solver.items)
    cli.print_solution(solver)
    cli.print_statistics(solver)
