import os
import django
import sys

# Setup Django environment
sys.path.append(r'c:\Users\ramro\OneDrive\Documents\chatbot for teacher')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from chatbot.models import StudentDetails, FacultyManagementGeneralInformation, AssessmentMark
from chatbot.chatbot_logic import ERPBot

def test_ca_info_display():
    """Test that CA sees HOD-like student information with all marks."""
    
    bot = ERPBot()
    
    # Find a student with a CA and some marks
    student = StudentDetails.objects.exclude(ca_id__isnull=True).exclude(ca_id='').first()
    if not student:
        print("No student with CA found")
        return
    
    ca_faculty = FacultyManagementGeneralInformation.objects.filter(id=student.ca_id).first()
    if not ca_faculty:
        print("CA faculty not found")
        return
    
    print("="*60)
    print("CA INFORMATION DISPLAY TEST")
    print("="*60)
    print(f"CA: {ca_faculty.name}")
    print(f"Student: {student.name} ({student.reg_no})")
    
    # Count marks for this student
    marks_count = AssessmentMark.objects.filter(student=student).count()
    print(f"Total marks records: {marks_count}")
    
    # Test basic info query
    print("\n--- Query: 'information of <reg_no>' ---")
    response = bot.process_query(f"information of {student.reg_no}", ca_faculty.faculty_id, role='CA')
    
    print("\n" + "="*60)
    print("RESPONSE:")
    print("="*60)
    print(response)
    print("\n" + "="*60)
    
    # Verify key elements are present
    checks = {
        "Has student name": student.name in response,
        "Has registration number": student.reg_no in response,
        "Has department": True if student.department and student.department.Department in response else False,
        "Has batch": str(student.batch) in response if student.batch else True,
        "Has Full Access scope": "All Subjects (Full Access)" in response or "Academic Marks" in response,
    }
    
    print("\nVERIFICATION CHECKS:")
    for check, passed in checks.items():
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {check}")
    
    all_passed = all(checks.values())
    print(f"\nOVERALL: {'PASS' if all_passed else 'FAIL'}")
    
    return all_passed

if __name__ == "__main__":
    success = test_ca_info_display()
    sys.exit(0 if success else 1)
