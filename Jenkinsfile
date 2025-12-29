pipeline {
    agent any

    triggers { 
        githubPush()
    }

    environment {
        IMAGE = "stardust18364/calculator-web"
        PORT = "5000"
    }

    stages {
        stage('Build Docker Image') {
            environment {
                DOCKER_HOST = "tcp://docker:2376"
                DOCKER_CERT_PATH = "/certs/client"
                DOCKER_TLS_VERIFY = "1"
            }
            steps {
                script {
                    COMMIT_HASH = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
                    IMAGE_TAG = "${IMAGE}:${COMMIT_HASH}"
                    sh "docker build --no-cache -t ${IMAGE_TAG} ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker_hub-ssh', 
                                                 usernameVariable: 'DOCKER_USER', 
                                                 passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin
                        docker push ${IMAGE_TAG}
                    """
                }
            }
        }

        stage('Deploy Container') {
            environment {
                DOCKER_HOST = "unix:///var/run/docker.sock"
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker_hub-ssh',
                                                 usernameVariable: 'DOCKER_USER',
                                                 passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin
                        docker stop calculator-web || true
                        docker rm calculator-web || true
                        docker pull ${IMAGE_TAG}
                        docker run -d -p ${PORT}:${PORT} --name calculator-web ${IMAGE_TAG}
                        docker ps -a
                    """
                }
            }
        }
    }

    post {
        success {
            echo "Deployment successful for commit ${COMMIT_HASH}"
        }
        failure {
            echo "Deployment failed!"
        }
    }
}
