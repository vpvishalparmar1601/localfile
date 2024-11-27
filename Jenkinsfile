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
                    // Running the Docker container with port mapping and Flask binding to 0.0.0.0
                    sh 'docker run -d -p ${APP_PORT}:${APP_PORT} --name ${DOCKER_IMAGE} ${DOCKER_IMAGE}:${DOCKER_TAG}'

                    // Capture logs from the running container
                    echo 'Getting logs from the Flask app container...'
                    sh 'docker logs ${DOCKER_IMAGE}'
                }
            }
        }

        stage('Wait for Flask App to be Ready') {
            steps {
                script {
                    echo 'Waiting for Flask app to be ready...'
                    // Wait until the Flask app responds with 200 OK
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
                    def response = ""
                    def attempts = 0
                    def maxAttempts = 5
                    // Retry logic in case the Flask app is slow to start
                    while (attempts < maxAttempts) {
                        response = sh(script: "curl -I --max-time 10 ${APP_URL} | head -n 1", returnStdout: true).trim()
                        echo "Response: ${response}"
                        if (response.contains("200 OK")) {
                            echo "Flask app is running successfully!"
                            break
                        } else {
                            echo "Flask app is not ready, retrying..."
                            attempts++
                            sleep(time: 10, unit: 'SECONDS')
                        }
                    }
                    if (!response.contains("200 OK")) {
                        error("Flask app test failed: ${response}")
                    }
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
