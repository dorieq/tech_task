## Table of Contents

- [Installation](#installation)
- [Redis Setup](#redis-setup)
- [Environment Variables](#environment-variables)
- [Running Tests](#running-tests)
- [Creating Superuser for Admin](#creating-superuser-for-admin)
- [Running the Development Server](#running-the-development-server)

---

## Installation

Follow these steps to set up the Django project:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/your_project.git
    cd your_project
    ```

2. **Create a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```

    - On Windows (PowerShell):

        ```bash
        .\venv\Scripts\Activate.ps1
        ```

4. **Install project dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Set up the database:**

    ```bash
    python manage.py migrate
    ```

---

## Redis Setup

Redis is required for caching and other asynchronous tasks. Follow these steps to install and start Redis:

1. **Install Redis (if not already installed):**

    - On macOS (using Homebrew):
      ```bash
      brew install redis
      ```

    - On Ubuntu/Debian:
      ```bash
      sudo apt update
      sudo apt install redis-server
      ```

    - On Windows (using WSL or Redis for Windows):
      ```bash
      wsl --install
      sudo apt install redis-server
      ```

2. **Start Redis server:**

    ```bash
    redis-server
    ```

3. **Verify Redis is running:**

    ```bash
    redis-cli ping
    # Response should be PONG
    ```

4. **Ensure Redis starts on boot (Linux/Mac):**

    ```bash
    sudo systemctl enable redis
    sudo systemctl start redis
    ```

---

## Environment Variables

Create an `.env` file in the root directory to store sensitive configuration details:

```ini
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
REDIS_HOST=localhost
REDIS_PORT=6379
SECRET_KEY=your-secret-key
```
Alternatively, use `.env.ci` for CI pipelines:

```ini
DEBUG=False
DATABASE_URL=sqlite:///ci-db.sqlite3
REDIS_HOST=localhost
REDIS_PORT=6379
SECRET_KEY=test-secret
```
---
## Running Tests
Run automated tests to verify project stability and functionality:

### Ensure Redis is running:
```bash
redis-server
```

### Run tests with the following command:
```bash
python manage.py test
```

## Creating Superuser for Admin
To access the Django admin interface and manage users, create a superuser:

### Run the following command:
```bash
python manage.py createsuperuser
```
Provide the requested details (username, email, and password).

## Accessing the Admin Interface
To access the Django admin interface, follow these steps:

### Access the admin interface at:
```bash
http://localhost:8000/admin/
```

---

## Running the Development Server
### Ensure all migrations are applied:
```bash
python manage.py migrate
```
### Run the server:
```bash
python manage.py runserver
```

### Access the project in your web browser at:
```
http://localhost:8000/
```