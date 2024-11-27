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
                    // Build the Docker image
                    sh 'docker build -t $DOCKER_IMAGE:$DOCKER_TAG .'
                }
            }
        }


        stage('Run Docker Container') {
            steps {
                script {
                    // Check if the image exists before attempting to run the container
                    sh 'docker images | grep ${DOCKER_IMAGE}:${DOCKER_TAG} || (echo "Docker image not found" && exit 1)'

                    // Stop and remove any running containers with the same name (optional)
                    sh 'docker ps -q --filter "name=${DOCKER_IMAGE}" | xargs -r docker stop || true'
                    sh 'docker ps -a -q --filter "name=${DOCKER_IMAGE}" | xargs -r docker rm || true'

                    // Run the Docker container in detached mode, bind port 5000 to the host
                    sh '''
                    docker run -d -p 5000:5000 --name ${DOCKER_IMAGE} ${DOCKER_IMAGE}:${DOCKER_TAG} || (echo "Docker run failed" && exit 1)
                    '''

                    // Check if the container is running
                    sh 'docker ps | grep ${DOCKER_IMAGE} || (echo "Docker container is not running" && exit 1)'
                }
            }
        }

        stage('Clean Up') {
            steps {
                script {
                    // Stop and remove any running containers using the image
                    sh '''
                    docker ps -a -q --filter "ancestor=${DOCKER_IMAGE}:${DOCKER_TAG}" | xargs -r docker rm -f || true
                    '''

                    // Remove the Docker image after cleaning up containers
                    sh '''
                    docker images -q ${DOCKER_IMAGE}:${DOCKER_TAG} | xargs -r docker rmi -f || true
                    '''
                }
            }
        }
    }

    post {
        always {
            script {
                // Additional cleanup to ensure no lingering containers or images
                sh 'docker ps -a -q --filter "name=${DOCKER_IMAGE}" | xargs -r docker rm -f || true'
                sh 'docker images -q ${DOCKER_IMAGE}:${DOCKER_TAG} | xargs -r docker rmi -f || true'
            }
        }
    }
}
