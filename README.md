# SocialDev

SocialDev is a backend-focused web application project designed to learn and implement JWT authentication, real-time communication using WebSockets, and database schema management. It offers a simple public chat room where authenticated users can chat in real time.

## Features

- User registration with email validation and hashed passwords
- User login with JWT-based authentication
- Real-time public chat using Flask-SocketIO WebSocket integration
- SQLite database for user and message storage
- RESTful API backend built on Flask framework

## Technologies Used

- **Backend:**
  - Python 3
  - Flask 3.1.1 (Flask-RESTful API, Flask-SocketIO)
  - SQLite for database
  - JWT (PyJWT) for authentication
  - Werkzeug for password hashing
  - Email-validator for email validation
- **Frontend:** (Handled separately; Node.js/npm with JavaScript)

## Project Structure

- `main.py` - Entry point to create and run Flask-SocketIO app
- `routes.py` - API endpoints for user registration and login
- `helpers.py` - Utility functions for DB access, JWT validation, email check
- `schema.sql` - SQL script for creating initial database tables
- `requirements.txt` - Python package dependencies

## Getting Started

### Backend Setup

1. Clone the repository:
   ```
   git clone https://github.com/KaungPyaeHtet/SocialDev.git
   cd SocialDev/backend
   ```
2. Create and activate a Python virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   .\venv\Scripts\activate   # Windows
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Initialize the database (run the SQL schema):
   ```
   sqlite3 app/users.db < schema.sql
   ```
5. Run the backend server:
   ```
   python main.py
   ```

### Frontend Setup

The frontend is located in the separate directory and managed via Node.js and npm.

1. Navigate to the frontend directory:
   ```
   cd ../frontend
   ```
2. Install dependencies:
   ```
   npm install
   ```
3. Run the frontend:
   ```
   npm start
   ```

### Usage

- Register a new user via `/register` endpoint with username, email, and password
- Login via `/login` endpoint to receive a JWT access token
- Use the JWT token to access the public chat room and send/receive messages in real time using WebSocket

## API Endpoints Overview

- `POST /register` - Register a new user (requires username, email, password)
- `POST /login` - Login and receive JWT token (requires username, email, password)

## Notes

- Passwords are stored securely with hashing using Werkzeug
- Emails are validated for format before registration
- JWT tokens are required in HTTP header for protected endpoints
- Simple SQLite database used; data stored in `app/users.db`
