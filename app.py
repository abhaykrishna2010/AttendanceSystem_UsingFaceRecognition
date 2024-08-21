from flask import Flask, render_template, request, redirect, session, Response, send_file
from models.database import init_db, get_user, mark_attendance_in_db, get_attendance_data, add_user, add_class, add_student
from models.detect import generate_frames
import pandas as pd
import time
import os

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize the database
init_db()

# Route: Login Page
@app.route('/')
def login():
    return render_template('login.html')

# Route: Handle Login
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    user = get_user(username, password)
    if user:
        session['user'] = user
        return redirect('/class-select')
    return 'Invalid credentials. Please try again.'

# Route: Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

# Route: Class Selection Page
@app.route('/class-select')
def class_select():
    if 'user' not in session:
        return redirect('/')
    # Fetch classes from the database
    # This is an example list. Replace with actual database query to fetch classes.
    classes = ["Class A", "Class B", "Class C"]  
    return render_template('class_select.html', classes=classes)

# Route: Handle Class Selection
@app.route('/select-class', methods=['POST'])
def select_class():
    selected_class = request.form['class']
    session['class'] = selected_class
    return redirect('/attendance')

# Route: Attendance Page
@app.route('/attendance')
def attendance():
    if 'class' not in session:
        return redirect('/class-select')
    return render_template('attendance.html')

# Route: Video Feed for Face Recognition
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Function: Mark Attendance Callback
def mark_attendance(name):
    if 'class' in session:
        class_name = session['class']
        mark_attendance_in_db(name, class_name)

# Route: Export Attendance Data to Excel/CSV
@app.route('/export-attendance')
def export_attendance():
    if 'class' not in session:
        return redirect('/class-select')

    # Get attendance data from the database
    class_name = session['class']
    attendance_data = get_attendance_data(class_name)

    if len(attendance_data):
        return "No attendance data found."

    # Convert data to DataFrame
    df = pd.DataFrame(attendance_data, columns=['Name', 'Registration Number', 'Date', 'Time', 'Status'])

    # Define filename
    filename = f"attendance_{class_name}_{time.strftime('%Y%m%d_%H%M%S')}.xlsx"
    filepath = os.path.join('static', 'exports', filename)

    # Create export directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Save to Excel
    df.to_excel(filepath, index=False)

    # Send file for download
    return send_file(filepath, as_attachment=True)

# Main Function to Run the App
if __name__ == '__main__':
    # Example data insertion (you can remove these after first run)
    add_user('abcd', 'pass')
    add_class('Class A')
    add_student('abhay', '123', 'Class A')
    add_student('nandana', '456', 'Class A')
    add_student('unknown', '789', 'Class A')

    # Run the Flask app
    app.run(debug=True)
