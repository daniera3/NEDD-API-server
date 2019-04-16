pipeline {
    agent { docker { image 'python:3-alpine' } }
    stages {
        stage('Git') {
            steps{
                // echo 'Getting the code from GitHub...'
                git 'https://github.com/daniera3/NEDD-API-server.git'
            }
        }
        stage('Requirements'){
            steps{
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    //echo 'Installing Requirements...'
                    sh 'pip3.7 install -U -r requirements.txt --user'
		            sh 'pip3 install --user -U requests'
                }
            }
        }
        stage('Run Tests'){
            steps{
                // echo 'Testing User app...'
		withEnv(["HOME=${env.WORKSPACE}"]) {
	 	        sh "python3.7 -m pytest -v  --junitxml=./nosetests.xml"

			}
            }
        }

	stage('Run site'){
            steps{
                // echo 'Testing User app...'
		withEnv(["HOME=${env.WORKSPACE}"]) {
	 	        sh "python3.7 website.py &"

			}
            }
        }
    }
}
