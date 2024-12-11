# Football Forum

Hello!
This is a web application designed for football enthusiasts to connect.
They can share posts, and engage in discussions. This platform allows users to create and interact with posts, teams, players, and much more.

## Features

- User authentication (login, registration, and profile management).
- Role-based permissions (Admin, Redactor, and Regular User).
- Post management with approval workflows.
- Player and team management with permissions-based editing and deletion.
- Commenting, liking, and sharing functionality.
- Search functionality for players, teams, and posts.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setup Instructions](#setup-instructions)
3. [Populating Initial Data](#populating-initial-data)
4. [Features](#features)
5. [Acknowledgements](#acknowledgements)

---

## Prerequisites

To run this project locally, ensure you have the following installed:

1. **Python 3.9+**
2. **PostgreSQL**
3. **pip** (Python package manager)
4. **Git** (optional, for cloning the repo)
5. **Virtual Environment** (recommended)

---

## Setup Instructions

Follow these steps to set up and run the project locally.

### 1. Clone the Repository
Clone the project repository to your local machine:
```bash
git clone https://github.com/angeluzunov10/footballForum.git
cd footballForum
```

### 2. Create a Virtual Environment
Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate
```

### 3. Install Requirements
Install the necessary dependencies:
```bash
pip install -r requirements.txt
```

### 4. Configure the Environment Variables
Create a `.env` file in the root directory and add the following:
```env
SECRET_KEY=your-secret-key
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=127.0.0.1
DB_PORT=5432
ALLOWED_HOSTS=127.0.0.1,localhost
```

Replace the placeholders (e.g., `your_database_name`, `your_database_user`) with your PostgreSQL credentials.

### 5. Set Up the Database
Run the following commands to prepare the database:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Populate Initial Data
Load the initial data (roles, permissions, and other pre-filled data):
```bash
python manage.py loaddata initial_data.json
```

### 7. Run the Server
Start the development server:
```bash
python manage.py runserver
```

Visit the application in your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## Populating Initial Data

To prefill the database with essential data (e.g., roles, permissions, initial posts), ensure you have the `initial_data.json` file in the project root and run:

```bash
python manage.py loaddata initial_data.json
```

This will automatically create default user groups, permissions, and some demo data for the project.

---

## Features

- **Dynamic Permissions**: Roles are defined for Admins, Redactors, and Regular Users.
- **Post Approval Workflow**: Posts require approval based on user roles.
- **Player and Team Management**: CRUD functionality for players and teams.
- **Search and Filter**: Search functionality for posts, players, and teams.
- **Static File Handling**: Preconfigured static files and media handling.

---

## Acknowledgements

- **Django Framework**: Robust backend framework for Python.
- **Bootstrap**: For responsive and stylish frontend design.
- **Crispy Forms**: Enhanced forms with Bootstrap styling.
- **PostgreSQL**: Reliable and scalable database solution.
