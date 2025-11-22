#!/usr/bin/env python3
"""
Script to fix admin credentials in users.json file
"""

import json
import os
from datetime import datetime
import uuid

# Load existing users
users_file = 'users.json'

if os.path.exists(users_file):
    with open(users_file, 'r') as f:
        users = json.load(f)
else:
    users = {}

# Check if we have an admin user
admin_user = None
admin_user_id = None

for user_id, user in users.items():
    if user.get('is_admin', False):
        admin_user = user
        admin_user_id = user_id
        break

# If no admin user exists, create one
if not admin_user:
    print("No admin user found. Creating a new admin user...")
    admin_user_id = str(uuid.uuid4())
    users[admin_user_id] = {
        'id': admin_user_id,
        'username': 'khsophea20@gmail.com',
        'password': '@Sp18052005',
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'is_admin': True
    }
    print("Created new admin user with username: khsophea20@gmail.com")
else:
    # Update existing admin user credentials
    print("Found existing admin user. Updating credentials...")
    users[admin_user_id]['username'] = 'khsophea20@gmail.com'
    users[admin_user_id]['password'] = '@Sp18052005'
    print(f"Updated admin user {admin_user.get('username', 'unknown')} to khsophea20@gmail.com")

# Save the updated users
with open(users_file, 'w') as f:
    json.dump(users, f, indent=2)

print("Admin credentials fixed successfully!")
print("Admin username: khsophea20@gmail.com")
print("Admin password: @Sp18052005")