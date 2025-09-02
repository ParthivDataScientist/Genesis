import os

# Define the project structure.
# A trailing slash "/" indicates a directory.
# No trailing slash indicates a file.
project_structure = [
    "Genesis/README.md",
    "Genesis/LICENSE",
    "Genesis/.gitignore",
    "Genesis/requirements.txt",
    "Genesis/CMakeLists.txt",
    "Genesis/docs/",
    "Genesis/docs/vision.md",
    "Genesis/docs/architecture.md",
    "Genesis/docs/roadmap.md",
    "Genesis/src/",
    "Genesis/src/cpp/",
    "Genesis/src/cpp/wake_word/",
    "Genesis/src/cpp/stt/",
    "Genesis/src/cpp/tts/",
    "Genesis/src/python/",
    "Genesis/src/python/core/",
    "Genesis/src/python/system_control/",
    "Genesis/src/python/ai/",
    "Genesis/src/python/memory/",
    "Genesis/src/bindings/",
    "Genesis/tests/",
    "Genesis/tests/cpp/",
    "Genesis/tests/python/",
    "Genesis/scripts/",
    "Genesis/scripts/setup_env.py",
    "Genesis/scripts/run_genesis.py",
    "Genesis/scripts/build_cpp.sh",
    "Genesis/assets/",
    "Genesis/assets/diagrams/",
    "Genesis/assets/audio/",
]

def create_project_scaffold(structure):
    """Creates the directories and empty files for the project."""
    created_paths = []
    
    for path in structure:
        try:
            # Check if the path is a directory
            if path.endswith('/'):
                os.makedirs(path, exist_ok=True)
                created_paths.append(f"Created directory: {path}")
            # Otherwise, it's a file
            else:
                # Ensure the parent directory exists before creating the file
                parent_dir = os.path.dirname(path)
                if parent_dir:
                    os.makedirs(parent_dir, exist_ok=True)
                
                # Create an empty file
                with open(path, 'w') as f:
                    pass
                created_paths.append(f"Created file:      {path}")
        except OSError as e:
            print(f"Error creating {path}: {e}")

    return created_paths

if __name__ == "__main__":
    print("🚀 Starting project scaffolding for 'Genesis'...")
    
    # Check if the root directory already exists
    if os.path.exists("Genesis"):
        print("\n⚠️  Warning: Directory 'Genesis' already exists.")
        overwrite = input("Do you want to proceed and create missing files/folders? (y/n): ").lower()
        if overwrite != 'y':
            print("Aborted by user.")
            exit()

    results = create_project_scaffold(project_structure)
    
    print("\n------------------------------------------")
    for result in results:
        print(result)
    print("------------------------------------------")
    print("\n✅ Project structure for 'Genesis' created successfully!")