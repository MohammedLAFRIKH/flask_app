pipeline {
    agent any

    environment {
        PYTHON = 'C:/Users/MOHAMMED LAFRIKH/AppData/Local/Programs/Python/Python311/python.exe'
        VENV = 'venv'
        VENV_PYTHON = 'venv\\Scripts\\python.exe'
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 30, unit: 'MINUTES')
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/aya-cyber/flask_app.git'
            }
        }

        stage('Setup Virtualenv') {
            steps {
                bat """
                if exist ${env.VENV} rmdir /s /q ${env.VENV}
                \"${env.PYTHON}\" -m venv ${env.VENV}
                \"${env.VENV_PYTHON}\" -m pip install --upgrade pip setuptools wheel
                """
            }
        }

        // Stage 'Install & Quality (Test)' commenté pour désactiver les tests qualité
        /*
        stage('Install & Quality (Test)') {
            steps {
                bat """
                \"${env.VENV_PYTHON}\" -m pip install -r requirements.txt
                \"${env.VENV_PYTHON}\" -m pip show flake8 >nul 2>&1 || \"${env.VENV_PYTHON}\" -m pip install flake8
                \"${env.VENV_PYTHON}\" -m pip show bandit >nul 2>&1 || \"${env.VENV_PYTHON}\" -m pip install bandit
                echo Running flake8...
                \"${env.VENV_PYTHON}\" -m flake8 . --format=xml --output-file=flake8-report.xml
                if %ERRORLEVEL% NEQ 0 (
                    echo [ERROR] Erreurs de style détectées par flake8.
                    exit /b %ERRORLEVEL%
                )
                echo Running bandit...
                \"${env.VENV_PYTHON}\" -m bandit -r . -f xml -o bandit-report.xml
                if %ERRORLEVEL% NEQ 0 (
                    echo [ERROR] Problèmes de sécurité détectés par bandit.
                    exit /b %ERRORLEVEL%
                )
                """
            }
            post {
                always {
                    archiveArtifacts artifacts: 'flake8-report.xml,bandit-report.xml', allowEmptyArchive: true
                }
            }
        }
        */

        stage('Run Tests') {
            steps {
                bat """
                if not exist reports mkdir reports
                \"${env.VENV_PYTHON}\" -m pytest --junitxml=reports/test-results.xml
                """
            }
            post {
                always {
                    junit 'reports/test-results.xml'
                }
            }
        }

        stage('Dependency Security Audit') {
            steps {
                bat """
                \"${env.VENV_PYTHON}\" -m pip show pip-audit >nul 2>&1 || \"${env.VENV_PYTHON}\" -m pip install pip-audit
                \"${env.VENV_PYTHON}\" -m pip_audit
                """
            }
        }

        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }

        stage('Run Flask App (Production)') {
            when {
                expression { currentBuild.currentResult == 'SUCCESS' }
            }
            steps {
                bat 'start "FlaskApp" /B \"%CD%\\${env.VENV_PYTHON}\" app.py > flask_app.log 2>&1'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'flask_app.log', allowEmptyArchive: true
                }
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
// This Jenkinsfile is designed to automate the deployment of a Flask application.
// It includes stages for cloning the repository, setting up a virtual environment,