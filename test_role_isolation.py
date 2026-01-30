import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from django.db import connections
from chatbot.chatbot_logic import ERPBot
import re

def clean_resp(resp):
    if isinstance(resp, dict):
        return f"{resp.get('text')} [CHART DATA: {len(resp.get('data', {}))} items]"
    return re.sub(r'[^\x00-\x7F]+', '[EMOJI]', resp)

def test_user_1202():
    print("=== TESTING USER 1202 MULTI-ROLE CONTEXT ===")
    faculty_id = '1202'
    
    # 1. Check roles in DB
    with connections['approval_system'].cursor() as cursor:
        cursor.execute("""
            SELECT u.id, r.role 
            FROM control_room_user u
            JOIN control_room_role r ON u.role_id = r.id
            WHERE u.Employee_id = %s
        """, [faculty_id])
        roles = cursor.fetchall()
        print(f"Roles found for 1202: {[r[1] for r in roles]}")
        all_roles = [r[1] for r in roles]

    bot = ERPBot()

    # 2. Test as HOD
    print("\n--- Testing ACTIVE ROLE: HOD ---")
    active_role = 'HOD'
    # Query for students (should list departmental students)
    resp = bot.process_query("list students", faculty_id, role=active_role, all_roles=all_roles)
    print(f"Query 'list students':\n{clean_resp(resp)}")

    # 3. Test as Faculty (Subject Handling)
    print("\n--- Testing ACTIVE ROLE: Faculty ---")
    active_role = 'Faculty'
    # Query for students (should only show assigned class students)
    resp = bot.process_query("list students", faculty_id, role=active_role, all_roles=all_roles)
    print(f"Query 'list students':\n{clean_resp(resp)}")

    # 4. Test as Office (Should deny student list)
    print("\n--- Testing ACTIVE ROLE: Office ---")
    # Looking at my code, I used 'Office' in the list of denied roles for student information
    active_role = 'Office'
    resp = bot.process_query("list students", faculty_id, role=active_role, all_roles=all_roles)
    print(f"Query 'list students':\n{clean_resp(resp)}")

    # 5. Test Access Restriction - Specific Student Outside Assignment but in Dept
    # Need to find a student in HOD's dept but not assigned to them specifically as CA/Mentor
    # For now testing generic denial
    print("\n--- Testing Role Isolation (Forbidden Access) ---")
    # Ask for marks as HOD (HOD can view all marks in dept)
    resp = bot.process_query("marks of 953624114030", faculty_id, role='HOD', all_roles=all_roles)
    print(f"Query 'marks' as HOD:\n{clean_resp(resp)}")
    
    # Ask for same marks as Office (Should deny)
    resp = bot.process_query("marks of 953624114030", faculty_id, role='Office', all_roles=all_roles)
    print(f"Query 'marks' as Office:\n{clean_resp(resp)}")

if __name__ == "__main__":
    test_user_1202()
