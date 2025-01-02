# Cloud Application

This is a cloud-based file storage system built with [Django](https://www.djangoproject.com/), integrated with [AWS S3](https://aws.amazon.com/s3/) for backend storage and using a MySQL database for user and data management.

## Features

1. **User Registration, Login, and Logout**  
   - Utilizes Django’s built-in auth system to provide user registration, login, and logout functionality.
2. **File Upload, Viewing, and Deletion**  
   - Uses [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) to connect to AWS S3 for file uploads, and provides a user interface for managing personal files.
3. **Directory-Based User Isolation**  
   - Uploaded files are stored under a directory named after the user's username, ensuring isolation among different users.
4. **Views and Templates**  
   - Django Templates + CSS (in the `static` folder) to create a simple interface.
5. **MySQL Database**  
   - Stores user information; can be configured in `settings.py`.


## Project Structure

```bash
cloudapplication
├── cloudapplication
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── mainapp
│   ├── migrations
│   ├── static
│   │   └── styles.css           # Custom CSS
│   ├── templates
│   │   ├── file_list.html
│   │   ├── header.html
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── profile.html
│   │   ├── register.html
│   │   └── upload.html
│   ├── upload_file
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── .env
├── .gitignore
├── manage.py
└── requirements.txt
```


## Main File Overview

- **cloudapplication/settings.py**  
  Core Django settings file, including configurations for the database, AWS S3, and static resources.

- **cloudapplication/urls.py**  
  URL routing configuration, mapping the home page / file list / uploads to functions in `mainapp/views.py`.

- **mainapp/views.py**  
  Primarily handles file uploads, deletions, user registration and login logic, as well as interactions with S3.

- **mainapp/forms.py**  
  Defines the user registration form and the file upload form.

- **mainapp/templates/**  
  Django template files (HTML). You can add `{% load static %}` to reference `styles.css` and other static files.


## Installation and Usage

### Prerequisites

- **Python**: 3.11.4  
- **Django**: 5.1.2  

### Steps

1. Clone this repository:
   ```bash
   git clone https://github.com/tonys61311/cloudapplication.git
   cd cloudapplication
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   或 venv\Scripts\activate  # Windows
   ```

3. Install dependencies：
   ```bash
   pip install -r requirements.txt
   ```

4. Create / Edit the .env 檔 (optional)

5. Configure the database (MySQL)

6. Apply migrations (migrate)
   ```bash
   python manage.py migrate
   ```

7. Create a superuser (optional)
   ```bash
   python manage.py createsuperuser
   ```

8. Run the development server
   ```bash
   python manage.py runserver
   ```