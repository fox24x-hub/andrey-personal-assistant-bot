import logging
from pathlib import Path

logger = logging.getLogger(__name__)

KNOWLEDGE_DIR = Path(__file__).parent.parent / "knowledge"

def load_knowledge() -> dict[str, str]:
    texts: dict[str, str] = {}
    if not KNOWLEDGE_DIR.exists():
        return texts
        
    for path in KNOWLEDGE_DIR.glob("*.md"):
        texts[path.stem] = path.read_text(encoding="utf-8")
        
    return texts

knowledge_texts = load_knowledge()
