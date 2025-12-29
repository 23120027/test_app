pipeline {
    agent any

    environment {
        IMAGE = "stardust18364/calculator-web"
        PORT = "8080"
    }

    triggers {
        githubPush() 
    }

    stages {
        stage('Checkout') {
            steps{
                sshagent(['github-ssh']) {  
                        sh 'git clone -b main git@github.com:23120027/test-app.git'
                    }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    COMMIT_HASH = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
                    IMAGE_TAG = "${IMAGE}:${COMMIT_HASH}"
                    sh "docker build -t ${IMAGE_TAG} ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker_hub-cred', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push ${IMAGE_TAG}
                    """
                }
            }
        }

        stage('Deploy') {
            steps {
                sh """
                docker stop calculator-web || true
                docker rm calculator-web || true
                docker pull ${IMAGE_TAG}
                docker run -d --name calculator-web -p ${PORT}:${PORT} ${IMAGE_TAG}
                """
            }
        }
    }

    post {
        success {
            echo " Deployment successful for commit ${COMMIT_HASH}"
        }
        failure {
            echo " Deployment failed!"
        }
    }
}
