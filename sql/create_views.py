def create_view_commands()->str:
    views_sql = """
        -- Views
        DROP VIEW IF EXISTS student_attendance_summary;

        CREATE VIEW student_attendance_summary AS
        SELECT
            s.student_id,
            s.name,
            COUNT(CASE WHEN a.status = 'Present' THEN 1 END) AS total_present_days
        FROM students s
        LEFT JOIN attendance a ON s.student_id = a.student_id
        GROUP BY s.student_id, s.name;
 
        DROP VIEW IF EXISTS student_average_performance;

        CREATE VIEW student_average_performance AS
        SELECT
            s.student_id,
            s.name,
            AVG(p.marks) AS average_marks
        FROM students s
        LEFT JOIN performance p ON s.student_id = p.student_id
        GROUP BY s.student_id, s.name;

        DROP VIEW IF EXISTS student_attendance_with_month_year;

        CREATE VIEW student_attendance_with_month_year AS
        SELECT
            a.student_id,
            s.name,
            a.attendance_date,
            a.status,
            YEAR(a.attendance_date) AS attendance_year,
            MONTH(a.attendance_date) AS attendance_month
        FROM attendance a
        JOIN students s ON a.student_id = s.student_id;
    """
    return views_sql
