pipeline {
    agent any

    environment {
        PYTHON = 'C:/Users/MOHAMMED LAFRIKH/AppData/Local/Programs/Python/Python311/python.exe'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/aya-cyber/flask_app.git'
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

        stage('Run Flask App') {
            steps {
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
