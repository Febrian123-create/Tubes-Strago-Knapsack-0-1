from flask import Flask, render_template, request
from KnapsackSolver import KnapsackSolver

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    output = None
    sorted_items = None
    statistics = None

    if request.method == "POST":
        capacity = int(request.form["capacity"])

        # Read dynamic item count from form
        item_count = int(request.form.get("itemCount", 8))
        if item_count < 8:
            item_count = 8

        # Ambil items dari form sesuai jumlah dinamis
        items = []
        for i in range(1, item_count + 1):
            name = request.form.get(f"name{i}")
            profit = request.form.get(f"profit{i}")
            weight = request.form.get(f"weight{i}")
            # Skip jika salah satu field kosong
            if name and profit and weight:
                items.append(
                    {"name": name, "profit": int(profit), "weight": int(weight)}
                )

        # Konversi list of dict menjadi list of Item
        from Item import Item

        items = [
            Item(i, item["name"], item["weight"], item["profit"])
            for i, item in enumerate(items)
        ]
        solver = KnapsackSolver(items, capacity)
        solver.solve()

        sorted_items = [
            {"name": item.name, "profit": item.profit, "weight": item.weight}
            for item in solver.items
        ]
        selected = [solver.items[i] for i in solver.best_items]
        output = {
            "selected": [
                {"name": it.name, "weight": it.weight, "profit": it.profit}
                for it in selected
            ],
            "total_weight": sum(it.weight for it in selected),
            "total_profit": solver.best_profit,
            "remaining": capacity - sum(it.weight for it in selected),
        }
        statistics = (
            f"Node dikunjungi: {solver.node_count} | Waktu: {solver.elapsed_ms:.3f} ms"
        )

    return render_template(
        "index.html", output=output, sorted_items=sorted_items, statistics=statistics
    )


if __name__ == "__main__":
    app.run(debug=True)
