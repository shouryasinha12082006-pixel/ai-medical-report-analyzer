import os
import shutil
import mysql.connector

def setup_project():
    print("Setting up AI Medical Report Analyzer project...")
    
    # Get the directory where setup.py is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Ensure static directories exist
    os.makedirs(os.path.join(base_dir, "static", "css"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "static", "js"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "templates"), exist_ok=True)
    
    # 2. Copy Dooper logo from bi dashboard
    src_logo = os.path.abspath(os.path.join(base_dir, "..", "dooper_bi_dashboard", "static", "logo.png"))
    dest_logo = os.path.join(base_dir, "static", "logo.png")
    
    if os.path.exists(src_logo):
        shutil.copy(src_logo, dest_logo)
        print(f"Successfully copied Dooper logo to {dest_logo}")
    else:
        print(f"Warning: Source logo not found at {src_logo}. Please make sure to copy it manually to {dest_logo}.")

    # 3. Initialize MySQL Database
    print("Connecting to MySQL...")
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123Shorya@"
        )
        cursor = conn.cursor()
        
        schema_path = os.path.join(base_dir, "medical_analyzer.sql")
        if os.path.exists(schema_path):
            with open(schema_path, "r") as f:
                schema_sql = f.read()
            
            # Execute MySQL commands separated by semicolon
            for command in schema_sql.split(";"):
                if command.strip():
                    cursor.execute(command)
            conn.commit()
            
            # Ensure profile_pic column exists (handles table pre-existence)
            try:
                cursor.execute("USE medical_analyzer")
                cursor.execute("ALTER TABLE users ADD COLUMN profile_pic VARCHAR(255) DEFAULT NULL")
                conn.commit()
                print("Successfully verified/added profile_pic column to users table.")
            except mysql.connector.Error:
                # Column already exists, ignore
                pass
                
            print("Successfully initialized MySQL database medical_analyzer")
        else:
            print(f"Error: {schema_path} not found!")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error initializing MySQL Database: {e}")
        print("Please make sure MySQL is running and the username/password in setup.py matches.")
    
    print("Setup completed!")

if __name__ == "__main__":
    setup_project()
