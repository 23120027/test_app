pipeline {
    agent any

    triggers { 
        githubPush()
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'git@github.com:23120027/test_app.git'
            }
        }

        stage('Build image') {
            environment {
                DOCKER_HOST = "tcp://docker:2376"
                DOCKER_CERT_PATH = "/certs/client"
                DOCKER_TLS_VERIFY = "1"
            }
            steps {
                sh 'docker build --no-cache -t stardust18364/calculator-web:latest .'
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    withCredentials([usernamePassword(credentialsId: 'docker_hub-ssh', 
                                                     usernameVariable: 'DOCKER_USER', 
                                                     passwordVariable: 'DOCKER_PASS')]) {
                        sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                        sh 'docker push stardust18364/calculator-web:latest'
                    }
                }
            }
        }

        stage('Pull image from Docker hub'){
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker_hub-ssh',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker stop calculator-web || true'
                    sh 'docker rm calculator-web || true'
                    sh 'docker rmi stardust18364/calculator-web:latest'
                    sh 'docker pull stardust18364/calculator-web:latest'
                }
            }
        }

        stage('Run container') {
            environment {
                DOCKER_HOST = "unix:///var/run/docker.sock"
            }
            steps {
                sh 'docker stop calculator-web || true'
                sh 'docker rm calculator-web || true'
                sh 'docker run -d -p 5000:5000 --name calculator-web stardust18364/calculator-web:latest'
            }
        }
    }
}