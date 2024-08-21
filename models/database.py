import sqlite3
from datetime import datetime

# Initialize the SQLite database (create tables if not exist)
def init_db():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    # Create classes table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS classes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_name TEXT UNIQUE NOT NULL
    )
    ''')

    # Create students table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        registration_number TEXT UNIQUE NOT NULL,
        class_id INTEGER,
        FOREIGN KEY (class_id) REFERENCES classes(id)
    )
    ''')

    # Create attendance table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (student_id) REFERENCES students(id)
    )
    ''')

    conn.commit()
    conn.close()

# Fetch a user from the database
def get_user(username, password):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()

    conn.close()
    return user

# Mark attendance for a student
def mark_attendance_in_db(name, class_name):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    # Fetch class ID
    cursor.execute('SELECT id FROM classes WHERE class_name=?', (class_name,))
    class_id = cursor.fetchone()

    if class_id:
        class_id = class_id[0]
        # Fetch student ID
        cursor.execute('SELECT id FROM students WHERE name=? AND class_id=?', (name, class_id))
        student_id = cursor.fetchone()

        if student_id:
            student_id = student_id[0]
            date_today = datetime.today().strftime('%Y-%m-%d')
            time_now = datetime.now().strftime('%H:%M:%S')

            # Check if attendance already marked
            cursor.execute('SELECT * FROM attendance WHERE student_id=? AND date=?', (student_id, date_today))
            existing_record = cursor.fetchone()

            if existing_record:
                print(f"Attendance already marked for {name} on {date_today}.")
            else:
                # Mark attendance
                cursor.execute('''
                INSERT INTO attendance (student_id, date, time, status)
                VALUES (?, ?, ?, ?)
                ''', (student_id, date_today, time_now, 'Present'))

                conn.commit()
                print(f"Attendance marked for {name} on {date_today}.")

        else:
            print(f"Student {name} not found in class {class_name}.")
    
    else:
        print(f"Class {class_name} not found.")

    conn.close()

# Fetch attendance data for exporting
def get_attendance_data(class_name):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    # Fetch class ID
    cursor.execute('SELECT id FROM classes WHERE class_name=?', (class_name,))
    class_id = cursor.fetchone()

    if class_id:
        class_id = class_id[0]

        # Fetch attendance records for the class
        cursor.execute('''
        SELECT students.name, students.registration_number, attendance.date, attendance.time, attendance.status
        FROM attendance
        INNER JOIN students ON attendance.student_id = students.id
        WHERE students.class_id = ?
        ''', (class_id,))

        attendance_data = cursor.fetchall()
        conn.close()
        return attendance_data

    else:
        print(f"Class {class_name} not found.")
        conn.close()
        return []

# Example function to add a user (this can be extended for user registration)
def add_user(username, password):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        print(f"User {username} added successfully.")
    except sqlite3.IntegrityError:
        print(f"User {username} already exists.")

    conn.close()

# Example function to add a class (this can be extended for class management)
def add_class(class_name):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO classes (class_name) VALUES (?)', (class_name,))
        conn.commit()
        print(f"Class {class_name} added successfully.")
    except sqlite3.IntegrityError:
        print(f"Class {class_name} already exists.")

    conn.close()

# Example function to add a student
def add_student(name, registration_number, class_name):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    # Fetch class ID
    cursor.execute('SELECT id FROM classes WHERE class_name=?', (class_name,))
    class_id = cursor.fetchone()

    if class_id:
        class_id = class_id[0]

        try:
            cursor.execute('''
            INSERT INTO students (name, registration_number, class_id)
            VALUES (?, ?, ?)
            ''', (name, registration_number, class_id))

            conn.commit()
            print(f"Student {name} added successfully to class {class_name}.")

        except sqlite3.IntegrityError:
            print(f"Student with registration number {registration_number} already exists.")

    else:
        print(f"Class {class_name} not found.")

    conn.close()
