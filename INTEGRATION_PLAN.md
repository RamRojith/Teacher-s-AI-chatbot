# Real-Time Database Integration Plan for Chatbot System

**Document Date:** January 22, 2026  
**Database:** `ramco_academic_system` (MySQL via phpMyAdmin)  
**Backend:** Django Framework  
**Current Database:** SQLite (will be transitioned to MySQL)

---

## Executive Summary

This plan outlines a secure, scalable architecture for integrating real-time academic data into your chatbot system without permanently storing sensitive student information. The chatbot will act as a **dynamic query layer** that retrieves authorized, contextual data on-demand from the MySQL database through Django's ORM.

### Key Principles
1. **Real-time Data Retrieval** - Query data on-demand; no data caching in chatbot memory
2. **Access Control** - Role-based authorization (Teacher, Advisor, Mentor, Admin)
3. **Data Privacy** - Student data never stored in chatbot logs or model parameters
4. **Immediate Updates** - Database changes reflected instantly in chatbot responses
5. **Scalability** - Architecture supports feature expansion without code refactoring

---

## Phase 1: Database Configuration & Connection

### 1.1 Switch from SQLite to MySQL

**Current State:** Using SQLite (`db.sqlite3`)  
**Target State:** MySQL database `ramco_academic_system`

#### Step 1: Install MySQL Driver
```bash
pip install mysqlclient
# OR (if mysqlclient fails)
pip install PyMySQL
```

#### Step 2: Update Django Settings
**File:** `erp_backend/settings.py`

Replace:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

With:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ramco_academic_system',           # Database name
        'USER': 'root',                             # phpMyAdmin user (modify as needed)
        'PASSWORD': 'your_password',                # Set your MySQL password
        'HOST': '127.0.0.1',                        # Local machine or remote IP
        'PORT': '3306',                             # Default MySQL port
        'OPTIONS': {
            'charset': 'utf8mb4',                   # Support for emojis & special chars
        },
        'CONN_MAX_AGE': 600,                        # Connection pooling (10 min)
    }
}
```

**Security Best Practice:** Store credentials in environment variables:
```python
import os
from decouple import config

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME', default='ramco_academic_system'),
        'USER': config('DB_USER', default='root'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='127.0.0.1'),
        'PORT': config('DB_PORT', default='3306'),
        'OPTIONS': {'charset': 'utf8mb4'},
        'CONN_MAX_AGE': 600,
    }
}
```

#### Step 3: Create `.env` File (Root Directory)
```
DB_NAME=ramco_academic_system
DB_USER=root
DB_PASSWORD=your_actual_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

#### Step 4: Install Python Decouple
```bash
pip install python-decouple
```

#### Step 5: Test Database Connection
```bash
python manage.py dbshell
```

If successful, you'll enter the MySQL shell. Exit with `exit`.

---

## Phase 2: Data Model Mapping

### 2.1 Identify Existing Tables in `ramco_academic_system`

**You need to map your existing MySQL tables** to Django models. Run this command to inspect:

```bash
python manage.py inspectdb --database default > chatbot/models_legacy.py
```

This generates Django models from existing MySQL tables.

### 2.2 Expected Core Tables Structure

Based on your requirements, the `ramco_academic_system` likely contains:

#### **Teacher Tables**
| Table | Purpose |
|-------|---------|
| `faculty` / `teachers` | Teacher credentials, ID, role |
| `teacher_subjects` | Subject allocations (Subject-Teacher mapping) |
| `class_advisors` | Class advisor assignments |
| `mentors` | Mentor assignments |

#### **Student Tables**
| Table | Purpose |
|-------|---------|
| `students` | Student info (ID, name, registration number, department, year) |
| `student_marks` / `marks` | Subject-wise marks |
| `student_attendance` / `attendance` | Attendance records |
| `student_performance` | Performance metrics |
| `student_notifications` | Notifications sent to students |

#### **Academic Data**
| Table | Purpose |
|-------|---------|
| `subjects` | Subject master (code, name) |
| `departments` | Department master |
| `academic_years` | Year/semester information |

### 2.3 Update Django Models to Match MySQL Schema

**File:** `chatbot/models.py`

Ensure your models match the MySQL table structure. Add new models for all tables:

```python
from django.db import models
from django.contrib.auth.models import AbstractUser

# ==================== TEACHER/FACULTY MODELS ====================

class Faculty(AbstractUser):
    """Extended User model for all academic staff"""
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Advisor', 'Class Advisor'),
        ('Mentor', 'Mentor'),
        ('Teacher', 'Subject Teacher'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=50, unique=True, null=True)
    department = models.CharField(max_length=50, null=True)
    
    class Meta:
        db_table = 'faculty'
    
    def __str__(self):
        return f"{self.name} ({self.role})"

# ==================== STUDENT MODELS ====================

class Department(models.Model):
    """Department master table"""
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'departments'
    
    def __str__(self):
        return self.name

class AcademicYear(models.Model):
    """Academic year/semester information"""
    year = models.IntegerField()
    semester = models.IntegerField(choices=[(1, '1'), (2, '2')])
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'academic_years'
        unique_together = ('year', 'semester')
    
    def __str__(self):
        return f"{self.year} - Sem {self.semester}"

class Student(models.Model):
    """Student information"""
    registration_number = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    year = models.IntegerField(choices=[(1, '1st Year'), (2, '2nd Year'), (3, '3rd Year'), (4, '4th Year')])
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    date_of_birth = models.DateField(null=True)
    admission_date = models.DateField()
    
    class Meta:
        db_table = 'students'
    
    def __str__(self):
        return f"{self.name} ({self.registration_number})"

# ==================== ACADEMIC DATA MODELS ====================

class Subject(models.Model):
    """Subject master"""
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    credits = models.IntegerField(default=3)
    semester = models.IntegerField(choices=[(1, '1'), (2, '2')])
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'subjects'
        unique_together = ('code', 'department')
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class SubjectAllocation(models.Model):
    """Teacher-Subject allocation"""
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='allocated_subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    semester = models.IntegerField()
    
    class Meta:
        db_table = 'subject_allocations'
        unique_together = ('faculty', 'subject', 'academic_year')
    
    def __str__(self):
        return f"{self.faculty.name} -> {self.subject.name}"

# ==================== MARKS & PERFORMANCE ====================

class Mark(models.Model):
    """Student marks"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT)
    marks_obtained = models.IntegerField()
    max_marks = models.IntegerField(default=100)
    percentage = models.FloatField(null=True, blank=True)  # Auto-calculated
    grade = models.CharField(max_length=5, null=True, blank=True)  # A, B, C, etc.
    exam_date = models.DateField()
    
    class Meta:
        db_table = 'marks'
        unique_together = ('student', 'subject', 'academic_year')
        ordering = ['-exam_date']
    
    def save(self, *args, **kwargs):
        self.percentage = (self.marks_obtained / self.max_marks) * 100
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student.name} - {self.subject.name}: {self.marks_obtained}/{self.max_marks}"

class Attendance(models.Model):
    """Student attendance"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Present', 'P'), ('Absent', 'A'), ('Leave', 'L')])
    
    class Meta:
        db_table = 'attendance'
        ordering = ['-date']
        unique_together = ('student', 'subject', 'date')
    
    def __str__(self):
        return f"{self.student.name} - {self.date}: {self.status}"

class StudentPerformance(models.Model):
    """Performance metrics (derived/calculated)"""
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='performance')
    current_cgpa = models.FloatField()
    overall_attendance_percentage = models.FloatField()
    subjects_passed = models.IntegerField()
    subjects_failed = models.IntegerField()
    rank = models.IntegerField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'student_performance'
    
    def __str__(self):
        return f"{self.student.name} - CGPA: {self.current_cgpa}"

# ==================== RELATIONSHIPS ====================

class Mentorship(models.Model):
    """Mentor-Student relationship"""
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='mentees')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='mentors')
    assigned_date = models.DateField(auto_now_add=True)
    
    class Meta:
        db_table = 'mentorship'
        unique_together = ('faculty', 'student')
    
    def __str__(self):
        return f"Mentor: {self.faculty.name} -> Mentee: {self.student.name}"

class ClassAdvisorship(models.Model):
    """Class Advisor assignment"""
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='advised_classes')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    year = models.IntegerField()
    assigned_date = models.DateField(auto_now_add=True)
    
    class Meta:
        db_table = 'class_advisorship'
        unique_together = ('faculty', 'department', 'year')
    
    def __str__(self):
        return f"Advisor: {self.faculty.name} -> {self.department.name} Year {self.year}"

# ==================== NOTIFICATIONS & REPORTS ====================

class Notification(models.Model):
    """Inter-faculty and system notifications"""
    sender = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='sent_notifications')
    receiver = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='received_notifications')
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    attachment = models.JSONField(null=True, blank=True)  # Store additional data
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['receiver', '-created_at']),
            models.Index(fields=['is_read']),
        ]
    
    def __str__(self):
        return f"{self.sender.name} -> {self.receiver.name}: {self.message[:50]}"

class ReportLog(models.Model):
    """Teacher submitted reports for class/student"""
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='submitted_reports')
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    content = models.TextField()
    report_type = models.CharField(max_length=50, choices=[
        ('performance', 'Class Performance'),
        ('behavior', 'Student Behavior'),
        ('progress', 'Progress Report'),
        ('concern', 'Concern Report'),
    ])
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, related_name='reports_about')
    submitted_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('acknowledged', 'Acknowledged'),
    ], default='submitted')
    
    class Meta:
        db_table = 'report_logs'
        ordering = ['-submitted_date']
    
    def __str__(self):
        return f"{self.faculty.name} - {self.title}"
```

---

## Phase 3: Access Control & Authorization Layer

### 3.1 Create Permission/Authorization Module

**File:** `chatbot/permissions.py`

```python
from enum import Enum
from .models import Faculty, SubjectAllocation, ClassAdvisorship, Mentorship

class ChatbotPermissions(Enum):
    """Define what each role can access"""
    
    # ADMIN can see all students and all teachers
    ADMIN_VIEW_ALL = "admin_view_all"
    
    # TEACHER can see:
    # - Students in their allocated subjects
    # - Their mentees (if mentor)
    # - Their class (if advisor)
    TEACHER_VIEW_CLASS = "teacher_view_class"
    TEACHER_VIEW_MENTEES = "teacher_view_mentees"
    TEACHER_VIEW_ADVISEES = "teacher_view_advisees"
    TEACHER_VIEW_SUBJECT_STUDENTS = "teacher_view_subject_students"
    
    # ADVISOR can see their entire class
    ADVISOR_VIEW_CLASS = "advisor_view_class"
    
    # MENTOR can see their mentees
    MENTOR_VIEW_MENTEES = "mentor_view_mentees"

class AccessControl:
    """Centralized access control logic"""
    
    @staticmethod
    def can_view_student(faculty: Faculty, student_id: str) -> bool:
        """
        Determine if a faculty member can view a student's data.
        Returns: True if allowed, False otherwise
        """
        # Admin can view everyone
        if faculty.role == 'Admin':
            return True
        
        # Teacher can view if:
        # 1. Student is in their allocated subject
        # 2. They are the student's mentor
        # 3. They are the student's class advisor
        
        # Check subject allocation
        subject_allocated = SubjectAllocation.objects.filter(
            faculty=faculty,
            subject__student_marks__student_id=student_id
        ).exists()
        
        # Check mentorship
        is_mentor = Mentorship.objects.filter(
            faculty=faculty,
            student_id=student_id
        ).exists()
        
        # Check advisorship
        is_advisor = ClassAdvisorship.objects.filter(
            faculty=faculty,
            department=student.department,
            year=student.year
        ).exists()
        
        return subject_allocated or is_mentor or is_advisor
    
    @staticmethod
    def get_accessible_students(faculty: Faculty) -> list:
        """
        Get list of students that a faculty member can access.
        """
        from django.db.models import Q
        
        if faculty.role == 'Admin':
            # Admin can see all students
            from .models import Student
            return Student.objects.all()
        
        # Teachers can see students they teach/mentor/advise
        mentee_ids = Mentorship.objects.filter(
            faculty=faculty
        ).values_list('student_id', flat=True)
        
        subject_student_ids = SubjectAllocation.objects.filter(
            faculty=faculty
        ).values('subject__student_marks__student_id').distinct()
        
        advisee_query = ClassAdvisorship.objects.filter(
            faculty=faculty
        ).values('department', 'year')
        
        from .models import Student
        return Student.objects.filter(
            Q(id__in=mentee_ids) |
            Q(id__in=subject_student_ids) |
            Q(department__in=[a['department'] for a in advisee_query],
              year__in=[a['year'] for a in advisee_query])
        ).distinct()
```

### 3.2 Add Authorization Decorators

**File:** `chatbot/decorators.py`

```python
from functools import wraps
from rest_framework.response import Response
from .models import Faculty
from .permissions import AccessControl

def check_chatbot_access(view_func):
    """Decorator to verify faculty access"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        faculty_id = request.data.get('faculty_id') if hasattr(request, 'data') else request.GET.get('faculty_id')
        
        if not faculty_id:
            return Response({'error': 'Unauthorized'}, status=401)
        
        try:
            faculty = Faculty.objects.get(id=faculty_id)
        except Faculty.DoesNotExist:
            return Response({'error': 'Faculty not found'}, status=404)
        
        request.faculty = faculty
        return view_func(request, *args, **kwargs)
    
    return wrapper

def check_student_access(view_func):
    """Decorator to verify access to specific student"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        faculty_id = request.data.get('faculty_id') or request.GET.get('faculty_id')
        student_id = kwargs.get('student_id') or request.GET.get('student_id')
        
        if not faculty_id or not student_id:
            return Response({'error': 'Missing parameters'}, status=400)
        
        try:
            faculty = Faculty.objects.get(id=faculty_id)
        except Faculty.DoesNotExist:
            return Response({'error': 'Faculty not found'}, status=404)
        
        if not AccessControl.can_view_student(faculty, student_id):
            return Response({'error': 'Access Denied'}, status=403)
        
        request.faculty = faculty
        return view_func(request, *args, **kwargs)
    
    return wrapper
```

---

## Phase 4: Data Retrieval Layer (Query Service)

### 4.1 Create Unified Data Access Service

**File:** `chatbot/data_service.py`

This module acts as the single source of truth for all database queries—ensuring real-time data retrieval without caching.

```python
from django.db.models import Avg, Count, Q, F, Sum
from django.utils import timezone
from datetime import timedelta
from .models import (
    Student, Faculty, Mark, Attendance, StudentPerformance,
    Subject, SubjectAllocation, Mentorship, ClassAdvisorship,
    Department, AcademicYear, Notification, ReportLog
)
from .permissions import AccessControl

class StudentDataService:
    """Retrieve real-time student data for chatbot"""
    
    @staticmethod
    def get_student_basic_info(student_id: str, faculty: Faculty) -> dict:
        """Fetch student basic information"""
        if not AccessControl.can_view_student(faculty, student_id):
            return {'error': 'Access Denied'}
        
        try:
            student = Student.objects.get(registration_number=student_id)
        except Student.DoesNotExist:
            return {'error': f'Student {student_id} not found'}
        
        return {
            'id': student.registration_number,
            'name': student.name,
            'department': student.department.name,
            'year': student.year,
            'email': student.email,
            'phone': student.phone,
            'gender': student.gender,
            'admission_date': student.admission_date.isoformat(),
        }
    
    @staticmethod
    def get_student_marks(student_id: str, faculty: Faculty, subject_id=None, semester=None) -> list:
        """
        Fetch real-time marks for a student.
        
        Args:
            student_id: Student registration number
            faculty: Faculty requesting data
            subject_id: Optional filter by subject
            semester: Optional filter by semester
        
        Returns: List of mark records
        """
        if not AccessControl.can_view_student(faculty, student_id):
            return []
        
        try:
            student = Student.objects.get(registration_number=student_id)
        except Student.DoesNotExist:
            return []
        
        marks_query = Mark.objects.filter(student=student)
        
        if subject_id:
            marks_query = marks_query.filter(subject_id=subject_id)
        
        if semester:
            marks_query = marks_query.filter(academic_year__semester=semester)
        
        marks_query = marks_query.select_related('subject', 'academic_year')
        
        return [{
            'subject': mark.subject.name,
            'subject_code': mark.subject.code,
            'marks': mark.marks_obtained,
            'max_marks': mark.max_marks,
            'percentage': mark.percentage,
            'grade': mark.grade,
            'exam_date': mark.exam_date.isoformat(),
            'academic_year': f"{mark.academic_year.year}-Sem{mark.academic_year.semester}"
        } for mark in marks_query]
    
    @staticmethod
    def get_student_attendance(student_id: str, faculty: Faculty, days=30) -> dict:
        """
        Fetch real-time attendance data.
        
        Args:
            student_id: Student registration number
            faculty: Faculty requesting data
            days: Last N days (default: 30)
        
        Returns: Attendance statistics
        """
        if not AccessControl.can_view_student(faculty, student_id):
            return {}
        
        try:
            student = Student.objects.get(registration_number=student_id)
        except Student.DoesNotExist:
            return {}
        
        cutoff_date = timezone.now().date() - timedelta(days=days)
        
        attendance_records = Attendance.objects.filter(
            student=student,
            date__gte=cutoff_date
        )
        
        total_classes = attendance_records.count()
        present_count = attendance_records.filter(status='Present').count()
        absent_count = attendance_records.filter(status='Absent').count()
        leave_count = attendance_records.filter(status='Leave').count()
        
        percentage = (present_count / total_classes * 100) if total_classes > 0 else 0
        
        return {
            'total_classes': total_classes,
            'present': present_count,
            'absent': absent_count,
            'leave': leave_count,
            'attendance_percentage': round(percentage, 2),
            'status': 'Good' if percentage >= 75 else 'At Risk',
            'period': f'Last {days} days'
        }
    
    @staticmethod
    def get_student_performance(student_id: str, faculty: Faculty) -> dict:
        """Fetch comprehensive performance metrics"""
        if not AccessControl.can_view_student(faculty, student_id):
            return {}
        
        try:
            student = Student.objects.get(registration_number=student_id)
            performance = StudentPerformance.objects.get(student=student)
        except (Student.DoesNotExist, StudentPerformance.DoesNotExist):
            return {}
        
        return {
            'cgpa': performance.current_cgpa,
            'attendance': performance.overall_attendance_percentage,
            'passed': performance.subjects_passed,
            'failed': performance.subjects_failed,
            'rank': performance.rank,
            'last_updated': performance.last_updated.isoformat(),
        }

class ClassDataService:
    """Retrieve real-time class/subject data"""
    
    @staticmethod
    def get_subject_class_performance(faculty: Faculty, subject_id: str) -> dict:
        """Get performance statistics for a subject's class"""
        try:
            subject = Subject.objects.get(code=subject_id)
        except Subject.DoesNotExist:
            return {}
        
        # Verify faculty teaches this subject
        if not SubjectAllocation.objects.filter(faculty=faculty, subject=subject).exists():
            return {'error': 'Access Denied'}
        
        marks = Mark.objects.filter(subject=subject)
        
        avg_marks = marks.aggregate(
            avg=Avg('percentage'),
            max=Max('marks_obtained'),
            min=Min('marks_obtained'),
            count=Count('id')
        )
        
        return {
            'subject': subject.name,
            'subject_code': subject.code,
            'total_students': avg_marks['count'],
            'class_average': round(avg_marks['avg'], 2) if avg_marks['avg'] else 0,
            'highest_score': avg_marks['max'],
            'lowest_score': avg_marks['min'],
            'pass_count': marks.filter(percentage__gte=40).count(),
            'fail_count': marks.filter(percentage__lt=40).count(),
        }

class AdvisorDataService:
    """Retrieve data for class advisors"""
    
    @staticmethod
    def get_class_overview(faculty: Faculty, department_code: str, year: int) -> dict:
        """Get overview of a class"""
        # Verify faculty is advisor
        advisorship = ClassAdvisorship.objects.filter(
            faculty=faculty,
            department__code=department_code,
            year=year
        ).first()
        
        if not advisorship:
            return {'error': 'Access Denied'}
        
        department = advisorship.department
        students = Student.objects.filter(department=department, year=year)
        
        # Get performance stats for all students in class
        total_students = students.count()
        avg_performance = StudentPerformance.objects.filter(
            student__in=students
        ).aggregate(
            avg_cgpa=Avg('current_cgpa'),
            avg_attendance=Avg('overall_attendance_percentage')
        )
        
        return {
            'department': department.name,
            'year': year,
            'total_students': total_students,
            'avg_cgpa': round(avg_performance['avg_cgpa'], 2) if avg_performance['avg_cgpa'] else 0,
            'avg_attendance': round(avg_performance['avg_attendance'], 2) if avg_performance['avg_attendance'] else 0,
            'students': [{'id': s.registration_number, 'name': s.name} for s in students]
        }

class NotificationService:
    """Handle notification queries and logging"""
    
    @staticmethod
    def log_interaction(faculty: Faculty, student_id: str, query: str, response: str):
        """
        Log chatbot interactions for audit purposes.
        Does NOT store student data, just query context.
        """
        Notification.objects.create(
            sender=faculty,
            receiver=faculty,
            student_id=student_id if student_id else None,
            message=f"Query: {query[:100]}...\nResponse: {response[:100]}...",
            attachment={'query_type': 'chatbot_interaction', 'timestamp': timezone.now().isoformat()}
        )
    
    @staticmethod
    def get_alerts_for_faculty(faculty: Faculty) -> list:
        """Get important alerts/notifications for faculty"""
        alerts = []
        
        # If advisor: check failing students
        advisorships = ClassAdvisorship.objects.filter(faculty=faculty)
        for advisorship in advisorships:
            failing_students = StudentPerformance.objects.filter(
                student__department=advisorship.department,
                student__year=advisorship.year,
                current_cgpa__lt=2.0
            ).select_related('student')
            
            for perf in failing_students:
                alerts.append({
                    'type': 'at_risk',
                    'student': perf.student.name,
                    'message': f"{perf.student.name} is at academic risk (CGPA: {perf.current_cgpa})",
                    'severity': 'high'
                })
        
        # If teacher: check excessive absences
        subjects = SubjectAllocation.objects.filter(faculty=faculty).values_list('subject_id', flat=True)
        absent_students = Attendance.objects.filter(
            subject_id__in=subjects,
            status='Absent',
            date__gte=timezone.now().date() - timedelta(days=7)
        ).values('student').annotate(
            absent_count=Count('id')
        ).filter(absent_count__gte=3).select_related('student')
        
        for record in absent_students:
            alerts.append({
                'type': 'high_absence',
                'student': record.student.name,
                'message': f"{record.student.name} has {record['absent_count']} absences in last 7 days",
                'severity': 'medium'
            })
        
        return alerts
```

---

## Phase 5: Enhanced Chatbot Logic Layer

### 5.1 Refactor Chatbot Logic with Real-Time Data Queries

**File:** `chatbot/chatbot_logic.py` (Refactored)

```python
import re
from datetime import datetime
from .models import Faculty, Student
from .permissions import AccessControl
from .data_service import StudentDataService, ClassDataService, AdvisorDataService, NotificationService
from .knowledge_base import KnowledgeBase

class ERPChatbot:
    """Enhanced chatbot with real-time database queries"""
    
    def __init__(self):
        self.kb = KnowledgeBase()
        self.student_service = StudentDataService()
        self.class_service = ClassDataService()
        self.advisor_service = AdvisorDataService()
        self.notification_service = NotificationService()
    
    def process_query(self, user_query: str, faculty_id: int) -> str:
        """
        Main entry point for processing queries.
        Executes real-time database queries based on user intent.
        """
        try:
            faculty = Faculty.objects.get(id=faculty_id)
        except Faculty.DoesNotExist:
            return "❌ Faculty not found. Please log in again."
        
        query_lower = user_query.strip().lower()
        
        # ==================== INTENT DETECTION ====================
        
        # 1. Student Marks Query
        if any(k in query_lower for k in ['mark', 'score', 'exam', 'result']):
            return self._handle_marks_query(faculty, user_query)
        
        # 2. Student Attendance Query
        if any(k in query_lower for k in ['attendance', 'present', 'absent', 'leave']):
            return self._handle_attendance_query(faculty, user_query)
        
        # 3. Student Performance/CGPA Query
        if any(k in query_lower for k in ['performance', 'cgpa', 'ranking', 'academic']):
            return self._handle_performance_query(faculty, user_query)
        
        # 4. Class Report/Analysis Query
        if any(k in query_lower for k in ['class report', 'subject report', 'class analysis']):
            return self._handle_class_analysis_query(faculty, user_query)
        
        # 5. Student Info Query
        if any(k in query_lower for k in ['student info', 'student details', 'who is']):
            return self._handle_student_info_query(faculty, user_query)
        
        # 6. Alerts/Notifications
        if any(k in query_lower for k in ['alert', 'notification', 'warning', 'at risk']):
            return self._handle_alerts_query(faculty)
        
        # Fallback to knowledge base
        kb_response = self.kb.search_help(query_lower)
        if kb_response:
            return kb_response
        
        return "🤔 I didn't understand that query. Try:\n- 'Show marks of student 101'\n- 'Attendance for student 102'\n- 'Class report for Mathematics'"
    
    def _handle_marks_query(self, faculty: Faculty, query: str) -> str:
        """Handle marks/scores queries - REAL-TIME DB QUERY"""
        student_ids = re.findall(r'\b(\d{3,4})\b', query)
        
        if not student_ids:
            return "Please specify a student ID. Example: 'Show marks of 101'"
        
        results = []
        for student_id in student_ids[:5]:  # Limit to 5 students
            try:
                student = Student.objects.get(registration_number=student_id)
                
                if not AccessControl.can_view_student(faculty, student_id):
                    results.append(f"❌ {student_id}: Access Denied")
                    continue
                
                # REAL-TIME QUERY
                marks = self.student_service.get_student_marks(student_id, faculty)
                
                if not marks:
                    results.append(f"📋 {student.name} ({student_id}): No marks found")
                    continue
                
                marks_summary = f"📊 {student.name} ({student_id}):\n"
                total_marks = 0
                total_percentage = 0
                
                for mark in marks:
                    marks_summary += f"  • {mark['subject_code']}: {mark['marks']}/{mark['max_marks']} ({mark['percentage']:.1f}%) [{mark['grade']}]\n"
                    total_percentage += mark['percentage']
                
                avg_percentage = total_percentage / len(marks)
                marks_summary += f"  📈 Average: {avg_percentage:.2f}%"
                
                results.append(marks_summary)
            
            except Student.DoesNotExist:
                results.append(f"❌ Student {student_id} not found")
        
        return "\n\n".join(results)
    
    def _handle_attendance_query(self, faculty: Faculty, query: str) -> str:
        """Handle attendance queries - REAL-TIME DB QUERY"""
        student_ids = re.findall(r'\b(\d{3,4})\b', query)
        
        if not student_ids:
            return "Please specify a student ID. Example: 'Attendance of 101'"
        
        student_id = student_ids[0]
        
        try:
            student = Student.objects.get(registration_number=student_id)
            
            if not AccessControl.can_view_student(faculty, student_id):
                return "❌ Access Denied"
            
            # REAL-TIME QUERY
            attendance = self.student_service.get_student_attendance(student_id, faculty)
            
            if not attendance:
                return f"❌ No attendance data for {student.name}"
            
            status_emoji = "✅" if attendance['attendance_percentage'] >= 75 else "⚠️"
            
            response = f"{status_emoji} {student.name} ({student_id}) - Last 30 Days\n"
            response += f"  • Present: {attendance['present']} days\n"
            response += f"  • Absent: {attendance['absent']} days\n"
            response += f"  • Leave: {attendance['leave']} days\n"
            response += f"  • Total Classes: {attendance['total_classes']}\n"
            response += f"  📊 Attendance: {attendance['attendance_percentage']}% [{attendance['status']}]"
            
            return response
        
        except Student.DoesNotExist:
            return f"❌ Student {student_id} not found"
    
    def _handle_performance_query(self, faculty: Faculty, query: str) -> str:
        """Handle performance/CGPA queries - REAL-TIME DB QUERY"""
        student_ids = re.findall(r'\b(\d{3,4})\b', query)
        
        if not student_ids:
            return "Please specify a student ID. Example: 'Performance of 101'"
        
        student_id = student_ids[0]
        
        try:
            student = Student.objects.get(registration_number=student_id)
            
            if not AccessControl.can_view_student(faculty, student_id):
                return "❌ Access Denied"
            
            # REAL-TIME QUERIES
            performance = self.student_service.get_student_performance(student_id, faculty)
            marks = self.student_service.get_student_marks(student_id, faculty)
            attendance = self.student_service.get_student_attendance(student_id, faculty)
            
            if not performance:
                return f"❌ No performance data for {student.name}"
            
            response = f"📈 {student.name} ({student_id}) - Overall Performance\n\n"
            response += f"  🎯 CGPA: {performance['cgpa']}\n"
            response += f"  📊 Attendance: {performance['attendance']:.1f}%\n"
            response += f"  ✅ Subjects Passed: {performance['passed']}\n"
            response += f"  ❌ Subjects Failed: {performance['failed']}\n"
            if performance['rank']:
                response += f"  🏆 Class Rank: {performance['rank']}\n"
            response += f"  🔄 Last Updated: {performance['last_updated']}"
            
            return response
        
        except Student.DoesNotExist:
            return f"❌ Student {student_id} not found"
    
    def _handle_class_analysis_query(self, faculty: Faculty, query: str) -> str:
        """Handle class/subject analysis queries - REAL-TIME DB QUERY"""
        # Extract subject name/code
        subject_match = re.search(r'(?:for|of)\s+([A-Za-z\s]+)', query)
        subject_code = subject_match.group(1).strip() if subject_match else None
        
        if not subject_code:
            return "Please specify a subject. Example: 'Class report for Mathematics'"
        
        # REAL-TIME QUERY
        analysis = self.class_service.get_subject_class_performance(faculty, subject_code)
        
        if not analysis or 'error' in analysis:
            return f"❌ Subject '{subject_code}' not found or access denied"
        
        response = f"📊 Class Analysis - {analysis['subject']} ({analysis['subject_code']})\n\n"
        response += f"  👥 Total Students: {analysis['total_students']}\n"
        response += f"  📈 Class Average: {analysis['class_average']}%\n"
        response += f"  🏆 Highest Score: {analysis['highest_score']}\n"
        response += f"  📉 Lowest Score: {analysis['lowest_score']}\n"
        response += f"  ✅ Passed: {analysis['pass_count']}\n"
        response += f"  ❌ Failed: {analysis['fail_count']}\n"
        
        pass_percentage = (analysis['pass_count'] / analysis['total_students'] * 100) if analysis['total_students'] > 0 else 0
        response += f"  📊 Pass Rate: {pass_percentage:.1f}%"
        
        return response
    
    def _handle_student_info_query(self, faculty: Faculty, query: str) -> str:
        """Handle student info queries - REAL-TIME DB QUERY"""
        student_ids = re.findall(r'\b(\d{3,4})\b', query)
        
        if not student_ids:
            return "Please specify a student ID. Example: 'Student 101 info'"
        
        student_id = student_ids[0]
        
        try:
            if not AccessControl.can_view_student(faculty, student_id):
                return "❌ Access Denied"
            
            # REAL-TIME QUERY
            info = self.student_service.get_student_basic_info(student_id, faculty)
            
            if 'error' in info:
                return f"❌ {info['error']}"
            
            response = f"👤 Student Information\n\n"
            response += f"  • ID: {info['id']}\n"
            response += f"  • Name: {info['name']}\n"
            response += f"  • Department: {info['department']}\n"
            response += f"  • Year: {info['year']}\n"
            response += f"  • Gender: {info['gender']}\n"
            response += f"  • Email: {info['email']}\n"
            response += f"  • Phone: {info['phone']}\n"
            response += f"  • Admission Date: {info['admission_date']}"
            
            return response
        
        except Exception as e:
            return f"❌ Error retrieving student information: {str(e)}"
    
    def _handle_alerts_query(self, faculty: Faculty) -> str:
        """Handle alerts/notifications queries - REAL-TIME DB QUERY"""
        # REAL-TIME QUERY
        alerts = self.notification_service.get_alerts_for_faculty(faculty)
        
        if not alerts:
            return "✅ No alerts at this time"
        
        response = f"🚨 Active Alerts ({len(alerts)})\n\n"
        
        for alert in alerts:
            emoji = "🔴" if alert['severity'] == 'high' else "🟡"
            response += f"{emoji} [{alert['type'].upper()}] {alert['message']}\n"
        
        return response
```

---

## Phase 6: API Integration Layer

### 6.1 Update Views with Real-Time Data Endpoints

**File:** `chatbot/views.py` (Updated)

```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .models import Faculty, Student, Notification
from .chatbot_logic import ERPChatbot
from .permissions import AccessControl
from .data_service import StudentDataService
from .decorators import check_chatbot_access, check_student_access

# ==================== AUTHENTICATION ====================

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Faculty login endpoint"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    from django.contrib.auth import authenticate
    user = authenticate(username=username, password=password)
    
    if user:
        return Response({
            'faculty_id': user.id,
            'name': user.name,
            'role': user.role,
            'email': user.email
        })
    
    return Response({'error': 'Invalid credentials'}, status=401)

# ==================== CHATBOT ENDPOINTS ====================

class ChatView(APIView):
    """Enhanced chat endpoint with real-time data"""
    
    def post(self, request):
        """
        POST /api/chat/
        
        Request:
        {
            "faculty_id": 1,
            "query": "Show marks of student 101"
        }
        
        Response:
        {
            "response": "...",
            "timestamp": "2026-01-22T10:30:00Z"
        }
        """
        query = request.data.get('query')
        faculty_id = request.data.get('faculty_id')
        
        if not query or not faculty_id:
            return Response(
                {'error': 'Missing query or faculty_id'},
                status=400
            )
        
        try:
            faculty = Faculty.objects.get(id=faculty_id)
        except Faculty.DoesNotExist:
            return Response({'error': 'Faculty not found'}, status=404)
        
        # Process query with real-time data
        chatbot = ERPChatbot()
        response_text = chatbot.process_query(query, faculty_id)
        
        from django.utils import timezone
        
        return Response({
            'response': response_text,
            'timestamp': timezone.now().isoformat(),
            'faculty_role': faculty.role
        })

# ==================== DATA QUERY ENDPOINTS ====================

class StudentDataView(APIView):
    """Real-time student data endpoint"""
    
    def get(self, request):
        """
        GET /api/student-data/?faculty_id=1&student_id=101&type=all
        
        Types: all, marks, attendance, performance, info
        """
        faculty_id = request.query_params.get('faculty_id')
        student_id = request.query_params.get('student_id')
        data_type = request.query_params.get('type', 'all')
        
        if not faculty_id or not student_id:
            return Response({'error': 'Missing parameters'}, status=400)
        
        try:
            faculty = Faculty.objects.get(id=faculty_id)
        except Faculty.DoesNotExist:
            return Response({'error': 'Faculty not found'}, status=404)
        
        if not AccessControl.can_view_student(faculty, student_id):
            return Response({'error': 'Access Denied'}, status=403)
        
        service = StudentDataService()
        
        data = {}
        
        if data_type in ['all', 'info']:
            data['info'] = service.get_student_basic_info(student_id, faculty)
        
        if data_type in ['all', 'marks']:
            data['marks'] = service.get_student_marks(student_id, faculty)
        
        if data_type in ['all', 'attendance']:
            data['attendance'] = service.get_student_attendance(student_id, faculty)
        
        if data_type in ['all', 'performance']:
            data['performance'] = service.get_student_performance(student_id, faculty)
        
        from django.utils import timezone
        data['query_timestamp'] = timezone.now().isoformat()
        data['note'] = 'Data is real-time and pulled directly from database'
        
        return Response(data)

class ClassDataView(APIView):
    """Real-time class analysis endpoint"""
    
    def get(self, request):
        """
        GET /api/class-data/?faculty_id=1&subject_id=PHY101
        """
        faculty_id = request.query_params.get('faculty_id')
        subject_id = request.query_params.get('subject_id')
        
        if not faculty_id or not subject_id:
            return Response({'error': 'Missing parameters'}, status=400)
        
        try:
            faculty = Faculty.objects.get(id=faculty_id)
        except Faculty.DoesNotExist:
            return Response({'error': 'Faculty not found'}, status=404)
        
        from .data_service import ClassDataService
        service = ClassDataService()
        
        analysis = service.get_subject_class_performance(faculty, subject_id)
        
        if 'error' in analysis:
            return Response(analysis, status=403)
        
        from django.utils import timezone
        analysis['query_timestamp'] = timezone.now().isoformat()
        
        return Response(analysis)

class AlertsView(APIView):
    """Real-time alerts endpoint"""
    
    def get(self, request):
        """
        GET /api/alerts/?faculty_id=1
        """
        faculty_id = request.query_params.get('faculty_id')
        
        if not faculty_id:
            return Response({'error': 'Missing faculty_id'}, status=400)
        
        try:
            faculty = Faculty.objects.get(id=faculty_id)
        except Faculty.DoesNotExist:
            return Response({'error': 'Faculty not found'}, status=404)
        
        from .data_service import NotificationService
        service = NotificationService()
        
        alerts = service.get_alerts_for_faculty(faculty)
        
        from django.utils import timezone
        return Response({
            'alerts': alerts,
            'count': len(alerts),
            'timestamp': timezone.now().isoformat()
        })

# ==================== NOTIFICATION ENDPOINTS ====================

class NotificationView(APIView):
    """Notification management"""
    
    def get(self, request):
        """GET /api/notifications/?faculty_id=1"""
        faculty_id = request.query_params.get('faculty_id')
        
        if not faculty_id:
            return Response({'error': 'Missing faculty_id'}, status=400)
        
        notifications = Notification.objects.filter(
            receiver_id=faculty_id,
            is_read=False
        ).select_related('sender', 'student')[:20]
        
        from django.utils import timezone
        
        data = []
        for n in notifications:
            local_time = timezone.localtime(n.created_at)
            data.append({
                'id': n.id,
                'sender_name': n.sender.name,
                'student_name': n.student.name if n.student else 'General',
                'message': n.message,
                'timestamp': local_time.strftime("%I:%M %p | %m/%d/%Y")
            })
        
        return Response(data)
    
    def post(self, request):
        """POST /api/notifications/ - Mark as read"""
        notification_ids = request.data.get('ids', [])
        
        Notification.objects.filter(
            id__in=notification_ids
        ).update(is_read=True, read_at=timezone.now())
        
        from django.utils import timezone
        return Response({
            'status': 'success',
            'updated': len(notification_ids),
            'timestamp': timezone.now().isoformat()
        })
```

### 6.2 Update URL Configuration

**File:** `erp_backend/urls.py` (Updated)

```python
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from chatbot import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Frontend Routes
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('index.html', TemplateView.as_view(template_name='index.html')),
    path('portal.html', TemplateView.as_view(template_name='portal.html'), name='portal'),
    path('dashboard.html', TemplateView.as_view(template_name='dashboard.html')),
    
    # API Routes - Authentication
    path('api/login/', views.login_view, name='login'),
    
    # API Routes - Chatbot (Real-Time)
    path('api/chat/', views.ChatView.as_view(), name='chatbot'),
    
    # API Routes - Data Queries (Real-Time)
    path('api/student-data/', views.StudentDataView.as_view(), name='student_data'),
    path('api/class-data/', views.ClassDataView.as_view(), name='class_data'),
    path('api/alerts/', views.AlertsView.as_view(), name='alerts'),
    
    # API Routes - Notifications
    path('api/notifications/', views.NotificationView.as_view(), name='notifications'),
    path('api/notifications/read/', views.NotificationView.as_view(), name='notifications_read'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

---

## Phase 7: Implementation Checklist & Security Considerations

### 7.1 Security Best Practices

#### Data Access
- ✅ **Role-Based Access Control (RBAC)** - Teachers only see their assigned students
- ✅ **Query-Time Validation** - Every data request validated against permissions
- ✅ **No Data Caching** - Fresh queries to DB every request
- ✅ **Audit Logging** - Log all data accesses

#### Data Protection
```python
# Example: Secure audit logging
class AuditLog(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT)
    action = models.CharField(max_length=100)
    student_id = models.CharField(max_length=50)  # Don't store full data
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    
    class Meta:
        db_table = 'audit_logs'
        indexes = [models.Index(fields=['faculty', '-timestamp'])]
```

#### API Security
```python
# Add throttling to prevent abuse
from rest_framework.throttling import UserRateThrottle

class CustomThrottle(UserRateThrottle):
    scope = 'chatbot'

# In settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
        'chatbot': '500/hour'
    }
}
```

### 7.2 Implementation Checklist

- [ ] **Phase 1:** Configure MySQL connection in Django settings
- [ ] **Phase 2:** Map existing MySQL tables to Django models
- [ ] **Phase 3:** Implement AccessControl and permission layer
- [ ] **Phase 4:** Create DataService classes for real-time queries
- [ ] **Phase 5:** Refactor chatbot logic to use real-time queries
- [ ] **Phase 6:** Create/Update API endpoints
- [ ] **Test 1:** Verify database connection
- [ ] **Test 2:** Test permission checks with different roles
- [ ] **Test 3:** Test real-time data retrieval and updates
- [ ] **Test 4:** Test API endpoints with sample requests
- [ ] **Test 5:** Performance testing (query response times)
- [ ] **Deployment 1:** Set up environment variables on server
- [ ] **Deployment 2:** Run migrations
- [ ] **Deployment 3:** Configure SSL/TLS for HTTPS

---

## Phase 8: Frontend Integration Example

### 8.1 Sample Frontend JavaScript

```javascript
// Example: Calling chatbot API from frontend
class ChatbotClient {
    constructor(baseUrl = '/api') {
        this.baseUrl = baseUrl;
        this.facultyId = null;
    }
    
    setFacultyId(id) {
        this.facultyId = id;
    }
    
    async sendQuery(query) {
        const response = await fetch(`${this.baseUrl}/chat/`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                faculty_id: this.facultyId,
                query: query
            })
        });
        
        const data = await response.json();
        
        // Data is REAL-TIME - no stale cache
        console.log('Response Timestamp:', data.timestamp);
        console.log('Data:', data.response);
        
        return data;
    }
    
    async getStudentData(studentId, dataType = 'all') {
        const response = await fetch(
            `${this.baseUrl}/student-data/?faculty_id=${this.facultyId}&student_id=${studentId}&type=${dataType}`
        );
        
        const data = await response.json();
        console.log('Query Timestamp:', data.query_timestamp);
        console.log('Note:', data.note); // "Data is real-time..."
        
        return data;
    }
}

// Usage
const chatbot = new ChatbotClient();
chatbot.setFacultyId(1);

// Query 1: Get real-time marks
await chatbot.sendQuery('Show marks of student 101');

// Query 2: Get real-time attendance
await chatbot.sendQuery('Attendance of 102');

// Query 3: Get alerts
await chatbot.sendQuery('Show alerts');
```

---

## Phase 9: Monitoring & Maintenance

### 9.1 Query Performance Monitoring

```python
# In settings.py - Enable query logging in development
if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        },
    }
```

### 9.2 Database Indexing Strategy

```python
# Ensure these indexes exist for fast queries:

class Meta:
    indexes = [
        models.Index(fields=['registration_number']),
        models.Index(fields=['department', 'year']),
        models.Index(fields=['student', 'subject']),
        models.Index(fields=['faculty', 'subject']),
        models.Index(fields=['date']),
        models.Index(fields=['receiver', '-created_at']),
    ]
```

---

## Summary Table: Query→Database Mapping

| Feature | Query | Database Table | Real-Time? | Cached? |
|---------|-------|-----------------|-----------|---------|
| Student Marks | "Show marks of 101" | `marks` | ✅ Yes | ❌ No |
| Attendance | "Attendance of 101" | `attendance` | ✅ Yes | ❌ No |
| Performance | "CGPA of 101" | `student_performance` | ✅ Yes | ❌ No |
| Class Report | "Class report for Math" | `marks` (aggregated) | ✅ Yes | ❌ No |
| Alerts | "Show alerts" | Multiple + `student_performance` | ✅ Yes | ❌ No |
| Student Info | "Student 101 info" | `students` | ✅ Yes | ❌ No |

---

## Next Steps After Plan Approval

1. **Environment Setup** - Install MySQL driver, configure .env
2. **Database Migration** - Migrate from SQLite to MySQL
3. **Model Updates** - Update Django models to match existing tables
4. **Permission Layer** - Implement AccessControl
5. **Data Service** - Create data retrieval layer
6. **Chatbot Refactor** - Update chatbot logic with real-time queries
7. **API Development** - Create/update endpoints
8. **Testing** - Unit, integration, and performance testing
9. **Deployment** - Configure production settings

---

**Document Status:** Draft - Awaiting Implementation  
**Maintained By:** Chatbot Development Team  
**Last Updated:** January 22, 2026
