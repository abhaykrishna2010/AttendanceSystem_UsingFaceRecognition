import datetime
from flask import Flask, render_template, Response, request, send_file
import pandas as pd
import os
from io import BytesIO
import sqlite3

from models.detect import generate_frames

app = Flask(__name__)

# In-memory storage for simplicity; replace with database if needed
attendance_data = []

def mark_attendance(name):
    # Record attendance data
    now = datetime.now()
    attendance_data.append({
        'name': name,
        'registration_number': "some_registration_number",  # Replace with actual data
        'date': now.strftime('%Y-%m-%d'),
        'time': now.strftime('%H:%M:%S'),
        'status': 'Present'
    })

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(attendance_callback=mark_attendance), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/export-attendance', methods=['GET'])
def export_attendance():
    if not attendance_data:
        return "No attendance data found"

    df = pd.DataFrame(attendance_data)
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    return send_file(output, mimetype='text/csv', as_attachment=True, download_name='attendance.csv')

# Your other routes and functions go here

if __name__ == '__main__':
    app.run(debug=True)
