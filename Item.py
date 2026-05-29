class Item:
    """Merepresentasikan satu barang dalam knapsack."""

    def __init__(self, item_id: int, name: str, weight: int, profit: int):
        self.id = item_id
        self.name = name
        self.weight = weight
        self.profit = profit

    @property
    def ratio(self) -> float:
        return self.profit / self.weight

    def __repr__(self) -> str:
        return (
            f"Item(id={self.id}, name={self.name!r}, w={self.weight}, p={self.profit})"
        )
