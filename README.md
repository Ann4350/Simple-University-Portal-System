# 🎓 University Portal System (CLI-Based)

A terminal-based university portal built in Python for students, teachers, and admins. This system allows role-based interactions such as course enrollments, CGPA tracking, teacher profile management, and admin-level controls.

> ⚠️ This is a demonstration system using in-memory data. No external databases are required.

---

## 🔧 Features

### 👩‍🎓 Students
- Enroll / Unenroll in courses (with capacity limits)
- Enter and update CGPA (auto-mapped from percentage grades)
- View academic records (semester-wise)
- Plot CGPA trends using `matplotlib`
- View teacher profiles
- Change password

### 👨‍🏫 Teachers
- View salary slips (placeholder)
- Update name and qualification
- Change password

### 👩‍💼 Admins
- Create login credentials for students and teachers
- Add / Remove students from course enrollments
- View system statistics (user roles, total courses)
- Change password
- View activity logs (basic)

---

## 🧠 Technologies Used

- **Python 3**
- **OOP Principles** (`abstract classes`, `inheritance`)
- **Matplotlib** for CGPA visualization
- **Text-based logging** using `datetime`
- Clean CLI interface (cross-platform `clear_screen`)

---

## 🏁 Getting Started

### 📦 Requirements

- Python 3.x
- `matplotlib`  
  
🧪 Sample Accounts
You can use any of these predefined accounts to test:

Admin
Username: admin

Password: admin123

Teacher
Username: teacher1

Password: teach123

Student
Username: student01

Password: stud001

(More student accounts available up to student20)

  ```bash
  pip install matplotlib
