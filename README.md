# MAD-2 Project: Influencer and Sponsorship Coordination Platform

## Overview
This project is an influencer and sponsorship coordination platform built using Vue.js for the frontend and Flask for the backend. The application uses SQLite and SQLAlchemy for database management, Bootstrap for styling, Redis for caching, and Celery for background jobs.

## Tech Stack
- **Flask**: For API
- **Vue.js (version 3)**: For UI
- **SQLite and SQLAlchemy**: For Database work
- **Vue.js CLI**: To start the project in the development server
- **Bootstrap**: For modals and styling
- **Redis**: For caching
- **Celery and Redis**: For backend jobs

## Setup Instructions

### Step 1: Create and Activate Virtual Environment

#### For WSL
1. Open your WSL terminal.
2. Navigate to your project directory.
3. Create a virtual environment:
    ```bash
    python3 -m venv venv
    ```
4. Activate the virtual environment:
    ```bash
    source venv/bin/activate
    ```

#### For PowerShell
1. Open PowerShell.
2. Navigate to your project directory.
3. Create a virtual environment:
    ```powershell
    python -m venv venv
    ```
4. Activate the virtual environment:
    ```powershell
    .\venv\Scripts\Activate
    ```

### Step 2: Clone the Project
1. Clone the project repository:
    ```bash
    git clone <https://github.com/rahulsharmaYS/MAD-2-Project>
    ```
2. Navigate to the project directory:
    ```bash
    cd <project_directory>
    ```

### Step 3: Install Backend Dependencies
1. Install the necessary Python packages:
    ```bash
    pip install -r requirements.txt
    ```

### Step 4: Setup Frontend
1. Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2. Ensure Node.js is installed in your local environment.
3. Install the necessary Node.js packages:
    ```bash
    npm install
    ```
4. Install additional dependencies listed in `dependencies.txt`:
    ```bash
    npm install $(cat dependencies.txt | xargs)
    ```

### Step 5: Run the Project
1. Navigate to the frontend directory (in case you are not):
    ```bash
    cd frontend
    ```
2. Run the development server (both frontend & backend):
    ```bash
    npm run dev
    ```

### Step 6: Setup Emailing
1. Create a Google App Password and update the email settings in `tasks.py`:
    ```python
    # Replace 'your_own_gmail@gmail.com' and 'your_smtp_password' with your own credentials in backend/tasks.py
    EMAIL = 'your_own_gmail@gmail.com'
    PASSWORD = 'your_smtp_password'
    ```
2. Save the changes to `tasks.py`.

### Step 7: Start Celery Workers and Beat
1. Open two additional terminals.
2. Activate the venv environment here too.
3. In each terminal, navigate to the backend directory:
    ```bash
    cd backend
    ```
4. Start the Celery worker in the first terminal:
    ```bash
    celery -A engine.celery worker -P solo --loglevel=info
    ```
5. Start the Celery beat in the second terminal:
    ```bash
    celery -A engine.celery beat --loglevel=debug
    ```

## Disclaimer
**Caution**: Do not use random Gmail accounts as this application will send emails to actual Gmail addresses. Ensure you use valid and authorized email credentials.

That's it! The project should now be up and running.
