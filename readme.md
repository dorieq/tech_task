## Table of Contents

- [Installation](#installation)

## Installation

1. **Navigate into the project directory:**

    ```bash
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

4. **Install the project dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Set up the database:**

    ```bash
    python manage.py migrate
    ```

6. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

8. **Access the project in your web browser at `http://localhost:8000/`.**
## Creating Superuser for Admin

To access the Django admin interface and perform administrative tasks such as managing users, groups, and permissions, you'll need to create a superuser. Follow these steps to create a superuser:

1. Run the following command in your terminal to create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

2. You'll be prompted to enter a username, email address, and password for the superuser. Follow the prompts to provide the required information.

3. Once the superuser is created successfully, you can access the Django admin interface by navigating to the `/admin/` URL in your web browser. Log in using the username and password you provided during the superuser creation process.

4. You'll now have access to various administrative tasks in the Django admin interface, allowing you to manage your project's data and configuration efficiently.
