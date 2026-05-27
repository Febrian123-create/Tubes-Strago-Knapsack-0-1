import time

best_profit   = 0
best_solution = []
node_count    = 0


def bound(index, weight, profit, items, W):
    if weight >= W:
        return 0

    bound_val    = profit
    total_weight = weight

    for i in range(index, len(items)):
        if total_weight + items[i]['weight'] <= W:
            total_weight += items[i]['weight']
            bound_val    += items[i]['profit']
        else:
            remaining  = W - total_weight
            bound_val += remaining * (items[i]['profit'] / items[i]['weight'])
            break

    return bound_val


def backtrack(index, weight, profit, chosen, items, W):
    global best_profit, best_solution, node_count

    node_count += 1

    if profit > best_profit:
        best_profit   = profit
        best_solution = chosen[:]

    if index == len(items):
        return

    if bound(index, weight, profit, items, W) <= best_profit:
        return

    if weight + items[index]['weight'] <= W:
        chosen.append(index)
        backtrack(
            index + 1,
            weight + items[index]['weight'],
            profit + items[index]['profit'],
            chosen, items, W
        )
        chosen.pop()

    backtrack(index + 1, weight, profit, chosen, items, W)


def _read_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            print("  [!] Nilai harus bilangan bulat positif (> 0).")
        except ValueError:
            print("  [!] Input tidak valid. Masukkan bilangan bulat.")


def _read_min_int(prompt, minimum):
    while True:
        try:
            value = int(input(prompt))
            if value >= minimum:
                return value
            print(f"  [!] Nilai harus minimal {minimum}.")
        except ValueError:
            print("  [!] Input tidak valid. Masukkan bilangan bulat.")


def input_items():
    SEP = "=" * 60

    print(f"\n{SEP}")
    print("  KNAPSACK 0/1 - Backtracking + Branch & Bound")
    print(SEP)

    n = _read_min_int("  Jumlah barang (minimal 1): ", 1)

    items = []
    for i in range(1, n + 1):
        print(f"\n  Barang {i}:")
        name   = input("    Nama   : ").strip() or f"Barang{i}"
        weight = _read_positive_int("    Berat  : ")
        profit = _read_positive_int("    Profit : ")
        items.append({"id": i, "name": name, "weight": weight, "profit": profit})

    print()
    W = _read_min_int("  Kapasitas knapsack W (minimal 1): ", 1)
    print()
    return items, W


def _sep(char="=", width=62):
    print(char * width)


def print_sorted_items(items_sorted):
    _sep()
    print("  DAFTAR BARANG  (diurutkan: rasio profit/berat desc)")
    _sep("-")
    print(f"  {'ID':<4}  {'Nama':<14}  {'Berat':>6}  {'Profit':>7}  {'Rasio':>7}")
    print(f"  {'-'*4}  {'-'*14}  {'-'*6}  {'-'*7}  {'-'*7}")
    for item in items_sorted:
        ratio = item["profit"] / item["weight"]
        print(
            f"  {item['id']:<4}  {item['name']:<14}  "
            f"{item['weight']:>6}  {item['profit']:>7}  {ratio:>7.2f}"
        )
    _sep()


def print_solution(best_solution, items_sorted, W):
    _sep()
    print("  SOLUSI OPTIMAL")
    _sep("-")

    if not best_solution:
        print("  Tidak ada barang yang dapat dimasukkan.")
        _sep()
        return

    print(f"  {'ID':<4}  {'Nama':<14}  {'Berat':>6}  {'Profit':>7}")
    print(f"  {'-'*4}  {'-'*14}  {'-'*6}  {'-'*7}")

    total_weight = 0
    total_profit = 0
    for idx in best_solution:
        item = items_sorted[idx]
        print(
            f"  {item['id']:<4}  {item['name']:<14}  "
            f"{item['weight']:>6}  {item['profit']:>7}"
        )
        total_weight += item["weight"]
        total_profit += item["profit"]

    print(f"  {'':>4}  {'-'*14}  {'-'*6}  {'-'*7}")
    print(f"  {'':>4}  {'TOTAL':<14}  {total_weight:>6}  {total_profit:>7}")
    print(f"\n  Sisa kapasitas: {W - total_weight} / {W}")
    _sep()


def print_statistics(node_count, elapsed_ms):
    print("  STATISTIK")
    _sep("-")
    print(f"  Jumlah node dikunjungi  : {node_count:,}")
    print(f"  Waktu eksekusi          : {elapsed_ms:.3f} ms")
    _sep()


def main():
    global best_profit, best_solution, node_count

    items, W = input_items()

    items_sorted = sorted(
        items,
        key=lambda x: x["profit"] / x["weight"],
        reverse=True
    )

    print_sorted_items(items_sorted)
    print(f"\n  Kapasitas Knapsack (W) = {W}\n")

    best_profit   = 0
    best_solution = []
    node_count    = 0

    print("  Menjalankan Backtracking + Branch & Bound ...\n")
    start = time.perf_counter()
    backtrack(0, 0, 0, [], items_sorted, W)
    end   = time.perf_counter()

    elapsed_ms = (end - start) * 1_000

    print_solution(best_solution, items_sorted, W)
    print_statistics(node_count, elapsed_ms)


if __name__ == "__main__":
    main()
