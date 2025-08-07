Ce fichier est écrit en Markdown à la main.
Ce fichier a pour but de centraliser les informations essentielles pour le projet afin de faciliter les LLM à le comprendre et à répondre aux questions.

## Description du projet
Ce projet est un outil permettant d'interroger des documents de manière interactive.

## Prérequis
- Python et la possibilité de créer un environnement virtuel.
- Serveur Ollama installé localement et modèle téléchargé (ex. `mistral`).
- Dépendances Python listées dans `requirements.txt`.

## Configuration
1. Créer et activer un environnement virtuel puis installer les dépendances :
   ```bash
   python -m venv .venv
   source .venv/bin/activate      # ou équivalent sous Windows
   pip install -r requirements.txt
   ```
2. Copier `settings.example.json` vers `settings.json` et ajuster les champs principaux :
   - `project_root` : chemin du projet à analyser.
   - `extensions` : extensions de fichiers à indexer.
   - `skip_dirs` : dossiers ignorés lors du scan.
   - `request_timeout` : délai maximal des requêtes vers Ollama.
   - `base_url` : URL du serveur Ollama.

## Fonctionnement de l'application
1. Vérifie que le serveur Ollama est accessible.
2. Supprime d'éventuelles variables de proxy et désactive la télémétrie afin de rester entièrement local.
3. Charge la configuration et parcourt le projet pour lire les fichiers ciblés.
4. Crée un index vectoriel avec `llama-index` et des embeddings générés par Ollama.
5. Ouvre une interface web `Gradio` pour poser des questions. L'option `--debug` affiche les étapes détaillées.

## Scripts utilitaires
- `reset-env.sh` et `reset-env.cmd` réinitialisent l'environnement Python, installent les dépendances et lancent l'application.

## Structure simplifiée du dépôt
```
doc-chat/
├── app.py
├── requirements.txt
├── settings.example.json
├── reset-env.sh / reset-env.cmd
└── README.md
```

## Licence
Projet distribué sous licence MIT.
