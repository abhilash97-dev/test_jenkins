pipeline {
    agent any

    environment {
        SPARK_REPO_URL = 'https://github.com/abhilash97-dev/spark.git'
        SPARK_REPO_DIR = 'spark_repo'
    }

    stages {
        stage('Checkout Repo A (Spark)') {
            steps {
                // Clone the spark repository into a separate directory
                sh "git clone ${SPARK_REPO_URL} ${SPARK_REPO_DIR}"
            }
        }

        stage('Check File Changes in Spark Repo') {
            steps {
                script {
                    // Navigate to the spark repository directory
                    dir("${SPARK_REPO_DIR}") {
                        // Get the last commit's SHA
                        def lastCommit = sh(script: "git rev-parse HEAD", returnStdout: true).trim()

                        // Get the previous commit's SHA
                        def previousCommit = sh(script: "git rev-parse HEAD~1", returnStdout: true).trim()

                        // Get the list of files changed in the last commit
                        def changedFiles = sh(script: "git diff --name-only ${previousCommit} ${lastCommit}", returnStdout: true).trim()

                        // Get detailed diffs
                        def diffOutput = sh(script: "git diff ${previousCommit} ${lastCommit}", returnStdout: true).trim()

                        echo "Files changed in the last push in Spark repo:"
                        echo changedFiles

                        echo "File diffs in Spark repo:"
                        echo diffOutput

                        // Write the changed files and diffs to files
                        writeFile file: 'changed_files.txt', text: changedFiles
                        writeFile file: 'diff_output.txt', text: diffOutput
                    }
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
                    sh "python3 process_repo/process_changes.py ${SPARK_REPO_DIR}/changed_files.txt ${SPARK_REPO_DIR}/diff_output.txt"
                }
            }
        }
    }
}
