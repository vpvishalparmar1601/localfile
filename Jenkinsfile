pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'flask-app'   // Name of your Docker image
        DOCKER_TAG = 'latest'        // Tag for your Docker image
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Checkout the latest code from your GitHub repository
                git 'https://github.com/vpvishalparmar1601/localfile.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Debugging: List the contents of the working directory to ensure Dockerfile is present
                    sh 'ls -l'

                    // Build the Docker image
                    sh 'docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .'

                    // Debugging: List Docker images after the build to ensure it's created
                    sh 'docker images'

                    // Ensure the image exists with the correct name and tag
                    sh 'docker images | grep ${DOCKER_IMAGE}:${DOCKER_TAG} || (echo "Docker image not found" && exit 1)'
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // Check if the image exists before attempting to run the container
                    sh 'docker images | grep ${DOCKER_IMAGE}:${DOCKER_TAG} || (echo "Docker image not found" && exit 1)'

                    // Stop any running container with the same name (optional)
                    sh 'docker ps -q --filter "name=${DOCKER_IMAGE}" | xargs -r docker stop'

                    // Remove the stopped container (optional)
                    sh 'docker ps -a -q --filter "name=${DOCKER_IMAGE}" | xargs -r docker rm'

                    // Run the Docker container
                    sh 'docker run -d -p 5000:5000 --name ${DOCKER_IMAGE} ${DOCKER_IMAGE}:${DOCKER_TAG} || (echo "Docker run failed" && exit 1)'
                }
            }
        }

        stage('Clean Up') {
            steps {
                script {
                    // Stop and remove any running containers using the image
                    sh '''
                    docker ps -a -q --filter "ancestor=${DOCKER_IMAGE}:${DOCKER_TAG}" | xargs -r docker rm -f
                    '''

                    // Remove the Docker image after cleaning up containers
                    sh '''
                    docker images -q ${DOCKER_IMAGE}:${DOCKER_TAG} | xargs -r docker rmi -f
                    '''
                }
            }
        }
    }

    post {
        always {
            script {
                // Additional cleanup to ensure no lingering containers or images
                sh 'docker ps -a -q --filter "name=${DOCKER_IMAGE}" | xargs -r docker rm -f'
                sh 'docker images -q ${DOCKER_IMAGE}:${DOCKER_TAG} | xargs -r docker rmi -f'
            }
        }
    }
}
