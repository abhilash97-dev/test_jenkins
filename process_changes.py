import sys
import json

def process_changes(changed_files_path, diff_output_path):
    # Read the changed files from the JSON file
    with open(changed_files_path, 'r') as f:
        changed_files = json.load(f)
    
    # Read the diffs
    with open(diff_output_path, 'r') as f:
        diff_output = f.read()

    # Process the changed files and diffs
    print("Processing the following files:")
    for file, status in changed_files.items():
        file_status = "New" if status == 1 else "Modified"
        print(f"- {file} ({file_status})")

    print("\nDiffs:")
    print(diff_output)

if __name__ == "__main__":
    # Get the file paths from the command-line arguments
    changed_files_path = sys.argv[1]
    diff_output_path = sys.argv[2]
    
    process_changes(changed_files_path, diff_output_path)
