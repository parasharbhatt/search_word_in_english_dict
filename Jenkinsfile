pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'python3 -m py_compile search_dict.py'
            }
        }
        stage('Test') {
            steps {
                sh 'py.test --verbose --junit-xml test-reports/results.xml tests/test_SearchApp.py'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
        stage('Deliver') {
            steps {
                sh 'pyinstaller --onefile search_dict.py'
            }
            post {
                success {
                    archiveArtifacts 'dist/search_dict'
                }
            }
        }
    }
}
