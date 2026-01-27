# services/knowledge.py
from pathlib import Path

KNOWLEDGE_DIR = Path(__file__).parent.parent / "knowledge"


def load_knowledge() -> dict[str, str]:
    texts: dict[str, str] = {}
    for path in KNOWLEDGE_DIR.glob("*.md"):
        texts[path.stem] = path.read_text(encoding="utf-8")
    if not texts:
        logger.warning(f"No knowledge files found in {KNOWLEDGE_DIR}")
    return texts



knowledge_texts = load_knowledge()
