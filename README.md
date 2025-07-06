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
| ![loginpage](https://github.com/Rohitshahare34/SHARESPHERE-student-Resource-and-Petrol-sharing-platform/blob/9d9029172fef9db90418bc58b0db4b17b740ab3d/Screenshots/Screenshot%202025-07-06%20142439.png) | Main landing page |
| ![sign up page ](https://via.placeholder.com/400x200/4e73df/ffffff?text=Homepage) | Main landing page |
| ![Homepage](https://via.placeholder.com/400x200/4e73df/ffffff?text=Homepage) | Main landing page |
| ![Buysellpage](https://via.placeholder.com/400x200/28a745/ffffff?text=Marketplace) | Buy & Sell interface |
| ![RideMate](https://via.placeholder.com/400x200/f0ad4e/ffffff?text=RideMate) | Ride sharing system |
| ![Profile](https://via.placeholder.com/400x200/1e2b3c/ffffff?text=Profile) | User profile page |

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
