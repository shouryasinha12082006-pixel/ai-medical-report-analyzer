import mysql.connector
import json
import os

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "123Shorya@"
DB_NAME = "medical_analyzer"

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def create_user(name, email, password_hash):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password_hash)
        )
        user_id = cursor.lastrowid
        
        # Initialize default settings for user
        cursor.execute(
            "INSERT IGNORE INTO settings (user_id, theme) VALUES (%s, %s)",
            (user_id, "light")
        )
        conn.commit()
        return user_id
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email, password, profile_pic, CAST(created_at AS CHAR) as created_at FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email, password, profile_pic, CAST(created_at AS CHAR) as created_at FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def update_user_profile_pic(user_id, filename):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("UPDATE users SET profile_pic = %s WHERE id = %s", (filename, user_id))
    conn.commit()
    cursor.close()
    conn.close()

def add_report(user_id, filename, file_type, raw_text, summary, key_findings, severity, alerts):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        INSERT INTO reports (user_id, filename, file_type, raw_text, summary, key_findings, severity, alerts)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (user_id, filename, file_type, raw_text, summary, json.dumps(key_findings), severity, json.dumps(alerts))
    )
    report_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return report_id

def get_reports_by_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, user_id, filename, file_type, CAST(upload_date AS CHAR) as upload_date, raw_text, summary, key_findings, severity, alerts FROM reports WHERE user_id = %s ORDER BY upload_date DESC",
        (user_id,)
    )
    reports = cursor.fetchall()
    cursor.close()
    conn.close()
    return reports

def get_report_by_id(report_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, user_id, filename, file_type, CAST(upload_date AS CHAR) as upload_date, raw_text, summary, key_findings, severity, alerts FROM reports WHERE id = %s AND user_id = %s",
        (report_id, user_id)
    )
    report = cursor.fetchone()
    cursor.close()
    conn.close()
    return report

def get_user_settings(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM settings WHERE user_id = %s", (user_id,))
    settings = cursor.fetchone()
    if not settings:
        cursor.execute("INSERT IGNORE INTO settings (user_id, theme) VALUES (%s, %s)", (user_id, "light"))
        conn.commit()
        cursor.execute("SELECT * FROM settings WHERE user_id = %s", (user_id,))
        settings = cursor.fetchone()
    cursor.close()
    conn.close()
    return settings

def update_user_settings(user_id, theme):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        INSERT INTO settings (user_id, theme) VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE theme = %s
        """,
        (user_id, theme, theme)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_dashboard_stats(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Total reports
    cursor.execute("SELECT COUNT(*) FROM reports WHERE user_id = %s", (user_id,))
    total = cursor.fetchone()[0]
    
    # Severity distribution
    cursor.execute("SELECT COUNT(*) FROM reports WHERE user_id = %s AND severity = 'Normal'", (user_id,))
    normal = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM reports WHERE user_id = %s AND severity = 'Moderate'", (user_id,))
    moderate = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM reports WHERE user_id = %s AND severity = 'Critical'", (user_id,))
    critical = cursor.fetchone()[0]
    
    cursor.close()
    
    # Recent reports
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, filename, CAST(upload_date AS CHAR) as upload_date, severity, summary FROM reports WHERE user_id = %s ORDER BY upload_date DESC LIMIT 5",
        (user_id,)
    )
    recent = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return {
        "total": total,
        "normal": normal,
        "moderate": moderate,
        "critical": critical,
        "recent": recent
    }

def delete_report(report_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM reports WHERE id = %s AND user_id = %s",
        (report_id, user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
