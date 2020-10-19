pipeline {
  options { disableConcurrentBuilds() }
  agent { label 'docker-slave' }
  stages {
    stage ('Pull repo code from github') {
      steps {
        checkout scm
      }
    }
    stage ('Run iac-quality-framework') {
      steps {
        sh  """ #!/bin/bash
                pip3 install -r requirements.txt
				pip3 install . 
            """
      }
    }
	stage('Test iac-quality-framework') {
        steps {
            sh  """ #!/bin/bash             
                    python -m unittest discover -s . -p "Test*.py"                    
                """
        }
    }	
	stage('SonarQube analysis'){
        environment {
          scannerHome = tool 'SonarQubeScanner'
        }
        steps {
            withSonarQubeEnv('SonarCloud') {
                      sh "${scannerHome}/bin/sonar-scanner"
            }
        }
    }
	stage('Build docker images') {
            steps {
                sh "docker build -t iacmetrics  -f Dockerfile ."                
            }
    }   
    stage('Push Dockerfile to DockerHub') {
            when {
               branch "master"
            }
            steps {
                withDockerRegistry(credentialsId: 'jenkins-sodalite.docker_token', url: '') {
                    sh  """#!/bin/bash                       
                            docker tag iacmetrics sodaliteh2020/iacmetrics:${BUILD_NUMBER}
                            docker tag iacmetrics sodaliteh2020/iacmetrics
                            docker push sodaliteh2020/iacmetrics:${BUILD_NUMBER}
                            docker push sodaliteh2020/iacmetrics
                        """
                }
            }
    }
  }
  post {
    failure {
        slackSend (color: '#FF0000', message: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
    }
    fixed {
        slackSend (color: '#6d3be3', message: "FIXED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})") 
    }
  }
}
