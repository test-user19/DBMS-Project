def create_table_commands()->str:
    tables_sql = """
    -- Create Tables
    DROP TABLE IF EXISTS attendance;
    DROP TABLE IF EXISTS performance;
    DROP TABLE IF EXISTS students;
    DROP TABLE IF EXISTS student_deletion_audit;
    
    CREATE TABLE IF NOT EXISTS students (
        student_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        roll_number VARCHAR(20),
        date_of_birth DATE,
        email VARCHAR(100),
        phone_number VARCHAR(20),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE IF NOT EXISTS attendance (
        attendance_id INT AUTO_INCREMENT PRIMARY KEY,
        student_id INT NOT NULL,
        attendance_date DATE NOT NULL,
        status VARCHAR(10) NOT NULL, -- e.g., 'Present', 'Absent', 'Late'
        notes VARCHAR(255),
        FOREIGN KEY (student_id) REFERENCES students(student_id),
        UNIQUE KEY unique_attendance (student_id, attendance_date)
    );
    
    CREATE TABLE IF NOT EXISTS performance (
        performance_id INT AUTO_INCREMENT PRIMARY KEY,
        student_id INT NOT NULL,
        subject VARCHAR(50) NOT NULL,
        exam_date DATE,
        marks DECIMAL(5, 2),
        grade VARCHAR(10),
        notes VARCHAR(255),
        FOREIGN KEY (student_id) REFERENCES students(student_id),
        UNIQUE KEY unique_performance (student_id, subject, exam_date)
    );
    
    CREATE TABLE IF NOT EXISTS student_deletion_audit (
        audit_id INT AUTO_INCREMENT PRIMARY KEY,
        student_id INT NOT NULL,
        name VARCHAR(100) NOT NULL,
        deletion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    return tables_sql
