pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
        VENV_PYTHON = "${env.WORKSPACE}\\${env.VENV_DIR}\\Scripts\\python.exe"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Virtualenv') {
            steps {
                bat """
                if exist ${VENV_DIR} rmdir /s /q ${VENV_DIR}
                python -m venv ${VENV_DIR}
                \"${VENV_PYTHON}\" -m pip install --upgrade pip setuptools wheel
                """
            }
        }

        stage('Install Dependencies') {
            steps {
                // Si tu as un fichier requirements.txt, utilise cette ligne : 
                // sinon remplace par l'installation directe de pytest
                
                bat """
                if exist requirements.txt (
                    \"${VENV_PYTHON}\" -m pip install -r requirements.txt
                ) else (
                    \"${VENV_PYTHON}\" -m pip install pytest
                )
                """
            }
        }

        stage('Run Tests') {
            steps {
                bat """
                if not exist reports mkdir reports
                \"${VENV_PYTHON}\" -m pytest --junitxml=reports/test-results.xml
                """
            }
            post {
                always {
                    junit 'reports/test-results.xml'
                }
            }
        }

        // Ajoute d’autres stages si besoin, par exemple déploiement, audit, etc.
    }

    post {
        failure {
            echo '❌ Une erreur est survenue.'
        }
    }
}
