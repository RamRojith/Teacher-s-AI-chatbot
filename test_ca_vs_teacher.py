import os
import django
import sys

# Setup Django environment
sys.path.append(r'c:\Users\ramro\OneDrive\Documents\chatbot for teacher')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from chatbot.models import StudentDetails, FacultyManagementGeneralInformation, AssessmentMark, AssignSubjectFaculty
from chatbot.chatbot_logic import ERPBot

def test_ca_vs_teacher():
    """Compare access levels between CA and Teacher for the same student."""
    
    bot = ERPBot()
    
    # Find a student with both marks and a CA
    student = StudentDetails.objects.filter(
        ca_id__isnull=False
    ).exclude(ca_id='').first()
    
    if not student:
        print("No suitable student found.")
        return
    
    # Get CA faculty
    ca_faculty = FacultyManagementGeneralInformation.objects.filter(id=student.ca_id).first()
    
    # Find a teacher who teaches this student's class
    teacher_assignment = AssignSubjectFaculty.objects.filter(
        department=student.department,
        batch=student.batch,
        section=student.section
    ).first()
    
    if not teacher_assignment:
        print(f"No teacher assignment found for {student.department.Department}, Batch {student.batch}, Section {student.section}")
        return
    
    teacher_faculty = teacher_assignment.faculty
    
    print("="*60)
    print("ROLE-BASED ACCESS COMPARISON TEST")
    print("="*60)
    print(f"\nStudent: {student.name} ({student.reg_no})")
    print(f"Department: {student.department.Department if student.department else 'None'}")
    print(f"Batch: {student.batch}, Section: {student.section}")
    
    # Get all subject marks for reference
    all_marks = AssessmentMark.objects.filter(student=student)
    subjects = set()
    for m in all_marks:
        if m.assessment and m.assessment.course:
            subjects.add(m.assessment.course.title)
    
    print(f"\nTotal subjects with marks: {len(subjects)}")
    if subjects:
        for s in sorted(subjects):
            print(f"  - {s}")
    
    print("\n" + "="*60)
    print("TEST 1: CLASS ADVISOR ACCESS")
    print("="*60)
    print(f"Faculty: {ca_faculty.name} (Role: CA)")
    print(f"Department: {ca_faculty.department.Department if ca_faculty.department else 'None'}")
    
    ca_response = bot.process_query(f"marks of {student.reg_no}", ca_faculty.faculty_id, role='CA')
    
    if "All Subjects (Full Access)" in ca_response:
        print("\n✓ CONFIRMED: CA has FULL ACCESS to all subjects")
    elif "All Subjects" in ca_response:
        print("\n✓ CA has unrestricted access")
    else:
        print("\n✗ WARNING: CA access might be restricted")
    
    print(f"\nResponse length: {len(ca_response)} characters")
    
    print("\n" + "="*60)
    print("TEST 2: TEACHER ACCESS")
    print("="*60)
    print(f"Faculty: {teacher_faculty.name} (Role: Teacher)")
    print(f"Department: {teacher_faculty.department.Department if teacher_faculty.department else 'None'}")
    print(f"Assigned Subject: {teacher_assignment.course.title if teacher_assignment.course else 'None'}")
    
    teacher_response = bot.process_query(f"marks of {student.reg_no}", teacher_faculty.faculty_id, role='Teacher')
    
    if "Assigned Subjects" in teacher_response:
        print("\n✓ CONFIRMED: Teacher is restricted to assigned subjects")
    elif "Access Denied" in teacher_response or "No assessment marks" in teacher_response:
        print("\n✓ Teacher has limited/no access (as expected)")
    else:
        print("\n? Teacher access level unclear")
    
    print(f"\nResponse length: {len(teacher_response)} characters")
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"CA Response Size: {len(ca_response)} chars")
    print(f"Teacher Response Size: {len(teacher_response)} chars")
    
    if len(ca_response) > len(teacher_response):
        print("\n✓ CA sees more data than Teacher (correct behavior)")
    else:
        print("\n⚠ Response sizes are similar - verify access levels")

if __name__ == "__main__":
    test_ca_vs_teacher()
