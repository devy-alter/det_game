import json
from pathlib import Path

from app.schemas.case import Case


class CaseLoader:
    def __init__(self):
        self.root = Path(__file__).parent / "data"

    def list_cases(self):
        return [self.load(path.stem) for path in sorted(self.root.glob("case_*.json"))]

    def load(self, case_id: str) -> Case:
        path = self.root / f"{case_id}.json"
        if not path.exists():
            raise FileNotFoundError(case_id)
        return Case.model_validate(json.loads(path.read_text(encoding="utf-8")))


loader = CaseLoader()
