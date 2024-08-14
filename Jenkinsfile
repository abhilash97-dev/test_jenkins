pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/abhilash97-dev/spark.git'  
    }

    stages {
        stage('Checkout Repo A') {
            steps {
                // Clone the main repository (Repo A)
                git branch: 'main', url: "${REPO_URL}"
            }
        }

        stage('Check File Changes') {
            steps {
                script {
                    // Get the last commit's SHA
                    def lastCommit = sh(script: "git rev-parse HEAD", returnStdout: true).trim()

                    // Get the previous commit's SHA
                    def previousCommit = sh(script: "git rev-parse HEAD~1", returnStdout: true).trim()

                    // Get the list of files changed in the last commit
                    def changedFiles = sh(script: "git diff --name-only ${previousCommit} ${lastCommit}", returnStdout: true).trim()

                    // Get detailed diffs
                    def diffOutput = sh(script: "git diff ${previousCommit} ${lastCommit}", returnStdout: true).trim()

                    echo "Files changed in the last push:"
                    echo changedFiles

                    echo "File diffs:"
                    echo diffOutput

                    // Write the changed files and diffs to files
                    writeFile file: 'changed_files.txt', text: changedFiles
                    writeFile file: 'diff_output.txt', text: diffOutput
                }
            }
        }

        stage('Run Python Script') {
            steps {
                script {
                    // Remove existing directory if it exists
                    sh "rm -rf process_repo"

                    // Clone Repo B where the Python script is stored
                    sh "git clone https://github.com/abhilash97-dev/test_jenkins.git process_repo"

                    // Run the Python script with the file paths as arguments
                    sh "python process_repo/process_changes.py changed_files.txt diff_output.txt"
                }
            }
        }
    }
}
