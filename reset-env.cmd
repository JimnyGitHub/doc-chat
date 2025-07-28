@echo off
REM ── Arrête le script si une commande échoue ─────────

REM 🛑 Désactiver un éventuel environnement actif
if defined VIRTUAL_ENV (
    echo 🔌 Désactivation de l'environnement Python actif...
    call deactivate
)

REM 🧹 Supprimer l'ancien venv
echo 🗑 Suppression de l'ancien .venv...
if exist .venv rmdir /s /q .venv

REM 🆕 Créer un nouveau venv
echo 🐍 Création du nouvel environnement virtuel...
python -m venv .venv
if errorlevel 1 exit /b 1

REM ✅ Activer
echo ✅ Activation de l'environnement...
call .venv\Scripts\activate.bat

REM 📦 Installer les dépendances
echo 📦 Installation des dépendances depuis requirements.txt...
pip install --proxy http://127.0.0.1:8888 --trusted-host pypi.org --trusted-host files.pythonhosted.org --disable-pip-version-check --no-cache-dir -r requirements.txt
if errorlevel 1 exit /b 1

REM ▶️ Vérifier la disponibilité d'Ollama
where ollama >nul 2>nul
if errorlevel 1 (
    echo ❌ Ollama est introuvable. Installez-le puis lancez 'ollama serve'.
    exit /b 1
)

curl -s http://localhost:11434/api/tags >nul 2>nul
if errorlevel 1 (
    echo 🔄 Démarrage du serveur Ollama...
    start /b "" ollama serve >nul 2>&1
    timeout /t 5 >nul
)

REM 🚀 Lancer l'application
echo 🚀 Lancement de l'assistant IA...
python app.py --debug
