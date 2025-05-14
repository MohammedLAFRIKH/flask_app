# deploy.ps1

try {
    # 1. Vérifier si l'environnement virtuel existe
    $env_dir = "venv"
    if (-Not (Test-Path $env_dir)) {
        Write-Host "Environnement virtuel non trouvé. Création en cours..."
        python -m venv $env_dir
        Write-Host "Environnement virtuel créé."
    }

    # 2. Activer l'environnement virtuel
    Write-Host "Activation de l'environnement virtuel..."
    $env_path = ".\$env_dir\Scripts\Activate.ps1"
    & $env_path

    # 3. Installer les dépendances
    Write-Host "Installation des dépendances..."
    pip install -r requirements.txt

    Write-Output "Setting up environment..."
    $env:FLASK_APP = "app.py"
    $env:FLASK_ENV = "development"

    # 4. Démarrer l'application Flask
    Write-Host "Démarrage de l'application Flask..."
    flask run
} catch {
    Write-Output "An error occurred: $_"
    exit 1
}
