import mysql.connector
from db_config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
import json  # Import the json library

def get_connection():
    return mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

def create_database_if_not_exists():
    try:
        mydb = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        mycursor = mydb.cursor()
        mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        mydb.commit()
        print(f"Database '{DB_NAME}' created successfully or already exists.")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()

# Student Operations using Stored Procedure
def add_student(name, class_name, roll_number, dob, email, phone):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.callproc('sp_add_new_student', [name, class_name, roll_number, dob, email, phone])
        conn.commit()
        # Fetch the last inserted ID (if needed, though the SP doesn't directly return it)
        cursor.execute("SELECT LAST_INSERT_ID()")
        result = cursor.fetchone()
        return result[0] if result else None
    except mysql.connector.Error as err:
        print(f"Error adding student: {err}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_all_students():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM students"
        cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error fetching students: {err}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_student_by_id(student_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM students WHERE student_id = %s"
        cursor.execute(query, (student_id,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        print(f"Error fetching student: {err}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def update_student(student_id, name, class_name, roll_number, dob, email, phone):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "UPDATE students SET name=%s, class=%s, roll_number=%s, date_of_birth=%s, email=%s, phone_number=%s WHERE student_id=%s"
        values = (name, class_name, roll_number, dob, email, phone, student_id)
        cursor.execute(query, values)
        conn.commit()
        return cursor.rowcount
    except mysql.connector.Error as err:
        print(f"Error updating student: {err}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def delete_student(student_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "DELETE FROM students WHERE student_id = %s"
        cursor.execute(query, (student_id,))
        conn.commit()
        return cursor.rowcount
    except mysql.connector.Error as err:
        print(f"Error deleting student: {err}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Attendance Operations using Stored Procedure with Transaction
def record_bulk_attendance(attendance_date, student_statuses):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Convert the list of dictionaries to a JSON string
        student_statuses_json = json.dumps(student_statuses)
        cursor.callproc('sp_record_bulk_attendance', [attendance_date, student_statuses_json])
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error recording bulk attendance: {err}")
        if conn:
            conn.rollback()
        if "Cannot mark attendance for a future date." in err.msg:
            return err.msg  # Return the specific error message from the trigger
        else:
            return "Error recording bulk attendance." # Return a generic error message
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def get_attendance_by_date(date):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT s.name, a.attendance_date, a.status, a.notes FROM attendance a JOIN students s ON a.student_id = s.student_id WHERE a.attendance_date = %s"
        cursor.execute(query, (date,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error fetching attendance: {err}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_attendance_by_student(student_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT attendance_date, status, notes FROM attendance WHERE student_id = %s ORDER BY attendance_date DESC"
        cursor.execute(query, (student_id,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error fetching attendance for student: {err}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def update_attendance(attendance_id, status, notes=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "UPDATE attendance SET status=%s, notes=%s WHERE attendance_id=%s"
        values = (status, notes, attendance_id)
        cursor.execute(query, values)
        conn.commit()
        return cursor.rowcount
    except mysql.connector.Error as err:
        print(f"Error updating attendance: {err}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Performance Operations using Stored Procedure
def add_performance(student_id, subject, exam_date, marks, notes=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.callproc('sp_update_student_performance', [student_id, subject, exam_date, marks, notes])
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error adding/updating performance: {err}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_performance_by_student(student_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT subject, exam_date, marks, grade, notes FROM performance WHERE student_id = %s"
        cursor.execute(query, (student_id,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error fetching performance for student: {err}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_all_performance():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT s.name, p.subject, p.exam_date, p.marks, p.grade FROM performance p JOIN students s ON p.student_id = s.student_id"
        cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error fetching all performance data: {err}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Operations using Views
def get_student_attendance_summary():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM student_attendance_summary"
        cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error fetching student attendance summary: {err}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_student_average_performance():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM student_average_performance"
        cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error fetching student average performance: {err}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_student_latest_attendance():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM student_latest_attendance"
        cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error fetching student latest attendance: {err}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

