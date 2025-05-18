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
                if not exist %VENV_DIR% (
                    "%PYTHON_PATH%" -m venv %VENV_DIR%
                )
                """
            }
        }

        stage('Install Dependencies') {
            steps {
                bat """
                set "VENV_PYTHON=%WORKSPACE%\\%VENV_DIR%\\Scripts\\python.exe"
                set "PATH=%WORKSPACE%\\%VENV_DIR%\\Scripts;%PATH%"
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
                """
            }
            post {
                always {
                    junit 'reports/test-results.xml'
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
