pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                set PATH=C:\python3_12_1\python.exe;%PATH%
                python3 -m py_compile search_dict.py
            }
        }
        stage('Test') {
            steps {
                py.test --verbose --junit-xml test-reports/results.xml tests/test_SearchApp.py
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
        stage('Deliver') {
            steps {
                pyinstaller --onefile search_dict.py
            }
            post {
                success {
                    archiveArtifacts 'dist/search_dict'
                }
            }
        }
    }
}
