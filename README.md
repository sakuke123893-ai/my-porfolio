# Dharam Jai Vardhan Reddy — Portfolio Website

A production-grade personal portfolio website for **Dharam Jai Vardhan Reddy**, Computer Science Engineering Student (Class of 2028).

## 🌐 Live Portfolio Features

- **5 Full-Screen Slide Deck** with CSS scroll-snap (`#about`, `#skills`, `#projects`, `#timeline`, `#contact`)
- **Ambient Animated Background** — cyber atmospheric frame (animated WebP)
- **Recruiter-First Design** with glowing avatar, status badge, and recruiter stats
- **1-Click Printable Digital Resume Modal** with `@media print` PDF support
- **Project Technical Architecture Deep-Dives** — interactive system flow modals
- **1-Click Recruiter Skill Filter Tabs** — filter projects by `Flask`, `React`, `IoT`, `Cloud`
- **1-Click Email Copy + Direct WhatsApp CTA**
- **Social Sharing Meta Tags** (OpenGraph + Twitter Card)
- **Contact Form** backed by Python/Flask + SQLite with parameterized queries (SQL injection safe)
- **Fully Editable** — update all content via `portfolio_data.json`

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, Vanilla CSS3, JavaScript (ES6+) |
| Backend | Python 3 + Flask |
| Database | SQLite3 (parameterized queries) |
| Fonts | Google Fonts (Inter, Outfit, JetBrains Mono) |
| Assets | Animated WebP ambient background |

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/sakuke123893-ai/jaiport.git
cd jaiport

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the server
python app.py
```

Open your browser at **`http://127.0.0.1:5000`**

## 📁 Project Structure

```
jaiport/
├── app.py                  # Flask backend server
├── database.py             # SQLite connection manager
├── schema.sql              # Database schema & seed data
├── portfolio_data.json     # ✏️ Editable portfolio content
├── requirements.txt        # Python dependencies
├── index.html              # Static HTML (works without Flask)
├── templates/
│   └── index.html          # Jinja2 template for Flask rendering
└── static/
    ├── css/style.css       # Complete design system
    ├── js/main.js          # Client-side interactivity
    └── images/
        ├── profile-photo.png
        └── animated-frame.webp
```

## ✏️ How to Edit Content

All text, skills, projects, and certifications are in one place:

```bash
portfolio_data.json
```

Just edit the JSON values and refresh your browser — no HTML or Python changes needed!

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serves the portfolio website |
| `GET` | `/api/portfolio-data` | Returns all editable portfolio config |
| `GET` | `/api/projects` | Returns all featured projects |
| `POST` | `/api/contact` | Saves contact form submissions to SQLite |
| `GET` | `/api/messages` | View saved contact inquiries |

## 👨‍💻 About

**Dharam Jai Vardhan Reddy**  
B.Tech Computer Science Engineering • Class of 2028  
📧 sakuke123893@gmail.com  
📱 +91 8328523265  
🔗 [LinkedIn](https://www.linkedin.com/in/dharam-jai-vardhan-reddy-6944a4328/)  
🐙 [GitHub](https://github.com/sakuke123893-ai)
