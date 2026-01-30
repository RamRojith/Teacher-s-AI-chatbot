# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class UserAccountsStudentdetails(models.Model):
    id = models.BigAutoField(primary_key=True)
    aadhar_number = models.CharField(unique=True, max_length=12, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    reg_no = models.CharField(unique=True, max_length=255, blank=True, null=True)
    regulation = models.CharField(max_length=50, blank=True, null=True)
    batch = models.CharField(max_length=50, blank=True, null=True)
    year = models.CharField(max_length=50, blank=True, null=True)
    semester = models.CharField(max_length=50, blank=True, null=True)
    section = models.CharField(max_length=10, blank=True, null=True)
    profile_img = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    mobile_no = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    ca = models.ForeignKey('FacultyManagementGeneralInformation', models.DO_NOTHING, blank=True, null=True)
    department = models.ForeignKey('UserAccountsAddDepartment', models.DO_NOTHING, blank=True, null=True)
    mentor = models.ForeignKey('FacultyManagementGeneralInformation', models.DO_NOTHING, related_name='useraccountsstudentdetails_mentor_set', blank=True, null=True)
    umis_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_accounts_studentdetails'
