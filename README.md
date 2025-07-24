# 🤖 doc-chat – Assistant IA local d'interrogation de docs de projet

**`doc-chat`** est un agent IA local qui vous permet d’interroger la documentation de n’importe quel projet à partir de ses fichiers `.md`, `.adoc`, `.puml`, etc.

Il fonctionne **en local**, sans cloud, grâce à [Ollama](https://ollama.com) et [llama-index](https://github.com/jerryjliu/llama_index).

---

## 🔧 Prérequis

### 1. 🐍 Installer Python (via Scoop pour Windows)

```powershell
scoop install python
```

Vérifiez l’installation :

```bash
python --version
```

---

### 2. 🤖 Installer Ollama

Suivre [https://ollama.com/download](https://ollama.com/download), puis télécharger le modèle par défaut (par exemple `mistral`) :

```bash
ollama run mistral
```

---

### 3. 📁 Préparer votre projet source

Votre projet doit contenir :

- des fichiers `README.md`, `README.adoc`, etc. 
- éventuellement un dossier `doc/` à la racine

---

## 🔄 Créer et utiliser un environnement Python isolé (`venv`)

### 🧪 Création du venv

Dans un terminal à la racine de `doc-chat` :

```bash
python -m venv .venv
```

### ▶️ Activation

**Sous PowerShell :**

```powershell
.venv\Scripts\Activate.ps1
```

**Sous CMD :**

```cmd
.venv\Scripts\activate.bat
```

**Sous Linux/macOS :**

```bash
source .venv/bin/activate
```

### 🛠️ Installation des dépendances

Une fois le `venv` activé :

```bash
pip install -r requirements.txt
```
Le paquet `ollama` doit être en version `>=0.5.1` afin d'être compatible avec
`llama-index-llms-ollama`. Le serveur **Ollama** peut rester en `0.1.x`, mais
il est recommandé de le garder à jour.
Ensuite, copiez le fichier d'exemple pour créer votre configuration locale :
```bash
cp settings.example.json settings.json
```

---

## ⚙️ Configuration

1. Copiez le fichier d'exemple :

```bash
cp settings.example.json settings.json
```

2. Modifiez le fichier `settings.json` pour indiquer le **chemin local** du projet, les extensions à indexer, les dossiers à ignorer et le délai maximal des requêtes :
```json
{
  "project_root": "../chemin/vers/mon-projet/",
  "extensions": [".md", ".adoc"],
  "skip_dirs": [".venv"],
  "request_timeout": 120,
}
```

Ce fichier est ignoré dans `.gitignore`.

La clé `request_timeout` indique, en secondes, le délai d'attente maximal pour les requêtes envoyées à Ollama (120 par défaut).

---

## 🚀 Lancer l’assistant

Une fois le venv activé et les dépendances installées :

```bash
python app.py [--debug]
```
L’option `--debug` affiche les étapes détaillées et la liste des fichiers lus.

Une interface web s’ouvrira automatiquement.

Si vous obtenez une erreur de type `RemoteProtocolError: Server disconnected`,
assurez‑vous que le serveur **Ollama** est bien lancé via `ollama serve` ou
`ollama run mistral` dans un autre terminal.

Si l'interface ne s'ouvre pas automatiquement, accédez-y via [http://localhost:7860](http://localhost:7860).

Lors de la première utilisation, lancez `ollama run mistral` une fois pour télécharger le modèle localement.

---

## 💬 Exemples de questions

- "Quels modules contient ce projet ?"
- "À quoi sert le fichier `doc/architecture.puml` ?"
- "Comment lancer l’application ?"

---

## 📁 Structure du projet

```
doc-chat/
├── app.py
├── requirements.txt
├── settings.example.json
├── README.md
├── .gitignore
└── .venv/              ← non versionné, généré localement
```

---

## 🛠️ Réinstallation rapide

```bash
git clone https://mon.gitlab/doc-chat.git
cd doc-chat
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp settings.example.json settings.json
# Modifier le fichier settings.json
ollama run mistral
python app.py
```

---

## ✅ Compatible avec Windows, Linux, macOS

Le projet est entièrement local et fonctionne sur toutes les plateformes compatibles avec Python et Ollama.

---

## 📄 Licence

Ce projet est distribué sous la licence MIT. Consultez le fichier [LICENSE](LICENSE) pour plus d'informations.
