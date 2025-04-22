pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_PROJECT_NAME = 'studyplanner'  // Modify to your project name if needed
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code...'
                checkout([ 
                    $class: 'GitSCM', 
                    branches: [[name: '*/main']], 
                    extensions: [], 
                    userRemoteConfigs: [[ 
                        url: 'https://github.com/abhishripathak/Study-Schedule-app.git', 
                        credentialsId: 'studyplan'  // Ensure this Jenkins credential ID exists
                    ]] 
                ])
            }
        }

        stage('Build') {
            steps {
                echo 'Building Docker Compose services...'
                script {
                    // Build the Docker images using Docker Compose
                    sh 'docker-compose -p $DOCKER_COMPOSE_PROJECT_NAME build'
                }
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Skipping tests for now...'
                // Add commands for running tests if applicable in your setup
                // Example: sh './run_tests.sh'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying the application using Docker Compose...'
                script {
                    // Deploy the Docker Compose services in detached mode
                    sh 'docker-compose -p $DOCKER_COMPOSE_PROJECT_NAME up -d'
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            // Cleanup steps can be added here, such as stopping containers if necessary
            // Example: sh 'docker-compose down'
        }

        success {
            echo 'Deployment successful!'
        }

        failure {
            echo 'Deployment failed. Check logs for errors.'
        }
    }
}
