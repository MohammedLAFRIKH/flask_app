pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
        PYTHON_PATH = "C:\\Users\\MOHAMMED LAFRIKH\\AppData\\Local\\Programs\\Python\\Python311\\python.exe"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                bat """
                if exist %VENV_DIR% rd /s /q %VENV_DIR%
                "%PYTHON_PATH%" -m venv %VENV_DIR%
                """
            }
        }

        stage('Install Dependencies') {
            steps {
                bat """
                set "VENV_PYTHON=%WORKSPACE%\\%VENV_DIR%\\Scripts\\python.exe"
                set "PATH=%WORKSPACE%\\%VENV_DIR%\\Scripts;%PATH%"
                where python
                echo %PATH%
                rem Vérification du python du venv
                "%VENV_PYTHON%" --version
                "%VENV_PYTHON%" -m pip --version
                call "%VENV_PYTHON%" -m pip install --upgrade pip
                if exist requirements.txt (
                    call "%VENV_PYTHON%" -m pip install -r requirements.txt
                ) else (
                    call "%VENV_PYTHON%" -m pip install flask pytest
                )
                """
            }
        }

        stage('Run Tests') {
            steps {
                bat """
                if not exist reports mkdir reports
                set "VENV_PYTHON=%WORKSPACE%\\%VENV_DIR%\\Scripts\\python.exe"
                call "%VENV_PYTHON%" -m pytest --junitxml=reports/test-results.xml

                rem === Idée : Générer un rapport de couverture de code ===
                call "%VENV_PYTHON%" -m pip show coverage >nul 2>&1 || call "%VENV_PYTHON%" -m pip install coverage
                call "%VENV_PYTHON%" -m coverage run -m pytest
                call "%VENV_PYTHON%" -m coverage xml -o reports/coverage.xml

                rem === BONUS : Générer un rapport HTML de couverture ===
                call "%VENV_PYTHON%" -m coverage html -d reports/htmlcov

                rem === BONUS : Afficher la couverture dans la console ===
                call "%VENV_PYTHON%" -m coverage report

                rem === AFKAR : Générer un rapport requirements.txt figé (pour reproductibilité)
                call "%VENV_PYTHON%" -m pip freeze > reports/requirements-freeze.txt

                rem === AFKAR : Vérifier la sécurité des dépendances (pip-audit)
                call "%VENV_PYTHON%" -m pip show pip-audit >nul 2>&1 || call "%VENV_PYTHON%" -m pip install pip-audit
                call "%VENV_PYTHON%" -m pip_audit > reports/pip-audit.txt

                rem === AFKAR : Générer un rapport de linting (flake8)
                call "%VENV_PYTHON%" -m pip show flake8 >nul 2>&1 || call "%VENV_PYTHON%" -m pip install flake8
                call "%VENV_PYTHON%" -m flake8 . --format=html --htmldir=reports/flake8-html || exit 0
                """
            }
            post {
                always {
                    junit 'reports/test-results.xml'
                    archiveArtifacts artifacts: 'reports/coverage.xml,reports/htmlcov/**,reports/requirements-freeze.txt,reports/pip-audit.txt,reports/flake8-html/**', allowEmptyArchive: true
                }
            }
        }
    }

    post {
        failure {
            echo '❌ Une erreur est survenue.'
        }
        success {
            echo '✅ Pipeline terminé avec succès.'
        }
    }
}
