# ShareSphere - Campus Marketplace Platform

<div align="center">
  <img src="https://img.shields.io/badge/Django-4.2+-green.svg" alt="Django">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Status-Demo-orange.svg" alt="Status">
</div>

## 📋 Project Overview

**ShareSphere** is a Django-based campus marketplace platform that enables students to buy, sell, and share resources within their academic community. The platform includes a marketplace for items and a ride-sharing system called RideMate.

## ✨ Key Features

###🔑 Login & Signup
- Secure registration for new users
- Email and password validation
- Password hashing and secure storage
- Login/logout functionality
- Session-based authentication
  
### 🛒 Buy & Sell Marketplace
- Product listings with categories (books, electronics, furniture)
- Search and filter functionality
- Image upload for products
- Direct messaging between users
- User ratings and feedback

### 🚗 RideMate - Ride Sharing
- Offer and request rides
- Route planning and scheduling
- Cost sharing and calculation
- User verification system
- Booking management

### 👤 User Management
- USN-based authentication
- Profile management
- Rating and feedback system
- Activity tracking

## 🛠️ Technology Stack

- **Backend**: Django 4.2+, Python 3.8+
- **Database**: SQLite (development), MySQL (production)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Additional**: Font Awesome, SweetAlert2

## 📁 Project Structure

```
sharesphere/
├── BuySell/              # Marketplace app
├── ridemate/             # Ride sharing app
├── login/                # Authentication app
├── templates/            # HTML templates
├── static/               # CSS, JS, images
├── media/                # User uploads
└── utils/                # Utility functions
```

## 🚀 Quick Setup

### Prerequisites
- Python 3.8+
- pip

### Installation Steps

1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/sharesphere.git
   cd sharesphere
   ```

2. **Setup Virtual Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Admin User**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Server**
   ```bash
   python manage.py runserver
   ```

7. **Access Application**
   - Main site: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## 🗄️ Database Configuration

### SQLite (Default)
No additional setup required for development.

### MySQL (Production)
```sql
CREATE DATABASE django_sharesphere;
CREATE USER 'django_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON django_sharesphere.* TO 'django_user'@'localhost';
FLUSH PRIVILEGES;
```

Update `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_sharesphere',
        'USER': 'django_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

## 🔒 Security Features

- CSRF protection
- SQL injection prevention
- XSS protection
- Secure file uploads
- User authentication
- Session management

## 📱 Screenshots

| Feature | Description |
|---------|-------------|
| <img src="https://github.com/Rohitshahare34/SHARESPHERE-student-Resource-and-Petrol-sharing-platform/raw/9d9029172fef9db90418bc58b0db4b17b740ab3d/Screenshots/Screenshot%202025-07-06%20142439.png" width="300"/> <img src="https://github.com/Rohitshahare34/SHARESPHERE-student-Resource-and-Petrol-sharing-platform/raw/236494f98f13b3647670d2f41768c6c69822dd18/Screenshots/Screenshot%202025-07-06%20142456.png" width="300"/> | Login and Signup pages |
| <img src="https://github.com/Rohitshahare34/SHARESPHERE-student-Resource-and-Petrol-sharing-platform/raw/236494f98f13b3647670d2f41768c6c69822dd18/Screenshots/Screenshot%202025-07-06%20142007.png" width="300"/> <img src="https://github.com/Rohitshahare34/SHARESPHERE-student-Resource-and-Petrol-sharing-platform/raw/9514f6118c7ba7b12090327b21f1689b49f0426f/Screenshots/Screenshot%202025-07-06%20141826.png" width="300"/> | Main landing page (Homepage) |
| <img src="https://github.com/Rohitshahare34/SHARESPHERE-student-Resource-and-Petrol-sharing-platform/raw/9514f6118c7ba7b12090327b21f1689b49f0426f/Screenshots/Screenshot%202025-07-06%20141739.png" width="200"/> <img src="https://github.com/Rohitshahare34/SHARESPHERE-student-Resource-and-Petrol-sharing-platform/raw/9514f6118c7ba7b12090327b21f1689b49f0426f/Screenshots/Screenshot%202025-07-06%20142312.png" width="200"/> <img src="https://github.com/Rohitshahare34/SHARESPHERE-student-Resource-and-Petrol-sharing-platform/raw/9514f6118c7ba7b12090327b21f1689b49f0426f/Screenshots/Screenshot%202025-07-06%20141723.png" width="200"/> | Buy & Sell interface |
| <img src="https://via.placeholder.com/600x300/f0ad4e/ffffff?text=RideMate" width="600"/> | Ride sharing system |
| <img src="https://github.com/Rohitshahare34/SHARESPHERE-student-Resource-and-Petrol-sharing-platform/raw/236494f98f13b3647670d2f41768c6c69822dd18/Screenshots/Screenshot%202025-07-06%20142354.png" width="600"/> | User profile page |



## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -m 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Open Pull Request

## 🐛 Bug Reports

Please include:
- Problem description
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)

## 📞 Contact

- **Email**: contact@sharesphere.edu
- **GitHub Issues**: [Report Issues](https://github.com/yourusername/sharesphere/issues)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔄 Version History

- **v1.0.0**: Initial release with marketplace and ride sharing
- **v1.1.0**: Added user ratings and feedback
- **v1.2.0**: Enhanced UI/UX and mobile responsiveness
- **v1.3.0**: Advanced search and filtering features

---

<div align="center">
  <p><strong>Made with ❤️ for the student community</strong></p>
  <p>ShareSphere - Connecting Students, Sharing Resources</p>
</div>
