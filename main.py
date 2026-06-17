from flask import Flask, render_template, request

from KnapsackSolver import KnapsackSolver
from Project import Project, SAMPLE_PROJECTS

app = Flask(__name__)


def build_tree(exploration_log: list[dict], best_items: list[int]) -> dict | None:
    """Rekonstruksi pohon eksplorasi backtracking dari exploration_log.

    Log ditulis pre-order (INCLUDE dieksplorasi sebelum EXCLUDE), sehingga
    parent-child dapat direkonstruksi dengan stack berdasarkan depth.
    """
    if not exploration_log:
        return None

    root = None
    stack: list[dict] = []  # stack node yang sedang aktif (jalur dari root)

    for entry in exploration_log:
        node = {
            "id": entry["node_id"],
            "depth": entry["depth"],
            "item": entry["item_name"],
            "profit": entry["profit_so_far"],
            "weight": entry["weight_so_far"],
            "action": entry["action"],
            "on_path": False,
            "children": [],
        }
        # Pop sampai stack top adalah parent (depth = node.depth - 1)
        while stack and stack[-1]["depth"] >= node["depth"]:
            stack.pop()
        if stack:
            stack[-1]["children"].append(node)
        else:
            root = node
        stack.append(node)

    # Tandai jalur solusi optimal: di depth i, pilih INCLUDE jika i ∈ best_items
    best_set = set(best_items)
    cur = root
    while cur is not None:
        cur["on_path"] = True
        wanted = "INCLUDE" if cur["depth"] in best_set else "EXCLUDE"
        cur = next((c for c in cur["children"] if c["action"] == wanted), None)

    return root


@app.route("/", methods=["GET", "POST"])
def home():
    output = None
    sorted_projects = None
    stats = None
    exploration_log = None
    tree = None
    budget = None
    submitted_projects = None

    if request.method == "POST":
        budget = int(request.form["budget"])

        # Baca jumlah proyek dinamis dari form (minimal 8)
        item_count = int(request.form.get("itemCount", 8))
        if item_count < 8:
            item_count = 8

        # Ambil proyek dari form
        projects = []
        for i in range(1, item_count + 1):
            name = request.form.get(f"name{i}")
            profit = request.form.get(f"profit{i}")
            duration = request.form.get(f"duration{i}")
            # Skip jika salah satu field kosong
            if name and profit and duration:
                projects.append(
                    Project(len(projects), name, int(profit), int(duration))
                )

        submitted_projects = [
            {"name": p.name, "profit": p.profit, "duration": p.duration}
            for p in projects
        ]

        solver = KnapsackSolver([p.to_item() for p in projects], budget)
        solver.solve()

        selected_idx = set(solver.best_items)
        sorted_projects = [
            {
                "name": item.name,
                "profit": item.profit,
                "duration": item.weight,
                "ratio": round(item.ratio, 2),
                "selected": i in selected_idx,
            }
            for i, item in enumerate(solver.items)
        ]

        selected = [solver.items[i] for i in solver.best_items]
        total_duration = sum(it.weight for it in selected)
        output = {
            "selected": [
                {"name": it.name, "duration": it.weight, "profit": it.profit}
                for it in selected
            ],
            "total_duration": total_duration,
            "total_profit": solver.best_profit,
            "remaining": budget - total_duration,
            "used_percent": round(total_duration / budget * 100, 1) if budget else 0,
        }

        exploration_log = solver.exploration_log
        stats = {
            "node_count": solver.node_count,
            "elapsed_ms": round(solver.elapsed_ms, 3),
        }
        tree = build_tree(exploration_log, solver.best_items)

    return render_template(
        "index.html",
        output=output,
        sorted_projects=sorted_projects,
        stats=stats,
        exploration_log=exploration_log,
        tree=tree,
        budget=budget,
        submitted_projects=submitted_projects,
        sample_projects=SAMPLE_PROJECTS,
    )


if __name__ == "__main__":
    app.run(debug=True)
