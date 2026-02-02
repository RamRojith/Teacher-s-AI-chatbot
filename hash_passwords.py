import os
import django
import MySQLdb
from django.contrib.auth.hashers import make_password, is_password_usable

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

def hash_plain_passwords():
    try:
        # Connect to the external approval system database
        db = MySQLdb.connect(host='localhost', user='root', passwd='', db='rit_approval_system')
        cursor = db.cursor()
        
        # Fetch all users
        cursor.execute("SELECT id, password, username, Employee_id FROM control_room_user")
        users = cursor.fetchall()
        
        updated_count = 0
        for user_id, current_pass, username, emp_id in users:
            # Check if it's already a Django hash
            # Django hashes usually start with 'pbkdf2_sha256$', 'bcrypt$', 'argon2$', etc.
            if '$' not in current_pass:
                print(f"Hashing password for user {username} (EmpID: {emp_id})...")
                hashed_pass = make_password(current_pass)
                cursor.execute("UPDATE control_room_user SET password = %s WHERE id = %s", [hashed_pass, user_id])
                updated_count += 1
        
        db.commit()
        db.close()
        print(f"\nSuccessfully hashed {updated_count} plain text passwords.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    hash_plain_passwords()
