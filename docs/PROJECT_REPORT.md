# AUTHVANTA
## Secure User Registration and Login Portal

**Tagline:** Secure Identity. Smarter Access.  
**Developed by:** Shanvi  
**Branch:** BE-CSE  
**Semester:** 5

---

## 1. Introduction

AUTHVANTA is a web-based secure user registration and login portal designed to protect user accounts and provide controlled access to application resources. It uses multiple security mechanisms to improve authentication, account protection and monitoring.

## 2. Problem Statement

Basic login systems may be vulnerable to weak passwords, unauthorized access, brute-force attacks and insecure password storage. AUTHVANTA addresses these concerns through password hashing, email verification, multi-factor authentication and security monitoring.

## 3. Objectives

- Develop a secure user registration and login system.
- Store passwords using Argon2 hashing.
- Verify user email addresses.
- Implement Time-Based One-Time Password (TOTP) MFA.
- Provide secure password reset functionality.
- Restrict repeated login attempts.
- Protect forms using CSRF protection.
- Provide admin access and security monitoring.

## 4. Technologies Used

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| Database | MySQL |
| Password Security | Argon2 |
| Authentication | Flask-Login |
| MFA | TOTP |
| Email | Gmail SMTP |
| Security | CSRF Protection, Rate Limiting |
| Testing | Pytest |
| Development | Visual Studio Code, Git |

## 5. Main Modules

1. User Registration
2. Email Verification
3. User Login and Logout
4. Password Hashing
5. Multi-Factor Authentication
6. Password Reset
7. User Dashboard
8. Admin Authentication
9. Admin Dashboard
10. Security Logs and Login Attempt Monitoring

## 6. System Workflow

1. A new user submits the registration form.
2. The system validates the submitted information.
3. The password is hashed using Argon2.
4. An email verification link is sent to the registered email.
5. The user verifies the email address.
6. The user logs in using valid credentials.
7. MFA is required where configured.
8. Successful authentication provides access to the user dashboard.
9. Security events are recorded for monitoring.
10. Administrators access protected administration features.

## 7. Security Features

- Argon2 password hashing.
- Email verification.
- TOTP-based multi-factor authentication.
- Password reset through email.
- Login rate limiting.
- CSRF protection.
- Protected user and admin routes.
- Security event logging.
- Login attempt tracking.

## 8. Testing

The application was tested using Pytest.

**Latest recorded test result: 11 passed.**

Tests cover application startup, login pages, admin login page, authentication-protected dashboards, CSRF rejection, password hashing, password verification, password strength validation and login rate limiting.

## 9. Expected Outcome

AUTHVANTA provides a centralized web-based authentication portal with additional security layers for user accounts and administrative access.

## 10. Future Scope

- OAuth-based social login.
- Advanced anomaly detection.
- Device and session management.
- Security analytics and reporting.
- Deployment with production-grade HTTPS and monitoring.

## 11. Conclusion

AUTHVANTA demonstrates the implementation of a secure authentication system using modern web development and cybersecurity practices. It combines password protection, email verification, MFA, access control and security monitoring in one application.
