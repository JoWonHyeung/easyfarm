pipeline {
	agent any
	parameters {
		string(name: 'VERSION', defaultValue: '', description: '')
	}
	stages {
		stage("Build") {
			steps {
				sh 'docker-compose build web'
			}
		}
		stage("Tag and Push") {
			steps {
				withCredentials([[$class: 'UsernamePasswordMultiBinding',
				credentialsId: 'docker-hub', 
				usernameVariable: 'DOCKER_USER_ID',
				passwordVariable: 'DOCKER_USER_PASSWORD'
				]]) {
					sh "docker tag capstone-pipeline_web:latest ${DOCKER_USER_ID}/jenkins-app:${BUILD_NUMBER}"
					sh "docker login -u ${DOCKER_USER_ID} -p ${DOCKER_USER_PASSWORD}"
					sh "docker push ${DOCKER_USER_ID}/jenkins-app:${BUILD_NUMBER}"
				}
			}
		}
		stage("deploy") {
			steps {
				sh "docker-compose up -d"
			}
		}
	}
}
