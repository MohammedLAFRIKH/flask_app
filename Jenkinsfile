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

        stage('Run Tests & Reports') {
            steps {
                bat """
                if not exist reports mkdir reports
                set "VENV_PYTHON=%WORKSPACE%\\%VENV_DIR%\\Scripts\\python.exe"

                rem -- Tests unitaires
                call "%VENV_PYTHON%" -m pytest --junitxml=reports/test-results.xml

                rem -- Couverture de code XML et HTML
                call "%VENV_PYTHON%" -m pip show coverage >nul 2>&1 || call "%VENV_PYTHON%" -m pip install coverage
                call "%VENV_PYTHON%" -m coverage run -m pytest
                call "%VENV_PYTHON%" -m coverage xml -o reports/coverage.xml
                call "%VENV_PYTHON%" -m coverage html -d reports/htmlcov
                call "%VENV_PYTHON%" -m coverage report

                rem -- Geler les dépendances
                call "%VENV_PYTHON%" -m pip freeze > reports/requirements-freeze.txt

                rem -- Audit sécurité des dépendances
                call "%VENV_PYTHON%" -m pip show pip-audit >nul 2>&1 || call "%VENV_PYTHON%" -m pip install pip-audit
                call "%VENV_PYTHON%" -m pip_audit > reports/pip-audit.txt

                rem -- Linting flake8 (HTML + XML)
                call "%VENV_PYTHON%" -m pip show flake8 >nul 2>&1 || call "%VENV_PYTHON%" -m pip install flake8
                call "%VENV_PYTHON%" -m flake8 . --format=html --htmldir=reports/flake8-html || exit 0
                call "%VENV_PYTHON%" -m flake8 . --format=xml --output-file=reports/flake8-report.xml || exit 0
                """
            }
            post {
                always {
                    junit 'reports/test-results.xml'
                    archiveArtifacts artifacts: 'reports/coverage.xml,reports/htmlcov/**,reports/requirements-freeze.txt,reports/pip-audit.txt,reports/flake8-html/**,reports/flake8-report.xml', allowEmptyArchive: true
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
