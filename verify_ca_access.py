import os
import django
import sys

# Setup Django environment
sys.path.append(r'c:\Users\ramro\OneDrive\Documents\chatbot for teacher')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from chatbot.models import StudentDetails, FacultyManagementGeneralInformation
from chatbot.chatbot_logic import ERPBot

def quick_ca_test():
    """Quick verification that CA sees 'All Subjects (Full Access)'."""
    
    bot = ERPBot()
    
    # Find a student with a CA
    student = StudentDetails.objects.exclude(ca_id__isnull=True).exclude(ca_id='').first()
    if not student:
        print("No student with CA found")
        return
    
    ca_faculty = FacultyManagementGeneralInformation.objects.filter(id=student.ca_id).first()
    if not ca_faculty:
        print("CA faculty not found")
        return
    
    print("Testing CA Access Control")
    print("-" * 50)
    print(f"CA: {ca_faculty.name}")
    print(f"Student: {student.name} ({student.reg_no})")
    
    # Query as CA
    response = bot.process_query(f"info of {student.reg_no}", ca_faculty.faculty_id, role='CA')
    
    # Check for full access indicator
    if "All Subjects (Full Access)" in response:
        print("\nRESULT: PASS - CA has full unrestricted access")
        print("Found scope: 'All Subjects (Full Access)'")
        return True
    elif "All Subjects" in response:
        print("\nRESULT: PASS - CA has unrestricted access")
        print("Found scope: 'All Subjects'")
        return True
    else:
        print("\nRESULT: FAIL - CA might be restricted")
        print(f"Response preview: {response[:200]}")
        return False

if __name__ == "__main__":
    success = quick_ca_test()
    sys.exit(0 if success else 1)
