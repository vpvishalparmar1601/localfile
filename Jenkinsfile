pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'flask-app'          // Docker image name
        DOCKER_TAG = 'latest'               // Docker image tag
        APP_PORT = '5000'                   // Flask app port
        APP_URL = "http://localhost:${APP_PORT}" // URL to test the app
        CHECKSUM_FILE = "${WORKSPACE}/checksum.txt" // File to store checksum
    }

    triggers {
        // Trigger the pipeline when there is a change in the GitHub repository
        githubPush()  // This will trigger on any push to the GitHub repository
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
                    def currentChecksum = sh(
                        script: "md5sum main.py | awk '{print \$1}'",
                        returnStdout: true
                    ).trim()

                    if (fileExists(CHECKSUM_FILE)) {
                        def previousChecksum = readFile(CHECKSUM_FILE).trim()
                        echo "Previous checksum: ${previousChecksum}"
                        echo "Current checksum: ${currentChecksum}"

                        if (previousChecksum != currentChecksum) {
                            echo "main.py has changed. Rebuilding Docker image..."
                            writeFile(file: CHECKSUM_FILE, text: currentChecksum)
                        } else {
                            echo "No changes in main.py. Skipping build stage."
                            currentBuild.result = 'NOT_BUILT'
                            return
                        }
                    } else {
                        echo "No previous checksum found. Storing current checksum."
                        writeFile(file: CHECKSUM_FILE, text: currentChecksum)
                    }
                }
            }
        }

        stage('Build Docker Image') {
            when {
                not { currentBuild.result == 'NOT_BUILT' }
            }
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .'
            }
        }

        stage('Run Docker Container') {
            when {
                not { currentBuild.result == 'NOT_BUILT' }
            }
            steps {
                script {
                    echo 'Stopping and removing any previous containers...'
                    sh 'docker ps -q --filter "name=${DOCKER_IMAGE}" | xargs -r docker stop'
                    sh 'docker ps -a -q --filter "name=${DOCKER_IMAGE}" | xargs -r docker rm'

                    echo 'Running Docker container...'
                    sh 'docker run -d -p ${APP_PORT}:${APP_PORT} --name ${DOCKER_IMAGE} ${DOCKER_IMAGE}:${DOCKER_TAG}'

                    echo 'Checking container logs...'
                    sh 'docker logs ${DOCKER_IMAGE}'
                }
            }
        }

        stage('Wait for Flask App to be Ready') {
            when {
                not { currentBuild.result == 'NOT_BUILT' }
            }
            steps {
                script {
                    echo 'Waiting for Flask app to become accessible...'
                    waitUntil {
                        script {
                            def response = sh(script: "curl -s -o /dev/null -w '%{http_code}' ${APP_URL}", returnStdout: true).trim()
                            echo "HTTP Response: ${response}"
                            return response == '200'
                        }
                    }
                    echo "Flask app is ready at ${APP_URL}"
                }
            }
        }

        stage('Test Flask App') {
            when {
                not { currentBuild.result == 'NOT_BUILT' }
            }
            steps {
                script {
                    echo "Testing Flask application at ${APP_URL}..."
                    def response = sh(script: "curl -s ${APP_URL}", returnStdout: true).trim()
                    echo "Response: ${response}"

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
            echo 'Ensuring all containers and images are cleaned up...'
            sh '''
            docker ps -a -q --filter "name=${DOCKER_IMAGE}" | xargs -r docker rm -f || true
            docker images -q ${DOCKER_IMAGE}:${DOCKER_TAG} | xargs -r docker rmi -f || true
            '''
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs for details.'
        }
    }
}
