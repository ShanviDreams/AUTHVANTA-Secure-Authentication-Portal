# AUTHVANTA — Secure Identity. Smarter Access.

**Secure User Registration and Login Portal** is a web-based authentication and security project built using Flask and MySQL. It provides secure user authentication, email verification, Multi-Factor Authentication (MFA), password recovery and security monitoring.

## Features

- Secure User Registration and Login
- Password Hashing using Argon2
- Email Verification
- Two-Factor / Multi-Factor Authentication (MFA) using TOTP
- Password Recovery and Reset
- Login Rate Limiting
- CSRF Protection
- Admin Login and Dashboard
- Role-Based Access Control
- Security Logs and Login Attempt Monitoring
- OAuth-based integration with CodeArena
- Responsive User Interface with Theme Support

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| MySQL | Database |
| SQLAlchemy | Database ORM |
| HTML5 | Web page structure |
| CSS3 | Styling and responsive UI |
| JavaScript | Frontend interaction |
| Argon2 | Password hashing |
| TOTP | Multi-factor authentication |
| SMTP | Email verification and recovery |
| Git & GitHub | Version control |

## Security Implementation

- **Argon2:** Secure password hashing instead of storing plain-text passwords.
- **Email Verification:** Confirms user email ownership.
- **MFA:** Adds an additional authentication layer using time-based OTP.
- **Rate Limiting:** Helps reduce repeated login attempts and brute-force attacks.
- **CSRF Protection:** Protects forms against Cross-Site Request Forgery.
- **Session Management:** Maintains authenticated user sessions.
- **Access Control:** Restricts protected pages and admin functionality.
- **Security Logging:** Records security-related activity for monitoring.

## Project Workflow

1. User registers using required details.
2. Password is validated and securely hashed.
3. Email verification is performed.
4. User logs in using credentials.
5. MFA verification is required when enabled.
6. Authenticated users access their dashboard.
7. Password recovery is available through email.
8. Admin can access protected management and security monitoring pages.

## Project Structure

```text
AUTHVANTA/
├── app/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── static/
│   ├── templates/
│   └── utils/
├── codearena/
├── docs/
├── tests/
├── run.py
├── run/setup scripts
├── requirements.txt
├── START_AUTHVANTA.bat
└── .gitignore
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/ShanviDreams/AUTHVANTA-Secure-Authentication-Portal.git
```

### 2. Navigate into the project

```bash
cd AUTHVANTA-Secure-Authentication-Portal
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure environment variables

Configure the required environment variables and database settings locally before running the application. Do not upload passwords, secret keys or email credentials to GitHub.

### 7. Run the application

```bash
python run.py
```

## Testing

The project includes automated tests using Pytest for application startup, authentication, password hashing, CSRF validation, password strength validation and rate limiting.

Run tests:

```bash
python -m pytest tests/test_app.py -v
```

## Future Scope

- Advanced security analytics
- Improved OAuth integrations
- Additional authentication mechanisms
- Enhanced monitoring and reporting
- Further security testing and hardening

## Author

**Shanvi Lakhwan**

BE Computer Science and Engineering

Cybersecurity Project

---

*AUTHVANTA — Secure Identity. Smarter Access.*
