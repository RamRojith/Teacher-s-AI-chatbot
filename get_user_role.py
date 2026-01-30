import MySQLdb

def get_user_role(emp_id):
    try:
        db = MySQLdb.connect(host='localhost', user='root', passwd='', db='rit_approval_system')
        cursor = db.cursor()
        cursor.execute("""
            SELECT u.username, u.role_id, r.role 
            FROM control_room_user u
            LEFT JOIN control_room_role r ON u.role_id = r.id
            WHERE u.username = %s OR u.Employee_id = %s
        """, (emp_id, emp_id))
        rows = cursor.fetchall()
        for row in rows:
            print(f"User: {row[0]} | RoleID: {row[1]} | RoleName: {row[2]}")
        db.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_user_role('1223')
    get_user_role('123')
