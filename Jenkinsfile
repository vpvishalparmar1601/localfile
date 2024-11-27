pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'flask-app'          // Docker image name
        DOCKER_TAG = 'latest'               // Docker image tag
        APP_PORT = '5000'                   // Flask app port
        APP_URL = "http://localhost:${APP_PORT}" // URL to test the app
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Checking out code from GitHub repository...'
                git 'https://github.com/vpvishalparmar1601/localfile.git'
            }
        }

        stage('Detect Changes in main.py') {
            steps {
                script {
                    def checksumBefore = sh(script: "md5sum main.py | awk '{print \$1}'", returnStdout: true).trim()
                    echo "Previous checksum: ${checksumBefore}"
                    sh 'cp main.py /tmp/main.py.backup || true' // Backup main.py
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def checksumAfter = sh(script: "md5sum main.py | awk '{print \$1}'", returnStdout: true).trim()
                    echo "Current checksum: ${checksumAfter}"

                    if (checksumAfter != checksumBefore) {
                        echo 'main.py changed. Rebuilding Docker image...'
                        sh 'docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .'
                    } else {
                        echo 'No changes in main.py. Skipping build.'
                    }
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
                    
                    if (response.contains('hello my application is working')) {
                        echo "Flask app test successful!"
                    } else {
                        error("Flask app test failed: Response was '${response}'")
                    }
                }
            }
        }

        stage('Clean Up') {
            steps {
                script {
                    echo 'Cleaning up Docker containers and images...'
                    sh '''
                    docker ps -a -q --filter "name=${DOCKER_IMAGE}" | xargs -r docker rm -f || true
                    docker images -q ${DOCKER_IMAGE}:${DOCKER_TAG} | xargs -r docker rmi -f || true
                    '''
                }
            }
        }
    }

    post {
        always {
            script {
                echo 'Ensuring no lingering Docker containers or images...'
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
            echo 'Pipeline failed. Check the logs for details.'
        }
    }
}
