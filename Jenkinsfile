pipeline {
    agent any

    stages {
        stage('Build image') {
            environment {
                DOCKER_HOST = "tcp://docker:2376"
                DOCKER_CERT_PATH = "/certs/client"
                DOCKER_TLS_VERIFY = "1"
            }
            steps {
                sh 'docker build -t stardust18364/calculator-web:latest .'
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker_hub-cred',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker push stardust18364/calculator-web:latest'
                }
            }
        }

        stage('Pull image from Docker hub'){
            steps {
                sh 'docker rm -f stardust18364/calculator-web:latest'
                withCredentials([usernamePassword(
                    credentialsId: 'docker_hub-cred',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker push stardust18364/calculator-web:latest'
                }
            }
        }

        stage('Run container') {
            environment {
                DOCKER_HOST = "unix:///var/run/docker.sock"
            }
            steps {
                sh 'docker run -d -p 5000:5000 --name calculator-web stardust18364/calculator-web:latest'
            }
        }
    }
}