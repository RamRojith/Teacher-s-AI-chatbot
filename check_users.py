import MySQLdb

def check_users():
    try:
        db = MySQLdb.connect(host='localhost', user='root', passwd='', db='rit_approval_system')
        cursor = db.cursor()
        
        # Check users 1223 and 123
        cursor.execute("""
            SELECT username, Employee_id, password, is_staff, is_superuser, is_active 
            FROM control_room_user 
            WHERE username IN ('1223', '123') OR Employee_id IN ('1223', '123')
        """)
        print("\nUser Details:")
        for row in cursor.fetchall():
            print(f"  User: {row[0]} | EmpID: {row[1]} | Pass: {row[2]} | Staff: {row[3]} | Admin: {row[4]} | Active: {row[5]}")
            
        # Check role table if it exists
        cursor.execute("SHOW TABLES LIKE 'control_room_role'")
        if cursor.fetchone():
            cursor.execute("SELECT * FROM control_room_role")
            print("\nRoles:")
            for row in cursor.fetchall():
                print(f"  {row}")
                
        db.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_users()
