pipeline {
  agent any 
  stages {
    stage('Maven: clean project') {
      steps {
			  bat """ 
			    mvn clean
          """
        }
    }
	stage('Maven: package project') {
      steps {
				bat """
				  mvn package 
          """
        }
    }
	stage('Maven: test project') {
      steps {
				bat """
				  mvn test      
          """
        }
    }
    stage('Send email notification'){
        steps{

            mail bcc: '', 
            body: "<b>Edison CI project </b><br>Project: ${env.JOB_NAME} <br>Build Number: ${env.BUILD_NUMBER} <br> URL for build: ${env.BUILD_URL}", 
            cc: '', 
            charset: 'UTF-8', 
            from: 'hadi.elme92@gmai.com', 
            mimeType: 'text/html', 
            replyTo: '', 
            subject: "EDISON ${env.JOB_NAME} Build Number: ${env.BUILD_NUMBER} ", 
            to: "hadi.elmekawi@ge.com";  

        }
    }
stage('Zip the project'){
  steps{
    bat """ del  "C:\\Program Files (x86)\\Jenkins\\workspace\\CI-W17\\ci_w17.zip"  """
    zip zipFile: 'ci_w17.zip', archive: false, dir: 'C:\\Program Files (x86)\\Jenkins\\workspace\\CI-W17'
  }
}

  stage('Archive zip folder'){
    steps{
      archiveArtifacts artifacts: 'ci_w17.zip', fingerprint: true
    }
  }
}
    post {
      always {
          junit 'target//surefire-reports/*.xml'
          recordIssues enabledForFailure: true, tools: [mavenConsole(), java(), javaDoc()]
          archiveArtifacts artifacts: mavenConsole(), fingerprint: true
      }
  }
}

