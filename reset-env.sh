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

  # 🚀 Lancer l'application
  echo "🚀 Lancement de l'assistant IA..."
  python app.py
