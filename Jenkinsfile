pipeline {
    agent {
        docker {
            image 'python:3.11'
        }
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code...'
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/abhishripathak/Study-Schedule-app.git',
                        credentialsId: 'studyplan'
                    ]]
                ])
            }
        }

        stage('Setup Environment') {
            steps {
                echo 'Installing dependencies...'
                sh '''
                    python -m ensurepip --upgrade
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running tests (if any)...'
                // Example: sh 'pytest'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying...'
                sh 'docker-compose up -d'
            }
        }
    }
}
