# Mehfil-e-Shayari 🏮

A dedicated digital space for the poetic soul, **Mehfil-e-Shayari** is a Flask-based platform designed to capture the atmosphere of a traditional late-night "Mehfil" (gathering of poetry lovers). 

It features a calm, warm, dark-mode aesthetic with golden accents, emphasizing the beauty of the written word.

## ✨ Features
- **Immersive Public Interface**: 
    - Dark theme (`Stone-900`) and warm typography (`Cinzel`, `Merriweather`).
    - Responsive grid of beautiful poetry cards.
    - Focus mode for reading individual pieces.
- **Secure Admin Panel**:
    - Session-based authentication.
    - Full CRUD (Create, Read, Update, Delete) capability.
    - Draft/Publish workflow.
    - Themed dashboard that matches the public site's calm mood.
- **Modern UI Components**:
    - Styled with Tailwind CSS and custom CSS for glowing effects.
    - Soft, rounded aesthetics (`rounded-xl` buttons and inputs).
    - Responsive design for mobile and desktop.

## 🛠️ Technology Stack
- **Backend**: Python 3.12, Flask, Werkzeug Security, MySQL Connector.
- **Database**: MySQL (Compatible with MariaDB/SQLite).
- **Frontend**: Jinja2 Templates, Tailwind CSS (via CDN), Google Fonts.
- **Styling**: Partial custom CSS `mehfil.css` for enhanced components (glows, rounded inputs).

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- MySQL Server

### Installation
1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/mehfil-e-shayari.git
    cd mehfil-e-shayari
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Setup Database**
    - Create a database (e.g., `mehfil_e_shayari`).
    - Run the schema script to create tables:
        ```bash
        mysql -u root -p mehfil_e_shayari < database/schema.sql
        ```

4.  **Configure Application**
    - Set environment variables in `.env` or edit `config.py` directly for `DB_USER`, `DB_PASSWORD`, etc.

5.  **Create Admin User**
    - Run the helper script to create your first admin account:
        ```bash
        python create_admin.py
        ```

6.  **Run the Server**
    ```bash
    python app.py
    ```
    Visit `http://localhost:5000` in your browser.

## 📸 Screenshots
*(Add your screenshots to the `screenshots/` folder)*
- **Home**: `screenshots/home.png`
- **Detail**: `screenshots/detail.png`
- **Admin Dashboard**: `screenshots/dashboard.png`
- **Editor**: `screenshots/editor.png`

## 🤝 Contributing
This is a personal project designed as a portfolio piece. Feel free to fork it and add your own features like user comments, "Wah Wah" buttons (likes), or audio recitations.

## 📜 License
MIT License. Crafted with ❤️ for Poetry.
