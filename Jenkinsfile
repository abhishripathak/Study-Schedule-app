pipeline {
    agent {
        docker {
            image 'docker:24.0.5-dind' // or any stable Docker-in-Docker image
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        IMAGE_NAME = "studyplanner"
        IMAGE_TAG = "v1"
        FULL_IMAGE_NAME = "${IMAGE_NAME}:${IMAGE_TAG}"
        CONTAINER_NAME = "studyplanner_container"
        GIT_REPO_URL = 'https://github.com/abhishripathak/Study-Schedule-app.git'
        GIT_CREDENTIALS_ID = 'studyplan'
    }

    stages {
        stage('Checkout') {
            steps {
                echo '🔄 Checking out code from GitHub...'
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    extensions: [],
                    userRemoteConfigs: [[
                        url: "${GIT_REPO_URL}",
                        credentialsId: "${GIT_CREDENTIALS_ID}"
                    ]]
                ])
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh 'docker build -t $FULL_IMAGE_NAME .'
            }
        }

        stage('Cleanup Old Container (Optional)') {
            steps {
                echo '🧹 Cleaning up old containers (if any)...'
                sh 'docker rm -f $CONTAINER_NAME || true'
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Deploying application using Docker Compose...'
                sh 'docker-compose -f docker-compose.yml up -d'
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Running tests (if defined)...'
                // Example placeholder — adjust based on your project
                // sh 'docker run --rm $FULL_IMAGE_NAME pytest'
            }
        }
    }
}
