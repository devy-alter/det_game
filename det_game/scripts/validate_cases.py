import json
from pathlib import Path
for path in Path("backend/app/cases/data").glob("case_*.json"):
    json.loads(path.read_text(encoding="utf-8"))
    print("OK", path)
