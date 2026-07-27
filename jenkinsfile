pipeline {
    agent any

    environment {
        // Change to your target AWS region
        AWS_REGION     = 'us-east-1' 
        S3_BUCKET      = 's3://chatpie'
        
        // ID of your AWS Credentials stored in Jenkins Credentials Manager
        AWS_CRED_ID    = 'aws-s3-credentials' 
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                // Adjust if using yarn/pnpm (e.g., 'yarn install --frozen-lockfile')
                sh 'npm ci' 
            }
        }

        stage('Build Project') {
            steps {
                // Builds your code into the ./dist directory
                sh 'npm run build' 
            }
        }

        stage('Deploy to S3') {
            steps {
                // Wraps execution with stored AWS Credentials
                withCredentials([usernamePassword(
                    credentialsId: "${AWS_CRED_ID}", 
                    usernameVariable: 'AWS_ACCESS_KEY_ID', 
                    passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                )]) {
                    sh """
                        aws s3 sync ./dist ${S3_BUCKET} \
                            --region ${AWS_REGION} \
                            --delete
                    """
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment to S3 succeeded!'
        }
        failure {
            echo 'Deployment failed. Check the console logs for details.'
        }
        always {
            // Clean up workspace after run
            cleanWs() 
        }
    }
}
