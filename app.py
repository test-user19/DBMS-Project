from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from sql.create_tables import create_table_commands
from sql.create_procedures import create_procedure_commands # Assuming create_procedures.py has this function
from sql.create_triggers import create_triggers_commands # Assuming create_triggers.py has this function
from sql.create_views import create_view_commands    # Assuming create_views.py has this function
from database_operations import (
    add_student, get_all_students, get_student_by_id, update_student, delete_student,
    record_bulk_attendance, get_attendance_by_date, get_attendance_by_student, update_attendance,
    add_performance, get_performance_by_student, get_all_performance,
    get_student_attendance_summary, get_student_average_performance, get_student_latest_attendance,create_database_if_not_exists,get_student_monthly_attendance,
    get_connection  # Import the get_connection function
)
import mysql.connector

app = Flask(__name__)
CORS(app)

def execute_sql_commands(db_connection):
    cursor = db_connection.cursor()
    try:
        create_tables = create_table_commands()
        for statement in create_tables.split(';'):
            if statement.strip():
                cursor.execute(statement)
        print("Tables created successfully.")
        db_connection.commit()

        create_views = create_view_commands()
        for statement in create_views.split(';'):
            if statement.strip():
                cursor.execute(statement+';')
        print("Views created successfully.")
        db_connection.commit()

        create_procedures = create_procedure_commands()
        cursor.execute(create_procedures,map_results=True)
        result_set, statement = cursor.fetchall(), cursor.statement
        while cursor.nextset():
            result_set, statement = cursor.fetchall(), cursor.statement
        print("Stored procedures created successfully.")

        create_triggers = create_triggers_commands()
        cursor.execute(create_triggers,map_results=True)
        result_set, statement = cursor.fetchall(), cursor.statement
        while cursor.nextset():
            result_set, statement = cursor.fetchall(), cursor.statement
        print("Triggers created successfully.")

    except mysql.connector.Error as err:
        print(f"Error executing SQL: {err}")
        db_connection.rollback()
    finally:
        cursor.close()

# Execute SQL setup on app startup
with app.app_context():
    create_database_if_not_exists()
    conn = get_connection()
    if conn:
        execute_sql_commands(conn)
        conn.close()

@app.route('/')
def index():
    return render_template('index.html')

# Student API Endpoints
@app.route('/api/students', methods=['POST'])
def create_student():
    data = request.get_json()
    student_id = add_student(data['name'], data.get('roll_number'), data.get('dob'), data.get('email'), data.get('phone'))
    if student_id:
        return jsonify({'message': 'Student added successfully', 'student_id': student_id}), 201
    return jsonify({'error': 'Failed to add student'}), 500

@app.route('/api/students', methods=['GET'])
def get_students():
    students = get_all_students()
    if students:
        student_list = []
        for student in students:
            student_list.append({
                'student_id': student[0],
                'name': student[1],
                'roll_number': student[2],
                'date_of_birth': str(student[3]),
                'email': student[4],
                'phone_number': student[5],
                'created_at': str(student[6])
            })
        return jsonify(student_list), 200
    return jsonify({'message': 'No students found'}), 200

@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = get_student_by_id(student_id)
    if student:
        return jsonify({
            'student_id': student[0],
            'name': student[1],
            'class': student[2],
            'roll_number': student[3],
            'date_of_birth': str(student[4]),
            'email': student[5],
            'phone_number': student[6],
            'created_at': str(student[7])
        }), 200
    return jsonify({'message': f'Student with ID {student_id} not found'}), 404

@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update_student_info(student_id):
    data = request.get_json()
    rows_affected = update_student(student_id, data['name'], data.get('class'), data.get('roll_number'), data.get('dob'), data.get('email'), data.get('phone'))
    if rows_affected > 0:
        return jsonify({'message': f'Student with ID {student_id} updated successfully'}), 200
    return jsonify({'error': f'Failed to update student with ID {student_id}'}), 500

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def remove_student(student_id):
    rows_affected = delete_student(student_id)
    if rows_affected > 0:
        return jsonify({'message': f'Student with ID {student_id} deleted successfully'}), 200
    return jsonify({'error': f'Failed to delete student with ID {student_id}'}), 500

# Attendance API Endpoints
@app.route('/api/attendance/bulk', methods=['POST'])
def record_attendance_bulk():
    data = request.get_json()
    attendance_date = data.get('attendance_date')
    student_id = data.get('student_id')
    status = data.get('status')
    notes = data.get('notes')
    if attendance_date and student_id and status:
        student_statuses = [{'student_id': student_id, 'status': status, 'notes': notes}]
        success = record_bulk_attendance(attendance_date, student_statuses)
        if success:
            return jsonify({'message': 'Attendance recorded successfully'}), 201
        return jsonify({'error': 'Failed to record attendance'}), 500
    elif attendance_date and data.get('student_statuses'):
        student_statuses = data.get('student_statuses')
        print(student_statuses)
        success = record_bulk_attendance(attendance_date, student_statuses)
    if success is True:
        return jsonify({'message': 'Bulk attendance recorded successfully!'}), 200
    elif isinstance(success, str):  # Check if the result is an error message
        return jsonify({'error': success}), 400  # Send a 400 Bad Request with the error message
    else:
        return jsonify({'error': 'Failed to record bulk attendance.'}), 500

@app.route('/api/attendance/<date>', methods=['GET'])
def get_attendance_for_date(date):
    attendance_records = get_attendance_by_date(date)
    if attendance_records:
        attendance_list = []
        for record in attendance_records:
            attendance_list.append({
                'student_name': record[0],
                'attendance_date': str(record[1]),
                'status': record[2],
                'notes': record[3]
            })
        return jsonify(attendance_list), 200
    return jsonify({'message': f'No attendance records found for {date}'}), 200

@app.route('/api/attendance/student/<int:student_id>', methods=['GET'])
def get_student_attendance(student_id):
    attendance_records = get_attendance_by_student(student_id)
    if attendance_records:
        attendance_list = []
        for record in attendance_records:
            attendance_list.append({
                'attendance_date': str(record[0]),
                'status': record[1],
                'notes': record[2]
            })
        return jsonify(attendance_list), 200
    return jsonify({'message': f'No attendance records found for student ID {student_id}'}), 200

@app.route('/api/attendance/<int:attendance_id>', methods=['PUT'])
def update_attendance_record(attendance_id):
    data = request.get_json()
    rows_affected = update_attendance(attendance_id, data.get('status'), data.get('notes'))
    if rows_affected > 0:
        return jsonify({'message': f'Attendance record with ID {attendance_id} updated successfully'}), 200
    return jsonify({'error': f'Failed to update attendance record with ID {attendance_id}'}), 500

# Performance API Endpoints
@app.route('/api/performance', methods=['POST'])
def add_student_performance():
    data = request.get_json()
    success = add_performance(data['student_id'], data['subject'], data.get('exam_date'), data['marks'], data.get('notes'))
    if success:
        return jsonify({'message': 'Performance added/updated successfully'}), 201
    return jsonify({'error': 'Failed to add/update performance'}), 500

@app.route('/api/performance/student/<int:student_id>', methods=['GET'])
def get_student_performance(student_id):
    performance_records = get_performance_by_student(student_id)
    if performance_records:
        performance_list = []
        for record in performance_records:
            performance_list.append({
                'subject': record[0],
                'exam_date': str(record[1]),
                'marks': float(record[2]) if record[2] else None,
                'grade': record[3],
                'notes': record[4]
            })
        return jsonify(performance_list), 200
    return jsonify({'message': f'No performance records found for student ID {student_id}'}), 200

@app.route('/api/performance', methods=['GET'])
def get_all_student_performance():
    performance_records = get_all_performance()
    if performance_records:
        performance_list = []
        for record in performance_records:
            performance_list.append({
                'student_name': record[0],
                'subject': record[1],
                'exam_date': str(record[2]),
                'marks': float(record[3]) if record[3] else None,
                'grade': record[4]
            })
        return jsonify(performance_list), 200
    return jsonify({'message': 'No performance records found'}), 200

# View API Endpoints
@app.route('/api/views/attendance_summary', methods=['GET'])
def get_attendance_summary_view():
    summary = get_student_attendance_summary()
    if summary:
        summary_list = []
        for row in summary:
            summary_list.append({
                'student_id': row[0],
                'name': row[1],
                'total_present_days': row[2]
            })
        return jsonify(summary_list), 200
    return jsonify({'message': 'No attendance summary data found'}), 200

@app.route('/api/views/average_performance', methods=['GET'])
def get_average_performance_view():
    performance = get_student_average_performance()
    if performance:
        performance_list = []
        for row in performance:
            performance_list.append({
                'student_id': row[0],
                'name': row[1],
                'average_marks': float(row[2]) if row[2] else None
            })
        return jsonify(performance_list), 200
    return jsonify({'message': 'No average performance data found'}), 200

@app.route('/api/views/latest_attendance', methods=['GET'])
def get_latest_attendance_view():
    latest_attendance = get_student_latest_attendance()
    if latest_attendance:
        attendance_list = []
        for row in latest_attendance:
            attendance_list.append({
                'student_id': row[0],
                'name': row[1],
                'latest_attendance_status': row[2],
                'latest_attendance_date': str(row[3]) if row[3] else None
            })
        return jsonify(attendance_list), 200
    return jsonify({'message': 'No latest attendance data found'}), 200

@app.route('/api/attendance/monthly', methods=['POST'])
def get_monthly_attendance():
    data = request.get_json()
    student_id = data.get('studentId')
    month = data.get('month')
    year = data.get('year')

    if not student_id or not month or not year:
        return jsonify({'error': 'Missing studentId, month, or year'}), 400

    present_dates = get_student_monthly_attendance(student_id, month, year)
    return jsonify({'presentDates': present_dates}), 200
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
