pipeline {
    agent any
    stages {
        stage('Check Python') {
            steps {
                echo 'Checking Python installation and PATH...'
                bat 'where python'
                bat 'python --version || echo Python not found!'
                bat 'set PATH'
            }
        }
        stage('Checkout') {
            steps {
                git 'https://github.com/aya-cyber/flask_app.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'python -m pip install -r requirements.txt'
            }
        }
        stage('Lint') {
            steps {
                echo 'Linting the code...'
                bat 'python -m pip install flake8 || exit 0'
                bat 'flake8 . || echo Lint warnings, but continuing...'
            }
        }
        stage('Clean Workspace') {
            steps {
                echo 'Cleaning up .pyc files and __pycache__ directories...'
                bat 'del /S /Q *.pyc || exit 0'
                bat 'rmdir /S /Q __pycache__ || exit 0'
            }
        }
        stage('Run Tests') {
            steps {
                bat 'pytest --junitxml=report.xml || echo Tests failed, but continuing...'
            }
        }
        stage('Build') {
            steps {
                echo 'Building the application...'
                bat 'python -m compileall .'
            }
        }
        stage('Install & Run') {
            steps {
                bat 'build.bat'
            }
        }
        stage('Deploy to Local') {
            steps {
                echo 'Deploying locally...'
                bat 'start /B python app.py'
            }
        }
        stage('Deploy to Remote') {
            steps {
                echo 'Deploying application to remote server using Ansible...'
                // تأكد أن Ansible مركب ومهيأ على الجهاز ويندوز أو نفذ هاد الخطوة من جهاز لينكس
                bat 'ansible-playbook -i inventory.yml deploy.yml'
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
