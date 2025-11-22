#!/bin/bash
# Deployment script for PythonAnywhere

echo "Updating instantly-email-service on PythonAnywhere..."

# Navigate to the project directory
cd ~/instantly || cd ~/instantly-email-service

# Pull the latest changes from GitHub
git pull origin main

# Install any new dependencies
pip install -r requirements.txt

# Reload the web app (you'll need to do this manually in the PythonAnywhere web tab)
echo "Please go to the PythonAnywhere web tab and reload your web application."

echo "Deployment completed!"