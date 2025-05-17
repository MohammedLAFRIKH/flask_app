pipeline {
    agent any

    environment {
        PYTHON = 'C:/Users/MOHAMMED LAFRIKH/AppData/Local/Programs/Python/Python311/python.exe'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/aya-cyber/flask_app.git'
<<<<<<< HEAD
            }
        }

        
        stage('Run Tests') {
            steps {
                bat "\"${env.PYTHON}\" -m pytest --junitxml=reports/test-results.xml"
            }
            post {
                always {
                    junit 'reports/test-results.xml'
                }
            }
        }

        stage('Static & Security Analysis') {
            steps {
                echo 'Analyse statique avec flake8...'
                bat "\"${env.PYTHON}\" -m pip install flake8"
                bat "\"${env.PYTHON}\" -m flake8 ."

                echo 'Analyse sécurité avec bandit...'
                bat "\"${env.PYTHON}\" -m pip install bandit"
                bat "\"${env.PYTHON}\" -m bandit -r ."
            }
        }

        stage('Run Flask App') {
            steps {
=======
            }
        }

        stage('Install Dependencies') {
            steps {
                bat "\"${env.PYTHON}\" -m pip install --upgrade pip"
                bat "\"${env.PYTHON}\" -m pip install -r requirements.txt"
            }
        }

        stage('Run Flask App') {
            steps {
>>>>>>> 1c4a14049d33759c849a32a0ddb3376feaec16c4
                bat "start /B \"${env.PYTHON}\" app.py"
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
