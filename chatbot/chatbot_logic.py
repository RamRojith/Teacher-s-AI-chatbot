import re
import random
from datetime import datetime
from django.db.models import Avg, Max, Min, Count, Q
from .models import (
    Faculty, Notification, Mentorship, ClassAdvisorship,
    Add_Department, Regulations, Course_category, Degree,
    InternalAssessment, Course, CourseEnrollment, AssignSubjectFaculty,
    StudentDetails, CourseOutcome, BloomsLevel, Assessments,
    Assessment_master, AssessmentMark, FacultyManagementGeneralInformation,
    StudentDashboardStats, Attendance
)
from .knowledge_base import KnowledgeBase
from openai import OpenAI

class ERPBot:
    def __init__(self):
        self.kb = KnowledgeBase()
    
    def process_query(self, user_query, faculty_id, role=None, all_roles=None, is_first_message=False):
        """
        Main entry point for processing user queries.
        active_role: The currently selected role in the ERP dashboard.
        """
        query = user_query.strip().lower()
        active_role = role  # Strict authority
        
        # FAIL-SAFE: If active role is missing or invalid, do not answer or deny.
        if not active_role:
             return "I'm sorry, I cannot perform any actions without an active role selection from your dashboard."
        
        # Check if user has multiple roles (for greeting/informational context only, not permissions)
        if all_roles is None:
            all_roles = [active_role]
        
        faculty_name = None
        faculty_info = self._get_faculty_info(faculty_id)
        if faculty_info:
            faculty_name = faculty_info.name
        
        # AUTHENTICATION FAILURE: Name is mandatory
        if not faculty_name:
            return f"⚠️ Authentication Error: Unable to retrieve your profile information. Please contact system administrator. (ID: {faculty_id})"
        
        # 0. Strict First-Time Greeting (Only appears once after login)
        if is_first_message:
            return f"Hello {faculty_name} 👋\nWhat would you like me to help you with today?"
        
        # 0.1 Diverse Greeting & Help Logic
        greeting_keywords = ["hi", "hello", "hey", "start", "good morning", "good afternoon", "good evening", "greetings"]
        help_keywords = ["help", "what can you do", "can you help", "how to use", "guide", "who are you"]

        if any(word in query for word in greeting_keywords) and len(query.split()) < 3:
            greet = random.choice([
                f"How can I assist you today, {faculty_name}?",
                "Ready for your query. What are you looking for?"
            ])
            return f"Hello {faculty_name}! {greet}"
        
        if any(word in query for word in help_keywords):
            return self.kb.get_help_text(active_role)

        # 1. INTENT RECOGNITION
        # 1.1 List Students Intent
        list_keywords = ["list", "show students", "get students", "who are the students", "students for", "student list"]
        if "list" in query or "students" in query:
            if any(k in query for k in ["list", "show", "get", "who are"]):
                target_dept = self._extract_department(query)
                batch_match = re.search(r'\b(20\d{2})\b', query)
                target_batch = batch_match.group(1) if batch_match else None
                return self._handle_list_students(faculty_id, active_role, target_dept=target_dept, target_batch=target_batch)

        # 1.2 Send Report Intent (Report to CA)
        if any(k in query for k in ["send report", "submit report"]):
             return self._handle_send_report(faculty_id, query, active_role=active_role)

        # 1.3 View Subject-Specific Reports (For Advisors)
        if any(k in query for k in ["view report", "show report", "subject report", "class report", "report history"]):
             # If "send" not in query and "submit" not in query, it's viewing
             if "send" not in query and "submit" not in query:
                return self._handle_view_subject_reports(faculty_id, query, active_role=active_role)

        # 1.4 Student Marks Chart Intent
        if any(k in query for k in ["chart", "graph", "plot", "visualize", "compare", "marks of"]):
            student_regs = re.findall(r'\b\d{12}\b', query)
            if student_regs:
                return self._handle_marks_chart(faculty_id, student_regs, query, active_role)

        # 2. DEFAULT FALLBACK: Student Search or Academic Query
        # Check for 12-digit reg no in the query
        reg_match = re.search(r'\b\d{12}\b', query)
        if reg_match:
            student_reg_no = reg_match.group(0)
            return self._handle_student_query(faculty_id, student_reg_no, query, active_role)

        # Final Fallback to Knowledge Base
        kb_response = self.kb.search_help(query)
        if kb_response:
            return kb_response

        return "I'm not sure how to help with that. Could you please specify a student registration number, or a task like 'list students' or 'analyze performance'?"

    def _handle_list_students(self, faculty_id, active_role, target_role=None, target_dept=None, target_batch=None):
        """
        Retrieves and lists students strictly based on the active role.
        """
        if active_role in ['Office', 'Lab', 'Staff', 'Maintenance']:
             return "I’m unable to provide that information under your current role selection."

        try:
            faculty_info = self._get_faculty_info(faculty_id)
            if not faculty_info:
                return "❌ Error: Could not find your faculty record."

            # Vice Principal Logic
            if active_role == 'Vice Principal':
                students = StudentDetails.objects.all()
                filters = []
                if target_dept:
                    students = students.filter(department=target_dept)
                    filters.append(target_dept.Department)
                if target_batch:
                    students = students.filter(batch=target_batch)
                    filters.append(f"Batch {target_batch}")
                
                limit_str = f" for {', '.join(filters)}" if filters else ""
                
                if not students.exists():
                     return f"No students found{limit_str}."

                student_list = "\n".join([f"- {s.name} ({s.reg_no})" for s in students[:100]])
                return f"🏫 **Vice Principal View: Student List{limit_str}**:\n\n{student_list}\n\nTotal Students: {students.count()}"

            # HOD Logic
            if active_role == 'HOD':
                dept = faculty_info.department
                if not dept: return "⚠️ Access Denied: No department assigned."
                
                # Check for special ML HOD case: If HOD of "Machine Learning" asking for "AIML"
                # (User complained about this failing)
                is_ml_faculty = "Machine Learning" in dept.Department
                
                students_qs = StudentDetails.objects.filter(department=dept)
                
                # If target dept is different, check for ML alias or Service HOD logic
                if target_dept and target_dept.id != dept.id:
                    is_ml_target = "AIML" in target_dept.Department
                    if is_ml_faculty and is_ml_target:
                        students_qs = StudentDetails.objects.filter(department=target_dept)
                    else:
                        # Standard RBAC: deny unless assigned (service logic removed for 'undo')
                        return f"⚠️ Access Denied: As HOD of {dept.Department}, you cannot view students of {target_dept.Department}."
                
                if target_batch:
                    students = students_qs.filter(batch=target_batch)
                    if not students.exists():
                         return f"No students found in {dept.Department} for Batch {target_batch}."
                    
                    student_list = "\n".join([f"- {s.name} ({s.reg_no})" for s in students[:100]])
                    return f"🏢 **HOD View: {dept.Department} (Batch {target_batch})**:\n\n{student_list}\n\nTotal: {students.count()}"
                
                else:
                    # Year-wise summary based on Batch mapping
                    summary = [f"🏢 **HOD View: {dept.Department}**\n"]
                    
                    batch_to_year = {'2025': '1st Year', '2024': '2nd Year', '2023': '3rd Year', '2022': '4th Year'}
                    year_counts = {label: 0 for label in batch_to_year.values()}
                    other_counts = {}
                    
                    for s in students_qs:
                        year_label = batch_to_year.get(s.batch)
                        if year_label: year_counts[year_label] += 1
                        else:
                            b_label = f"Batch {s.batch}" if s.batch and s.batch != '0' else "Other"
                            other_counts[b_label] = other_counts.get(b_label, 0) + 1
                    
                    for year_label in ['1st Year', '2nd Year', '3rd Year', '4th Year']:
                        summary.append(f"{year_label}: {year_counts[year_label]}")
                    for b_label, count in other_counts.items():
                         summary.append(f"{b_label}: {count}")
                    
                    total = students_qs.count()
                    summary.append(f"\n**Total Students**: {total}")
                    return "\n".join(summary)

            # Faculty/Advisor/Mentor Logic: Strict Section-Based & Assignment-Based Access
            students_qs = StudentDetails.objects.none()
            view_label = "Assigned Students"

            if active_role == 'Mentor':
                students_qs = StudentDetails.objects.filter(mentor_id=str(faculty_info.id))
                view_label = "Your Mentees"
            
            elif active_role in ['Advisor', 'CA']:
                students_qs = StudentDetails.objects.filter(ca_id=str(faculty_info.id))
                view_label = "Your Class"

            elif active_role in ['Teacher', 'Faculty']:
                # Strictly only students in assigned batches and sections via AssignSubjectFaculty
                assignments = AssignSubjectFaculty.objects.filter(faculty=faculty_info)
                if not assignments.exists():
                    return "No assigned classes found for your profile in the official records."
                
                # Filter students that match any of the department/batch/section assignments
                q_objs = Q()
                for a in assignments:
                    q_objs |= Q(department=a.department, batch=a.batch, section=a.section)
                
                students_qs = StudentDetails.objects.filter(q_objs)
                view_label = "Your Subject Students"

            if target_batch:
                students_qs = students_qs.filter(batch=target_batch)
            if target_dept:
                students_qs = students_qs.filter(department=target_dept)

            if not students_qs.exists():
                 return f"No students found under your role access for the specified criteria."

            student_list = "\n".join([f"- {s.name} ({s.reg_no}) [Sec: {s.section}]" for s in students_qs[:100]])
            return f"👨‍🎓 **{view_label}**:\n\n{student_list}\n\nTotal: {students_qs.count()}"

        except Exception as e:
            return f"❌ Error retrieving student list: {str(e)}"

    def _handle_student_query(self, faculty_id, student_reg_no, query, active_role):
        try:
            student = StudentDetails.objects.filter(reg_no__iexact=student_reg_no).first()
            if not student:
                 return f"Student {student_reg_no} not found."
            
            faculty_info = self._get_faculty_info(faculty_id)
            if not faculty_info: return "❌ Authentication Error."

            # Intelligent RBAC: Check access strictly based on active_role and official assignments
            is_authorized = False
            auth_reason = ""
            
            if active_role == 'Vice Principal': 
                is_authorized = True
            
            elif active_role == 'HOD':
                # HOD gets access to their department OR via service assignments
                if student.department == faculty_info.department: 
                    is_authorized = True
                else:
                    # ML Alias match check (Preserve ML HOD access to AIML)
                    if faculty_info.department and "Machine Learning" in faculty_info.department.Department and student.department and "AIML" in student.department.Department:
                        is_authorized = True
                    else:
                        # Check if HOD's department serves this student's class (Service HOD Logic)
                        is_authorized = AssignSubjectFaculty.objects.filter(
                            course__department=faculty_info.department,
                            department=student.department,
                            batch=student.batch,
                            section=student.section
                        ).exists()
                        if is_authorized:
                            auth_reason = f"Authorized as Service HOD: Viewing {faculty_info.department.Department} subjects for {student.department.Department} student."
            
            elif active_role in ['Advisor', 'CA']: 
                is_authorized = (str(student.ca_id) == str(faculty_info.id))
            
            elif active_role == 'Mentor': 
                is_authorized = (str(student.mentor_id) == str(faculty_info.id))
            
            elif active_role in ['Teacher', 'Faculty']:
                # SMART ROLE DETECTION: Check if this teacher is actually the CA for this student
                # If so, auto-elevate to CA access level
                # Robust check: allow matching against Faculty PK (standard) or Employee ID (legacy)
                ca_id_str = str(student.ca_id).strip() if student.ca_id else ""
                faculty_pk = str(faculty_info.id)
                faculty_emp_id = str(faculty_info.faculty_id) if faculty_info.faculty_id else ""
                
                is_ca_for_student = (ca_id_str == faculty_pk) or (ca_id_str == faculty_emp_id and faculty_emp_id != "")
                
                if is_ca_for_student:
                    # Auto-elevate to CA access
                    is_authorized = True
                    active_role = 'CA'  # Upgrade role to CA for this query
                    auth_reason = f"Auto-elevated to Class Advisor access (you are CA for this student)"
                else:
                    # Standard teacher authorization check
                    assignments = AssignSubjectFaculty.objects.filter(
                        faculty=faculty_info,
                        department=student.department,
                        batch=student.batch,
                        section=student.section
                    )
                    
                    if assignments.exists():
                        is_authorized = True
                    else:
                        # HEURISTIC FALLBACK: If faculty is from a Service Department (Maths, Physics, etc.)
                        # grant access to the profile but marks will be filtered later.
                        service_depts = ['Maths', 'Physics', 'Chemistry', 'English', 'Physical Education']
                        faculty_dept_name = faculty_info.department.Department if faculty_info.department else ""
                        
                        if any(sd in faculty_dept_name for sd in service_depts):
                            is_authorized = True
                            auth_reason = f"Authorized as Service Faculty ({faculty_dept_name})"
                        else:
                            auth_reason = f"Access Denied: You are not assigned to {student.department.Department} - Section {student.section}."

            if not is_authorized:
                return auth_reason or "I’m unable to provide that information under your current role selection."

            query_lower = query.lower()

            # ===== MARKS FILTERING BASED ON ROLE AND SCOPE =====
            # Retrieve all marks for this student
            marks = AssessmentMark.objects.filter(student=student)
            
            # ROLE-BASED FILTERING:
            # - Vice Principal, CA, Advisor, Mentor: FULL ACCESS to all marks (no filtering)
            # - HOD: Filtered to their department's subjects only
            # - Teacher/Faculty: Filtered to their explicitly assigned subjects only
            
            current_scope = "All Subjects"  # Default for unrestricted roles
            
            if active_role in ['Vice Principal', 'CA', 'Advisor', 'Mentor']:
                # UNRESTRICTED ACCESS: Class Advisors, Mentors, and VPs see ALL marks
                # No filtering applied - they have complete visibility into student performance
                current_scope = "All Subjects (Full Access)"
                
            elif active_role == 'HOD':
                # HOD: Restricted to their department's subjects
                marks = marks.filter(assessment__course__department=faculty_info.department)
                current_scope = f"{faculty_info.department.Department} Subjects"
                
                # Verify if any marks exist in their scope
                if not marks.exists():
                    return f"👤 **Student Profile: {student.name}**\n\nℹ️ No assessment marks found for {current_scope}. (Access restricted to your department subjects only)."
                    
            elif active_role in ['Teacher', 'Faculty']:
                # TEACHER: Strictly restricted to their assigned subjects
                assigned_courses_qs = AssignSubjectFaculty.objects.filter(
                    faculty=faculty_info,
                    department=student.department,
                    batch=student.batch,
                    section=student.section
                )
                
                if assigned_courses_qs.exists():
                    # Explicit assignment exists - filter to assigned courses
                    assigned_course_ids = assigned_courses_qs.values_list('course', flat=True)
                    course_names = ", ".join(list(assigned_courses_qs.values_list('course__title', flat=True)))
                    marks = marks.filter(assessment__course__id__in=assigned_course_ids)
                    current_scope = f"Assigned Subjects ({course_names})"
                else:
                    # Fallback for Service Department Faculty (Maths, Physics, etc.)
                    # Filter by department name keyword matching
                    dept_keyword = faculty_info.department.Department.lower().replace("maths", "math").replace("physics", "physic")
                    marks = marks.filter(Q(assessment__course__title__icontains=dept_keyword) | Q(assessment__course__department=faculty_info.department))
                    current_scope = f"{faculty_info.department.Department} Subjects"
                
                # Verify if any marks exist in their scope
                if not marks.exists():
                    return f"👤 **Student Profile: {student.name}**\n\nℹ️ No assessment marks found for your {current_scope} scope. (Access restricted to your assigned subjects only)."

            # Generate marks string for display
            marks_str = ", ".join([f"{m.assessment.Assessmentname}: {m.marks_raw}" for m in marks if m.assessment]) if marks.exists() else "No assessment marks available"
            
            # ===== DETERMINE RESPONSE TYPE =====
            # Check if user is asking for detailed performance analysis or just basic info
            analysis_keywords = ['performance', 'analyze', 'analysis', 'analyze', 'report', 'evaluate', 'assessment']
            wants_analysis = any(keyword in query_lower for keyword in analysis_keywords)
            
            # For CA, HOD, and VP: Default to profile view unless analysis is explicitly requested
            # For Teacher/Mentor: Provide analysis when they have limited marks
            if active_role in ['Vice Principal', 'CA', 'Advisor', 'HOD'] and not wants_analysis:
                # ===== PROFILE + MARKS SUMMARY VIEW (HOD-like) =====
                dept_name = student.department.Department if student.department else "N/A"
                
                profile_info = [
                    f"👤 **Student Profile: {student.name}**",
                    f"**Registration No**: {student.reg_no}",
                    f"**Department**: {dept_name}",
                    f"**Batch**: {student.batch or 'N/A'}",
                    f"**Year/Semester**: {student.year or 'N/A'} / {student.semester or 'N/A'}",
                    f"**Section**: {student.section or 'N/A'}",
                    f"**Email**: {student.email or 'N/A'}",
                    f"**Mobile**: {student.mobile_no or 'N/A'}",
                ]
                
                # Add marks summary
                if marks.exists():
                    profile_info.append(f"\n📊 **Academic Marks ({current_scope})**:")
                    
                    # Group marks by subject
                    marks_by_subject = {}
                    for m in marks:
                        if m.assessment and m.assessment.course:
                            subject = m.assessment.course.title
                            if subject not in marks_by_subject:
                                marks_by_subject[subject] = []
                            marks_by_subject[subject].append(f"{m.assessment.Assessmentname}: {m.marks_raw}")
                    
                    # Display marks grouped by subject
                    for subject, subject_marks in sorted(marks_by_subject.items()):
                        profile_info.append(f"\n**{subject}**:")
                        for mark in subject_marks:
                            profile_info.append(f"  • {mark}")
                else:
                    profile_info.append(f"\nℹ️ No assessment marks available for {current_scope}.")
                
                return "\n".join(profile_info)
            
            else:
                # ===== AI-POWERED PERFORMANCE ANALYSIS =====
                achievements, co_curricular, publications, projects, attendance = "N/A", "N/A", "N/A", "N/A", "N/A"
                
                client = OpenAI(api_key="ollama", base_url="http://172.16.71.109:11434/v1")

                system_prompt_template = f"""You are a strict Academic Performance Analyzer for the {current_scope}.
Your task is to analyze a student's performance strictly within the provided metrics.
IMPORTANT: You are only seeing data for {current_scope}. Do not make assumptions about other subjects.

📊 PERFORMANCE METRICS (MANDATORY)
You must evaluate the student using the following metrics ONLY:
- Achievements
- Co-Curricular Activities
- Publications
- Projects
- Attendance
- Academic Marks (Scope: {current_scope})

🧠 ANALYSIS RULES (STRICT)
1️⃣ Strength and Weakness Identification: Every metric must appear either in Strengths or Weaknesses.
2️⃣ Year-Wise Interpretation: 
   - 1st/2nd Year: Supportive, developmental tone. Focus on exposure.
   - 3rd/4th Year: Direct, professional tone. Focus on skill readiness.

📌 RECOMMENDATION RULES: Provide actionable, practical advice for each metric.

🧾 RESPONSE STRUCTURE:
Student Performance Analysis ({current_scope})
Year of Study: {{{{YEAR}}}}

Strengths:
• {{{{STRENGTH_1}}}}

Weaknesses:
• {{{{WEAKNESS_1}}}}

Recommendations:
1. {{{{RECOMMENDATION_1}}}}

Conclusion:
{{{{CLEAR_SUMMARY_AND_FACULTY_INSIGHT}}}}"""

                user_message = f"Student Profile: {student.name}, Year: {student.year or 'N/A'}, Dept: {student.department.Department if student.department else 'N/A'}.\nMetrics: Achievements: {achievements}, Co-Curricular: {co_curricular}, Publications: {publications}, Projects: {projects}, Attendance: {attendance}, Academic Marks: {marks_str}."

                try:
                    response = client.chat.completions.create(
                        model="deepseek-r1:1.5b",
                        messages=[{"role": "system", "content": system_prompt_template}, {"role": "user", "content": user_message}],
                        temperature=0.1
                    )
                    full_resp = response.choices[0].message.content
                    return re.sub(r'<think>.*?(?:</think>|$)', '', full_resp, flags=re.DOTALL | re.IGNORECASE).strip()
                except Exception as e:
                    return f"⚠️ **AI Service Error**: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"

    def _handle_view_subject_reports(self, faculty_id, query, active_role=None):
        if active_role not in ['Advisor', 'HOD', 'Vice Principal']:
            return "Access Denied."
        
        # Simplified report viewing logic
        reports = Notification.objects.filter(receiver_id=faculty_id, message__startswith="REPORT|")
        if active_role == 'Vice Principal': reports = Notification.objects.filter(message__startswith="REPORT|")
        
        if not reports.exists(): return "No reports found."
        
        resp = "📋 **Subject Reports**:\n\n"
        for r in reports[:10]:
            resp += f"• From {r.sender.name}: {r.message.split('|')[2] if len(r.message.split('|')) > 2 else r.message}\n"
        return resp

    def _handle_marks_chart(self, faculty_id, student_identifiers, query, active_role):
        return {"text": "📊 Comparison chart generating...", "type": "chart", "data": {"Sample": 80}}

    def _extract_department(self, query):
        clean_query = re.sub(r'[^a-zA-Z0-9\s]', ' ', query.lower())
        aliases = {'ml': 'AIML', 'ai': 'Artificial', 'cse': 'Engineering', 'cs': 'Engineering', 'it': 'Information'}
        for alias, keyword in aliases.items():
            if f" {alias} " in f" {clean_query} ":
                return Add_Department.objects.filter(Department__icontains=keyword).first()
        for d in Add_Department.objects.all():
            if d.Department and d.Department.lower() in clean_query:
                 return d
        return None

    def _get_faculty_info(self, faculty_id):
        try:
            f = FacultyManagementGeneralInformation.objects.filter(faculty_id=faculty_id).first()
            if f: return f
            # Legacy/Approval System lookup
            from django.db import connections
            with connections['approval_system'].cursor() as cursor:
                cursor.execute("SELECT u.username, d.department FROM control_room_user u JOIN control_room_department d ON u.Department_id = d.id WHERE u.Employee_id = %s", [faculty_id])
                row = cursor.fetchone()
                if row:
                    name, dept_name = row[0], row[1]
                    dept = Add_Department.objects.filter(Department__iexact=dept_name).first()
                    if not dept and "Machine Learning" in dept_name:
                        dept = Add_Department.objects.filter(Department__icontains="AIML").first()
                    class TransientFaculty:
                        def __init__(self, name, dept): self.name, self.department, self.id = name, dept, 0
                    return TransientFaculty(name, dept)
        except: pass
        return None

    def _handle_send_report(self, faculty_id, query, active_role=None):
        return "Not implemented in undo mode."
