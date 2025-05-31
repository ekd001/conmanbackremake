# ConmanBackRemake

Conman is a backend application developed with Django and Django REST Framework. It's purpose is to manage ESAAD entrance exam. This project includes features such as user management, profiles, contests, dossiers, students, and much more. It is designed to be extensible and easy to configure.

## Key Features

- User and profile management.
- Contest and general information management.
- Creation and management of dossiers, obtained diplomas, and students.
- Generation of mock data for development and testing.
- RESTful API with Swagger documentation.

---

## Prerequisites

Before starting, make sure you have the following installed on your machine:

- Python 3.9 or higher
- `pip` (Python package manager)
- `conda` (optional, for managing environments)
- SQLite database (default)

---

## Installation

### Step 1: Clone the repository

Clone this repository to your local machine:

```bash
git clone git@github.com:ekd001/conmanbackremake.git
cd conmanbackremake
```

### Step 2: Create a virtual environment

#### Using `venv`:
```bash
python -m venv env
source env/bin/activate  # On Linux/Mac
env\Scripts\activate      # On Windows
```

#### Using `conda`:
```bash
conda create -n conmanback python=3.9 -y
conda activate conmanback
```

### Step 3: Install dependencies

#### Using `pip`:
```bash
pip install django djangorestframework drf-yasg pyjwt cryptography requests pillow pyyaml djangorestframework-simplejwt
```

#### Using `conda`:
```bash
conda install -y -c conda-forge django djangorestframework drf-yasg pyjwt cryptography requests pillow pyyaml
pip install djangorestframework-simplejwt
```

---

## Starting the Project

### Step 1: Initial setup

Run the `first_start.sh` script to set up the project, apply migrations, generate mock data, and start the server:

```bash
chmod +x first_start.sh
./first_start.sh
```

### Step 2: Access the application

Once the server is running, access the application at [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## Mock User Access

The `first_start.sh` script generates mock users for testing purposes. Here are their credentials:

- **Admin**:
  - Access Code: `admin123`
  - Password: `adminpass`
- **User**:
  - Access Code: `user123`
  - Password: `userpass`

---

## API Documentation

Swagger documentation is available at the following URL once the server is running:

[http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)

---

## Project Structure

Here is an overview of the project structure:

```
conmanbackremake/
├── api/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── authentication.py
│   ├── mocks_data.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── services.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
├── db.sqlite3
├── manage.py
├── first_start.sh
└── README.md
```