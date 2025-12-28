pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t stardust18364/calculator-web:latest .'
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-cred',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker push stardust18364/calculator-web:latest'
                }
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker rm -f calculator-web || true'
                sh 'docker run -d -p 5000:5000 --name calculator-web stardust18364/calculator-web:latest'
            }
        }
    }
}
