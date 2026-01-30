import MySQLdb

try:
    db = MySQLdb.connect(host="localhost", user="root", passwd="", db="rit_approval_system")
    cursor = db.cursor()
    cursor.execute("SELECT username, Employee_id FROM control_room_user WHERE is_active = 1 LIMIT 10")
    rows = cursor.fetchall()
    print("Active Users in rit_approval_system:")
    for r in rows:
        print(f"Username: {r[0]} | Employee_id: {r[1]}")
    db.close()
except Exception as e:
    print(f"Error: {e}")
