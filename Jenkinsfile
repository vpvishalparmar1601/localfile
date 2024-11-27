pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'flask-app'  // Name of your Docker image
        DOCKER_TAG = 'latest'       // Tag for your Docker image
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
                    // Stop any running container from a previous build (optional)
                    sh 'docker ps -q --filter "name=$DOCKER_IMAGE" | xargs -r docker stop'

                    // Remove the stopped container (optional)
                    sh 'docker ps -a -q --filter "name=$DOCKER_IMAGE" | xargs -r docker rm'

                    // Run the Docker container
                    sh 'docker run -d -p 5000:5000 --name $DOCKER_IMAGE $DOCKER_IMAGE:$DOCKER_TAG'
                }
            }
        }

        stage('Clean Up') {
            steps {
                script {
                    // Optionally, remove the Docker image after use to save space
                    sh 'docker rmi $DOCKER_IMAGE:$DOCKER_TAG'
                }
            }
        }
    }

    post {
        always {
            // Clean up the Docker container after build completion
            sh 'docker ps -a -q --filter "name=$DOCKER_IMAGE" | xargs -r docker rm -f'
        }
    }
}
