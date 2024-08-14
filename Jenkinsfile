pipeline {
    agent any

    environment {
        SPARK_REPO_URL = 'https://github.com/abhilash97-dev/spark.git'
        TEST_REPO_URL = 'https://github.com/abhilash97-dev/test_jenkins.git'
        SPARK_REPO_DIR = 'spark_repo'
        TEST_REPO_DIR = 'process_repo'
    }

    stages {
        stage('Checkout Repo A (Spark)') {
            steps {
                script {
                    // Check if the directory exists and remove it if it does
                    sh """
                        if [ -d "${SPARK_REPO_DIR}" ]; then
                            rm -rf ${SPARK_REPO_DIR}
                        fi
                    """

                    // Clone the Spark repository
                    sh "git clone ${SPARK_REPO_URL} ${SPARK_REPO_DIR}"
                }
            }
        }

        stage('Check Python File Changes in Spark Repo') {
            steps {
                script {
                    // Navigate to the Spark repo directory
                    dir("${SPARK_REPO_DIR}") {
                        // Get the last commit's SHA
                        def lastCommit = sh(script: "git rev-parse HEAD", returnStdout: true).trim()

                        // Get the previous commit's SHA
                        def previousCommit = sh(script: "git rev-parse HEAD~1", returnStdout: true).trim()

                        // Get the list of files changed in the last commit
                        def changedFiles = sh(script: "git diff --name-only ${previousCommit} ${lastCommit}", returnStdout: true).trim()

                        def pyOutput = [:]
                        def pyDiffs = ""

                        changedFiles.split('\n').each { file ->
                            if (file.endsWith('.py')) {
                                // Check if the file is new or existing
                                def fileStatus = sh(script: "git diff --name-status ${previousCommit} ${lastCommit} | grep ${file} | awk '{print \$1}'", returnStdout: true).trim()
                                def status = (fileStatus == 'A') ? 1 : 0
                                pyOutput[file] = status

                                // Get the diff for the .py file
                                def diff = sh(script: "git diff ${previousCommit} ${lastCommit} -- ${file}", returnStdout: true).trim()
                                pyDiffs += "File: ${file}\n${diff}\n\n"
                            }
                        }

                        // Convert map to JSON format
                        def json = groovy.json.JsonOutput.toJson(pyOutput)

                        // Write the JSON output to a file
                        writeFile file: 'python_file_changes.json', text: json
                        echo "Changed Python files:"
                        echo json

                        // Write the diffs for .py files to a file
                        if (pyDiffs) {
                            writeFile file: 'py_diff_output.txt', text: pyDiffs
                            echo "Python file diffs saved to py_diff_output.txt"
                        } else {
                            echo "No Python file changes detected."
                        }
                    }
                }
            }
        }

        stage('Run Python Script') {
            steps {
                script {
                    // Remove existing process_repo directory if it exists
                    sh """
                        if [ -d "${TEST_REPO_DIR}" ]; then
                            rm -rf ${TEST_REPO_DIR}
                        fi
                    """

                    // Clone the repository where the Python script is stored
                    sh "git clone ${TEST_REPO_URL} ${TEST_REPO_DIR}"

                    // Run the Python script with the JSON file path as an argument
                    sh "python3 ${TEST_REPO_DIR}/process_changes.py ${SPARK_REPO_DIR}/python_file_changes.json"
                }
            }
        }
    }
}
