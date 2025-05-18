pipeline {
    agent any

    environment {
        VENV = 'venv'
        VENV_PYTHON = 'venv\\Scripts\\python.exe'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/aya-cyber/flask_app.git'
            }
        }

        stage('Setup Virtualenv') {
            steps {
                bat '''
                echo [INFO] Suppression de l'ancien venv s'il existe...
                if exist venv rmdir /s /q venv

                echo [INFO] Détection de Python...
                where python > python_path.txt 2>nul
                if not exist python_path.txt (
                    echo [ERREUR] Python n'a pas été trouvé dans le PATH.
                    exit /b 1
                )

                set /p PY_PATH=<python_path.txt
                del python_path.txt

                echo [INFO] Python détecté: %PY_PATH%
                call "%PY_PATH%" -m venv venv
                call "venv\\Scripts\\python.exe" -m pip install --upgrade pip setuptools wheel
                '''
            }
        }

        stage('Install & Quality (Test)') {
            steps {
                bat '''
                call "venv\\Scripts\\python.exe" -m pip install -r requirements.txt
                call "venv\\Scripts\\python.exe" -m pip show flake8 >nul 2>&1 || call "venv\\Scripts\\python.exe" -m pip install flake8
                call "venv\\Scripts\\python.exe" -m pip show bandit >nul 2>&1 || call "venv\\Scripts\\python.exe" -m pip install bandit
                call "venv\\Scripts\\python.exe" -m flake8 . --format=xml --output-file=flake8-report.xml
                call "venv\\Scripts\\python.exe" -m bandit -r . -f xml -o bandit-report.xml
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'flake8-report.xml,bandit-report.xml', allowEmptyArchive: true
                }
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                if not exist reports mkdir reports
                call "venv\\Scripts\\python.exe" -m pytest --junitxml=reports/test-results.xml
                '''
            }
            post {
                always {
                    junit 'reports/test-results.xml'
                }
            }
        }

        stage('Dependency Security Audit') {
            steps {
                bat '''
                call "venv\\Scripts\\python.exe" -m pip show pip-audit >nul 2>&1 || call "venv\\Scripts\\python.exe" -m pip install pip-audit
                call "venv\\Scripts\\python.exe" -m pip_audit
                '''
            }
        }

        stage('Run Flask App (Production)') {
            when {
                expression { currentBuild.currentResult == 'SUCCESS' }
            }
            steps {
                bat 'start "FlaskApp" /B "venv\\Scripts\\python.exe" app.py > flask_app.log 2>&1'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'flask_app.log', allowEmptyArchive: true
                }
            }
        }

        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }
    }

    post {
        success {
            echo '✅ Déploiement local terminé avec succès.'
        }
        failure {
            echo '❌ Une erreur est survenue.'
        }
    }
}
