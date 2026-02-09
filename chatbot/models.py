from django.db import models
from django.contrib.auth.models import AbstractUser

class Faculty(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Vice Principal', 'Vice Principal'),
        ('Advisor', 'Advisor'),
        ('Mentor', 'Mentor'),
        ('Teacher', 'Teacher'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.role})"

class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    year = models.IntegerField()
    gender = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} ({self.id})"

class Mentorship(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='mentees')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='mentors')

    class Meta:
        unique_together = ('faculty', 'student')

class ClassAdvisorship(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='advised_classes')
    department = models.CharField(max_length=50)
    year = models.IntegerField()

    class Meta:
        unique_together = ('faculty', 'department', 'year')

class SubjectAllocation(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='allocated_subjects')
    subject = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    year = models.IntegerField()

class StudentDashboardStats(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='dashboard_stats')
    projects = models.IntegerField(default=0)
    achievements = models.IntegerField(default=0)
    publications = models.IntegerField(default=0)
    co_curricular = models.IntegerField(default=0)

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=20) # e.g., 'Present', 'Absent'

    class Meta:
        ordering = ['-date']

class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    subject = models.CharField(max_length=100)
    score = models.IntegerField()

class Notification(models.Model):
    sender = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='sent_notifications')
    receiver = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='received_notifications')
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

# Placeholders for missing models to be provided by user
class Add_Department(models.Model):
    Department = models.CharField(db_column='Department', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_accounts_add_department'

    def __str__(self):
        return self.Department or "No Dept"

class Regulations(models.Model):
    year = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'course_management_regulations'

    def __str__(self):
        return self.year or "Unnamed Regulation"

class Course_category(models.Model):
    course_category_name = models.CharField(db_column='Course_category_name', max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_management_course_category'

    def __str__(self):
        return self.course_category_name or "Unnamed Category"

class Degree(models.Model):
    degree = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_accounts_degree'

    def __str__(self):
        return self.degree or "Unnamed Degree"

class InternalAssessment(models.Model):
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE, null=True, blank=True)
    iat = models.CharField(max_length=50, null=True, blank=True, help_text="E.g. iat1, iat2 or IAT1")

    class Meta:
        managed = False
        db_table = 'examination_management_internalassessment'
        constraints = [
            models.UniqueConstraint(fields=["degree", "iat"], name="uniq_degree_iat_erp")
        ]
        ordering = ["degree", "iat"]

    def __str__(self):
        deg = getattr(self.degree, "degree", None) or "-"
        return f"{deg} : {self.iat or 'Unspecified'}"

class Course(models.Model):
    department = models.ForeignKey(
        Add_Department,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="courses"
    )
    course_code = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    regulation = models.ForeignKey(Regulations, on_delete=models.CASCADE, null=True, blank=True) 
    year = models.CharField(max_length=10, null=True, blank=True)
    semester = models.CharField(max_length=10, null=True, blank=True)
    elective = models.ForeignKey(Course_category, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = "course_management_course"
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ['course_code']

    def __str__(self):
        dept_name = self.department.Department if self.department else "No Dept"
        return f"{self.course_code or 'N/A'} - {self.title or 'No Title'} ({dept_name})"

class CourseEnrollment(models.Model):
    department = models.ForeignKey(Add_Department, on_delete=models.SET_NULL, null=True, blank=True)
    faculty = models.ForeignKey("FacultyManagementGeneralInformation", on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey("StudentDetails", on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    batch = models.CharField(max_length=200, null=True, blank=True)
    section = models.CharField(max_length=100, null=True, blank=True)
    enrollment_date = models.DateField(null=True, blank=True)
    regulation = models.ForeignKey(Regulations, on_delete=models.CASCADE, null=True, blank=True)
    enroll = models.IntegerField(default=0)  # Changed to Integer to match ERP
    is_open_elective = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'course_management_courseenrollment'

class AssignSubjectFaculty(models.Model):
    department = models.ForeignKey(Add_Department, on_delete=models.SET_NULL, null=True, blank=True)
    faculty = models.ForeignKey("FacultyManagementGeneralInformation", on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name="course_assign")
    regulation = models.ForeignKey(Regulations, on_delete=models.CASCADE, null=True, blank=True)
    batch = models.CharField(max_length=200, null=True, blank=True)
    section = models.CharField(max_length=100, null=True, blank=True)
    reason = models.CharField(max_length=500, null=True, blank=True)
    academic_year = models.CharField(max_length=9, null=True, blank=True)
    is_active = models.IntegerField(default=1)

    class Meta:
        managed = False
        db_table = 'course_management_assignsubjectfaculty'

class StudentDetails(models.Model):
    aadhar_number = models.CharField(max_length=12, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    reg_no = models.CharField(max_length=255, unique=True, null=True, blank=True)
    department = models.ForeignKey(Add_Department, on_delete=models.CASCADE, null=True, blank=True)
    regulation = models.CharField(max_length=50, null=True, blank=True)
    batch = models.CharField(max_length=50, null=True, blank=True)
    year = models.CharField(max_length=50, null=True, blank=True)
    semester = models.CharField(max_length=50, null=True, blank=True)
    umis_id = models.CharField(max_length=50, null=True, blank=True)
    section = models.CharField(max_length=10, null=True, blank=True)
    profile_img = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    mobile_no = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    ca_id = models.CharField(max_length=50, null=True, blank=True)
    mentor_id = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'user_accounts_studentdetails'

class CourseOutcome(models.Model):
    co_name = models.CharField(max_length=255, null=True, blank=True)
    co_code = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'examination_management_courseoutcome'

    def __str__(self):
        return self.co_name or "Unnamed Course Outcome"

class BloomsLevel(models.Model):
    level_code = models.CharField(max_length=10, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'examination_management_bloomslevel'

    def __str__(self):
        return self.level_code or "Unnamed Bloom's Level"

class Assessments(models.Model):
    assessment_name = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        managed = False
        db_table = 'examination_management_assessments'

    def __str__(self):
        return self.assessment_name or "Unnamed Assessment Type"

class Assessment_master(models.Model):
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE,null=True,blank=True,) 
    department = models.ForeignKey(Add_Department, on_delete=models.CASCADE,null=True,blank=True,) 
    regulation = models.ForeignKey(Regulations, on_delete=models.CASCADE,null=True,blank=True,) 
    semester = models.CharField(max_length=100, null=True, blank=True) 
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="assignments_by_name") 
    module = models.CharField(max_length=100, null=True, blank=True) 
    internal_assessment = models.ForeignKey(InternalAssessment,on_delete=models.SET_NULL,null=True, blank=True,related_name="assessment_masters")
    
    faculty_id = models.CharField(max_length=100, null=True, blank=True) 
    weightage = models.CharField(max_length=100, null=True, blank=True) 
    co_code = models.ForeignKey(CourseOutcome, on_delete=models.CASCADE,null=True,blank=True,) 
    level_code = models.ForeignKey(BloomsLevel, on_delete=models.CASCADE,null=True,blank=True,)
    assessment = models.ForeignKey(
        Assessments,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="assessment_masters",
    )
    # Match ERP casing
    Assessmentname = models.CharField(db_column='Assessmentname', max_length=255, null=True, blank=True)
    customAssessmentname = models.CharField(db_column='customAssessmentname', max_length=255, null=True, blank=True)
    Maxmarks = models.IntegerField(db_column='Maxmarks', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'faculty_management_assessment_master'

    def __str__(self):
        return self.Assessmentname or "Unnamed Assessment Master"

class AssessmentMark(models.Model):
    assignment = models.ForeignKey(
        AssignSubjectFaculty,
        on_delete=models.CASCADE,
        related_name="marks",
        null=True, blank=True
    )
    assessment = models.ForeignKey(
        Assessment_master,
        on_delete=models.CASCADE,
        related_name="marks",
        null=True, blank=True
    )
    student = models.ForeignKey(
        StudentDetails,
        on_delete=models.CASCADE,
        related_name="assessment_marks",
        null=True, blank=True
    )
    marks_raw = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    marks_weighted = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    marks = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    remarks = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField() # auto_now_add removed to match ERP
    updated_at = models.DateTimeField() # auto_now removed to match ERP

    class Meta:
        managed = False
        db_table = 'faculty_management_assessmentmark'
        unique_together = (("assignment", "assessment", "student"),)

    def __str__(self):
        return f"{self.assignment_id} | A:{self.assessment_id} | S:{self.student_id} -> {self.marks_raw or self.marks}"

class FacultyManagementGeneralInformation(models.Model):
    id = models.BigAutoField(primary_key=True)
    faculty_id = models.IntegerField(blank=True, null=True) # Linked to Employee_id in approval system
    name = models.CharField(max_length=225, blank=True, null=True)
    personal_email = models.CharField(max_length=225, blank=True, null=True)
    college_email = models.CharField(max_length=225, blank=True, null=True)
    phone = models.BigIntegerField(blank=True, null=True)
    department = models.ForeignKey(Add_Department, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faculty_management_general_information'

    def __str__(self):
        return self.name or "Unnamed Faculty"

# --- Approval System / Control Room Models ---

class ControlRoomRole(models.Model):
    id = models.IntegerField(primary_key=True)
    role = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'control_room_role'
        app_label = 'chatbot'

class ControlRoomDepartment(models.Model):
    id = models.IntegerField(primary_key=True)
    department = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'control_room_department'
        app_label = 'chatbot'

class ControlRoomUser(models.Model):
    id = models.IntegerField(primary_key=True)
    Employee_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    role = models.ForeignKey(ControlRoomRole, on_delete=models.DO_NOTHING, db_column='role_id')
    department = models.ForeignKey(ControlRoomDepartment, on_delete=models.DO_NOTHING, db_column='Department_id', null=True)
    is_active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'control_room_user'
        app_label = 'chatbot'

# --- Dashboard & Performance Models ---

class StudentDashboardStats(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='dashboard_stats')
    gpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    achievements = models.IntegerField(default=0)
    co_curricular = models.IntegerField(default=0)
    publications = models.IntegerField(default=0)
    projects = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Student Dashboard Stats"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late')])
    subject = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Attendance"
