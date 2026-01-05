# Secure Event Management Application

A secure, robust Django web application designed for managing events with a strong focus on security best practices, including OWASP ASVS compliance.

## Project Description
This application allows users to register, view events, and manage their profiles. Administrators have access to a dedicated dashboard to manage events and registrations, viewing security audit logs. the system implements strict access controls, secure session management, and protection against common web vulnerabilities.

## Security Features
This project implements the following security measures:
*   **Authentication**: Secure login/logout flows, password hashing (PBKDF2), and strong password validators.
*   **Authorization**: Role-Based Access Control (RBAC). Only admins can access the dashboard; regular users are restricted to public views.
*   **Session Security**: 
    *   `SESSION_COOKIE_HTTPONLY = True` (Prevents XSS session theft)
    *   Session timeout set to 60 seconds for high security.
    *   Session expires on browser close.
*   **CSRF Protection**: All forms protected with CSRF tokens. Middlewares enabled.
*   **Audit Logging**: Critical actions (login, registration, admin actions) are logged to `security.log` for audit trails.
*   **Input Validation**: Strict form validation to prevent injection attacks.

## Dependencies
*   **Python** 3.10+
*   **Django** 5.0+
*   **django-ratelimit** (for login protection)

## Installation Steps
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/danialnunez16-creator/secure-event-app.git
    cd secure-event-app
    ```
2.  **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```
3.  **Install Dependencies**:
    ```bash
    pip install django django-ratelimit
    ```
4.  **Configure Environment**:
    *   Copy `.env.example` to `.env`
    *   Set your `SECRET_KEY` and `DEBUG=False`

## How to Run
1.  **Apply Migrations**:
    ```bash
    python src/manage.py migrate
    ```
2.  **Create Superuser**:
    ```bash
    python src/manage.py createsuperuser
    ```
3.  **Start the Server**:
    ```bash
    python src/manage.py runserver
    ```
    Access the app at `http://127.0.0.1:8000`.

## Application Screenshots
*(Add your screenshots here)*

*   **Login Page**
    ![Login Page](docs/screenshots/login.png)

*   **Admin Dashboard**
    ![Admin Dashboard](docs/screenshots/dashboard.png)
