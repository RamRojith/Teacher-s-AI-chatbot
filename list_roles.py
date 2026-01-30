import MySQLdb

def list_all_roles():
    try:
        db = MySQLdb.connect(host='localhost', user='root', passwd='', db='rit_approval_system')
        cursor = db.cursor()
        cursor.execute("SELECT id, role FROM control_room_role ORDER BY id")
        for row in cursor.fetchall():
            print(f"{row[0]}: {row[1]}")
        db.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_all_roles()
