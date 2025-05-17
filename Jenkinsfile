pipeline {
    agent any

    stages {
        stage('Checkout') {
steps {
                git branch: 'main', url: 'https://github.com/aya-cyber/flask_app.git'
            }
        }

         stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Flask App') {
            steps {
                bat 'start /B python app.py'
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
