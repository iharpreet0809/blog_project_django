# Blog_Project_Django- DIGITAL DIARY
🚀 Welcome to Digital Diary - A Modern Blogging Platform

A sophisticated full-stack blogging platform built with Django and MySQL, featuring a sleek UI, robust backend, and seamless user experience. This project showcases clean architecture, modern development practices, and attention to performance and security.

### Blog Features
- **Rich Text Editor**: CKEditor for creating formatted blog posts
- **Categories & Tags**: Organize content with categories and flexible tagging
- **Search & Filter**: Advanced search across titles, content, and tags
- **Pagination**: Efficient content browsing with pagination
- **RSS Feed**: Subscribe to blog updates
- **View Tracking**: Track post popularity
- **Featured Posts**: Highlight important content
- **Related Posts**: Suggest relevant content to readers
---

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- MySQL server
- (Optional) Virtual environment tool (e.g., `venv` or `virtualenv`)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/blog_project_django.git
   cd blog_project_django
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Database Setup

1. **Create a MySQL database and user:**
   ```sql
   CREATE DATABASE blog_db CHARACTER SET UTF8;
   CREATE USER 'blog_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON blog_db.* TO 'blog_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

2. **Configure database settings in `blog_project/settings.py`:**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'blog_db',
           'USER': 'blog_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

3. **Apply migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### Running the Project

1. **Create a superuser for the admin panel:**
   ```bash
   python manage.py createsuperuser
   ```

2. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

3. **Access the site:**
   - Blog: [http://localhost:8000/](http://localhost:8000/)
   - Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## Usage

- Visit the homepage to see the list of blog posts.
- Click on a post to view its details.
- Use the admin panel to add/edit/delete posts, categories, and tags.
- Upload images for blog covers and author profiles.
- Use the contact form to send messages (configure email settings as needed).

---

## Screenshots

<!-- Add screenshots here -->
#1. Home Page
![Home Page](screenshot/homepage.png)

#2. Blog Detail
![Blog Detail](screenshot/blog_detail.png)

#3. About & Contact
![Admin Panel](screenshot/about_contact.png)

#. Admin Panel
![Admin Panel](screenshot/admin_home.png)

---

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements or bug fixes.

---

## License

This project is licensed under the [GPU License](LICENSE).

---

## Contact

| <a href="https://www.linkedin.com/in/harpreet22/" target="_blank"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" alt="LinkedIn" height="22" style="vertical-align:middle;"/></a> | [![Email](https://img.shields.io/badge/email-talkwithharpreet@gmail.com-red?style=flat-square&logo=gmail)](mailto:talkwithharpreet@gmail.com) |
|:---:|:---:|

---
