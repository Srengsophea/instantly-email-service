from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import uuid
import json
import requests
from datetime import datetime
from functools import wraps
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')  # In production, use a secure secret key

# Files to store data
USERS_FILE = 'users.json'
EMAIL_ACCOUNTS_FILE = 'email_accounts.json'

# Mail.tm API configuration
MAIL_TM_API_URL = os.getenv('MAIL_TM_API_URL', 'https://api.mail.tm')

def load_users():
    """Load users from file"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            return {}
    return {}

def save_users(users):
    """Save users to file"""
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=2)
        return True
    except Exception as e:
        return False

def load_email_accounts():
    """Load email accounts from file"""
    if os.path.exists(EMAIL_ACCOUNTS_FILE):
        try:
            with open(EMAIL_ACCOUNTS_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            return []
    return []

def save_email_accounts(accounts):
    """Save email accounts to file"""
    try:
        with open(EMAIL_ACCOUNTS_FILE, 'w') as f:
            json.dump(accounts, f, indent=2)
        return True
    except Exception as e:
        return False

def get_available_domains():
    """Fetch available domains from Mail.tm"""
    try:
        response = requests.get(f'{MAIL_TM_API_URL}/domains?page=1')
        if response.status_code == 200:
            data = response.json()
            return [domain['domain'] for domain in data['hydra:member']]
    except Exception as e:
        pass
    return ['mail.tm', 'tmpmail.org', 'emailtemporal.net', 'tempmail.demo']

# Load data when app starts
users = load_users()
email_accounts = load_email_accounts()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user_id' in session:
        user_id = session['user_id']
        user = users.get(user_id, {})
        user_emails = [email for email in email_accounts if email.get('user_id') == user_id]
        # Get only the last 5 emails for the dashboard
        recent_emails = user_emails[-5:] if len(user_emails) >= 5 else user_emails
        available_domains = get_available_domains()
        return render_template('dashboard.html', user=user, emails=recent_emails, all_emails_count=len(user_emails), domains=available_domains)
    return render_template('index.html')

@app.route('/my-emails')
@login_required
def my_emails():
    user_id = session['user_id']
    user = users.get(user_id, {})
    user_emails = [email for email in email_accounts if email.get('user_id') == user_id]
    # Sort emails by creation date (newest first)
    user_emails.sort(key=lambda x: x['created_at'], reverse=True)
    available_domains = get_available_domains()
    return render_template('my_emails.html', user=user, emails=user_emails, domains=available_domains)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'success': False, 'error': 'Username and password are required'})
    
    # Check if user already exists
    for user_id, user in users.items():
        if user['username'] == username:
            return jsonify({'success': False, 'error': 'Username already exists'})
    
    # Create new user
    user_id = str(uuid.uuid4())
    users[user_id] = {
        'id': user_id,
        'username': username,
        'password': password,  # In production, hash the password
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Save users
    save_users(users)
    
    # Log in the user
    session['user_id'] = user_id
    
    return jsonify({'success': True, 'message': 'User created successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'success': False, 'error': 'Username and password are required'})
    
    # Find user
    for user_id, user in users.items():
        if user['username'] == username and user['password'] == password:
            session['user_id'] = user_id
            return jsonify({'success': True, 'message': 'Login successful'})
    
    return jsonify({'success': False, 'error': 'Invalid username or password'})

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    user_id = session['user_id']
    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    # Verify current password
    user = users.get(user_id, {})
    if user.get('password') != current_password:
        return jsonify({'success': False, 'error': 'Current password is incorrect'})
    
    # Update password
    users[user_id]['password'] = new_password
    save_users(users)
    
    return jsonify({'success': True, 'message': 'Password changed successfully'})

@app.route('/change_username', methods=['POST'])
@login_required
def change_username():
    user_id = session['user_id']
    data = request.get_json()
    new_username = data.get('new_username')
    
    if not new_username:
        return jsonify({'success': False, 'error': 'Username is required'})
    
    # Check if username is already taken
    for uid, user in users.items():
        if user['username'] == new_username and uid != user_id:
            return jsonify({'success': False, 'error': 'Username is already taken'})
    
    # Update username
    users[user_id]['username'] = new_username
    save_users(users)
    
    # Update session
    session['user_id'] = user_id
    
    return jsonify({'success': True, 'message': 'Username changed successfully'})

@app.route('/delete_email/<email_id>', methods=['POST'])
@login_required
def delete_email(email_id):
    user_id = session['user_id']
    
    # Find and remove the email account
    global email_accounts
    email_accounts = load_email_accounts()  # Reload to ensure we have the latest data
    
    # Find the email account and verify ownership
    email_account = None
    for i, account in enumerate(email_accounts):
        if account['id'] == email_id and account.get('user_id') == user_id:
            email_account = account
            # Remove the email account
            email_accounts.pop(i)
            break
    
    if not email_account:
        return jsonify({'success': False, 'error': 'Email account not found or access denied'})
    
    # Save updated email accounts
    save_email_accounts(email_accounts)
    
    return jsonify({'success': True, 'message': 'Email deleted successfully'})

@app.route('/profile')
@login_required
def profile():
    user_id = session['user_id']
    user = users.get(user_id, {})
    return render_template('profile.html', user=user)

@app.route('/generate_email', methods=['POST'])
@login_required
def generate_email():
    user_id = session['user_id']
    data = request.get_json()
    domain = data.get('domain')
    
    # If no domain provided, get the first available one
    if not domain:
        available_domains = get_available_domains()
        if available_domains:
            domain = available_domains[0]
        else:
            domain = 'mail.tm'
    
    # Generate a unique username and password
    username = str(uuid.uuid4())[:8]
    password = str(uuid.uuid4())
    email_address = f"{username}@{domain}"
    
    try:
        # Create account on Mail.tm
        account_data = {
            'address': email_address,
            'password': password
        }
        
        response = requests.post(f'{MAIL_TM_API_URL}/accounts', json=account_data)
        
        if response.status_code in [200, 201]:
            # Get authentication token
            token_data = {
                'address': email_address,
                'password': password
            }
            
            token_response = requests.post(f'{MAIL_TM_API_URL}/token', json=token_data)
            
            if token_response.status_code in [200, 201]:
                token = token_response.json()['token']
                
                # Store the email account with user association
                email_obj = {
                    'id': str(uuid.uuid4()),
                    'user_id': user_id,
                    'address': email_address,
                    'username': username,
                    'domain': domain,
                    'password': password,
                    'token': token,
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'messages': []
                }
                
                email_accounts.append(email_obj)
                
                # Save to file
                save_email_accounts(email_accounts)
                
                return jsonify({'success': True, 'email': email_obj})
            else:
                return jsonify({'success': False, 'error': 'Failed to get authentication token'})
        else:
            return jsonify({'success': False, 'error': 'Failed to create email account'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get_user_emails')
@login_required
def get_user_emails():
    user_id = session['user_id']
    # Reload accounts from file to ensure we have the latest data
    global email_accounts
    email_accounts = load_email_accounts()
    user_emails = [email for email in email_accounts if email.get('user_id') == user_id]
    return jsonify({'emails': user_emails})

@app.route('/get_inbox/<email_id>')
@login_required
def get_inbox(email_id):
    user_id = session['user_id']
    try:
        # Reload accounts from file
        global email_accounts
        email_accounts = load_email_accounts()
        
        # Find the email account and verify ownership
        email_account = None
        for account in email_accounts:
            if account['id'] == email_id and account.get('user_id') == user_id:
                email_account = account
                break
        
        if not email_account:
            return jsonify({'success': False, 'error': 'Email account not found or access denied'})
        
        # Use Mail.tm API to get inbox messages
        headers = {
            'Authorization': f'Bearer {email_account["token"]}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            f'{MAIL_TM_API_URL}/messages',
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            messages = data.get('hydra:member', [])
            return jsonify({'success': True, 'messages': messages})
        else:
            return jsonify({'success': True, 'messages': []})
            
    except Exception as e:
        return jsonify({'success': True, 'messages': []})

if __name__ == '__main__':
    app.run(debug=True)