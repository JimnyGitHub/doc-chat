import json
from pathlib import Path
import requests
import argparse
import logging

from llama_index.core import Document, VectorStoreIndex
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.settings import Settings
import gradio as gr

# ── arguments & journalisation ───────────────────────────────
parser = argparse.ArgumentParser(
    description="Assistant IA local pour interroger la documentation")
parser.add_argument(
    "--debug", action="store_true",
    help="affiche le déroulé complet du chargement")
args = parser.parse_args()

logging.basicConfig(
    level=logging.DEBUG if args.debug else logging.INFO,
    format="%(message)s")
logger = logging.getLogger(__name__)

# ── 0) vérification du serveur Ollama ───────────────────────
def check_ollama(url: str = "http://localhost:11434") -> None:
    """Vérifie que le serveur Ollama est disponible."""
    logger.debug("Connexion au serveur Ollama…")
    try:
        r = requests.get(f"{url}/api/tags", timeout=5)
        r.raise_for_status()
    except Exception as e:
        raise SystemExit(
            f"Ollama semble indisponible sur {url}. Lancez `ollama serve` ou `ollama run mistral` dans un autre terminal."
        ) from e
    logger.debug("Serveur Ollama prêt")

logger.debug("Étape 0 : vérification du serveur")
check_ollama()

# ── 1) chemin projet ────────────────────────────────────────
logger.debug("Étape 1 : lecture de la configuration")
with open("settings.json") as f:
    cfg = json.load(f)

root = Path(cfg["project_root"]).resolve()
# Extensions à prendre en compte, exemple : [".md", ".adoc"]
exts = {e.lower() for e in cfg.get("extensions", [".md", ".adoc", ".puml"])}
if not root.exists():
    raise FileNotFoundError(root)
logger.debug(f"Racine du projet : {root}")
logger.debug(f"Extensions : {', '.join(sorted(exts))}")

# ── 2) lecture fichiers ─────────────────────────────────────
logger.debug("Étape 2 : analyse des fichiers")
docs = []
# Dossiers à exclure pour accélérer le scan
skip_dirs = {".git", ".venv", "node_modules", "target"}
for f in root.rglob("*"):
    # Ignorer les fichiers situés dans les dossiers exclus
    if any(part in skip_dirs for part in f.parts):
        continue
    if f.is_file() and f.suffix.lower() in exts:
        try:
            logger.debug(f"Lecture de {f}")
            docs.append(Document(text=f.read_text(encoding="utf-8"),
                                 metadata={"path": str(f)}))
        except Exception as e:
            logger.warning(f"⚠️ {f} ignoré — {e}")
if not docs:
    raise ValueError(
        "Aucun fichier correspondant aux extensions "
        f"{', '.join(sorted(exts))} trouvé"
    )
logger.debug(f"{len(docs)} fichiers chargés")

# ── 3) config 100 % locale ──────────────────────────────────
logger.debug("Étape 3 : configuration des modèles")
Settings.llm         = Ollama(model="mistral")
Settings.embed_model = OllamaEmbedding(model_name="mistral")

# ── 4) index & moteur ───────────────────────────────────────
logger.debug("Étape 4 : création de l'index")
index  = VectorStoreIndex.from_documents(docs)     # Settings déjà peuplé
engine = index.as_query_engine()

# ── 5) interface ────────────────────────────────────────────
def chat(q): return str(engine.query(q))

logger.debug("Étape 5 : lancement de l'interface web")
gr.Interface(chat, "text", "text",
             title="Assistant IA – Doc projet Java").launch()
