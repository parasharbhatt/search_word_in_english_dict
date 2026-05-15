pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                C:\PROGRA~1\Git\bin\sh.exe 'python3 -m py_compile search_dict.py'
            }
        }
        stage('Test') {
            steps {
                C:\PROGRA~1\Git\bin\sh.exe 'py.test --verbose --junit-xml test-reports/results.xml tests/test_SearchApp.py'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
        stage('Deliver') {
            steps {
                C:\PROGRA~1\Git\bin\sh.exe 'pyinstaller --onefile search_dict.py'
            }
            post {
                success {
                    archiveArtifacts 'dist/search_dict'
                }
            }
        }
    }
}
