#!/usr/bin/env python3
"""
Setup script for the Instantly Email Service
"""

import os
import subprocess
import sys

def check_python_version():
    """Check if Python 3.6 or higher is installed"""
    if sys.version_info < (3, 6):
        print("Error: Python 3.6 or higher is required.")
        sys.exit(1)
    print(f"Python version {sys.version} is compatible.")

def install_requirements():
    """Install required packages from requirements.txt"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        sys.exit(1)

def check_env_file():
    """Check if .env file exists, if not create from example"""
    if not os.path.exists(".env"):
        print("Creating .env file from example...")
        if os.path.exists(".env.example"):
            with open(".env.example", "r") as example_file:
                content = example_file.read()
            
            with open(".env", "w") as env_file:
                env_file.write(content)
            
            print(".env file created. Please update the SECRET_KEY in .env with a strong secret key.")
        else:
            print("Warning: .env.example file not found.")
            # Create a basic .env file
            with open(".env", "w") as env_file:
                env_file.write("SECRET_KEY=your-secret-key-here\n")
                env_file.write("MAIL_TM_API_URL=https://api.mail.tm\n")
            print(".env file created with default values. Please update the SECRET_KEY in .env with a strong secret key.")
    else:
        print(".env file already exists.")

def main():
    print("Setting up Instantly Email Service...")
    
    # Check Python version
    check_python_version()
    
    # Install requirements
    install_requirements()
    
    # Check/create .env file
    check_env_file()
    
    print("\nSetup complete!")
    print("Next steps:")
    print("1. Update the SECRET_KEY in .env with a strong secret key")
    print("2. Run 'python app.py' to start the application")
    print("3. Visit http://localhost:5000 in your browser")

if __name__ == "__main__":
    main()