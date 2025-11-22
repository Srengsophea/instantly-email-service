#!/usr/bin/env python3
"""
Python script to update the application on PythonAnywhere
"""

import os
import subprocess
import sys

def update_pythonanywhere():
    """Update the application on PythonAnywhere"""
    print("Updating instantly-email-service on PythonAnywhere...")
    
    # Try to find the project directory
    project_dirs = ['~/instantly', '~/instantly-email-service']
    project_dir = None
    
    for directory in project_dirs:
        expanded_dir = os.path.expanduser(directory)
        if os.path.exists(expanded_dir):
            project_dir = expanded_dir
            break
    
    if not project_dir:
        print("Error: Could not find project directory. Please make sure the application is installed in ~/instantly or ~/instantly-email-service")
        return False
    
    print(f"Found project directory: {project_dir}")
    os.chdir(project_dir)
    
    try:
        # Pull the latest changes from GitHub
        print("Pulling latest changes from GitHub...")
        result = subprocess.run(['git', 'pull', 'origin', 'main'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("Git pull successful!")
            print(result.stdout)
        else:
            print("Error during git pull:")
            print(result.stderr)
            return False
        
        # Install any new dependencies
        print("Installing/updating dependencies...")
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("Dependencies updated successfully!")
            print(result.stdout)
        else:
            print("Warning: Error during dependency installation:")
            print(result.stderr)
        
        print("\nUpdate completed successfully!")
        print("Please go to the PythonAnywhere web tab and reload your web application.")
        return True
        
    except Exception as e:
        print(f"Error during update: {e}")
        return False

if __name__ == "__main__":
    update_pythonanywhere()