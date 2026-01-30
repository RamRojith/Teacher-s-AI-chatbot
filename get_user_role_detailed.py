import MySQLdb

def get_user_role_detailed():
    try:
        db = MySQLdb.connect(host='localhost', user='root', passwd='', db='rit_approval_system')
        cursor = db.cursor()
        cursor.execute("""
            SELECT u.username, u.Employee_id, u.role_id, r.role, u.password
            FROM control_room_user u
            LEFT JOIN control_room_role r ON u.role_id = r.id
            WHERE u.username IN ('1223', '123') OR u.Employee_id IN ('1223', '123')
        """)
        rows = cursor.fetchall()
        for row in rows:
            print(f"Username: {row[0]} | EmpID: {row[1]} | RoleID: {row[2]} | Role: {row[3]} | Pass: {row[4][:10]}...")
        db.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_user_role_detailed()
