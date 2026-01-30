# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Academicdetails(models.Model):
    id = models.BigAutoField(primary_key=True)
    counsellingapplicationno = models.CharField(db_column='CounsellingApplicationNo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    gqadmissionnumber = models.CharField(db_column='GQAdmissionNumber', max_length=255, blank=True, null=True)  # Field name made lowercase.
    counsellinggeneralrank = models.CharField(db_column='CounsellingGeneralRank', max_length=255, blank=True, null=True)  # Field name made lowercase.
    scholarship = models.CharField(db_column='ScholarShip', max_length=255, blank=True, null=True)  # Field name made lowercase.
    firstgraduatecertificateno = models.CharField(db_column='FirstGraduateCertificateNo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    govper = models.CharField(db_column='GovPer', max_length=255, blank=True, null=True)  # Field name made lowercase.
    occupation = models.CharField(db_column='Occupation', max_length=255)  # Field name made lowercase.
    jobdetails = models.CharField(db_column='JobDetails', max_length=255)  # Field name made lowercase.
    annualincome = models.CharField(db_column='AnnualIncome', max_length=255)  # Field name made lowercase.
    nameofthebank = models.CharField(db_column='NameOfTheBank', max_length=255)  # Field name made lowercase.
    branchnameofthebank = models.CharField(db_column='BranchNameOfTheBank', max_length=255)  # Field name made lowercase.
    branchcodeno = models.CharField(db_column='BranchCodeNo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ifsc = models.CharField(db_column='IFSC', max_length=255)  # Field name made lowercase.
    micr = models.CharField(db_column='MICR', max_length=255)  # Field name made lowercase.
    accountholdername = models.CharField(db_column='AccountHolderName', max_length=255)  # Field name made lowercase.
    accountno = models.CharField(db_column='AccountNo', max_length=255)  # Field name made lowercase.
    how = models.CharField(db_column='How', max_length=255)  # Field name made lowercase.
    dateadmission = models.DateTimeField(db_column='DateAdmission')  # Field name made lowercase.
    admissioncategory = models.CharField(db_column='AdmissionCategory', max_length=255, blank=True, null=True)  # Field name made lowercase.
    academicyear = models.CharField(db_column='AcademicYear', max_length=255, blank=True, null=True)  # Field name made lowercase.
    admissionrecordsid = models.IntegerField(db_column='AdmissionRecordsId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'academicdetails'


class ApprovalManagementDegreeApproval(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    approver = models.ForeignKey('FacultyManagementGeneralInformation', models.DO_NOTHING, blank=True, null=True)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)
    role_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'approval_management_degree_approval'
        unique_together = (('role_id', 'department'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CourseManagementAssignsubjectfaculty(models.Model):
    id = models.BigAutoField(primary_key=True)
    batch = models.CharField(max_length=200, blank=True, null=True)
    section = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.IntegerField()
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)
    faculty = models.ForeignKey('FacultyManagementGeneralInformation', models.DO_NOTHING, blank=True, null=True)
    course = models.ForeignKey('CourseManagementCourse', models.DO_NOTHING, blank=True, null=True)
    regulation = models.ForeignKey('CourseManagementRegulations', models.DO_NOTHING, blank=True, null=True)
    reason = models.CharField(max_length=500, blank=True, null=True)
    academic_year = models.CharField(max_length=9, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_management_assignsubjectfaculty'


class CourseManagementCaassign(models.Model):
    id = models.BigAutoField(primary_key=True)
    reg_no = models.CharField(max_length=50, blank=True, null=True)
    batch = models.CharField(max_length=200, blank=True, null=True)
    section = models.CharField(max_length=100, blank=True, null=True)
    ca_id = models.BigIntegerField(blank=True, null=True)
    department_id = models.BigIntegerField()
    student_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_management_caassign'


class CourseManagementCourse(models.Model):
    id = models.BigAutoField(primary_key=True)
    course_code = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    year = models.CharField(max_length=10, blank=True, null=True)
    semester = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.IntegerField()
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)
    elective = models.ForeignKey('CourseManagementCourseCategory', models.DO_NOTHING, blank=True, null=True)
    regulation = models.ForeignKey('CourseManagementRegulations', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_management_course'


class CourseManagementCourseCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    course_category_name = models.CharField(db_column='Course_category_name', max_length=25, blank=True, null=True)  # Field name made lowercase.
    regulation = models.ForeignKey('CourseManagementRegulations', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_management_course_category'


class CourseManagementCourseandexaminationfunction(models.Model):
    id = models.BigAutoField(primary_key=True)
    function = models.CharField(max_length=500)
    permission = models.IntegerField()
    role_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'course_management_courseandexaminationfunction'


class CourseManagementCourseenrollment(models.Model):
    id = models.BigAutoField(primary_key=True)
    batch = models.CharField(max_length=200, blank=True, null=True)
    section = models.CharField(max_length=100, blank=True, null=True)
    enrollment_date = models.DateField(blank=True, null=True)
    enroll = models.IntegerField()
    course = models.ForeignKey(CourseManagementCourse, models.DO_NOTHING, blank=True, null=True)
    regulation = models.ForeignKey('CourseManagementRegulations', models.DO_NOTHING, blank=True, null=True)
    faculty = models.ForeignKey('FacultyManagementGeneralInformation', models.DO_NOTHING, blank=True, null=True)
    student = models.ForeignKey('UserAccountsStudentdetails', models.DO_NOTHING, blank=True, null=True)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)
    is_open_elective = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_management_courseenrollment'


class CourseManagementCoursehours(models.Model):
    id = models.BigAutoField(primary_key=True)
    leture_hpwk = models.CharField(max_length=15, blank=True, null=True)
    leture_npwk = models.CharField(max_length=15, blank=True, null=True)
    tutorial_hpwk = models.CharField(max_length=15, blank=True, null=True)
    tutorial_npwk = models.CharField(max_length=15, blank=True, null=True)
    laboratory_hpwk = models.CharField(max_length=15, blank=True, null=True)
    laboratory_npwk = models.CharField(max_length=15, blank=True, null=True)
    total_hours = models.CharField(max_length=15, blank=True, null=True)
    credits = models.CharField(max_length=15, blank=True, null=True)
    course = models.ForeignKey(CourseManagementCourse, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'course_management_coursehours'


class CourseManagementCourseplan(models.Model):
    id = models.BigAutoField(primary_key=True)
    academic_year = models.CharField(max_length=9, blank=True, null=True)
    unit_module_no = models.CharField(max_length=50, blank=True, null=True)
    co_no = models.CharField(max_length=50, blank=True, null=True)
    delivery_method = models.CharField(max_length=100, blank=True, null=True)
    topic = models.TextField(blank=True, null=True)
    content_beyond_syllabus = models.TextField(blank=True, null=True)
    innovative_practice = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    course = models.ForeignKey(CourseManagementCourse, models.DO_NOTHING, blank=True, null=True)
    faculty = models.ForeignKey('FacultyManagementGeneralInformation', models.DO_NOTHING, blank=True, null=True)
    faculty_department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)
    period_no = models.CharField(max_length=50, blank=True, null=True)
    justify = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_management_courseplan'


class CourseManagementFacultysubjectwillingness(models.Model):
    id = models.BigAutoField(primary_key=True)
    year = models.CharField(max_length=10, blank=True, null=True)
    semester = models.CharField(max_length=10, blank=True, null=True)
    academic_year = models.CharField(max_length=9, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    course = models.ForeignKey(CourseManagementCourse, models.DO_NOTHING, blank=True, null=True)
    degree = models.ForeignKey('UserAccountsDegree', models.DO_NOTHING, blank=True, null=True)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)
    faculty = models.ForeignKey('FacultyManagementGeneralInformation', models.DO_NOTHING, blank=True, null=True)
    regulation = models.ForeignKey('CourseManagementRegulations', models.DO_NOTHING, blank=True, null=True)
    status = models.CharField(max_length=20)
    section = models.CharField(max_length=100, blank=True, null=True)
    batch = models.CharField(max_length=200, blank=True, null=True)
    no_of_time_handled = models.CharField(db_column='No_of_time_handled', max_length=200, blank=True, null=True)  # Field name made lowercase.
    no_of_time_handled_in_rit = models.CharField(db_column='No_of_time_handled_in_RIT', max_length=200, blank=True, null=True)  # Field name made lowercase.
    pass_percentage_obtained = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_management_facultysubjectwillingness'


class CourseManagementMentorassign(models.Model):
    id = models.BigAutoField(primary_key=True)
    batch = models.CharField(max_length=200, blank=True, null=True)
    section = models.CharField(max_length=100, blank=True, null=True)
    reg_no = models.CharField(max_length=50, blank=True, null=True)
    department_id = models.BigIntegerField()
    mentor_id = models.BigIntegerField(blank=True, null=True)
    student_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_management_mentorassign'


class CourseManagementPassoutstudents(models.Model):
    id = models.BigAutoField(primary_key=True)
    year_of_passing = models.IntegerField()
    certificate_number = models.CharField(max_length=100, blank=True, null=True)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)
    conduct = models.CharField(max_length=20, blank=True, null=True)
    qualified_higher_class = models.CharField(max_length=3, blank=True, null=True)
    reason_for_tc = models.CharField(max_length=255, blank=True, null=True)
    tc_requested_date = models.DateField(blank=True, null=True)
    student = models.ForeignKey('UserAccountsStudentdetails', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_management_passoutstudents'


class CourseManagementPeriodallocation(models.Model):
    id = models.BigAutoField(primary_key=True)
    section = models.CharField(max_length=1, blank=True, null=True)
    year = models.CharField(max_length=10)
    semester = models.CharField(max_length=10)
    day = models.CharField(max_length=30)
    first_period = models.CharField(max_length=200, blank=True, null=True)
    second_period = models.CharField(max_length=200, blank=True, null=True)
    third_period = models.CharField(max_length=200, blank=True, null=True)
    fourth_period = models.CharField(max_length=200, blank=True, null=True)
    fifth_period = models.CharField(max_length=200, blank=True, null=True)
    sixth_period = models.CharField(max_length=200, blank=True, null=True)
    seventh_period = models.CharField(max_length=200, blank=True, null=True)
    eighth_period = models.CharField(max_length=200, blank=True, null=True)
    nineth_period = models.CharField(max_length=200, blank=True, null=True)
    tenth_period = models.CharField(max_length=200, blank=True, null=True)
    department_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_management_periodallocation'


class CourseManagementRegulations(models.Model):
    id = models.BigAutoField(primary_key=True)
    year = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'course_management_regulations'


class CourseManagementSectionmaster(models.Model):
    id = models.BigAutoField(primary_key=True)
    section = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_management_sectionmaster'


class CourseManagementStudentleaveodapplication(models.Model):
    id = models.BigAutoField(primary_key=True)
    application_type = models.CharField(max_length=10)
    from_date = models.DateField()
    to_date = models.DateField()
    total_days = models.PositiveIntegerField()
    reason = models.TextField()
    proof_file = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    study_year = models.CharField(max_length=50, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    ca_id = models.BigIntegerField(blank=True, null=True)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)
    mentor_id = models.BigIntegerField(blank=True, null=True)
    student = models.ForeignKey('UserAccountsStudentdetails', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_management_studentleaveodapplication'


class CourseManagementSubjectrequest(models.Model):
    id = models.BigAutoField(primary_key=True)
    semester = models.CharField(max_length=10, blank=True, null=True)
    batch = models.CharField(max_length=200, blank=True, null=True)
    academic_year = models.CharField(max_length=9, blank=True, null=True)
    reason = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=10)
    requested_on = models.DateTimeField()
    is_active = models.IntegerField()
    course = models.ForeignKey(CourseManagementCourse, models.DO_NOTHING, blank=True, null=True)
    faculty = models.ForeignKey('FacultyManagementGeneralInformation', models.DO_NOTHING, blank=True, null=True)
    faculty_department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)
    regulation = models.ForeignKey(CourseManagementRegulations, models.DO_NOTHING, blank=True, null=True)
    requested_department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, related_name='coursemanagementsubjectrequest_requested_department_set', blank=True, null=True)
    section = models.CharField(max_length=100, blank=True, null=True)
    requested_to_department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, related_name='coursemanagementsubjectrequest_requested_to_department_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_management_subjectrequest'


class CourseManagementUpdatesemester(models.Model):
    id = models.BigAutoField(primary_key=True)
    register_number = models.CharField(max_length=100, blank=True, null=True)
    batch = models.CharField(max_length=100, blank=True, null=True)
    year = models.IntegerField()
    semester = models.IntegerField()
    regulation = models.CharField(max_length=100, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    section = models.CharField(max_length=100, blank=True, null=True)
    student_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'course_management_updatesemester'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ExaminationManagementAssessments(models.Model):
    id = models.BigAutoField(primary_key=True)
    assessment_name = models.CharField(max_length=255, blank=True, null=True)
    question_paper_required = models.IntegerField()
    degree = models.ForeignKey('UserAccountsDegree', models.DO_NOTHING, blank=True, null=True)
    internal_assessment = models.ForeignKey('ExaminationManagementInternalassessment', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'examination_management_assessments'


class ExaminationManagementAssessmentweightage(models.Model):
    id = models.BigAutoField(primary_key=True)
    selected_assessment_percentage = models.FloatField()
    activity_percentage = models.FloatField()
    created_at = models.DateTimeField()
    degree = models.ForeignKey('UserAccountsDegree', models.DO_NOTHING)
    regulation = models.ForeignKey(CourseManagementRegulations, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'examination_management_assessmentweightage'


class ExaminationManagementBloomslevel(models.Model):
    id = models.BigAutoField(primary_key=True)
    level_code = models.CharField(max_length=10, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'examination_management_bloomslevel'


class ExaminationManagementCourseoutcome(models.Model):
    id = models.BigAutoField(primary_key=True)
    regulation = models.CharField(max_length=50, blank=True, null=True)
    co_code = models.CharField(max_length=20, blank=True, null=True)
    co_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'examination_management_courseoutcome'


class ExaminationManagementExaminationfunction(models.Model):
    id = models.BigAutoField(primary_key=True)
    function = models.CharField(max_length=500)
    permission = models.IntegerField()
    role_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'examination_management_examinationfunction'


class ExaminationManagementExampattern(models.Model):
    id = models.BigAutoField(primary_key=True)
    year = models.CharField(max_length=10, blank=True, null=True)
    semester = models.CharField(max_length=10, blank=True, null=True)
    academic_year = models.CharField(max_length=9, blank=True, null=True)
    pattern = models.CharField(max_length=50, blank=True, null=True)
    for_exam = models.CharField(max_length=50, blank=True, null=True)
    degree = models.ForeignKey('UserAccountsDegree', models.DO_NOTHING, blank=True, null=True)
    regulation = models.ForeignKey(CourseManagementRegulations, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'examination_management_exampattern'


class ExaminationManagementExampatternsetting(models.Model):
    id = models.BigAutoField(primary_key=True)
    department_code = models.CharField(max_length=10)
    department_name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=20)
    course_title = models.CharField(max_length=200)
    batch = models.CharField(max_length=20, blank=True, null=True)
    section = models.CharField(max_length=10, blank=True, null=True)
    iat = models.CharField(max_length=50, blank=True, null=True)
    regulation_year = models.CharField(max_length=10)
    year = models.CharField(max_length=10)
    semester = models.CharField(max_length=10)
    academic_year = models.CharField(max_length=20)
    pattern = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'examination_management_exampatternsetting'
        unique_together = (('department_code', 'course_code', 'batch', 'section', 'iat'),)


class ExaminationManagementExperimentMarks(models.Model):
    id = models.BigAutoField(primary_key=True)
    work_program = models.PositiveSmallIntegerField()
    observation = models.PositiveSmallIntegerField()
    record = models.PositiveSmallIntegerField()
    total = models.PositiveSmallIntegerField()
    experiment_no = models.PositiveSmallIntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    co = models.ForeignKey(ExaminationManagementCourseoutcome, models.DO_NOTHING, blank=True, null=True)
    courses = models.ForeignKey(CourseManagementCourseenrollment, models.DO_NOTHING, blank=True, null=True)
    student = models.ForeignKey('UserAccountsStudentdetails', models.DO_NOTHING)
    assessment = models.ForeignKey('ExaminationManagementInternalassessment', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'examination_management_experiment_marks'


class ExaminationManagementFinalMarks(models.Model):
    id = models.BigAutoField(primary_key=True)
    co_marks = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    co_code = models.ForeignKey(ExaminationManagementCourseoutcome, models.DO_NOTHING, blank=True, null=True)
    student = models.ForeignKey('UserAccountsStudentdetails', models.DO_NOTHING, blank=True, null=True)
    exam = models.ForeignKey('ExaminationManagementStudentexam', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'examination_management_final_marks'


class ExaminationManagementGrademaster(models.Model):
    id = models.BigAutoField(primary_key=True)
    degree = models.CharField(max_length=255, blank=True, null=True)
    regulation = models.CharField(max_length=255, blank=True, null=True)
    grade_from = models.FloatField(blank=True, null=True)
    grade_to = models.FloatField(blank=True, null=True)
    class_category = models.CharField(max_length=255, blank=True, null=True)
    mark_from = models.IntegerField(blank=True, null=True)
    mark_to = models.IntegerField(blank=True, null=True)
    grade = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'examination_management_grademaster'


class ExaminationManagementInternalassessment(models.Model):
    id = models.BigAutoField(primary_key=True)
    iat = models.CharField(max_length=50, blank=True, null=True)
    degree = models.ForeignKey('UserAccountsDegree', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'examination_management_internalassessment'
        unique_together = (('degree', 'iat'),)


class ExaminationManagementModellab(models.Model):
    id = models.BigAutoField(primary_key=True)
    model_lab_name = models.CharField(max_length=255)
    degree = models.ForeignKey('UserAccountsDegree', models.DO_NOTHING, blank=True, null=True)
    internal_assessment = models.ForeignKey(ExaminationManagementInternalassessment, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'examination_management_modellab'
        unique_together = (('degree', 'model_lab_name'),)


class ExaminationManagementModellabmarks(models.Model):
    id = models.BigAutoField(primary_key=True)
    program = models.PositiveSmallIntegerField()
    viva = models.PositiveSmallIntegerField()
    total = models.PositiveSmallIntegerField()
    batch = models.CharField(max_length=20, blank=True, null=True)
    section = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    courses = models.ForeignKey(CourseManagementCourseenrollment, models.DO_NOTHING, blank=True, null=True)
    student = models.ForeignKey('UserAccountsStudentdetails', models.DO_NOTHING)
    internal_assessment = models.ForeignKey(ExaminationManagementInternalassessment, models.DO_NOTHING, blank=True, null=True)
    model_lab = models.ForeignKey(ExaminationManagementModellab, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'examination_management_modellabmarks'
        unique_together = (('student', 'courses', 'model_lab', 'internal_assessment', 'batch', 'section'),)


class ExaminationManagementOptionmarks(models.Model):
    id = models.BigAutoField(primary_key=True)
    option_letter = models.CharField(max_length=2)
    marks_i = models.PositiveIntegerField()
    marks_ii = models.PositiveIntegerField()
    blooms_level_i = models.ForeignKey(ExaminationManagementBloomslevel, models.DO_NOTHING, blank=True, null=True)
    blooms_level_ii = models.ForeignKey(ExaminationManagementBloomslevel, models.DO_NOTHING, related_name='examinationmanagementoptionmarks_blooms_level_ii_set', blank=True, null=True)
    course_outcome_i = models.ForeignKey(ExaminationManagementCourseoutcome, models.DO_NOTHING, blank=True, null=True)
    course_outcome_ii = models.ForeignKey(ExaminationManagementCourseoutcome, models.DO_NOTHING, related_name='examinationmanagementoptionmarks_course_outcome_ii_set', blank=True, null=True)
    question = models.ForeignKey('ExaminationManagementQuestion', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'examination_management_optionmarks'


class ExaminationManagementPart(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=1)
    total_questions = models.IntegerField()
    exam_pattern = models.ForeignKey(ExaminationManagementExampattern, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'examination_management_part'


class ExaminationManagementProgrammeoutcome(models.Model):
    id = models.BigAutoField(primary_key=True)
    regulation = models.CharField(max_length=50, blank=True, null=True)
    po_code = models.CharField(max_length=20, blank=True, null=True)
    po_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'examination_management_programmeoutcome'


class ExaminationManagementQuestion(models.Model):
    id = models.BigAutoField(primary_key=True)
    number = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField()
    part = models.ForeignKey(ExaminationManagementPart, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'examination_management_question'


class ExaminationManagementSquadmember(models.Model):
    id = models.BigAutoField(primary_key=True)
    appointment_ref = models.CharField(unique=True, max_length=100, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    facultyid = models.IntegerField(db_column='facultyId', blank=True, null=True)  # Field name made lowercase.
    designation = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    iat = models.CharField(max_length=3, blank=True, null=True)
    no_of_hall = models.PositiveIntegerField(blank=True, null=True)
    duration = models.CharField(max_length=2, blank=True, null=True)
    hall_numbers = models.CharField(max_length=200, blank=True, null=True)
    reported = models.CharField(max_length=20)
    semester = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'examination_management_squadmember'


class ExaminationManagementSquadmemberreport(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_filled = models.DateTimeField()
    seating_appropriate = models.IntegerField(blank=True, null=True)
    classrooms_clean = models.IntegerField(blank=True, null=True)
    seating_as_arrangement = models.IntegerField(blank=True, null=True)
    materials_distributed = models.IntegerField(blank=True, null=True)
    only_permitted_materials = models.IntegerField(blank=True, null=True)
    register_no_written = models.IntegerField(blank=True, null=True)
    no_markings_on_paper = models.IntegerField(blank=True, null=True)
    id_worn = models.IntegerField(blank=True, null=True)
    unruly_behaviour = models.IntegerField(blank=True, null=True)
    followed_rules = models.IntegerField(blank=True, null=True)
    faculty_present = models.IntegerField(blank=True, null=True)
    faculty_misconduct = models.IntegerField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    squad_member = models.OneToOneField(ExaminationManagementSquadmember, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'examination_management_squadmemberreport'


class ExaminationManagementStudentexam(models.Model):
    id = models.BigAutoField(primary_key=True)
    reg_no = models.CharField(max_length=20)
    student_name = models.CharField(max_length=100)
    department_code = models.CharField(max_length=20)
    department_name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=20)
    course_title = models.CharField(max_length=100)
    batch = models.CharField(max_length=20, blank=True, null=True)
    section = models.CharField(max_length=10, blank=True, null=True)
    exam_name = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField()
    pattern = models.ForeignKey(ExaminationManagementExampatternsetting, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'examination_management_studentexam'


class ExaminationManagementStudentinternalmark(models.Model):
    id = models.BigAutoField(primary_key=True)
    exam_name = models.CharField(max_length=50, blank=True, null=True)
    part_name = models.CharField(max_length=10, blank=True, null=True)
    question_number = models.CharField(max_length=10, blank=True, null=True)
    sub_question = models.CharField(max_length=10, blank=True, null=True)
    option_letter = models.CharField(max_length=5, blank=True, null=True)
    max_marks = models.PositiveIntegerField()
    marks_obtained = models.PositiveIntegerField()
    reg_no = models.CharField(max_length=20, blank=True, null=True)
    course_code = models.CharField(max_length=20, blank=True, null=True)
    batch = models.CharField(max_length=20, blank=True, null=True)
    section = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField()
    co_code = models.ForeignKey(ExaminationManagementCourseoutcome, models.DO_NOTHING, blank=True, null=True)
    enrollment = models.ForeignKey(CourseManagementCourseenrollment, models.DO_NOTHING, blank=True, null=True)
    level_code = models.ForeignKey(ExaminationManagementBloomslevel, models.DO_NOTHING, blank=True, null=True)
    pattern = models.ForeignKey(ExaminationManagementExampattern, models.DO_NOTHING, blank=True, null=True)
    student = models.ForeignKey('UserAccountsStudentdetails', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'examination_management_studentinternalmark'
        unique_together = (('student', 'enrollment', 'exam_name', 'part_name', 'question_number', 'sub_question', 'option_letter'),)


class ExaminationManagementStudentmark(models.Model):
    id = models.BigAutoField(primary_key=True)
    part_name = models.CharField(max_length=10, blank=True, null=True)
    question_number = models.CharField(max_length=10, blank=True, null=True)
    sub_question = models.CharField(max_length=10, blank=True, null=True)
    option_letter = models.CharField(max_length=5, blank=True, null=True)
    max_marks = models.PositiveIntegerField()
    marks_obtained = models.PositiveIntegerField()
    created_at = models.DateTimeField()
    co_code = models.ForeignKey(ExaminationManagementCourseoutcome, models.DO_NOTHING, blank=True, null=True)
    level_code = models.ForeignKey(ExaminationManagementBloomslevel, models.DO_NOTHING, blank=True, null=True)
    student_exam = models.ForeignKey(ExaminationManagementStudentexam, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'examination_management_studentmark'


class FacultyLeaveManagementAlteration(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    class_name = models.CharField(max_length=50, blank=True, null=True)
    hour = models.IntegerField(blank=True, null=True)
    faculty_altered_to = models.ForeignKey('FacultyManagementGeneralInformation', models.DO_NOTHING, blank=True, null=True)
    leave_application = models.ForeignKey('FacultyLeaveManagementLeaveapplication', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faculty_leave_management_alteration'


class FacultyLeaveManagementLeaveallotment(models.Model):
    id = models.BigAutoField(primary_key=True)
    academic_year = models.CharField(max_length=10, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    default_allotment = models.IntegerField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    role = models.ForeignKey('FacultyManagementDesignationmaster', models.DO_NOTHING, blank=True, null=True)
    leave_type = models.ForeignKey('FacultyLeaveManagementLeavetype', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faculty_leave_management_leaveallotment'
        unique_together = (('academic_year', 'role', 'leave_type'),)


class FacultyLeaveManagementLeaveapplication(models.Model):
    id = models.BigAutoField(primary_key=True)
    academic_year = models.CharField(max_length=10, blank=True, null=True)
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    requested_date = models.DateTimeField(blank=True, null=True)
    role = models.ForeignKey('FacultyManagementDesignationmaster', models.DO_NOTHING, blank=True, null=True)
    user_id = models.BigIntegerField(blank=True, null=True)
    leave_type = models.ForeignKey('FacultyLeaveManagementLeavetype', models.DO_NOTHING, blank=True, null=True)
    faculty = models.ForeignKey('FacultyManagementGeneralInformation', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faculty_leave_management_leaveapplication'


class FacultyLeaveManagementLeaveapprovers(models.Model):
    id = models.BigAutoField(primary_key=True)
    approver_level = models.PositiveIntegerField()
    is_cross_department_approver = models.CharField(max_length=3, blank=True, null=True)
    approver_department_id = models.BigIntegerField(blank=True, null=True)
    approver_role_id = models.BigIntegerField(blank=True, null=True)
    creator_role_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faculty_leave_management_leaveapprovers'


class FacultyLeaveManagementLeaveapproversdata(models.Model):
    id = models.BigAutoField(primary_key=True)
    reason = models.CharField(max_length=225, blank=True, null=True)
    status = models.CharField(max_length=16, blank=True, null=True)
    approver_level = models.PositiveIntegerField(blank=True, null=True)
    approved_date = models.DateTimeField(blank=True, null=True)
    approver_id_id = models.BigIntegerField(blank=True, null=True)
    creator_id_id = models.BigIntegerField(blank=True, null=True)
    leave_application = models.ForeignKey(FacultyLeaveManagementLeaveapplication, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faculty_leave_management_leaveapproversdata'


class FacultyLeaveManagementLeavebalance(models.Model):
    id = models.BigAutoField(primary_key=True)
    academic_year = models.CharField(max_length=10, blank=True, null=True)
    available = models.IntegerField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    used = models.IntegerField(blank=True, null=True)
    designation = models.ForeignKey('FacultyManagementDesignationmaster', models.DO_NOTHING, blank=True, null=True)
    user_id = models.BigIntegerField(blank=True, null=True)
    leave_type = models.ForeignKey('FacultyLeaveManagementLeavetype', models.DO_NOTHING, blank=True, null=True)
    faculty = models.ForeignKey('FacultyManagementGeneralInformation', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faculty_leave_management_leavebalance'


class FacultyLeaveManagementLeavepermissionfunction(models.Model):
    id = models.BigAutoField(primary_key=True)
    function = models.CharField(max_length=255, blank=True, null=True)
    permission = models.IntegerField()
    role_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faculty_leave_management_leavepermissionfunction'


class FacultyLeaveManagementLeavetype(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)
    code = models.CharField(unique=True, max_length=10)

    class Meta:
        managed = False
        db_table = 'faculty_leave_management_leavetype'


class FacultyLeaveManagementPermissionrequest(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    from_time = models.TimeField(blank=True, null=True)
    to_time = models.TimeField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    faculty = models.ForeignKey('FacultyManagementGeneralInformation', models.DO_NOTHING, blank=True, null=True)
    user_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faculty_leave_management_permissionrequest'


class FacultyManagementAcademicBackground(models.Model):
    id = models.BigAutoField(primary_key=True)
    degree = models.CharField(max_length=30, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    board_university = models.CharField(max_length=100, blank=True, null=True)
    year_of_passing = models.PositiveIntegerField(blank=True, null=True)
    marks_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    sslc_certificate = models.CharField(max_length=100, blank=True, null=True)
    hsc_certificate = models.CharField(max_length=100, blank=True, null=True)
    ug_certificate = models.CharField(max_length=100, blank=True, null=True)
    pg_certificate = models.CharField(max_length=100, blank=True, null=True)
    phd_certificate = models.CharField(max_length=100, blank=True, null=True)
    postdoc_certificate = models.CharField(db_column='postDoc_certificate', max_length=100, blank=True, null=True)  # Field name made lowercase.
    mphil_certificate = models.CharField(max_length=100, blank=True, null=True)
    faculty = models.ForeignKey('FacultyManagementGeneralInformation', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faculty_management_academic_background'


class FacultyManagementAcademicexperience(models.Model):
    id = models.BigAutoField(primary_key=True)
    institute_name = models.CharField(max_length=225, blank=True, null=True)
    designation = models.CharField(max_length=225, blank=True, null=True)
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    certificate = models.CharField(max_length=500, blank=True, null=True)
    relieving_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    faculty = models.ForeignKey('FacultyManagementGeneralInformation', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faculty_management_academicexperience'


class FacultyManagementAnnouncement(models.Model):
    id = models.BigAutoField(primary_key=True)
    academic_year = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    attachment = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_active = models.IntegerField()
    created_by = models.ForeignKey('FacultyManagementGeneralInformation', models.DO_NOTHING, blank=True, null=True)
    faculty = models.ForeignKey('FacultyManagementGeneralInformation', models.DO_NOTHING, related_name='facultymanagementannouncement_faculty_set', blank=True, null=True)
    updated_by = models.ForeignKey('FacultyManagementGeneralInformation', models.DO_NOTHING, related_name='facultymanagementannouncement_updated_by_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faculty_management_announcement'


class FacultyManagementAnnouncementDepartments(models.Model):
    id = models.BigAutoField(primary_key=True)
    announcement = models.ForeignKey(FacultyManagementAnnouncement, models.DO_NOTHING)
    add_department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'faculty_management_announcement_departments'
        unique_together = (('announcement', 'add_department'),)


class FacultyManagementAnnouncementRoles(models.Model):
    id = models.BigAutoField(primary_key=True)
    announcement_id = models.BigIntegerField()
    role_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'faculty_management_announcement_roles'
        unique_together = (('announcement_id', 'role_id'),)


class FacultyManagementAnnouncementUsers(models.Model):
    id = models.BigAutoField(primary_key=True)
    announcement = models.ForeignKey(FacultyManagementAnnouncement, models.DO_NOTHING)
    general_information = models.ForeignKey('FacultyManagementGeneralInformation', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'faculty_management_announcement_users'
        unique_together = (('announcement', 'general_information'),)


class FacultyManagementAssessmentMaster(models.Model):
    id = models.BigAutoField(primary_key=True)
    semester = models.CharField(max_length=100, blank=True, null=True)
    module = models.CharField(max_length=100, blank=True, null=True)
    faculty_id = models.CharField(max_length=100, blank=True, null=True)
    weightage = models.CharField(max_length=100, blank=True, null=True)
    assessmentname = models.CharField(db_column='Assessmentname', max_length=255, blank=True, null=True)  # Field name made lowercase.
    maxmarks = models.IntegerField(db_column='Maxmarks', blank=True, null=True)  # Field name made lowercase.
    assessment_id = models.BigIntegerField(blank=True, null=True)
    co_code = models.ForeignKey(ExaminationManagementCourseoutcome, models.DO_NOTHING, blank=True, null=True)
    course = models.ForeignKey(CourseManagementCourse, models.DO_NOTHING)
    degree = models.ForeignKey('UserAccountsDegree', models.DO_NOTHING, blank=True, null=True)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)
    level_code = models.ForeignKey(ExaminationManagementBloomslevel, models.DO_NOTHING, blank=True, null=True)
    regulation = models.ForeignKey(CourseManagementRegulations, models.DO_NOTHING, blank=True, null=True)
    customassessmentname = models.CharField(db_column='customAssessmentname', max_length=255, blank=True, null=True)  # Field name made lowercase.
    internal_assessment = models.ForeignKey(ExaminationManagementInternalassessment, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faculty_management_assessment_master'


class FacultyManagementAssessmentmark(models.Model):
    id = models.BigAutoField(primary_key=True)
    marks = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    remarks = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    assessment = models.ForeignKey(FacultyManagementAssessmentMaster, models.DO_NOTHING, blank=True, null=True)
    assignment = models.ForeignKey(CourseManagementAssignsubjectfaculty, models.DO_NOTHING, blank=True, null=True)
    student = models.ForeignKey('UserAccountsStudentdetails', models.DO_NOTHING, blank=True, null=True)
    marks_raw = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    marks_weighted = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faculty_management_assessmentmark'
        unique_together = (('assignment', 'assessment', 'student'),)


class FacultyManagementDesignationmaster(models.Model):
    id = models.BigAutoField(primary_key=True)
    designation_name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'faculty_management_designationmaster'


class FacultyManagementFacultyfunction(models.Model):
    id = models.BigAutoField(primary_key=True)
    function = models.CharField(max_length=500)
    permission = models.IntegerField()
    role_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'faculty_management_facultyfunction'


class FacultyManagementGeneralInformation(models.Model):
    id = models.BigAutoField(primary_key=True)
    faculty_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=225, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=225, blank=True, null=True)
    personal_email = models.CharField(max_length=225, blank=True, null=True)
    college_email = models.CharField(max_length=225, blank=True, null=True)
    phone = models.BigIntegerField(blank=True, null=True)
    blood_group = models.CharField(max_length=225, blank=True, null=True)
    community = models.CharField(max_length=225, blank=True, null=True)
    caste = models.CharField(max_length=225, blank=True, null=True)
    religion = models.CharField(max_length=225, blank=True, null=True)
    doj = models.DateField(blank=True, null=True)
    apaar_id = models.CharField(max_length=100, blank=True, null=True)
    anu_id = models.CharField(max_length=100, blank=True, null=True)
    aicte_id = models.CharField(max_length=100, blank=True, null=True)
    annauniversity_affiliation_id = models.CharField(max_length=100, blank=True, null=True)
    pan_number = models.CharField(db_column='PAN_number', max_length=100, blank=True, null=True)  # Field name made lowercase.
    aadhar_number = models.CharField(db_column='Aadhar_number', max_length=100, blank=True, null=True)  # Field name made lowercase.
    pan_certificate = models.CharField(db_column='PAN_certificate', max_length=100, blank=True, null=True)  # Field name made lowercase.
    aadhar_certificate = models.CharField(db_column='Aadhar_certificate', max_length=100, blank=True, null=True)  # Field name made lowercase.
    approval = models.CharField(max_length=10)
    appointment_type = models.CharField(max_length=20, blank=True, null=True)
    basic_pay = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    agp = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pay_scale_notes = models.CharField(max_length=255, blank=True, null=True)
    recruitment_mode = models.CharField(max_length=30, blank=True, null=True)
    nature_of_duties = models.CharField(max_length=50, blank=True, null=True)
    confirmation_date = models.DateField(blank=True, null=True)
    probation_period_months = models.PositiveIntegerField(blank=True, null=True)
    probation_confirmation_reference = models.CharField(max_length=255, blank=True, null=True)
    probation_confirmation_document = models.CharField(max_length=100, blank=True, null=True)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)
    designation = models.ForeignKey(FacultyManagementDesignationmaster, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faculty_management_general_information'


class FacultyManagementIndustryexperience(models.Model):
    id = models.BigAutoField(primary_key=True)
    company_name = models.CharField(max_length=225, blank=True, null=True)
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    certificate = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    designation = models.ForeignKey(FacultyManagementDesignationmaster, models.DO_NOTHING, blank=True, null=True)
    faculty = models.ForeignKey(FacultyManagementGeneralInformation, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faculty_management_industryexperience'


class FacultyManagementMission(models.Model):
    id = models.BigAutoField(primary_key=True)
    mission_statement = models.TextField()
    year = models.PositiveIntegerField(blank=True, null=True)
    is_active = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    created_by = models.ForeignKey(FacultyManagementGeneralInformation, models.DO_NOTHING, blank=True, null=True)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faculty_management_mission'


class FacultyManagementOpenElectiveOffer(models.Model):
    id = models.BigAutoField(primary_key=True)
    slots = models.CharField(max_length=100, blank=True, null=True)
    academic_year = models.CharField(max_length=100, blank=True, null=True)
    batch = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    course = models.ForeignKey(CourseManagementCourse, models.DO_NOTHING, blank=True, null=True)
    created_by = models.ForeignKey(FacultyManagementGeneralInformation, models.DO_NOTHING, blank=True, null=True)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)
    faculty = models.ForeignKey(FacultyManagementGeneralInformation, models.DO_NOTHING, related_name='facultymanagementopenelectiveoffer_faculty_set', blank=True, null=True)
    offered_from_dept = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, related_name='facultymanagementopenelectiveoffer_offered_from_dept_set', blank=True, null=True)
    regulation = models.ForeignKey(CourseManagementRegulations, models.DO_NOTHING, blank=True, null=True)
    updated_by = models.ForeignKey(FacultyManagementGeneralInformation, models.DO_NOTHING, related_name='facultymanagementopenelectiveoffer_updated_by_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faculty_management_open_elective_offer'


class FacultyManagementOpenElectiveOffertodept(models.Model):
    id = models.BigAutoField(primary_key=True)
    offer = models.ForeignKey(FacultyManagementOpenElectiveOffer, models.DO_NOTHING)
    offered_to_dept = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'faculty_management_open_elective_offertodept'


class FacultyManagementProgramEducationalObjective(models.Model):
    id = models.BigAutoField(primary_key=True)
    peo_statement = models.TextField()
    year = models.PositiveIntegerField(blank=True, null=True)
    is_active = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    created_by = models.ForeignKey(FacultyManagementGeneralInformation, models.DO_NOTHING, blank=True, null=True)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faculty_management_program_educational_objective'


class FacultyManagementProgramSpecificOutcomes(models.Model):
    id = models.BigAutoField(primary_key=True)
    pso_statement = models.TextField()
    year = models.PositiveIntegerField(blank=True, null=True)
    is_active = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    created_by = models.ForeignKey(FacultyManagementGeneralInformation, models.DO_NOTHING, blank=True, null=True)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faculty_management_program_specific_outcomes'


class FacultyManagementResearchexperience(models.Model):
    id = models.BigAutoField(primary_key=True)
    research_area = models.CharField(max_length=225, blank=True, null=True)
    institute = models.CharField(max_length=225, blank=True, null=True)
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    certificate = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    faculty = models.ForeignKey(FacultyManagementGeneralInformation, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faculty_management_researchexperience'


class FacultyManagementVision(models.Model):
    id = models.BigAutoField(primary_key=True)
    year = models.PositiveIntegerField(blank=True, null=True)
    vision_statement = models.TextField()
    is_active = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    created_by = models.ForeignKey(FacultyManagementGeneralInformation, models.DO_NOTHING, blank=True, null=True)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faculty_management_vision'
        unique_together = (('department', 'year'),)


class FeeManagementFeeentry(models.Model):
    id = models.BigAutoField(primary_key=True)
    department_id = models.CharField(max_length=200, blank=True, null=True)
    batch = models.CharField(max_length=4)
    quota = models.CharField(max_length=100, blank=True, null=True)
    year_1 = models.DecimalField(max_digits=10, decimal_places=2)
    year_2 = models.DecimalField(max_digits=10, decimal_places=2)
    year_3 = models.DecimalField(max_digits=10, decimal_places=2)
    year_4 = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    degree = models.ForeignKey('UserAccountsDegree', models.DO_NOTHING, blank=True, null=True)
    fee_category = models.ForeignKey('FeeManagementFeetype', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'fee_management_feeentry'


class FeeManagementFeeperimissonfunction(models.Model):
    id = models.BigAutoField(primary_key=True)
    function = models.CharField(max_length=500)
    permission = models.IntegerField()
    role_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'fee_management_feeperimissonfunction'


class FeeManagementFeetype(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fee_management_feetype'


class FeeManagementScholarshipdeduction(models.Model):
    id = models.BigAutoField(primary_key=True)
    scholarship = models.CharField(db_column='Scholarship', max_length=100, blank=True, null=True)  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=100, blank=True, null=True)  # Field name made lowercase.
    quota = models.CharField(db_column='Quota', max_length=100, blank=True, null=True)  # Field name made lowercase.
    scholarship_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fee_management_scholarshipdeduction'
        unique_together = (('scholarship', 'department', 'quota'),)


class FeeManagementTransportfee(models.Model):
    id = models.BigAutoField(primary_key=True)
    amount_per_semester = models.DecimalField(max_digits=10, decimal_places=2)
    amount_per_year = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField()
    stage = models.OneToOneField('FeeManagementTransportstage', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'fee_management_transportfee'


class FeeManagementTransportstage(models.Model):
    id = models.BigAutoField(primary_key=True)
    stage_no = models.PositiveIntegerField(unique=True)
    distance_from = models.DecimalField(max_digits=6, decimal_places=2)
    distance_to = models.DecimalField(max_digits=6, decimal_places=2)
    bus_stop = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fee_management_transportstage'


class FeedbackManagementCourseExitSurveyQuestion(models.Model):
    id = models.BigAutoField(primary_key=True)
    question_text = models.CharField(max_length=500)
    academic_year = models.CharField(max_length=20, blank=True, null=True)
    blooms_level = models.ForeignKey(ExaminationManagementBloomslevel, models.DO_NOTHING, blank=True, null=True)
    program_outcome = models.ForeignKey(ExaminationManagementProgrammeoutcome, models.DO_NOTHING, blank=True, null=True)
    question_type = models.ForeignKey('FeedbackManagementCouseExitSurveyQuestionType', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feedback_management_course_exit_survey_question'


class FeedbackManagementCouseExitSurveyQuestionType(models.Model):
    id = models.BigAutoField(primary_key=True)
    question_type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feedback_management_couse_exit_survey_question_type'


class FeedbackManagementFeedbackpermission(models.Model):
    id = models.BigAutoField(primary_key=True)
    function = models.CharField(max_length=500)
    permission = models.IntegerField()
    role_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'feedback_management_feedbackpermission'


class FeedbackManagementStudentCourseExitSurveyFeedback(models.Model):
    id = models.BigAutoField(primary_key=True)
    rating = models.IntegerField(blank=True, null=True)
    year = models.CharField(max_length=100, blank=True, null=True)
    semester = models.CharField(max_length=100, blank=True, null=True)
    academic_year = models.CharField(max_length=100, blank=True, null=True)
    batch = models.CharField(max_length=100, blank=True, null=True)
    submitted_at = models.DateTimeField()
    enrolled_course = models.ForeignKey(CourseManagementCourseenrollment, models.DO_NOTHING)
    question = models.ForeignKey(FeedbackManagementCourseExitSurveyQuestion, models.DO_NOTHING)
    student = models.ForeignKey('UserAccountsStudentdetails', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'feedback_management_student_course_exit_survey_feedback'


class HourAttendance(models.Model):
    id = models.BigAutoField(primary_key=True)
    faculty_id = models.IntegerField(blank=True, null=True)
    batch = models.CharField(max_length=20, blank=True, null=True)
    section = models.CharField(max_length=10, blank=True, null=True)
    period = models.PositiveIntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    reg_no = models.CharField(max_length=20, blank=True, null=True)
    student_name = models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(max_length=10)
    course = models.ForeignKey(CourseManagementCourse, models.DO_NOTHING, blank=True, null=True)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hour_attendance'


class NbaAcademicperformancefirstyear(models.Model):
    id = models.BigAutoField(primary_key=True)
    caym1_label = models.CharField(max_length=16, blank=True, null=True)
    caym2_label = models.CharField(max_length=16, blank=True, null=True)
    caym3_label = models.CharField(max_length=16, blank=True, null=True)
    academic_year_range = models.CharField(max_length=128, blank=True, null=True)
    x_caym1 = models.DecimalField(max_digits=5, decimal_places=2)
    x_caym2 = models.DecimalField(max_digits=5, decimal_places=2)
    x_caym3 = models.DecimalField(max_digits=5, decimal_places=2)
    y_caym1 = models.IntegerField()
    y_caym2 = models.IntegerField()
    y_caym3 = models.IntegerField()
    z_caym1 = models.IntegerField()
    z_caym2 = models.IntegerField()
    z_caym3 = models.IntegerField()
    api_1 = models.DecimalField(max_digits=6, decimal_places=2)
    api_2 = models.DecimalField(max_digits=6, decimal_places=2)
    api_3 = models.DecimalField(max_digits=6, decimal_places=2)
    average_api = models.DecimalField(max_digits=6, decimal_places=2)
    max_marks = models.IntegerField()
    marks_awarded = models.DecimalField(max_digits=6, decimal_places=2)
    is_verified = models.IntegerField()
    admin_remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'nba_academicperformancefirstyear'


class NbaAcademicperformancesecondyear(models.Model):
    id = models.BigAutoField(primary_key=True)
    caym1_label = models.CharField(max_length=16, blank=True, null=True)
    caym2_label = models.CharField(max_length=16, blank=True, null=True)
    caym3_label = models.CharField(max_length=16, blank=True, null=True)
    academic_year_range = models.CharField(max_length=128, blank=True, null=True)
    x_caym1 = models.DecimalField(max_digits=5, decimal_places=2)
    x_caym2 = models.DecimalField(max_digits=5, decimal_places=2)
    x_caym3 = models.DecimalField(max_digits=5, decimal_places=2)
    y_caym1 = models.IntegerField()
    y_caym2 = models.IntegerField()
    y_caym3 = models.IntegerField()
    z_caym1 = models.IntegerField()
    z_caym2 = models.IntegerField()
    z_caym3 = models.IntegerField()
    api_1 = models.DecimalField(max_digits=6, decimal_places=2)
    api_2 = models.DecimalField(max_digits=6, decimal_places=2)
    api_3 = models.DecimalField(max_digits=6, decimal_places=2)
    average_api = models.DecimalField(max_digits=6, decimal_places=2)
    max_marks = models.IntegerField()
    marks_awarded = models.DecimalField(max_digits=6, decimal_places=2)
    is_verified = models.IntegerField()
    admin_remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'nba_academicperformancesecondyear'


class NbaAcademicperformancethirdyear(models.Model):
    id = models.BigAutoField(primary_key=True)
    caym1_label = models.CharField(max_length=16, blank=True, null=True)
    caym2_label = models.CharField(max_length=16, blank=True, null=True)
    caym3_label = models.CharField(max_length=16, blank=True, null=True)
    academic_year_range = models.CharField(max_length=128, blank=True, null=True)
    x_caym1 = models.DecimalField(max_digits=5, decimal_places=2)
    x_caym2 = models.DecimalField(max_digits=5, decimal_places=2)
    x_caym3 = models.DecimalField(max_digits=5, decimal_places=2)
    y_caym1 = models.IntegerField()
    y_caym2 = models.IntegerField()
    y_caym3 = models.IntegerField()
    z_caym1 = models.IntegerField()
    z_caym2 = models.IntegerField()
    z_caym3 = models.IntegerField()
    api_1 = models.DecimalField(max_digits=6, decimal_places=2)
    api_2 = models.DecimalField(max_digits=6, decimal_places=2)
    api_3 = models.DecimalField(max_digits=6, decimal_places=2)
    average_api = models.DecimalField(max_digits=6, decimal_places=2)
    max_marks = models.IntegerField()
    marks_awarded = models.DecimalField(max_digits=6, decimal_places=2)
    is_verified = models.IntegerField()
    admin_remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'nba_academicperformancethirdyear'


class NbaDeptpublicationrow(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=256, blank=True, null=True)
    pub_type = models.CharField(max_length=32, blank=True, null=True)
    editor_name = models.CharField(max_length=128, blank=True, null=True)
    student_semester = models.CharField(max_length=64, blank=True, null=True)
    num_issues = models.IntegerField(blank=True, null=True)
    copy_type = models.CharField(max_length=16, blank=True, null=True)
    weblink = models.CharField(max_length=200, blank=True, null=True)
    submission = models.ForeignKey('NbaDeptpublicationssubmission', models.DO_NOTHING, blank=True, null=True)
    cay_bucket = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nba_deptpublicationrow'


class NbaDeptpublicationssubmission(models.Model):
    id = models.BigAutoField(primary_key=True)
    academic_year_range = models.CharField(max_length=64, blank=True, null=True)
    is_verified = models.IntegerField(blank=True, null=True)
    admin_remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)
    marks_awarded = models.DecimalField(max_digits=6, decimal_places=2)
    max_marks = models.IntegerField()
    caym1_count = models.IntegerField()
    caym2_count = models.IntegerField()
    caym3_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nba_deptpublicationssubmission'


class NbaEnrolmentratiofirstyear(models.Model):
    id = models.BigAutoField(primary_key=True)
    academic_year_range = models.CharField(max_length=50, blank=True, null=True)
    is_verified = models.IntegerField()
    admin_remarks = models.TextField(blank=True, null=True)
    sanctioned_intake_cay = models.PositiveIntegerField(blank=True, null=True)
    sanctioned_intake_caym1 = models.PositiveIntegerField(blank=True, null=True)
    sanctioned_intake_caym2 = models.PositiveIntegerField(blank=True, null=True)
    admitted_cay = models.PositiveIntegerField(blank=True, null=True)
    admitted_caym1 = models.PositiveIntegerField(blank=True, null=True)
    admitted_caym2 = models.PositiveIntegerField(blank=True, null=True)
    supernumerary_cay = models.PositiveIntegerField(blank=True, null=True)
    supernumerary_caym1 = models.PositiveIntegerField(blank=True, null=True)
    supernumerary_caym2 = models.PositiveIntegerField(blank=True, null=True)
    er_cay = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    er_caym1 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    er_caym2 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    average_er = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    er_points = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    max_marks = models.PositiveIntegerField(blank=True, null=True)
    marks_awarded = models.PositiveIntegerField(blank=True, null=True)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nba_enrolmentratiofirstyear'


class NbaNbaperimissonfunction(models.Model):
    id = models.BigAutoField(primary_key=True)
    function = models.CharField(max_length=500)
    permission = models.IntegerField()
    role_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'nba_nbaperimissonfunction'


class NbaPlacementhigherstudiesentrepreneurship(models.Model):
    id = models.BigAutoField(primary_key=True)
    lyg_label = models.CharField(max_length=16, blank=True, null=True)
    lygm1_label = models.CharField(max_length=16, blank=True, null=True)
    lygm2_label = models.CharField(max_length=16, blank=True, null=True)
    academic_year_range = models.CharField(max_length=128, blank=True, null=True)
    fs_lyg = models.IntegerField()
    fs_lygm1 = models.IntegerField()
    fs_lygm2 = models.IntegerField()
    x_lyg = models.IntegerField()
    y_lyg = models.IntegerField()
    z_lyg = models.IntegerField()
    x_lygm1 = models.IntegerField()
    y_lygm1 = models.IntegerField()
    z_lygm1 = models.IntegerField()
    x_lygm2 = models.IntegerField()
    y_lygm2 = models.IntegerField()
    z_lygm2 = models.IntegerField()
    p_1 = models.DecimalField(max_digits=6, decimal_places=2)
    p_2 = models.DecimalField(max_digits=6, decimal_places=2)
    p_3 = models.DecimalField(max_digits=6, decimal_places=2)
    average_p = models.DecimalField(max_digits=6, decimal_places=2)
    placement_points = models.DecimalField(max_digits=6, decimal_places=2)
    max_marks = models.IntegerField()
    is_verified = models.IntegerField()
    admin_remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING)
    marks_awarded = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nba_placementhigherstudiesentrepreneurship'


class NbaSanctionedintake(models.Model):
    id = models.BigAutoField(primary_key=True)
    year = models.CharField(max_length=20, blank=True, null=True)
    sanctioned_intake = models.PositiveIntegerField(blank=True, null=True)
    degree = models.ForeignKey('UserAccountsDegree', models.DO_NOTHING, blank=True, null=True)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nba_sanctionedintake'


class NbaSocietiessubmission(models.Model):
    id = models.BigAutoField(primary_key=True)
    academic_year_range = models.CharField(max_length=64, blank=True, null=True)
    is_verified = models.IntegerField(blank=True, null=True)
    admin_remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    max_marks = models.IntegerField(blank=True, null=True)
    marks_awarded = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    national_events_count = models.IntegerField(blank=True, null=True)
    international_events_count = models.IntegerField(blank=True, null=True)
    state_events_count = models.IntegerField(blank=True, null=True)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)
    caym1_events_count = models.IntegerField(blank=True, null=True)
    caym2_events_count = models.IntegerField(blank=True, null=True)
    caym3_events_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nba_societiessubmission'


class NbaSocietychapter(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    type = models.CharField(max_length=50)
    scope = models.CharField(max_length=32, blank=True, null=True)
    inauguration_year = models.IntegerField(blank=True, null=True)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)
    submission = models.ForeignKey(NbaSocietiessubmission, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nba_societychapter'


class NbaSocietyevent(models.Model):
    id = models.BigAutoField(primary_key=True)
    event_title = models.CharField(max_length=256, blank=True, null=True)
    body_name = models.CharField(max_length=256, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    level = models.CharField(max_length=32, blank=True, null=True)
    society = models.ForeignKey(NbaSocietychapter, models.DO_NOTHING, blank=True, null=True)
    submission = models.ForeignKey(NbaSocietiessubmission, models.DO_NOTHING, blank=True, null=True)
    cay_bucket = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nba_societyevent'


class NbaStudenteventrow(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.CharField(max_length=128, blank=True, null=True)
    event_title = models.CharField(max_length=256, blank=True, null=True)
    level = models.CharField(max_length=32, blank=True, null=True)
    award = models.CharField(max_length=128, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    submission = models.ForeignKey('NbaStudenteventssubmission', models.DO_NOTHING, blank=True, null=True)
    cay_bucket = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nba_studenteventrow'


class NbaStudenteventssubmission(models.Model):
    id = models.BigAutoField(primary_key=True)
    academic_year_range = models.CharField(max_length=64, blank=True, null=True)
    is_verified = models.IntegerField(blank=True, null=True)
    admin_remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)
    marks_awarded = models.DecimalField(max_digits=6, decimal_places=2)
    max_marks = models.IntegerField()
    caym1_count = models.IntegerField(blank=True, null=True)
    caym2_count = models.IntegerField(blank=True, null=True)
    caym3_count = models.IntegerField(blank=True, null=True)
    international_events_count = models.IntegerField(blank=True, null=True)
    national_events_count = models.IntegerField(blank=True, null=True)
    state_events_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nba_studenteventssubmission'


class NbaStudentpublicationrow(models.Model):
    id = models.BigAutoField(primary_key=True)
    publisher_name = models.CharField(max_length=256, blank=True, null=True)
    venue_title = models.CharField(max_length=256, blank=True, null=True)
    volume_issue = models.CharField(max_length=128, blank=True, null=True)
    award_name = models.CharField(max_length=256, blank=True, null=True)
    student = models.CharField(max_length=256, blank=True, null=True)
    venue_type = models.CharField(max_length=32, blank=True, null=True)
    submission = models.ForeignKey('NbaStudentpublicationssubmission', models.DO_NOTHING, blank=True, null=True)
    cay_bucket = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nba_studentpublicationrow'


class NbaStudentpublicationssubmission(models.Model):
    id = models.BigAutoField(primary_key=True)
    academic_year_range = models.CharField(max_length=64, blank=True, null=True)
    is_verified = models.IntegerField(blank=True, null=True)
    admin_remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)
    marks_awarded = models.DecimalField(max_digits=6, decimal_places=2)
    max_marks = models.IntegerField()
    caym1_count = models.IntegerField()
    caym2_count = models.IntegerField()
    caym3_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nba_studentpublicationssubmission'


class NbaSuccessratestipulated(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    lyg_label = models.CharField(max_length=16, blank=True, null=True)
    lygm1_label = models.CharField(max_length=16, blank=True, null=True)
    lygm2_label = models.CharField(max_length=16, blank=True, null=True)
    academic_year_range = models.CharField(max_length=128, blank=True, null=True)
    a_lyg = models.PositiveIntegerField(blank=True, null=True)
    a_lygm1 = models.PositiveIntegerField(blank=True, null=True)
    a_lygm2 = models.PositiveIntegerField(blank=True, null=True)
    b_lyg = models.PositiveIntegerField(blank=True, null=True)
    b_lygm1 = models.PositiveIntegerField(blank=True, null=True)
    b_lygm2 = models.PositiveIntegerField(blank=True, null=True)
    sr_1 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    sr_2 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    sr_3 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    average_sr = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    sr_points = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    is_verified = models.IntegerField()
    admin_remarks = models.TextField(blank=True, null=True)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING)
    marks_awarded = models.PositiveIntegerField(blank=True, null=True)
    max_marks = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nba_successratestipulated'


class StudentAchievements(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    mentor_id = models.CharField(max_length=200, blank=True, null=True)
    register_no = models.CharField(max_length=20)
    batch = models.CharField(max_length=20)
    section = models.CharField(max_length=1, blank=True, null=True)
    semester = models.IntegerField()
    date = models.DateField()
    award_name = models.CharField(max_length=200)
    contest = models.CharField(max_length=200)
    given_by = models.CharField(max_length=200)
    event_type = models.CharField(max_length=50)
    certificate = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_achievements'


class StudentManagementAcademiccalendar(models.Model):
    id = models.BigAutoField(primary_key=True)
    batch = models.CharField(max_length=100, blank=True, null=True)
    semester = models.IntegerField()
    file = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'student_management_academiccalendar'
        unique_together = (('batch', 'semester'),)


class StudentManagementAssignapproval(models.Model):
    id = models.BigAutoField(primary_key=True)
    approver_level = models.PositiveIntegerField()
    is_cross_department_approver = models.CharField(max_length=3, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    approver_department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)
    approver_role_id = models.BigIntegerField(blank=True, null=True)
    creator_role_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_management_assignapproval'


class StudentManagementBonafideapplication(models.Model):
    id = models.BigAutoField(primary_key=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    other_reason = models.TextField(blank=True, null=True)
    father_name = models.CharField(max_length=255, blank=True, null=True)
    year_display = models.CharField(max_length=50, blank=True, null=True)
    applied_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20)
    student = models.ForeignKey('UserAccountsStudentdetails', models.DO_NOTHING, blank=True, null=True)
    academic_year = models.CharField(max_length=9, blank=True, null=True)
    batch = models.CharField(max_length=10, blank=True, null=True)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)
    regulation = models.CharField(max_length=10, blank=True, null=True)
    semester = models.CharField(max_length=10, blank=True, null=True)
    year = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_management_bonafideapplication'


class StudentManagementBonafideapprovalflow(models.Model):
    id = models.BigAutoField(primary_key=True)
    approver_role_id = models.IntegerField(blank=True, null=True)
    approver_level = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20)
    acted_on = models.DateTimeField()
    created_on = models.DateTimeField()
    application = models.ForeignKey(StudentManagementBonafideapplication, models.DO_NOTHING, blank=True, null=True)
    approver_department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_management_bonafideapprovalflow'


class StudentManagementDailyAttendance(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    faculty = models.ForeignKey(FacultyManagementGeneralInformation, models.DO_NOTHING, blank=True, null=True)
    academic_year = models.CharField(max_length=20, blank=True, null=True)
    afternoon_status = models.CharField(max_length=10, blank=True, null=True)
    full_day_status = models.CharField(max_length=10, blank=True, null=True)
    marked_at = models.DateTimeField(blank=True, null=True)
    marked_by = models.ForeignKey(FacultyManagementGeneralInformation, models.DO_NOTHING, related_name='studentmanagementdailyattendance_marked_by_set', blank=True, null=True)
    morning_status = models.CharField(max_length=10, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    section = models.CharField(max_length=10, blank=True, null=True)
    semester = models.CharField(max_length=20, blank=True, null=True)
    student = models.ForeignKey('UserAccountsStudentdetails', models.DO_NOTHING, blank=True, null=True)
    updated_by = models.ForeignKey(FacultyManagementGeneralInformation, models.DO_NOTHING, related_name='studentmanagementdailyattendance_updated_by_set', blank=True, null=True)
    year = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_management_daily_attendance'


class StudentManagementFeereceipt(models.Model):
    id = models.BigAutoField(primary_key=True)
    batch = models.CharField(max_length=50, blank=True, null=True)
    section = models.CharField(max_length=5, blank=True, null=True)
    semester = models.IntegerField(blank=True, null=True)
    fee_receipt = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField()
    status = models.CharField(max_length=10)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)
    student = models.ForeignKey('UserAccountsStudentdetails', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_management_feereceipt'


class StudentManagementHourattendance(models.Model):
    id = models.BigAutoField(primary_key=True)
    batch = models.CharField(max_length=20, blank=True, null=True)
    section = models.CharField(max_length=10, blank=True, null=True)
    period = models.PositiveSmallIntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    academic_year = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    course = models.ForeignKey(CourseManagementCourse, models.DO_NOTHING, blank=True, null=True)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)
    faculty = models.ForeignKey(FacultyManagementGeneralInformation, models.DO_NOTHING, blank=True, null=True)
    marked_at = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    semester = models.CharField(max_length=20, blank=True, null=True)
    student = models.ForeignKey('UserAccountsStudentdetails', models.DO_NOTHING, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    year = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_management_hourattendance'


class StudentManagementManualfeeentry(models.Model):
    id = models.BigAutoField(primary_key=True)
    entered_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    entered_at = models.DateTimeField()
    entered_by = models.CharField(max_length=100, blank=True, null=True)
    fee_receipt = models.OneToOneField(StudentManagementFeereceipt, models.DO_NOTHING)
    transaction_id = models.CharField(unique=True, max_length=50, blank=True, null=True)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'student_management_manualfeeentry'


class StudentManagementStudentachievements(models.Model):
    id = models.BigAutoField(primary_key=True)
    batch = models.CharField(max_length=100, blank=True, null=True)
    section = models.CharField(max_length=100, blank=True, null=True)
    semester = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField()
    award_name = models.CharField(max_length=200)
    contest = models.CharField(max_length=200)
    given_by = models.CharField(max_length=200)
    event_type = models.CharField(max_length=50)
    certificate = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)
    academic_year = models.CharField(max_length=100, blank=True, null=True)
    mentor = models.ForeignKey(FacultyManagementGeneralInformation, models.DO_NOTHING, blank=True, null=True)
    student = models.ForeignKey('UserAccountsStudentdetails', models.DO_NOTHING, blank=True, null=True)
    year = models.CharField(max_length=100, blank=True, null=True)
    is_verified = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'student_management_studentachievements'


class StudentManagementStudentcoExCurricular(models.Model):
    id = models.BigAutoField(primary_key=True)
    batch = models.CharField(max_length=100, blank=True, null=True)
    semester = models.CharField(max_length=100, blank=True, null=True)
    year = models.CharField(max_length=100, blank=True, null=True)
    academic_year = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    activity_type = models.CharField(max_length=20, blank=True, null=True)
    event_name = models.CharField(max_length=255, blank=True, null=True)
    level = models.CharField(max_length=20)
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    total_days = models.PositiveIntegerField(blank=True, null=True)
    certificate = models.CharField(max_length=100, blank=True, null=True)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)
    mentor = models.ForeignKey(FacultyManagementGeneralInformation, models.DO_NOTHING, blank=True, null=True)
    student = models.ForeignKey('UserAccountsStudentdetails', models.DO_NOTHING, blank=True, null=True)
    section = models.CharField(max_length=100, blank=True, null=True)
    is_verified = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'student_management_studentco_ex_curricular'


class StudentManagementStudentmanagementpermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    function = models.CharField(max_length=500)
    permission = models.IntegerField()
    role_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'student_management_studentmanagementpermissions'


class StudentManagementStudentname(models.Model):
    id = models.BigAutoField(primary_key=True)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)
    project = models.ForeignKey('StudentManagementStudentprojects', models.DO_NOTHING)
    student = models.ForeignKey('UserAccountsStudentdetails', models.DO_NOTHING, blank=True, null=True)
