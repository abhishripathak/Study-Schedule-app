pipeline {
    agent any

    environment {
        IMAGE_NAME = "studyplanner"  // Adjusted to your project name
        IMAGE_TAG = "v1"
        FULL_IMAGE_NAME = "${IMAGE_NAME}:${IMAGE_TAG}"
        CONTAINER_NAME = "studyplanner_container"  // Adjusted to your project container name
        GIT_REPO_URL = 'https://github.com/abhishripathak/Study-Schedule-app.git'  // Your GitHub repo URL
        GIT_CREDENTIALS_ID = 'studyplan'  // Use the correct credentials ID for Jenkins
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout([ 
                    $class: 'GitSCM', 
                    branches: [[name: '*/main']], 
                    extensions: [], 
                    userRemoteConfigs: [[ 
                        url: GIT_REPO_URL, 
                        credentialsId: GIT_CREDENTIALS_ID 
                    ]] 
                ])
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    sh 'docker build -t $FULL_IMAGE_NAME .'  // Builds the Docker image with the correct name and tag
                }
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running tests (if any)...'
                // Example: sh 'docker run --rm $FULL_IMAGE_NAME pytest'
                // Add your test commands if needed
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application using Docker Compose...'
                script {
                    sh 'docker-compose -f docker-compose.yml up -d'  // Deploys with Docker Compose
                }
            }
        }

        stage('Cleanup Old Container (Optional)') {
            steps {
                echo 'Cleaning up old containers...'
                script {
                    sh "docker rm -f $CONTAINER_NAME || true"  // Removes old containers if any
                }
            }
        }
    }
}
