import os
import django
import sys

# Setup Django environment
sys.path.append(r'c:\Users\ramro\OneDrive\Documents\chatbot for teacher')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from chatbot.models import StudentDetails, FacultyManagementGeneralInformation
from chatbot.chatbot_logic import ERPBot

def test_auto_role_elevation():
    """Test that Teachers who are also CAs get auto-elevated to CA access."""
    
    bot = ERPBot()
    
    # Test with B.Revathi and student 953624243079
    faculty = FacultyManagementGeneralInformation.objects.filter(name__icontains='revathi').first()
    student = StudentDetails.objects.get(reg_no='953624243079')
    
    print("="*70)
    print("SMART ROLE ELEVATION TEST")
    print("="*70)
    print(f"Faculty: {faculty.name} (ID: {faculty.id})")
    print(f"Student: {student.name} ({student.reg_no})")
    print(f"Student's CA_ID: {student.ca_id}")
    print(f"Is CA for student: {str(faculty.id) == str(student.ca_id)}")
    
    print("\n" + "="*70)
    print("SCENARIO: Teacher role querying student they're CA for")
    print("="*70)
    print("Expected: Auto-elevate to CA access, show all marks")
    
    # Query as Teacher role (should auto-elevate to CA)
    response = bot.process_query(
        f"information of {student.reg_no}", 
        faculty.faculty_id, 
        role='Teacher'  # Logged in as Teacher, not CA
    )
    
    print("\nResponse:")
    print("-"*70)
    print(response)
    print("-"*70)
    
    # Verify success criteria
    checks = {
        "Shows student profile": student.name in response,
        "Shows full info (not just assigned subjects error)": "Access restricted to your assigned subjects only" not in response,
        "Shows marks or profile data": ("Academic Marks" in response or "Registration No" in response),
        "No subject restriction error": "No assessment marks found for your Assigned Subjects" not in response,
    }
    
    print("\nVERIFICATION:")
    for check, passed in checks.items():
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {check}")
    
    all_passed = all(checks.values())
    
    if all_passed:
        print("\nRESULT: SUCCESS - Role auto-elevation working!")
        print("B.Revathi can now query her CA students even when logged in as Teacher")
    else:
        print("\nRESULT: FAILED - Role auto-elevation not working")
    
    return all_passed

if __name__ == "__main__":
    success = test_auto_role_elevation()
    sys.exit(0 if success else 1)
