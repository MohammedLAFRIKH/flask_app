pipeline {
    agent any

    environment {
        PYTHON = 'C:/Users/MOHAMMED LAFRIKH/AppData/Local/Programs/Python/Python311/python.exe'
        VENV_DIR = 'venv'
        VENV_PYTHON = "${env.VENV_DIR}\\Scripts\\python.exe"
        REPORTS_DIR = 'reports'
        LOGS_DIR = 'logs'
    }

    options {
        // Garde les 10 dernières builds pour éviter surcharge disque
        buildDiscarder(logRotator(numToKeepStr: '10'))
        // Timeout global de la pipeline (ex: 30 minutes)
        timeout(time: 30, unit: 'MINUTES')
        // Affiche les sorties de commande en temps réel (utile pour debugging)
        ansiColor('xterm')
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo '🔄 Clonage du dépôt Git...'
                git branch: 'main', url: 'https://github.com/aya-cyber/flask_app.git'
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                echo "⚙️ Création et activation de l'environnement virtuel '${env.VENV_DIR}'..."
                bat """
                if exist ${env.VENV_DIR} (
                    echo Suppression de l'ancien environnement virtuel...
                    rmdir /s /q ${env.VENV_DIR}
                )
                \"${env.PYTHON}\" -m venv ${env.VENV_DIR}
                call \"${env.VENV_DIR}\\Scripts\\activate.bat\"
                \"${env.VENV_PYTHON}\" -m pip install --upgrade pip setuptools wheel
                """
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '📦 Installation des dépendances depuis requirements.txt...'
                bat """
                call \"${env.VENV_DIR}\\Scripts\\activate.bat\"
                \"${env.VENV_PYTHON}\" -m pip install -r requirements.txt
                """
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Exécution des tests avec pytest...'
                bat """
                if exist ${env.REPORTS_DIR} rmdir /s /q ${env.REPORTS_DIR}
                mkdir ${env.REPORTS_DIR}
                call \"${env.VENV_DIR}\\Scripts\\activate.bat\"
                \"${env.VENV_PYTHON}\" -m pytest --junitxml=${env.REPORTS_DIR}\\test-results.xml
                """
            }
            post {
                always {
                    junit "${env.REPORTS_DIR}/test-results.xml"
                }
            }
        }

        stage('Dependency Security Audit') {
            steps {
                echo '🔒 Audit de sécurité des dépendances avec pip-audit...'
                bat """
                call \"${env.VENV_DIR}\\Scripts\\activate.bat\"
                \"${env.VENV_PYTHON}\" -m pip show pip-audit >nul 2>&1 || \"${env.VENV_PYTHON}\" -m pip install pip-audit
                \"${env.VENV_PYTHON}\" -m pip_audit
                """
            }
        }

        stage('Clean Workspace') {
            steps {
                echo '🧹 Nettoyage de l’espace de travail Jenkins...'
                cleanWs()
            }
        }

        stage('Run Flask App (Production)') {
            when {
                expression { currentBuild.currentResult == 'SUCCESS' }
            }
            steps {
                echo '🚀 Lancement de l’application Flask en arrière-plan...'
                bat """
                if not exist ${env.LOGS_DIR} mkdir ${env.LOGS_DIR}
                start "FlaskApp" /B cmd /c \"call ${env.VENV_DIR}\\Scripts\\activate.bat && \"${env.VENV_PYTHON}\" app.py > ${env.LOGS_DIR}\\flask_app.log 2>&1\"
                """
            }
            post {
                always {
                    archiveArtifacts artifacts: "${env.LOGS_DIR}/flask_app.log", allowEmptyArchive: true
                }
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline terminée avec succès !'
        }
        failure {
            echo '❌ La pipeline a rencontré une erreur.'
        }
        always {
            echo '🏁 Fin de la pipeline.'
        }
    }
}
