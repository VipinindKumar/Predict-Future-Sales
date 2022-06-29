pipeline {
    agent any
    stages {
        stage('Build') {
             environment {
                DISABLE_AUTH = 'true'
                DB_ENGINE    = 'sqlite'
            }
            steps {
                sh 'echo "Hello World"'
                sh '''
                    echo "Multiline shell steps works too"
                    ls -lah
                '''
                echo "Database engine is ${DB_ENGINE}"
                echo "DISABLE_AUTH is ${DISABLE_AUTH}"
                sh 'printenv'
            }
        }
        stage('Deploy') {
            steps {
                retry(3) {
                    sh 'echo "Deploy stage is working now"'
                }
            }
        }
    }
}
