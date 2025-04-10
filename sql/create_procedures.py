def create_procedure_commands()->str:
    procedures_sql = """
    -- Stored Procedures
    DROP PROCEDURE IF EXISTS sp_add_new_student;
    
    CREATE PROCEDURE sp_add_new_student (
        IN in_name VARCHAR(100),
        IN in_roll_number VARCHAR(20),
        IN in_dob DATE,
        IN in_email VARCHAR(100),
        IN in_phone_number VARCHAR(20)
    )
    BEGIN
        INSERT INTO students (name, roll_number, date_of_birth, email, phone_number)
        VALUES (in_name, in_roll_number, in_dob, in_email, in_phone_number);
    END;
    
    DROP PROCEDURE IF EXISTS sp_record_bulk_attendance;
    
    CREATE PROCEDURE sp_record_bulk_attendance (
        IN in_attendance_date DATE,
        IN in_student_statuses JSON
    )
    BEGIN
        DECLARE i INT DEFAULT 0;
        DECLARE student_id INT;
        DECLARE status VARCHAR(10);
        DECLARE notes VARCHAR(255);
        
        START TRANSACTION;
        
        DROP TEMPORARY TABLE IF EXISTS temp_attendance_data;
        
        CREATE TEMPORARY TABLE temp_attendance_data (
            student_id INT,
            status VARCHAR(10),
            notes VARCHAR(255)
        );
        
        WHILE i < JSON_LENGTH(in_student_statuses) DO
            SET student_id = JSON_EXTRACT(in_student_statuses, CONCAT('$[', i, '].student_id'));
            SET status = JSON_UNQUOTE(JSON_EXTRACT(in_student_statuses, CONCAT('$[', i, '].status')));
            SET notes = JSON_UNQUOTE(JSON_EXTRACT(in_student_statuses, CONCAT('$[', i, '].notes')));
            
            INSERT INTO temp_attendance_data (student_id, status, notes) VALUES (student_id, status, notes);
            
            SET i = i + 1;
        END WHILE;
        
        INSERT INTO attendance (student_id, attendance_date, status, notes)
        SELECT tad.student_id, in_attendance_date, tad.status, tad.notes
        FROM temp_attendance_data tad
        ON DUPLICATE KEY UPDATE status = tad.status, notes = tad.notes;
        
        DROP TEMPORARY TABLE IF EXISTS temp_attendance_data;
        
        COMMIT;
    END;
    
    DROP PROCEDURE IF EXISTS sp_update_student_performance;
    
    CREATE PROCEDURE sp_update_student_performance (
        IN in_student_id INT,
        IN in_subject VARCHAR(50),
        IN in_exam_date DATE,
        IN in_marks DECIMAL(5, 2),
        IN in_notes VARCHAR(255)
    )
    BEGIN
        INSERT INTO performance (student_id, subject, exam_date, marks, notes)
        VALUES (in_student_id, in_subject, in_exam_date, in_marks, in_notes)
        ON DUPLICATE KEY UPDATE
            exam_date = in_exam_date,
            marks = in_marks,
            notes = in_notes;
    END;
    """
    return procedures_sql
