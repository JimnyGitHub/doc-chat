#!/bin/bash

set -e  # Stopper si une commande échoue

# 🛑 Désactiver un éventuel environnement actif
if [[ "$VIRTUAL_ENV" != "" ]]; then
  echo "🔌 Désactivation de l'environnement Python actif..."
  deactivate
fi

# 🧹 Supprimer l'ancien venv
echo "🗑 Suppression de l'ancien .venv..."
rm -rf .venv

# 🆕 Créer un nouveau venv
echo "🐍 Création du nouvel environnement virtuel..."
python3 -m venv .venv

# ✅ Activer
echo "✅ Activation de l'environnement..."
source .venv/bin/activate

# 📦 Installer les dépendances
echo "📦 Installation des dépendances depuis requirements.txt..."
pip install --no-cache-dir -r requirements.txt

# ▶️ Vérifier la disponibilité d'Ollama
if ! command -v ollama >/dev/null; then
  echo "❌ Ollama est introuvable. Installez-le puis lancez 'ollama serve'."
  exit 1
fi
if ! curl -s http://localhost:11434/api/tags >/dev/null; then
  echo "🔄 Démarrage du serveur Ollama..."
  ollama serve >/dev/null 2>&1 &
  sleep 5
fi

# 🚀 Lancer l'application
echo "🚀 Lancement de l'assistant IA..."
python app.py --debug
