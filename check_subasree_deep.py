import os
import django
import sys

# Setup Django environment
sys.path.append(r'c:\Users\ramro\OneDrive\Documents\chatbot for teacher')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from django.db import connections
from chatbot.models import FacultyManagementGeneralInformation, AssignSubjectFaculty, StudentDetails

def check_subasree():
    print("--- Local DB Check ---")
    suba = FacultyManagementGeneralInformation.objects.filter(name__icontains='subasree').first()
    if suba:
        print(f"Found in local DB: {suba.name}, PK: {suba.id}, EmpID: {suba.faculty_id}, Dept: {suba.department}")
        assignments = AssignSubjectFaculty.objects.filter(faculty=suba)
        print(f"Assignments count: {assignments.count()}")
    else:
        print("Not found in local DB.")

    print("\n--- Approval System Check ---")
    try:
        with connections['approval_system'].cursor() as cursor:
            # Check users
            cursor.execute("SELECT id, username, Employee_id, Department_id FROM control_room_user WHERE username LIKE %s", ['%suba%'])
            rows = cursor.fetchall()
            for row in rows:
                print(f"User in Approval: {row}")
                
            # Check if there are any "assignment" like tables in approval system
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"Total tables in Approval System: {len(tables)}")
            # Looking for tables related to course/faculty/subject
            relevant_tables = [t[0] for t in tables if any(k in t[0].lower() for k in ['assign', 'subject', 'faculty', 'course', 'handling'])]
            print(f"Relevant tables: {relevant_tables}")
    except Exception as e:
        print(f"Error checking approval system: {e}")

if __name__ == "__main__":
    check_subasree()
