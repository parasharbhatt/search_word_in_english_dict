pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {
        stage('Setup') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                bat 'python -m pytest --verbose --junit-xml=test-reports/results.xml --html=test-reports/report.html --self-contained-html --cov=. --cov-report=term-missing --cov-report=html:test-reports/coverage tests/'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                    publishHTML(target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'test-reports',
                        reportFiles: 'report.html',
                        reportName: 'Pytest Report'
                    ])
                    publishHTML(target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'test-reports/coverage',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                    archiveArtifacts artifacts: 'test-reports/**/*', fingerprint: true
                }
            }
        }

        stage('Build') {
            steps {
                bat 'python -m py_compile search_dict.py'
                bat 'pyinstaller --noconsole --onefile --add-data "data.json;." --name EnglishDictionarySearch search_dict.py'
            }
            post {
                success {
                    archiveArtifacts artifacts: 'dist/*.exe', fingerprint: true
                }
            }
        }
    }
}
