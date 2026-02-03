import os
import django
import sys

# Setup Django environment
sys.path.append(r'c:\Users\ramro\OneDrive\Documents\chatbot for teacher')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from chatbot.models import StudentDetails, FacultyManagementGeneralInformation, AssessmentMark
from chatbot.chatbot_logic import ERPBot

def test_ca_full_access():
    """Test that a Class Advisor can see ALL marks for their students, not just their own subjects."""
    
    bot = ERPBot()
    
    # Find a student with a CA assigned
    student = StudentDetails.objects.exclude(ca_id__isnull=True).exclude(ca_id='').first()
    if not student:
        print("No student with CA assigned found.")
        return
    
    ca_id = student.ca_id
    faculty = FacultyManagementGeneralInformation.objects.filter(id=ca_id).first()
    
    if not faculty:
        print(f"CA with ID {ca_id} not found in faculty table.")
        return
    
    print(f"=== CLASS ADVISOR TEST ===")
    print(f"CA: {faculty.name} (ID: {faculty.faculty_id})")
    print(f"Student: {student.name} ({student.reg_no})")
    print(f"Student Department: {student.department.Department if student.department else 'None'}")
    
    # Check all marks this student has
    all_marks = AssessmentMark.objects.filter(student=student)
    unique_subjects = set()
    for m in all_marks:
        if m.assessment and m.assessment.course:
            unique_subjects.add(m.assessment.course.title)
    
    print(f"\nStudent has marks in {len(unique_subjects)} subjects:")
    for subject in sorted(unique_subjects):
        print(f"  - {subject}")
    
    # Test CA query
    print(f"\n=== CA Query Test ===")
    response = bot.process_query(f"Performance of {student.reg_no}", faculty.faculty_id, role='CA')
    
    # Check if response contains scope information
    if "All Subjects (Full Access)" in response or "All Subjects" in response:
        print("✓ CA has full access scope!")
    else:
        print("✗ WARNING: CA might be restricted!")
    
    print(f"\nResponse preview:\n{response[:500]}...")

if __name__ == "__main__":
    test_ca_full_access()
