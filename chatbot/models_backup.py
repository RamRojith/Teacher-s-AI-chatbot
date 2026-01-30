from django.db import models
from django.contrib.auth.models import AbstractUser

class Faculty(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Advisor', 'Advisor'),
        ('Mentor', 'Mentor'),
        ('Teacher', 'Teacher'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
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
    Department = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.Department or "No Dept"

class Regulations(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name or "Unnamed Regulation"

class Course_category(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name or "Unnamed Category"

class Degree(models.Model):
    degree = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.degree or "Unnamed Degree"

class InternalAssessment(models.Model):
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE, null=True, blank=True)
    iat = models.CharField(max_length=50, null=True, blank=True, help_text="E.g. iat1, iat2 or IAT1")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["degree", "iat"], name="uniq_degree_iat")
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
        db_table = "course_management_course"
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ['course_code']

    def __str__(self):
        dept_name = self.department.Department if self.department else "No Dept"
        return f"{self.course_code or 'N/A'} - {self.title or 'No Title'} ({dept_name})"

class CourseEnrollment(models.Model):
    # department_id = models.IntegerField(null=True, blank=True)
    department = models.ForeignKey(Add_Department,on_delete=models.SET_NULL,
         null=True,
        blank=True,)
    # faculty_id = models.IntegerField(null=True, blank=True)
    # student_id = models.IntegerField(null=True, blank=True)
    faculty = models.ForeignKey("Faculty", on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey("StudentDetails", on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    batch = models.CharField(max_length=200, null=True, blank=True)
    section = models.CharField(max_length=100, null=True, blank=True)
    enrollment_date = models.DateField(null=True, blank=True)
    regulation = models.ForeignKey(Regulations, on_delete=models.CASCADE, null=True, blank=True)
    enroll = models.BooleanField(default=False)  # False = Unenrolled, True = Enrolled
    is_open_elective = models.BooleanField(default=False, null=True, blank=True)

class AssignSubjectFaculty(models.Model):
    REASON_CHOICES = [
        "Preference from the faculty members",
        "Consideration of specialization of the faculty members",
        "Analyzing the efficiency of the faculty member in handling same subject in previous semesters/ similar subjects.",
        "Feedback from the students",
        "If a Particular subject is not chosen by any one, the HOD allocates it to the senior faculty member with the corresponding specialization or to someone he thinks can do honest effort in handling the subject by undergoing any FDP in that area.",
        "Other",  # UI trigger for custom text
    ]

    department = models.ForeignKey(Add_Department, on_delete=models.SET_NULL, null=True, blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name="course_assign")
    regulation = models.ForeignKey(Regulations, on_delete=models.CASCADE, null=True, blank=True)
    batch = models.CharField(max_length=200, null=True, blank=True)
    section = models.CharField(max_length=100, null=True, blank=True)
    reason = models.CharField(max_length=500, null=True, blank=True)
    academic_year = models.CharField(max_length=9, null=True, blank=True)  # e.g., 2024-2025
    is_active = models.BooleanField(default=True)

class StudentDetails(models.Model):
    aadhar_number = models.CharField(
        max_length=12,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Aadhar Number"
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    reg_no = models.CharField(max_length=255, unique=True, null=True, blank=True, verbose_name="Register Number")
    department = models.ForeignKey(Add_Department, on_delete=models.CASCADE, null=True, blank=True)
    regulation = models.CharField(max_length=50, null=True, blank=True)
    batch = models.CharField(max_length=50, null=True, blank=True)
    year = models.CharField(max_length=50, null=True, blank=True)
    semester = models.CharField(max_length=50, null=True, blank=True)
    umis_id = models.CharField(max_length=50, null=True, blank=True)
    section = models.CharField(max_length=10, null=True, blank=True)
    profile_img = models.ImageField(upload_to="student_profiles_photos/", null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    mobile_no = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True, choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ])

class CourseOutcome(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name or "Unnamed Course Outcome"

class BloomsLevel(models.Model):
    level = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.level or "Unnamed Bloom's Level"

class Assessments(models.Model):
    assessment_name = models.CharField(max_length=100, null=True, blank=True, unique=True)
    
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

    # assessment_name = models.ForeignKey('examination_management.Assessments', on_delete=models.CASCADE, to_field='assessment_name', db_column='assessment_name', related_name='assessment_names')
    
    faculty_id = models.CharField(max_length=100, null=True, blank=True) 
    weightage = models.CharField(max_length=100, null=True, blank=True) 
    co_code = models.ForeignKey(CourseOutcome, on_delete=models.CASCADE,null=True,blank=True,) 
    level_code = models.ForeignKey(BloomsLevel, on_delete=models.CASCADE,null=True,blank=True,)
    assessment = models.ForeignKey(
        Assessments,
        on_delete=models.CASCADE,
        null=True, blank=True,
         # keep DB constraint disabled if that’s your convention
        related_name="assessment_masters",
    )
    # Cached fields for display/reporting
    Assessmentname = models.CharField(max_length=255, null=True, blank=True)
    customAssessmentname = models.CharField(max_length=255, null=True, blank=True)
    Maxmarks = models.IntegerField(null=True, blank=True)

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

    # teacher-entered raw mark (what they type into the form)
    marks_raw = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    # computed weighted contribution (same units as your weight system — e.g. out of 70)
    marks_weighted = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)

    # legacy / compatibility column (optional)
    marks = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    remarks = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("assignment", "assessment", "student")

    def __str__(self):
        return f"{self.assignment_id} | A:{self.assessment_id} | S:{self.student_id} -> {self.marks_raw or self.marks}"

