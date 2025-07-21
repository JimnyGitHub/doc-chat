import json
from pathlib import Path
import requests

from llama_index.core import Document, VectorStoreIndex
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.settings import Settings
import gradio as gr

# ── 0) vérification du serveur Ollama ───────────────────────
def check_ollama(url: str = "http://localhost:11434") -> None:
    """Vérifie que le serveur Ollama est disponible."""
    try:
        r = requests.get(f"{url}/api/tags", timeout=5)
        r.raise_for_status()
    except Exception as e:
        raise SystemExit(
            f"Ollama semble indisponible sur {url}. Lancez `ollama serve` ou `ollama run mistral` dans un autre terminal."
        ) from e

check_ollama()

# ── 1) chemin projet ────────────────────────────────────────
with open("settings.json") as f:
    cfg = json.load(f)

root = Path(cfg["project_root"]).resolve()
# Extensions à prendre en compte, exemple : [".md", ".adoc"]
exts = {e.lower() for e in cfg.get("extensions", [".md", ".adoc", ".puml"])}
if not root.exists():
    raise FileNotFoundError(root)

# ── 2) lecture fichiers ─────────────────────────────────────
docs = []
# Dossiers à exclure pour accélérer le scan
skip_dirs = {".git", ".venv", "node_modules", "target"}
for f in root.rglob("*"):
    # Ignorer les fichiers situés dans les dossiers exclus
    if any(part in skip_dirs for part in f.parts):
        continue
    if f.is_file() and f.suffix.lower() in exts:
        try:
            docs.append(Document(text=f.read_text(encoding="utf-8"),
                                 metadata={"path": str(f)}))
        except Exception as e:
            print(f"⚠️ {f} ignoré — {e}")
if not docs:
    raise ValueError(
        "Aucun fichier correspondant aux extensions "
        f"{', '.join(sorted(exts))} trouvé"
    )

# ── 3) config 100 % locale ──────────────────────────────────
Settings.llm         = Ollama(model="mistral")
Settings.embed_model = OllamaEmbedding(model_name="mistral")

# ── 4) index & moteur ───────────────────────────────────────
index  = VectorStoreIndex.from_documents(docs)     # Settings déjà peuplé
engine = index.as_query_engine()

# ── 5) interface ────────────────────────────────────────────
def chat(q): return str(engine.query(q))

gr.Interface(chat, "text", "text",
             title="Assistant IA – Doc projet Java").launch()
