pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                bat 'python -m py_compile search_dict.py'
            }
        }
        stage('Test') {
            steps {
                bat 'py.test --verbose --junit-xml test-reports/results.xml tests/test_SearchApp.py'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
        stage('Deliver') {
            steps {
                bat 'python -m pyinstaller --onefile search_dict.py'
            }
            post {
                success {
                    archiveArtifacts 'dist/search_dict'
                }
            }
        }
    }
}
