import MySQLdb

try:
    db = MySQLdb.connect(host="localhost", user="root", passwd="", db="rit_approval_system")
    cursor = db.cursor()
    # Fetching credentials for Dr. Kaliappan M (Employee ID 1223) as an example
    cursor.execute("SELECT Employee_id, password FROM control_room_user WHERE Employee_id = '1223'")
    row = cursor.fetchone()
    if row:
        print(f"Employee ID (Username): {row[0]}")
        print(f"Password (Hashed): {row[1]}")
    else:
        print("User not found.")
    db.close()
except Exception as e:
    print(f"Error: {e}")
