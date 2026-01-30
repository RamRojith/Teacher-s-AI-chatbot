import os
import django
import random
from datetime import datetime, timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from chatbot.models import (
    Student, Faculty, Mark, Attendance, StudentDashboardStats, 
    Mentorship, ClassAdvisorship, SubjectAllocation
)

def seed():
    print("Clearing existing data...")
    Student.objects.all().delete()
    Faculty.objects.all().delete()

    print("Seeding students and faculty...")
    
    # 1. Create Students
    students = []
    genders = ['Male'] * 30 + ['Female'] * 30
    random.shuffle(genders)
    
    for i in range(1, 61):
        s_id = 100 + i
        s = Student.objects.create(
            id=s_id,
            name=f"Student {i}",
            department="CS",
            year=2,
            gender=genders[i-1]
        )
        students.append(s)

    # 2. Create Faculty
    faculty_data = [
        (1223, "DR. KALIAPPAN M (Advisor)", "Advisor", "1223", "pass123"),
        (2, "Prof. X (Mentor A)", "Mentor", "mentor1", "pass123"),
        (3, "Prof. Y (Mentor B)", "Mentor", "mentor2", "pass123"),
        (4, "Prof. Z (Mentor C)", "Mentor", "mentor3", "pass123"),
        (5, "Mr. Physics", "Teacher", "phys_teacher", "pass123"),
        (6, "Ms. AI", "Teacher", "ai_teacher", "pass123"),
        (7, "Mrs. Math", "Teacher", "math_teacher", "pass123"),
        (8, "Mr. Chem", "Teacher", "chem_teacher", "pass123"),
        (9, "Ms. English", "Teacher", "eng_teacher", "pass123")
    ]
    
    faculty_list = []
    for f_id, name, role, user, pwd in faculty_data:
        f = Faculty.objects.create_user(
            id=f_id,
            username=user,
            password=pwd,
            name=name,
            role=role
        )
        faculty_list.append(f)

    # 3. Allocations
    advisor_faculty = Faculty.objects.get(id=1223)
    ClassAdvisorship.objects.create(faculty=advisor_faculty, department="CS", year=2)

    mentors = [Faculty.objects.get(id=i) for i in [2, 3, 4]]
    for i, s in enumerate(students):
        mentor = mentors[i // 20] # 20 students per mentor
        Mentorship.objects.create(faculty=mentor, student=s)

    subjects_map = {5: "Physics", 6: "AI", 7: "Math", 8: "Chemistry", 9: "English"}
    for f_id, subj in subjects_map.items():
        teacher = Faculty.objects.get(id=f_id)
        SubjectAllocation.objects.create(faculty=teacher, subject=subj, department="CS", year=2)

    # 4. Marks, Attendance & Stats
    all_subjects = list(subjects_map.values())
    for s in students:
        # Dashboard Stats
        if random.random() > 0.7:
             StudentDashboardStats.objects.create(student=s, projects=random.randint(2,5), achievements=random.randint(1,3), publications=random.randint(0,2), co_curricular=random.randint(2,5))
        else:
             StudentDashboardStats.objects.create(student=s, projects=random.randint(0,2), achievements=0, publications=0, co_curricular=random.randint(0,2))

        # Marks
        for sub in all_subjects:
            Mark.objects.create(student=s, subject=sub, score=random.randint(40, 100))

        # Attendance (30 days)
        days_present = random.randint(20, 30)
        base_date = datetime(2023, 11, 1)
        for d in range(30):
            date = base_date + timedelta(days=d)
            status = "Present" if d < days_present else "Absent"
            Attendance.objects.create(student=s, date=date, status=status)

    print("Seeding complete!")

if __name__ == "__main__":
    seed()
