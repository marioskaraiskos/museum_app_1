# 🏛️ Museum Web Application

> **A responsive and accessible museum web application built with Flask** | Showcasing modern web design principles and user-centered UX

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/flask-2.0%2B-green?style=flat-square&logo=flask)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)
![Status](https://img.shields.io/badge/status-Prototype-yellow?style=flat-square)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🏠 **Home Page** | Overview with featured exhibits and upcoming events |
| 🖼️ **Exhibits Gallery** | Browse museum collections and exhibits |
| 📰 **News Section** | Latest museum news and announcements |
| 📅 **Events Page** | View upcoming and past events |
| 🛎️ **Services Info** | Available services and amenities |
| 💬 **Feedback Form** | Visitor feedback submission |
| 📧 **Contact Page** | Museum information and contact form |
| 👤 **User Authentication** | Login and registration system (prototype) |
| 📱 **Responsive Design** | Works seamlessly on desktop, tablet, and mobile |
| ♿ **Accessibility** | Semantic HTML and WCAG compliance |
| 🎨 **Modern UI** | Clean and professional design |

---

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher** ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/download))
- **pip** (comes with Python)

### Installation Steps

#### 1️⃣ Clone the Repository

```bash
git clone https://github.com/marioskaraiskos/museum_app_1.git
cd museum_app_1
```

#### 2️⃣ Create a Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4️⃣ Run the Application

```bash
python app.py
```

#### 5️⃣ Access the Application

Open your browser and navigate to:

```
🌐 http://127.0.0.1:5000
```

---

## 📁 Project Structure

```
museum_app_1/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Project dependencies
├── templates/            # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── exhibits.html
│   ├── news.html
│   ├── events.html
│   ├── services.html
│   ├── feedback.html
│   ├── contact.html
│   ├── login.html
│   └── register.html
│
├── static/               # Static files
│   ├── css/
│   │   └── style.css
│   ├── images/
│   └── js/
│       └── script.js
│
└── README.md            # This file
```

---

## 🛠️ Technology Stack

| Technology | Purpose |
|-----------|---------|
| ![Flask](https://img.shields.io/badge/-Flask-black?style=flat&logo=flask) | Backend web framework |
| ![Python](https://img.shields.io/badge/-Python-3776ab?style=flat&logo=python&logoColor=white) | Programming language |
| ![HTML5](https://img.shields.io/badge/-HTML5-E34C26?style=flat&logo=html5&logoColor=white) | Markup language |
| ![CSS3](https://img.shields.io/badge/-CSS3-1572B6?style=flat&logo=css3&logoColor=white) | Styling |
| ![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) | Client-side interactivity |

---

## 📝 Usage

### For Visitors

1. **Browse Exhibits** 🖼️ - Explore the museum's collections
2. **Check Events** 📅 - View upcoming events and activities
3. **Read News** 📰 - Stay updated with latest announcements
4. **Learn About Services** 🛎️ - Discover what the museum offers
5. **Submit Feedback** 💬 - Share your museum experience
6. **Register & Login** 👤 - Create an account (future: book visits)
7. **Contact Us** 📧 - Get in touch with the museum

### For Developers

- Explore the clean, modular code structure
- Study responsive design patterns
- Review accessibility best practices
- Extend functionality as needed

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Port 5000 already in use** | Change port in `app.py` or stop the conflicting service |
| **Module not found error** | Ensure virtual environment is activated and dependencies are installed |
| **Page styling issues** | Clear browser cache (Ctrl+Shift+Delete or Cmd+Shift+Delete) |
| **Form not submitting** | Check browser console for errors (F12) |

---

## 🚧 Future Development

- 📅 **Visit Booking System** - Allow users to book museum visits
- 💳 **Payment Integration** - Online ticket purchasing
- 🗺️ **Interactive Map** - Museum floor plan navigation
- 🎧 **Audio Guide** - Guided tour experience
- 🔍 **Advanced Search** - Search exhibits and collections
- 📊 **Admin Dashboard** - Manage content and users
- 📱 **Mobile App** - Native mobile application

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** - see the LICENSE file for details.

---

## 👨‍💻 Author

**Mario Skaraiskos**

- GitHub: [@marioskaraiskos](https://github.com/marioskaraiskos)
- Repository: [museum_app_1](https://github.com/marioskaraiskos/museum_app_1)

---

## 📞 Support

Have questions or found a bug? Feel free to:

- 📧 Open an [Issue](https://github.com/marioskaraiskos/museum_app_1/issues)
- 💬 Start a [Discussion](https://github.com/marioskaraiskos/museum_app_1/discussions)
- 📝 Check existing [Issues](https://github.com/marioskaraiskos/museum_app_1/issues)

---

## 🌟 Show Your Support

If this project helped you, please consider giving it a ⭐ Star!

---

[![Live Demo](https://img.shields.io/badge/Live-Demo-green)](https://museum-app-1-gdps.onrender.com/)

<div align="center">

**Made with ❤️ and Flask by Marios karaiskos**

</div>
