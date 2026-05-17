#!/usr/bin/env python3
"""
Simple test script to verify the temporary email generator application
"""

import unittest
import sys
import os
from unittest.mock import patch, Mock

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestApp(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        # Import the app
        from main import app, users
        self.app = app.test_client()
        # Add test user to users database to prevent session clearing redirect guards
        users['test_user_id'] = {
            'id': 'test_user_id',
            'username': 'testuser',
            'password': 'testpass',
            'created_at': '2026-05-17 00:00:00',
            'is_admin': True
        }

    def test_index_page(self):
        """Test that the index page loads correctly"""
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Instantly', result.data)

    @patch('main.requests.post')
    @patch('main.requests.get')
    def test_signup_and_login(self, mock_get, mock_post):
        """Test user signup and login"""
        # Test signup with a unique username
        import uuid
        unique_username = f"testuser_{uuid.uuid4()}"
        
        response = self.app.post('/signup',
                               json={'username': unique_username, 'password': 'testpass'})
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertTrue(data['success'])
        
        # Test login
        response = self.app.post('/login',
                               json={'username': unique_username, 'password': 'testpass'})
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertTrue(data['success'])

    @patch('main.requests.post')
    @patch('main.requests.get')
    def test_generate_email(self, mock_get, mock_post):
        """Test email generation endpoint"""
        # First login
        with self.app.session_transaction() as sess:
            sess['user_id'] = 'test_user_id'
        
        # Mock domain response
        mock_domain_response = Mock()
        mock_domain_response.status_code = 200
        mock_domain_response.json.return_value = {
            'hydra:member': [
                {'domain': 'mail.tm'}
            ]
        }
        mock_get.return_value = mock_domain_response
        
        # Mock account creation response
        mock_account_response = Mock()
        mock_account_response.status_code = 201
        mock_account_response.json.return_value = {}
        
        # Mock token response
        mock_token_response = Mock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {'token': 'test_token'}
        
        mock_post.side_effect = [mock_account_response, mock_token_response]  # For account creation and token
        
        response = self.app.post('/generate_email',
                               json={'domain': 'mail.tm'})
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertIn('success', data)

    def test_get_user_emails(self):
        """Test getting user emails list"""
        # Login first
        with self.app.session_transaction() as sess:
            sess['user_id'] = 'test_user_id'
            
        response = self.app.get('/get_user_emails')
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertIn('emails', data)

    @patch('main.load_email_accounts')
    @patch('main.requests.get')
    def test_get_inbox(self, mock_get, mock_load):
        """Test getting inbox for an email address"""
        # Login first
        with self.app.session_transaction() as sess:
            sess['user_id'] = 'test_user_id'
        
        # Mock load_email_accounts
        mock_load.return_value = [{
            'id': 'test_id',
            'user_id': 'test_user_id',
            'address': 'test@example.com',
            'token': 'test_token'
        }]
        
        # Mock the API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'hydra:member': [
                {
                    'id': '1',
                    'from': {'address': 'sender@example.com'},
                    'subject': 'Test Email',
                    'text': 'This is a test email',
                    'createdAt': '2023-01-01T12:00:00.000Z'
                }
            ]
        }
        mock_get.return_value = mock_response
        
        response = self.app.get('/get_inbox/test_id')
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertTrue(data['success'])

    @patch('main.load_email_accounts')
    @patch('main.requests.get')
    def test_get_message(self, mock_get, mock_load):
        """Test getting a specific email message details"""
        # Login first
        with self.app.session_transaction() as sess:
            sess['user_id'] = 'test_user_id'
        
        # Mock load_email_accounts
        mock_load.return_value = [{
            'id': 'test_id',
            'user_id': 'test_user_id',
            'address': 'test@example.com',
            'token': 'test_token'
        }]
        
        # Mock the API response for specific message details
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 'msg_1',
            'from': {'address': 'sender@example.com'},
            'subject': 'Test Message Details',
            'text': 'Full email body details',
            'html': ['<p>Full email body details</p>'],
            'createdAt': '2023-01-01T12:00:00.000Z'
        }
        mock_get.return_value = mock_response
        
        response = self.app.get('/get_message/test_id/msg_1')
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['message']['id'], 'msg_1')
        self.assertEqual(data['message']['subject'], 'Test Message Details')

if __name__ == '__main__':
    unittest.main()