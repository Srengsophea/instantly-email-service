import sys
import os

# Add your project directory to the path
path = '/home/srengsophea/instantly'
if path not in sys.path:
    sys.path.append(path)

# Change to the project directory
os.chdir(path)

# Set environment variables
os.environ['SECRET_KEY'] = 'your-very-secret-key-here'

# Import your application
from main import app as application

# For debugging - this can be removed later
print("WSGI loaded successfully")