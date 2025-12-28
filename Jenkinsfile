pipeline {
    agent any

    stages {
        stage('Build image (DinD)') {
            environment {
                DOCKER_HOST = "tcp://docker:2376"
                DOCKER_CERT_PATH = "/certs/client"
                DOCKER_TLS_VERIFY = "1"
            }
            steps {
                sh 'docker build -t stardust18364/calculator-web:latest .'
            }
        }

        stage('Run container (Host Docker)') {
            environment {
                DOCKER_HOST = "unix:///var/run/docker.sock"
            }
            steps {
                sh 'docker rm -f calculator-web || true'
                sh 'docker run -d -p 5000:5000 --name calculator-web stardust18364/calculator-web:latest'
            }
        }
    }
}