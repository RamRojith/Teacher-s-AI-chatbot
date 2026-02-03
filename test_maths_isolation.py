import os
import django
import sys
import re

# Setup Django environment
sys.path.append(r'c:\Users\ramro\OneDrive\Documents\chatbot for teacher')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from chatbot.models import StudentDetails, Add_Department, FacultyManagementGeneralInformation, AssignSubjectFaculty, AssessmentMark
from chatbot.chatbot_logic import ERPBot

def test_subject_isolation():
    bot = ERPBot()
    
    # Target Departments
    maths_dept = Add_Department.objects.get(id=13)
    cse_dept = Add_Department.objects.get(id=4)
    
    print(f"Testing with Maths Dept (ID 13) and CSE Dept (ID 4)")

    # Find a CSE student
    student = StudentDetails.objects.filter(department=cse_dept).first()
    if not student:
        print("No CSE student found.")
        return
    print(f"Student: {student.name} ({student.reg_no}) from {student.department.Department}")

    # Find a Maths faculty
    maths_faculty = FacultyManagementGeneralInformation.objects.filter(department=maths_dept).first()
    if not maths_faculty:
        print("No Maths faculty found.")
        return
    print(f"Faculty: {maths_faculty.name} (ID: {maths_faculty.faculty_id}) from {maths_faculty.department.Department}")

    # Ensure the Maths faculty is assigned to this student's section to pass authorization
    # If not assigned, we'll temporarily create an assignment for the test
    assignment = AssignSubjectFaculty.objects.filter(
        faculty=maths_faculty,
        department=student.department,
        batch=student.batch,
        section=student.section
    ).first()
    
    if not assignment:
        print(f"Note: {maths_faculty.name} is NOT assigned to this student's section. Access should be denied.")
    else:
        print(f"Note: {maths_faculty.name} IS assigned to teach {assignment.course.title} to this student.")

    # Test 1: Query student as Teacher (Should be restricted to their subjects)
    print("\n--- Test 1: Teacher Query (Subject Restricted) ---")
    response = bot.process_query(f"Analyze performance of {student.reg_no}", maths_faculty.faculty_id, role='Teacher')
    print(f"Response Snippet: {response[:300]}...")

    # Test 2: Query student as HOD (Should be restricted to their department's subjects)
    print("\n--- Test 2: HOD Query (Department Restricted) ---")
    response = bot.process_query(f"Analyze {student.reg_no}", maths_faculty.faculty_id, role='HOD')
    print(f"Response Snippet: {response[:300]}...")

if __name__ == "__main__":
    test_subject_isolation()
