import logging
from pathlib import Path

logger = logging.getLogger(__name__)

KNOWLEDGE_DIR = Path(__file__).parent.parent / "knowledge"

def load_knowledge() -> dict[str, str]:
    texts: dict[str, str] = {}
    if not KNOWLEDGE_DIR.exists():
        logger.warning(f"Knowledge directory not found: {KNOWLEDGE_DIR}")
        return texts
        
    for path in KNOWLEDGE_DIR.glob("*.md"):
        try:
            texts[path.stem] = path.read_text(encoding="utf-8")
            logger.debug(f"Loaded knowledge: {path.stem}")
        except Exception as e:
            logger.error(f"Failed to load {path}: {e}")
            
    logger.info(f"Loaded {len(texts)} knowledge files")
    return texts

knowledge_texts = load_knowledge()
