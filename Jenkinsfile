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
                if exist %VENV_DIR% rd /s /q %VENV_DIR%
                "%PYTHON_PATH%" -m venv %VENV_DIR%
                """
            }
        }

        stage('Install Dependencies') {
            steps {
                bat """
                set "VENV_PYTHON=%WORKSPACE%\\%VENV_DIR%\\Scripts\\python.exe"
                set "PATH=%WORKSPACE%\\%VENV_DIR%\\Scripts;%PATH%"
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

        stage('Run Tests & Reports') {
            steps {
                bat """
                if not exist reports mkdir reports
                set "VENV_PYTHON=%WORKSPACE%\\%VENV_DIR%\\Scripts\\python.exe"

                rem -- Nettoyage des fichiers pyc et caches avant tests
                for /r %%i in (*.pyc) do del "%%i"
                for /d /r %%d in (__pycache__) do rd /s /q "%%d"

                rem -- Tests unitaires avec affichage détaillé et arrêt sur première erreur
                call "%VENV_PYTHON%" -m pytest --maxfail=1 --disable-warnings -v --junitxml=reports/test-results.xml

                rem -- Couverture de code XML et HTML
                call "%VENV_PYTHON%" -m pip show coverage >nul 2>&1 || call "%VENV_PYTHON%" -m pip install coverage
                call "%VENV_PYTHON%" -m coverage run -m pytest
                call "%VENV_PYTHON%" -m coverage xml -o reports/coverage.xml
                call "%VENV_PYTHON%" -m coverage html -d reports/htmlcov
                call "%VENV_PYTHON%" -m coverage report

                rem -- Générer badge de couverture
                call "%VENV_PYTHON%" -m pip show coverage-badge >nul 2>&1 || call "%VENV_PYTHON%" -m pip install coverage-badge
                call "%VENV_PYTHON%" -m coverage_badge -o reports/coverage-badge.svg -f

                rem -- Geler les dépendances
                call "%VENV_PYTHON%" -m pip freeze > reports/requirements-freeze.txt

                rem -- Audit sécurité des dépendances
                call "%VENV_PYTHON%" -m pip show pip-audit >nul 2>&1 || call "%VENV_PYTHON%" -m pip install pip-audit
                call "%VENV_PYTHON%" -m pip_audit > reports/pip-audit.txt

                rem -- Linting flake8 (HTML + XML)
                call "%VENV_PYTHON%" -m pip show flake8 >nul 2>&1 || call "%VENV_PYTHON%" -m pip install flake8
                call "%VENV_PYTHON%" -m flake8 . --format=html --htmldir=reports/flake8-html || exit 0
                call "%VENV_PYTHON%" -m flake8 . --format=xml --output-file=reports/flake8-report.xml || exit 0

                rem -- AUTOMATISATION : Générer un changelog automatique (git log)
                git log -10 --pretty=format:"%%h - %%an, %%ar : %%s" > reports/last-commits.txt

                rem -- AUTOMATISATION : Générer un rapport de dépendances obsolètes
                call "%VENV_PYTHON%" -m pip show pip-review >nul 2>&1 || call "%VENV_PYTHON%" -m pip install pip-review
                call "%VENV_PYTHON%" -m pip_review --local > reports/pip-review.txt

                rem -- AUTOMATISATION : Générer un rapport requirements.txt trié
                call "%VENV_PYTHON%" -m pip freeze | sort > reports/requirements-sorted.txt
                """
            }
            post {
                always {
                    junit 'reports/test-results.xml'
                    archiveArtifacts artifacts: 'reports/coverage.xml,reports/htmlcov/**,reports/requirements-freeze.txt,reports/requirements-sorted.txt,reports/pip-audit.txt,reports/pip-review.txt,reports/flake8-html/**,reports/flake8-report.xml,reports/coverage-badge.svg,reports/last-commits.txt', allowEmptyArchive: true
                    // Pour publier les rapports HTML, assurez-vous d'installer le plugin "HTML Publisher" puis ajoutez ce bloc dans un script :
                    // script {
                    //     publishHTML(target: [reportDir: 'reports/htmlcov', reportFiles: 'index.html', reportName: 'Coverage Report', keepAll: true])
                    //     publishHTML(target: [reportDir: 'reports/flake8-html', reportFiles: 'index.html', reportName: 'Flake8 Lint Report', keepAll: true])
                    // }
                }
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline terminé avec succès.'
            // Tag Git automatique (nécessite credentials configurés dans Jenkins)
            script {
                def tagName = "build-${env.BUILD_NUMBER}"
                bat "git config --global user.email \"ayawahatezzaitoune2@gmail.com\""
                bat "git config --global user.name \"aya-cyber\""
                bat "git tag ${tagName}"
                bat "git push origin ${tagName}"
                echo "Tag ${tagName} créé et poussé."
            }
        }
        failure {
            echo '❌ Une erreur est survenue.'
        }
    }
}
