# Instantly - Temporary Email Service

A Flask-based web application that allows users to create temporary email addresses using the Mail.tm API.

## Features

- Create temporary email addresses instantly
- Check inbox for received emails
- User authentication (signup/login)
- Password and username management
- Delete email addresses
- Responsive web design

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd SMTPdev
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the project root directory with the following content:
   ```
   SECRET_KEY=your-secret-key-here
   ```

2. Replace `your-secret-key-here` with a strong secret key for your Flask application.

## Running the Application

1. Make sure your virtual environment is activated.

2. Run the Flask application:
   ```bash
   python app.py
   ```

3. Open your web browser and navigate to `http://127.0.0.1:5000`

## Usage

1. Sign up for a new account or log in if you already have one
2. Create temporary email addresses from the dashboard
3. Check the inbox for each email address to view received messages
4. Manage your account settings from the profile page

## Project Structure

```
SMTPdev/
├── templates/
│   ├── dashboard.html
│   ├── index.html
│   ├── my_emails.html
│   └── profile.html
├── app.py
├── users.json
├── email_accounts.json
├── requirements.txt
└── README.md
```

## API Endpoints

- `GET /` - Home page (login/signup)
- `GET /dashboard` - User dashboard
- `GET /my-emails` - List all user emails
- `GET /profile` - User profile page
- `POST /signup` - Create new user account
- `POST /login` - User login
- `POST /logout` - User logout
- `POST /generate_email` - Create new temporary email
- `GET /get_user_emails` - Get all user emails
- `GET /get_inbox/<email_id>` - Get inbox for specific email
- `POST /change_password` - Change user password
- `POST /change_username` - Change user username
- `POST /delete_email/<email_id>` - Delete email address

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Mail.tm](https://mail.tm) for providing the temporary email API
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Bootstrap](https://getbootstrap.com/) for the frontend framework