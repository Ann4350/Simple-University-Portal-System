import os
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from datetime import datetime

# Configuration class for constants
class Config:
    MAX_ENROLLMENT = 4
    CGPA_SCALE = {90: 4.0, 85: 3.7, 80: 3.3, 75: 3.0, 70: 2.7, 65: 2.3, 60: 2.0, 0: 0.0}  # Grade to CGPA mapping

# Utility functions
def log_action(username, action):
    """Log user actions to a text file with timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S PKT')
    with open('activity_log.txt', 'a') as f:
        f.write(f"{timestamp} - User: {username} - Action: {action}\n")

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_valid_input(prompt, valid_options=None, type_func=str, error_msg="Invalid input. Try again."):
    """Get valid input from the user with optional validation."""
    while True:
        try:
            choice = type_func(input(prompt).strip())
            if valid_options and choice not in valid_options:
                print(f"{error_msg} Options: {valid_options}")
                continue
            return choice
        except ValueError:
            print(error_msg)

# Base User class
class User(ABC):
    """Abstract base class for all users."""
    def __init__(self, username, password, name):
        self.username = username
        self.__password = password
        self.name = name

    def check_password(self, password):
        """Check if the provided password matches the stored password."""
        return self.__password == password

    def set_password(self, new_password):
        """Set a new password."""
        self.__password = new_password

    @abstractmethod
    def show_menu(self):
        """Display the menu for the user role."""
        pass

# Student class
class Student(User):
    """Class representing a student user."""
    def __init__(self, username, password, name):
        super().__init__(username, password, name)
        self.academic_records = {}  # Instance variable to store records

    def enroll_course(self, course_id):
        """Enroll the student in a course if capacity and limits allow."""
        courses = {'CSE101': {'name': 'Intro to AI', 'section': 'A', 'students': [], 'max_seats': 15},
                   'MAT201': {'name': 'Discrete Math', 'section': 'B', 'students': [], 'max_seats': 15},
                   'PHY301': {'name': 'Physics II', 'section': 'C', 'students': [], 'max_seats': 15}}
        log_action(self.username, f"Enrolled in course {course_id}")

        if course_id not in courses:
            print("Invalid course ID.")
            return

        enrolled_courses = [rec['course_id'] for rec in self.academic_records.get(self.username, [])]
        if len(enrolled_courses) >= Config.MAX_ENROLLMENT:
            print("You have reached the maximum course enrollment limit.")
            return

        if course_id in enrolled_courses:
            print("Already enrolled in this course.")
            return

        section = courses[course_id].get('section', 'N/A')
        students = courses[course_id].get('students', [])
        if len(students) >= courses[course_id].get('max_seats', 0):
            print(f"Section {section} is full. Cannot enroll.")
            return

        students.append(self.username)
        courses[course_id]['students'] = students

        if self.username not in self.academic_records:
            self.academic_records[self.username] = []
        self.academic_records[self.username].append({
            'course_id': course_id,
            'semester': len(self.academic_records.get(self.username, [])) + 1,
            'grades': [],
            'cgpa': 0.0
        })
        print(f"Enrolled in course {course_id}, section {section} successfully.")

    def unenroll_course(self, course_id):
        """Unenroll the student from a course."""
        courses = {'CSE101': {'name': 'Intro to AI', 'section': 'A', 'students': [], 'max_seats': 15},
                   'MAT201': {'name': 'Discrete Math', 'section': 'B', 'students': [], 'max_seats': 15},
                   'PHY301': {'name': 'Physics II', 'section': 'C', 'students': [], 'max_seats': 15}}
        log_action(self.username, f"Unenrolled from course {course_id}")

        if course_id not in courses:
            print("Invalid course ID.")
            return

        students = courses[course_id].get('students', [])
        if self.username in students:
            students.remove(self.username)
            courses[course_id]['students'] = students
        else:
            print("You are not enrolled in this course.")
            return

        if self.username in self.academic_records:
            self.academic_records[self.username] = [rec for rec in self.academic_records[self.username] if rec['course_id'] != course_id]

        print(f"Unenrolled from course {course_id} successfully.")

    def view_academic_records(self):
        """Display the student's academic records."""
        courses = {'CSE101': {'name': 'Intro to AI', 'section': 'A', 'students': [], 'max_seats': 15},
                   'MAT201': {'name': 'Discrete Math', 'section': 'B', 'students': [], 'max_seats': 15},
                   'PHY301': {'name': 'Physics II', 'section': 'C', 'students': [], 'max_seats': 15}}
        log_action(self.username, "Viewed academic records")

        if self.username not in self.academic_records or not self.academic_records[self.username]:
            print("No academic records found.")
            return

        print(f"Academic records for {self.name}:")
        for rec in self.academic_records[self.username]:
            course_name = courses.get(rec['course_id'], {}).get('name', 'Unknown')
            print(f"- Course: {course_name} ({rec['course_id']})")
            print(f"  Semester: {rec['semester']}")
            print(f"  Grades: {rec['grades']}")
            print(f"  CGPA: {rec['cgpa']}")
            print()

    def enter_cgpa(self, course_id):
        """Allow the student to enter grades and calculate CGPA for a specific course."""
        log_action(self.username, f"Entered CGPA for course {course_id}")
        if self.username not in self.academic_records or not self.academic_records[self.username]:
            print("No academic records found. Please enroll in a course first.")
            return

        for rec in self.academic_records[self.username]:
            if rec['course_id'] == course_id:
                try:
                    grade = float(get_valid_input(f"Enter grade percentage for {course_id} (0-100): ", type_func=float, error_msg="Grade must be a number between 0 and 100"))
                    if 0 <= grade <= 100:
                        cgpa = next((v for k, v in sorted(Config.CGPA_SCALE.items(), reverse=True) if grade >= k), 0.0)
                        rec['grades'].append(grade)
                        rec['cgpa'] = cgpa
                        print(f"CGPA updated to {cgpa} for {course_id} based on grade {grade}%.")
                    else:
                        print("Grade must be between 0 and 100.")
                except ValueError:
                    print("Invalid grade value.")
                return
        print(f"No record found for course {course_id}.")

    def plot_cgpa(self):
        """Plot the CGPA trend over semesters."""
        log_action(self.username, "Plotted CGPA trend")
        if self.username not in self.academic_records or not self.academic_records[self.username]:
            print("No CGPA data available to plot.")
            return

        semesters = [rec['semester'] for rec in self.academic_records[self.username]]
        cgpas = [rec['cgpa'] for rec in self.academic_records[self.username]]

        plt.plot(semesters, cgpas, marker='o')
        plt.title(f"CGPA Trend for {self.name}")
        plt.xlabel('Semester')
        plt.ylabel('CGPA')
        plt.ylim(0, 4)
        plt.grid(True)
        plt.show()

    def change_password(self):
        """Change the student's password."""
        current = input("Enter current password: ")
        if not self.check_password(current):
            print("Incorrect password.")
            return
        new_pass = input("Enter new password: ")
        self.set_password(new_pass)
        log_action(self.username, "Changed password")
        print("Password changed successfully.")

    def view_teacher_profiles(self):
        """Display profiles of all teachers."""
        users = INITIAL_USERS  # Use embedded users
        log_action(self.username, "Viewed teacher profiles")
        print("Teachers list and profiles:")
        for u, info in users.items():
            if info.get('role') == 'teacher':
                print(f"- {info['name']} (Username: {u})")

    def show_menu(self):
        """Display and handle the student menu."""
        while True:
            clear_screen()
            print(f"\nStudent Menu - {self.name}")
            print("1. Enroll in course")
            print("2. Unenroll from course")
            print("3. View academic records")
            print("4. Enter CGPA")
            print("5. Plot CGPA trend")
            print("6. View teacher profiles")
            print("7. Change password")
            print("8. Logout")

            choice = get_valid_input("Enter your choice: ", ['1', '2', '3', '4', '5', '6', '7', '8'])
            if choice == '1':
                course_id = input("Enter course ID to enroll: ")
                self.enroll_course(course_id)
            elif choice == '2':
                course_id = input("Enter course ID to unenroll: ")
                self.unenroll_course(course_id)
            elif choice == '3':
                self.view_academic_records()
            elif choice == '4':
                course_id = input("Enter course ID to update CGPA: ")
                self.enter_cgpa(course_id)
            elif choice == '5':
                self.plot_cgpa()
            elif choice == '6':
                self.view_teacher_profiles()
            elif choice == '7':
                self.change_password()
            elif choice == '8':
                break
            input("Press Enter to continue...")

# Teacher class
class Teacher(User):
    """Class representing a teacher user."""
    def view_salary_slips(self):
        """Display the teacher's salary slips."""
        salaries = {}  # In-memory salaries
        log_action(self.username, "Viewed salary slips")
        slips = salaries.get(self.username, [])
        if not slips:
            print("No salary slips found.")
            return
        print(f"Salary slips for {self.name}:")
        for slip in slips:
            print(f"Month: {slip['month']}, Amount: {slip['amount']}")

    def add_update_delete_info(self):
        """Update the teacher's personal information."""
        users = INITIAL_USERS  # Use embedded users
        info = users[self.username]

        print("Update your personal information:")
        new_name = input(f"Name ({info['name']}): ").strip() or info['name']
        new_qual = input("Qualification (optional): ").strip() or info.get('qualification', '')

        info.update({'name': new_name, 'qualification': new_qual})
        users[self.username] = info
        log_action(self.username, "Updated personal information")
        print("Information updated.")

    def change_password(self):
        """Change the teacher's password."""
        current = input("Enter current password: ")
        if not self.check_password(current):
            print("Incorrect password.")
            return
        new_pass = input("Enter new password: ")
        self.set_password(new_pass)
        users = INITIAL_USERS  # Use embedded users
        users[self.username]['password'] = new_pass
        log_action(self.username, "Changed password")
        print("Password changed successfully.")

    def show_menu(self):
        """Display and handle the teacher menu."""
        while True:
            clear_screen()
            print(f"\nTeacher Menu - {self.name}")
            print("1. View salary slips")
            print("2. Update personal information")
            print("3. Change password")
            print("4. Logout")

            choice = get_valid_input("Enter your choice: ", ['1', '2', '3', '4'])
            if choice == '1':
                self.view_salary_slips()
            elif choice == '2':
                self.add_update_delete_info()
            elif choice == '3':
                self.change_password()
            elif choice == '4':
                break
            input("Press Enter to continue...")

# Admin class
class Admin(User):
    """Class representing an admin user."""
    def full_access(self):
        """Display all user data."""
        users = INITIAL_USERS  # Use embedded users
        log_action(self.username, "Viewed full access data")
        print("All user data:")
        for u, info in users.items():
            print(f"{u}: {info}")

    def create_login_ids(self, role):
        """Create new user login IDs for the specified role."""
        users = INITIAL_USERS  # Use embedded users
        log_action(self.username, f"Created new {role} user")

        username = input("Enter username: ").strip()
        if username in users:
            print("User already exists.")
            return

        if role not in ['student', 'teacher']:
            print("Invalid role for creation.")
            return

        name = input("Enter full name: ").strip()
        password = input("Enter password: ").strip()

        users[username] = {'role': role, 'name': name, 'password': password}
        if role == 'teacher':
            users[username]['qualification'] = ''
        print(f"{role.capitalize()} user created successfully.")

    def manage_enrollments(self):
        """Manage course enrollments for users."""
        courses = {'CSE101': {'name': 'Intro to AI', 'section': 'A', 'students': [], 'max_seats': 15},
                   'MAT201': {'name': 'Discrete Math', 'section': 'B', 'students': [], 'max_seats': 15},
                   'PHY301': {'name': 'Physics II', 'section': 'C', 'students': [], 'max_seats': 15}}
        users = INITIAL_USERS  # Use embedded users
        log_action(self.username, "Managed enrollments")

        course_id = input("Enter course ID: ")
        if course_id not in courses:
            print("Invalid Course ID.")
            return

        action = get_valid_input("Add or Remove user? (a/r): ", ['a', 'r'])
        username = input("Enter username: ").strip()

        if username not in users:
            print("User not found.")
            return

        students = courses[course_id].get('students', [])
        if action == 'a':
            if username not in students:
                if len(students) >= courses[course_id].get('max_seats', 0):
                    print("Course section full.")
                    return
                students.append(username)
                print(f"User {username} added to course {course_id}.")
            else:
                print("User already enrolled.")
        elif action == 'r':
            if username in students:
                students.remove(username)
                print(f"User {username} removed from course {course_id}.")
            else:
                print("User is not enrolled in this course.")
        courses[course_id]['students'] = students

    def view_system_stats(self):
        """Display system statistics."""
        users = INITIAL_USERS  # Use embedded users
        courses = {'CSE101': {'name': 'Intro to AI', 'section': 'A', 'students': [], 'max_seats': 15},
                   'MAT201': {'name': 'Discrete Math', 'section': 'B', 'students': [], 'max_seats': 15},
                   'PHY301': {'name': 'Physics II', 'section': 'C', 'students': [], 'max_seats': 15}}
        log_action(self.username, "Viewed system stats")

        total_users = len(users)
        total_students = sum(1 for u in users.values() if u.get('role') == 'student')
        total_teachers = sum(1 for u in users.values() if u.get('role') == 'teacher')
        total_admins = sum(1 for u in users.values() if u.get('role') == 'admin')

        print("System statistics:")
        print(f"Total users: {total_users}")
        print(f"Total students: {total_students}")
        print(f"Total teachers: {total_teachers}")
        print(f"Total admins: {total_admins}")
        print(f"Total courses: {len(courses)}")

    def view_updates_by_teachers(self):
        """Placeholder for viewing teacher updates."""
        log_action(self.username, "Viewed updates by teachers")
        print("Viewing updates by teachers is not implemented.")

    def change_password(self):
        """Change the admin's password."""
        current = input("Enter current password: ")
        if not self.check_password(current):
            print("Incorrect password.")
            return
        new_pass = input("Enter new password: ")
        self.set_password(new_pass)
        users = INITIAL_USERS  # Use embedded users
        users[self.username]['password'] = new_pass
        log_action(self.username, "Changed password")
        print("Password changed successfully.")

    def show_menu(self):
        """Display and handle the admin menu."""
        while True:
            clear_screen()
            print(f"\nAdmin Menu - {self.name}")
            print("1. Create new student")
            print("2. Create new teacher")
            print("3. Manage enrollments")
            print("4. View system statistics")
            print("5. View updates by teachers (not implemented)")
            print("6. Change password")
            print("7. Logout")

            choice = get_valid_input("Enter your choice: ", ['1', '2', '3', '4', '5', '6', '7'])
            if choice == '1':
                self.create_login_ids('student')
            elif choice == '2':
                self.create_login_ids('teacher')
            elif choice == '3':
                self.manage_enrollments()
            elif choice == '4':
                self.view_system_stats()
            elif choice == '5':
                self.view_updates_by_teachers()
            elif choice == '6':
                self.change_password()
            elif choice == '7':
                break
            input("Press Enter to continue...")

# Authentication and initialization
INITIAL_USERS = {
    'admin': {'role': 'admin', 'name': 'Administrator', 'password': 'admin123'},
    'teacher1': {'role': 'teacher', 'name': 'John Smith', 'password': 'teach123', 'qualification': 'PhD'},
    'student01': {'role': 'student', 'name': 'Student 01', 'password': 'stud001'},
    'student02': {'role': 'student', 'name': 'Student 02', 'password': 'stud002'},
    'student03': {'role': 'student', 'name': 'Student 03', 'password': 'stud003'},
    'student04': {'role': 'student', 'name': 'Student 04', 'password': 'stud004'},
    'student05': {'role': 'student', 'name': 'Student 05', 'password': 'stud005'},
    'student06': {'role': 'student', 'name': 'Student 06', 'password': 'stud006'},
    'student07': {'role': 'student', 'name': 'Student 07', 'password': 'stud007'},
    'student08': {'role': 'student', 'name': 'Student 08', 'password': 'stud008'},
    'student09': {'role': 'student', 'name': 'Student 09', 'password': 'stud009'},
    'student10': {'role': 'student', 'name': 'Student 10', 'password': 'stud010'},
    'student11': {'role': 'student', 'name': 'Student 11', 'password': 'stud011'},
    'student12': {'role': 'student', 'name': 'Student 12', 'password': 'stud012'},
    'student13': {'role': 'student', 'name': 'Student 13', 'password': 'stud013'},
    'student14': {'role': 'student', 'name': 'Student 14', 'password': 'stud014'},
    'student15': {'role': 'student', 'name': 'Student 15', 'password': 'stud015'},
    'student16': {'role': 'student', 'name': 'Student 16', 'password': 'stud016'},
    'student17': {'role': 'student', 'name': 'Student 17', 'password': 'stud017'},
    'student18': {'role': 'student', 'name': 'Student 18', 'password': 'stud018'},
    'student19': {'role': 'student', 'name': 'Student 19', 'password': 'stud019'},
    'student20': {'role': 'student', 'name': 'Student 20', 'password': 'stud020'},
}

def login():
    """Authenticate a user and return the corresponding user object."""
    users = INITIAL_USERS  # Use embedded users
    print(f"Available users: {list(users.keys())}")  # Debug print
    log_action('system', f"Login attempt for user")

    username = input("Username: ").strip()
    if username not in users:
        print(f"User not found. Available users: {list(users.keys())}")
        return None

    password = input("Password: ").strip()
    if users[username]['password'] != password:
        print("Incorrect password.")
        return None

    role = users[username]['role']
    name = users[username]['name']

    user_classes = {'student': Student, 'teacher': Teacher, 'admin': Admin}
    user_class = user_classes.get(role)
    if not user_class:
        print("Invalid role assigned to user.")
        return None

    user = user_class(username, password, name)
    user.set_password(password)
    log_action(username, "Logged in")
    return user

def init_courses():
    """Initialize courses data if not present (in-memory for now)."""
    pass  # Courses are now defined within methods

def init_salary_slips():
    """Initialize salary slips data if not present (in-memory for now)."""
    pass  # Salary slips are now defined within methods

def init_users():
    """Initialize users data (already embedded)."""
    pass  # Users are now in INITIAL_USERS

def main():
    """Main function to run the portal system."""
    clear_screen()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S PKT')
    print(f"Welcome to the Portal System (Student / Teacher / Admin) - {current_time}")
    init_courses()
    init_salary_slips()
    init_users()

    user = None
    while not user:
        user = login()

    user.show_menu()
    log_action(user.username, "Logged out")
    print("Logged out. Goodbye.")

if __name__ == '__main__':
    main()