pipeline {
    agent any
    stages {
        stage('Deploy to Local') {
            steps {
                echo 'Deploying locally...'
                bat 'start /B "C:\\Users\\MOHAMMED LAFRIKH\\AppData\\Local\\Microsoft\\WindowsApps\\python3.11.exe" app.py'
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
