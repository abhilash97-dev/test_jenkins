import sys

def process_changes(changed_files_path, diff_output_path):
    # Read the changed files
    with open(changed_files_path, 'r') as f:
        changed_files = f.read().splitlines()
    
    # Read the diffs
    with open(diff_output_path, 'r') as f:
        diff_output = f.read()

    # Process the changed files and diffs
    print("Processing the following files:")
    for file in changed_files:
        print(f"- {file}")

    print("\nDiffs:")
    print(diff_output)

if __name__ == "__main__":
    # Get the file paths from the command-line arguments
    changed_files_path = sys.argv[1]
    diff_output_path = sys.argv[2]
    
    process_changes(changed_files_path, diff_output_path)
