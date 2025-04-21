pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Run Tests') {
            steps {
                sh 'python manage.py test'
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Deployment steps would go here'
            }
        }
    }
}
