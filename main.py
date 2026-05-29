from KnapsackCLI import KnapsackCLI
from KnapsackSolver import KnapsackSolver


def main() -> None:
    cli = KnapsackCLI()

    items, capacity = cli.read_items_and_capacity()

    solver = KnapsackSolver(items, capacity)

    cli.print_sorted_items(solver.items)
    print(f"\n  Kapasitas Knapsack (W) = {capacity}\n")

    print("  Menjalankan Backtracking + Branch & Bound ...\n")
    solver.solve()

    cli.print_solution(solver)
    cli.print_statistics(solver)


if __name__ == "__main__":
    main()
