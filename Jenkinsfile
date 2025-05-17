pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/aya-cyber/flask_app.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                bat 'py -3.11 -m pip install --upgrade pip'
                bat 'py -3.11 -m pip install -r requirements.txt'
            }
        }

        stage('Deploy to Local') {
            steps {
                echo 'Deploying locally...'
                bat 'start /B py -3.11 app.py'
            }
        }
    }
}
