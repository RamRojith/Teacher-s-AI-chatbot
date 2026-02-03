import os
import django
import sys

# Setup Django environment
sys.path.append(r'c:\Users\ramro\OneDrive\Documents\chatbot for teacher')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from chatbot.models import StudentDetails, Add_Department, FacultyManagementGeneralInformation, AssignSubjectFaculty
from chatbot.chatbot_logic import ERPBot

def test_rbac():
    bot = ERPBot()
    
    # Let's find some sample data
    depts = list(Add_Department.objects.all())
    if len(depts) < 2:
        print("Not enough departments for test.")
        return

    dept_a = depts[0]
    dept_b = depts[1]

    print(f"Dept A: {dept_a.id} - {dept_a.Department}")
    print(f"Dept B: {dept_b.id} - {dept_b.Department}")

    # Find a student in Dept A
    student_a = StudentDetails.objects.filter(department=dept_a).first()
    if not student_a:
        print(f"No students found in {dept_a.Department}")
        return
    print(f"Sample Student (Dept A): {student_a.name} ({student_a.reg_no})")

    # Find a faculty in Dept B
    faculty_b = FacultyManagementGeneralInformation.objects.filter(department=dept_b).first()
    if not faculty_b:
        print(f"No faculty found in {dept_b.Department}")
        # Try finding ANY faculty and we'll check their dept
        faculty_b = FacultyManagementGeneralInformation.objects.first()
        if not faculty_b:
            print("No faculty found at all.")
            return
        dept_b = faculty_b.department
        print(f"Using Faculty: {faculty_b.name} from Dept: {dept_b.Department if dept_b else 'None'}")
    else:
        print(f"Sample Faculty (Dept B): {faculty_b.name} (ID: {faculty_b.faculty_id})")
        
    # Find a student in faculty_b's department
    student_b = StudentDetails.objects.filter(department=dept_b).first()
    if student_b:
        print(f"Sample Student (Dept B): {student_b.name} ({student_b.reg_no})")

    # Test 1: Faculty B (Teacher role) query Student A (different department)
    print(f"\n--- Test 1: Teacher ({dept_b.Department}) querying Student ({dept_a.Department}) ---")
    response = bot.process_query(f"Marks for {student_a.reg_no}", faculty_b.faculty_id, role='Teacher')
    print(f"Response: {response}")

    # Check if they ARE assigned (might happen in real data)
    is_assigned = AssignSubjectFaculty.objects.filter(
        faculty=faculty_b,
        department=student_a.department,
        batch=student_a.batch,
        section=student_a.section
    ).exists()
    print(f"Actually assigned in DB? {is_assigned}")

    # Test 2: Faculty B (HOD role) query Student A (different department)
    print(f"\n--- Test 2: HOD ({dept_b.Department}) querying Student ({dept_a.Department}) ---")
    response = bot.process_query(f"Marks for {student_a.reg_no}", faculty_b.faculty_id, role='HOD')
    print(f"Response: {response}")

    # Test 3: List students of Dept A as HOD of Dept B
    print(f"\n--- Test 3: HOD ({dept_b.Department}) listing {dept_a.Department} Students ---")
    response = bot.process_query(f"list students in {dept_a.Department}", faculty_b.faculty_id, role='HOD')
    print(f"Response: {response}")

if __name__ == "__main__":
    test_rbac()
