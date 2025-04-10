def create_triggers_commands()-> str:
    triggers_sql = """
    -- Triggers
    DROP TRIGGER IF EXISTS tr_set_default_grade;
    
    CREATE TRIGGER tr_set_default_grade
    BEFORE INSERT ON performance
    FOR EACH ROW
    BEGIN
        IF NEW.grade IS NULL THEN
            IF NEW.marks >= 90 THEN
                SET NEW.grade = 'A+';
            ELSEIF NEW.marks >= 80 THEN
                SET NEW.grade = 'A';
            ELSEIF NEW.marks >= 70 THEN
                SET NEW.grade = 'B';
            ELSEIF NEW.marks >= 60 THEN
                SET NEW.grade = 'C';
            ELSE
                SET NEW.grade = 'F';
            END IF;
        END IF;
    END;
    
    DROP TRIGGER IF EXISTS tr_prevent_future_attendance;
    
    CREATE TRIGGER tr_prevent_future_attendance
    BEFORE INSERT ON attendance
    FOR EACH ROW
    BEGIN
        IF NEW.attendance_date > CURDATE() THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Cannot mark attendance for a future date.';
        END IF;
    END;
    
    DROP TRIGGER IF EXISTS tr_log_student_deletion;
    
    CREATE TRIGGER tr_log_student_deletion
    BEFORE DELETE ON students
    FOR EACH ROW
    BEGIN
        INSERT INTO student_deletion_audit (student_id, name)
        VALUES (OLD.student_id, OLD.name);
    END;
    """
    return triggers_sql
