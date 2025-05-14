pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/MohammedLAFRIKH/flask_app.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'pytest || echo "Tests failed, but continuing..."'
            }
        }
        stage('Build') {
            steps {
                echo 'Building the application...'
                sh 'python -m compileall .'
            }
        }
        stage('Deploy to Local') {
            steps {
                sh 'cd "c:\Users\MOHAMMED LAFRIKH\Desktop\flask_app"'
                sh 'python app.py'
            }
        }
        stage('Deploy to Remote') {
            steps {
                echo 'Deploying application to remote server using Ansible...'
                sh 'ansible-playbook -i inventory.yml deploy.yml'
            }
        }
    }
    post {
        always {
            echo 'Pipeline execution completed.'
        }
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
    }
}
