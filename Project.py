from Item import Item


class Project:
    """Merepresentasikan satu proyek dalam simulasi pemilihan proyek.

    P = profit, W = duration (durasi pengerjaan dalam hari).
    """

    def __init__(self, project_id: int, name: str, profit: int, duration: int):
        self.id = project_id
        self.name = name
        self.profit = profit
        self.duration = duration

    @property
    def ratio(self) -> float:
        """Rasio profit per hari (profit/duration)."""
        return self.profit / self.duration

    def to_item(self) -> Item:
        """Adapter ke Item agar bisa diproses KnapsackSolver (weight = durasi)."""
        return Item(self.id, self.name, self.duration, self.profit)

    def __repr__(self) -> str:
        return (
            f"Project(id={self.id}, name={self.name!r}, "
            f"p={self.profit}, w={self.duration} hari)"
        )

SAMPLE_PROJECTS = [
    {"name": "Website Toko Online", "profit": 500, "duration": 10},
    {"name": "Aplikasi Mobile Kasir", "profit": 800, "duration": 20},
    {"name": "Desain UI/UX Landing Page", "profit": 300, "duration": 5},
    {"name": "Sistem Informasi Sekolah", "profit": 650, "duration": 15},
    {"name": "Company Profile", "profit": 200, "duration": 4},
    {"name": "Integrasi Payment Gateway", "profit": 400, "duration": 7},
    {"name": "Dashboard Analitik", "profit": 550, "duration": 12},
    {"name": "Chatbot Customer Service", "profit": 350, "duration": 8},
]
