import os
import django
import sys

# Setup Django environment
sys.path.append(r'c:\Users\ramro\OneDrive\Documents\chatbot for teacher')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from chatbot.models import StudentDetails, FacultyManagementGeneralInformation, AssignSubjectFaculty, AssessmentMark
from chatbot.chatbot_logic import ERPBot

def compare_ca_vs_teacher_info():
    """Compare info display between CA and Teacher."""
    
    bot = ERPBot()
    
    # Find a student with marks
    student = StudentDetails.objects.exclude(ca_id__isnull=True).filter(
        assessment_marks__isnull=False
    ).distinct().first()
    
    if not student:
        student = StudentDetails.objects.exclude(ca_id__isnull=True).first()
    
    if not student:
        print("No suitable student found")
        return False
    
    ca_faculty = FacultyManagementGeneralInformation.objects.filter(id=student.ca_id).first()
    
    # Find a teacher for this student
    teacher_assignment = AssignSubjectFaculty.objects.filter(
        department=student.department,
        batch=student.batch,
        section=student.section
    ).first()
    
    if not teacher_assignment:
        print("No teacher assignment found")
        return False
    
    teacher_faculty = teacher_assignment.faculty
    
    print("="*70)
    print("CA vs TEACHER INFORMATION DISPLAY COMPARISON")
    print("="*70)
    print(f"Student: {student.name} ({student.reg_no})")
    print(f"Department: {student.department.Department if student.department else 'N/A'}")
    
    # Count subjects with marks
    marks = AssessmentMark.objects.filter(student=student)
    subjects = set()
    for m in marks:
        if m.assessment and m.assessment.course:
            subjects.add(m.assessment.course.title)
    print(f"Subjects with marks: {len(subjects)}")
    
    print("\n" + "="*70)
    print("TEST 1: CLASS ADVISOR VIEW")
    print("="*70)
    print(f"Faculty: {ca_faculty.name} (Role: CA)")
    
    ca_response = bot.process_query(f"info of {student.reg_no}", ca_faculty.faculty_id, role='CA')
    print("\nResponse:")
    print("-"*70)
    print(ca_response)
    
    ca_subject_count = sum(1 for subj in subjects if subj in ca_response)
    print(f"\nSubjects shown: {ca_subject_count}/{len(subjects)}")
    
    print("\n" + "="*70)
    print("TEST 2: TEACHER VIEW")
    print("="*70)
    print(f"Faculty: {teacher_faculty.name} (Role: Teacher)")
    print(f"Assigned Subject: {teacher_assignment.course.title if teacher_assignment.course else 'N/A'}")
    
    teacher_response = bot.process_query(f"info of {student.reg_no}", teacher_faculty.faculty_id, role='Teacher')
    print("\nResponse:")
    print("-"*70)
    print(teacher_response)
    
    teacher_subject_count = sum(1 for subj in subjects if subj in teacher_response)
    print(f"\nSubjects shown: {teacher_subject_count}/{len(subjects)}")
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    results = {
        "CA shows profile info (Reg No, Dept, etc.)": "Registration No" in ca_response or "Reg No" in ca_response,
        "CA shows ALL subjects": ca_subject_count == len(subjects) if subjects else True,
        "CA has 'Full Access' indicator": "All Subjects (Full Access)" in ca_response or "Academic Marks" in ca_response,
        "Teacher is subject-restricted": teacher_subject_count < len(subjects) if len(subjects) > 1 else True,
    }
    
    for desc, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {desc}")
    
    all_passed = all(results.values())
    print(f"\nOVERALL: {'PASS - CA has proper HOD-like access' if all_passed else 'FAIL - Access not configured correctly'}")
    
    return all_passed

if __name__ == "__main__":
    success = compare_ca_vs_teacher_info()
    sys.exit(0 if success else 1)
