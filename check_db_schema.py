import MySQLdb

def check_db():
    print("--- Database: ramco_academic_system ---")
    try:
        db = MySQLdb.connect(host='localhost', user='root', passwd='', db='ramco_academic_system')
        cursor = db.cursor()
        
        cursor.execute("DESC user_accounts_studentdetails")
        print("\nColumns in user_accounts_studentdetails:")
        for row in cursor.fetchall():
            print(f"  {row[0]} ({row[1]})")
            
        db.close()
    except Exception as e:
        print(f"Error checking ramco_academic_system: {e}")

    print("\n--- Database: rit_approval_system ---")
    try:
        db = MySQLdb.connect(host='localhost', user='root', passwd='', db='rit_approval_system')
        cursor = db.cursor()
        
        cursor.execute("DESC control_room_user")
        print("\nColumns in control_room_user:")
        for row in cursor.fetchall():
            print(f"  {row[0]} ({row[1]})")
            
        cursor.execute("SELECT username, Employee_id, password FROM control_room_user WHERE username IN ('1223', '123') OR Employee_id IN ('1223', '123')")
        print("\nSpecific Users (1223, 123):")
        for row in cursor.fetchall():
            print(f"  Username: {row[0]} | EmpID: {row[1]} | Password: {row[2][:20]}...")

        # Also check for roles/types in this DB
        cursor.execute("SHOW TABLES LIKE '%role%'")
        roles_tables = cursor.fetchall()
        if roles_tables:
            print("\nRole related tables:")
            for t in roles_tables:
                print(f"  {t[0]}")
                
        db.close()
    except Exception as e:
        print(f"Error checking rit_approval_system: {e}")

if __name__ == "__main__":
    check_db()
