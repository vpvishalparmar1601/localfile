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

                    echo 'Getting logs from the Flask app container...'
                    sh 'docker logs ${DOCKER_IMAGE}'
                }
            }
        }

        stage('Wait for Flask App to be Ready') {
            steps {
                script {
                    echo 'Waiting for Flask app to be ready...'
                    waitUntil {
                        script {
                            def response = sh(script: "curl -s -o /dev/null -w '%{http_code}' ${APP_URL}", returnStdout: true).trim()
                            return response == '200'
                        }
                    }
                    echo "Flask app is now accessible!"
                }
            }
        }

        stage('Test Flask App') {
            steps {
                script {
                    echo "Testing Flask application at ${APP_URL}..."
                    def response = sh(script: "curl -s ${APP_URL}", returnStdout: true).trim()
                    if (response.contains('Flask app is running!')) {
                        echo "Flask app test successful!"
                    } else {
                        error("Flask app test failed: Response was '${response}'")
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully! The Flask app is running on http://localhost:5000.'
        }
        failure {
            echo 'Pipeline failed. Check the logs for details.'
        }
    }
}
