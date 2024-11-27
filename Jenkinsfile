pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'flask-app'    // Name of the Docker image
        DOCKER_TAG = 'latest'         // Tag for the Docker image
        APP_PORT = '5000'             // Port where the Flask app will run
        APP_URL = "http://localhost:${APP_PORT}"  // URL for testing the app
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Checking out code from GitHub repository...'
                git 'https://github.com/vpvishalparmar1601/localfile.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    sh 'docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .'
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    echo 'Stopping and removing any previous containers...'
                    sh 'docker ps -q --filter "name=${DOCKER_IMAGE}" | xargs -r docker stop'
                    sh 'docker ps -a -q --filter "name=${DOCKER_IMAGE}" | xargs -r docker rm'

                    echo 'Running Docker container...'
                    sh 'docker run -d -p ${APP_PORT}:${APP_PORT} --name ${DOCKER_IMAGE} ${DOCKER_IMAGE}:${DOCKER_TAG}'
                }
            }
        }

        stage('Test Flask App') {
            steps {
                script {
                    // Test the Flask application
                    sh 'curl -I http://localhost:5000 || echo "Flask app not responding"'
                }
            }
        }

        stage('Clean Up') {
            steps {
                script {
                    echo 'Cleaning up Docker containers and images...'
                    sh '''
                    docker ps -a -q --filter "ancestor=${DOCKER_IMAGE}:${DOCKER_TAG}" | xargs -r docker rm -f || true
                    docker images -q ${DOCKER_IMAGE}:${DOCKER_TAG} | xargs -r docker rmi -f || true
                    '''
                }
            }
        }
    }

    post {
        always {
            script {
                echo 'Final cleanup to ensure no lingering Docker containers or images...'
                sh '''
                docker ps -a -q --filter "name=${DOCKER_IMAGE}" | xargs -r docker rm -f || true
                docker images -q ${DOCKER_IMAGE}:${DOCKER_TAG} | xargs -r docker rmi -f || true
                '''
            }
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the logs for errors.'
        }
    }
}
