from datetime import datetime
from pathlib import Path


class ReportService:
    def __init__(self, base_dir: str | None = None):
        self.base_dir = Path(base_dir or "reports")
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def create_report(self, title: str, content: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{title.lower().replace(' ', '_')}.txt"
        path = self.base_dir / filename
        path.write_text(content, encoding="utf-8")
        return str(path)
