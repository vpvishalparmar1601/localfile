pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'flask-app'            // Docker image name
        DOCKER_TAG = 'latest'                 // Docker image tag
        APP_PORT = '5000'                     // Flask app port
        APP_URL = "http://localhost:${APP_PORT}" // URL to test the app
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
                    // Check if the main.py file has changed
                    def changes = sh(script: 'git diff --name-only HEAD~1 HEAD', returnStdout: true).trim()
                    echo "Detected changes: ${changes}"

                    // If main.py has changed, set a flag to trigger rebuild
                    if (changes.contains('main.py')) {
                        env.REBUILD = 'true'
                    } else {
                        env.REBUILD = 'false'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            when {
                expression { return env.REBUILD == 'true' }
            }
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .'
            }
        }

        stage('Run Docker Container') {
            when {
                expression { return env.REBUILD == 'true' }
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
                expression { return env.REBUILD == 'true' }
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
                expression { return env.REBUILD == 'true' }
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
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs for details.'
        }
    }
}
