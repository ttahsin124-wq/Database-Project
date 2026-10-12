---

```markdown
<div align="center">

# 📰 News Blog Management System
### *A sleek, dark-themed Desktop Management Suite built with Python, Tkinter & MySQL*

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![ttkbootstrap](https://img.shields.io/badge/ttkbootstrap-Cyborg_Theme-17a2b8?style=for-the-badge&logo=bootstrap&logoColor=white)](https://ttkbootstrap.readthedocs.io/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=for-the-badge)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

<br />

<p align="center">
  <b>Manage users, author posts, filter records, and track publications seamlessly with a modern dark interface.</b>
</p>

</div>

---

## 🌟 Overview

The **News Blog Management System** is a lightweight yet feature-rich desktop application designed for news outlets, blogging teams, and editorial offices. Built using **ttkbootstrap**'s sleek `cyborg` theme, it replaces clunky native UI elements with responsive, modern styling and connects to a **MySQL** relational database backend.

---

## ✨ Features

### 👤 User Management
- **Full CRUD Support**: Add new users, update user records (Name, Email, Age, Contact), and delete inactive members.
- **Cascading Deletions**: Automatically cleans up associated news articles when a user is removed.
- **Dynamic Search**: Filter users instantly by `Name`, `User ID`, or `Age`.
- **Author Publication Viewer**: Double-click any user to open a pop-up listing all articles written by that author, with full read-only body inspection.

### 📰 News Management
- **Multi-Author Publishing**: Select authors directly from a dropdown populated from the database.
- **Smart Snippets**: Long article titles are intelligently formatted and truncated with ellipsis (`...`) in the main treeview table for clean layout readability.
- **Article Reader & Editor**: Double-click articles to instantly open the editor modal to update headline and story content.
- **Quick Search**: Filter news records by `Title`, `News ID`, or `Author Name`.

### ⚡ UI & Performance Highlights
- 🌙 **Modern Dark Mode**: Powered by ttkbootstrap's `cyborg` palette with deep-navy header highlights.
- 🔄 **Bidirectional Column Sorting**: Click any column header to sort in ascending (`↑`) or descending (`↓`) order, with automatic numeric and alphabetical handling.
- 🛡️ **Data Validation**: Built-in validation checks (e.g., numeric validation for age).

---

## 🗄️ Database Architecture

The application requires a MySQL database named **`news_project`**. Run the following SQL script in MySQL Workbench, phpMyAdmin, or your MySQL CLI before launching the application:

```sql
-- 1. Create the database
CREATE DATABASE IF NOT EXISTS news_project
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE news_project;

-- 2. Create the Users table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    age INT,
    contact_number VARCHAR(25)
);

-- 3. Create the News table
CREATE TABLE IF NOT EXISTS news (
    news_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_news_user 
        FOREIGN KEY (user_id) 
        REFERENCES users(user_id) 
        ON DELETE CASCADE
);
```

> [!NOTE]
> The `ON DELETE CASCADE` constraint guarantees relational integrity: deleting a user automatically removes all their submitted articles.

---

## 🚀 Getting Started

### 📋 Prerequisites

Ensure you have the following installed on your system:
- **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
- **MySQL Server 8.0+**: [Download MySQL](https://dev.mysql.com/downloads/installer/)

---

### 📦 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/news-blog-management.git
   cd news-blog-management
   ```

2. **Create and Activate a Virtual Environment** *(Recommended)*
   - **Windows:**
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies**
   ```bash
   pip install ttkbootstrap mysql-connector-python
   ```

4. **Configure Database Connection**
   Open the application script (`main.py` or your script name) and configure the credentials in the `get_db()` function:
   ```python
   def get_db():
       try:
           conn = mysql.connector.connect(
               host="localhost",
               user="YOUR_MYSQL_USERNAME",      # e.g., root or nisa_tahsin
               password="YOUR_MYSQL_PASSWORD",  # e.g., 123456789
               database="news_project"
           )
           return conn
       except mysql.connector.Error as e:
           messagebox.showerror("Database Error", f"Could not connect to MySQL:\n{e}")    
           return None
   ```

   > [!TIP]
   > For production setups, consider moving credentials to a `.env` file or environment variables rather than hardcoding them in the source.

---

### 🖥️ Running the Application

Execute the application with:
```bash
python main.py
```

---

## 💡 Keyboard & Mouse Shortcuts

| Action | Target | Result |
| :--- | :--- | :--- |
| **Single Click** | Table Header | Sort table ascending (`↑`) / descending (`↓`) |
| **Double Click** | Any User Row | Opens a modal listing all news written by that user |
| **Double Click** | Any News Row | Opens the news editor popup to view or update content |

---

## 🛠️ Tech Stack

- **GUI Framework**: [Tkinter](https://docs.python.org/3/library/tkinter.html) & [ttkbootstrap](https://ttkbootstrap.readthedocs.io/) (`cyborg` theme)
- **Programming Language**: [Python 3](https://www.python.org/)
- **Database Engine**: [MySQL](https://www.mysql.com/)
- **Database Connector**: [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/)

---

## 📌 Project Roadmap & Future Enhancements

- [ ] Add `.env` support with `python-dotenv` for secure credential storage.
- [ ] Export news reports and user lists to PDF / Excel / CSV.
- [ ] Implement pagination for large datasets.
- [ ] Support category tags and thumbnail images for news posts.
- [ ] Add role-based authentication (Admin vs. Author login screen).

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the project.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <sub>Built with ❤️ by <a href="https://github.com/your-username">Nisa Tahsin</a></sub>
</div>
```

---

### 💡 Quick Tips for Even Better Presentation:
1. Replace `your-username` with your actual GitHub username.
2. If you name your Python file `main.py` or `app.py`, update that in the README accordingly.
3. You can take a screenshot of your running app and place an image right under the title using:
   ```markdown
   <p align="center">
     <img src="assets/preview.png" alt="App Preview" width="800"/>
   </p>
   ```
