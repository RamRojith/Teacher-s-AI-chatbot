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
    StudentDashboardStats, Attendance, ControlRoomUser
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

        # FAIL-SAFE: We need at least a faculty_id
        if not faculty_id:
             return "I'm sorry, I cannot perform any actions without a valid user identity."
        
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
        # 1.0 "My Students" intent (CA role only, unless mentor is explicitly requested)
        my_student_phrases = [
            "my students", "my student", "my class", "my classes",
            "my mentees", "my mentee", "my advisees", "my advisee",
            "my ca students", "my advisor students"
        ]
        if any(p in query for p in my_student_phrases):
            target_dept = self._extract_department(query)
            batch_match = re.search(r'\b(20\d{2})\b', query)
            target_batch = batch_match.group(1) if batch_match else None

            # If explicitly asking for mentees, return mentor list only
            if "mentee" in query or "mentees" in query:
                return self._handle_my_students(faculty_id, relations={"mentor"}, target_dept=target_dept, target_batch=target_batch)

            # If explicitly asking for class/CA/advisor, return CA list only
            if "class" in query or "ca" in query or "advisor" in query or "advisee" in query:
                return self._handle_my_students(faculty_id, relations={"ca"}, target_dept=target_dept, target_batch=target_batch)

            # Default: CA only
            return self._handle_my_students(faculty_id, relations={"ca"}, target_dept=target_dept, target_batch=target_batch)

        # 1.0 Subject Handling Intent
        subject_phrases = [
            "which subject", "which subjects", "my subjects", "my courses",
            "subject i handle", "subjects i handle", "subject i'm handling",
            "subjects i'm handling", "subject i am handling", "subjects i am handling",
            "handling subject", "handling subjects", "subject handling", "subjects handling",
            "assigned subject", "assigned subjects", "subjects assigned",
            "what do i teach", "what am i teaching", "courses i teach", "course i teach"
        ]
        subject_terms = ["subject", "subjects", "course", "courses"]
        subject_intent = any(p in query for p in subject_phrases) or (
            any(k in query for k in ["handle", "handling", "assigned", "teach", "teaching"])
            and any(t in query for t in subject_terms)
        )
        if subject_intent:
            return self._handle_subjects_handled(faculty_id, active_role)

        # 1.05 Mentee-specific intent (explicit mentor list)
        if "mentee" in query or "mentees" in query or "mentor students" in query or "mentor student" in query:
            target_dept = self._extract_department(query)
            batch_match = re.search(r'\b(20\d{2})\b', query)
            target_batch = batch_match.group(1) if batch_match else None
            return self._handle_my_students(faculty_id, relations={"mentor"}, target_dept=target_dept, target_batch=target_batch)

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
        Retrieves and lists students based on the ACTIVE role scope.
        Respects the database assignments for CA, Mentor, Subject Teacher, HOD, or VP.
        """
        try:
            faculty_info = self._get_faculty_info(faculty_id)
            if not faculty_info:
                return "❌ Error: Could not find your faculty record."

            # Enforce role-based scope (do not aggregate across roles)
            role_scope = set()
            if active_role == 'Vice Principal':
                role_scope.add('vp')
            elif active_role == 'HOD':
                role_scope.add('hod')
            elif active_role in ['Advisor', 'CA']:
                role_scope.add('ca')
            elif active_role == 'Mentor':
                role_scope.add('mentor')
            elif active_role in ['Teacher', 'Faculty']:
                role_scope.add('subject')
            else:
                return "❌ Access Denied: Your current role is not permitted to list students."

            # Collect all accessible students based on different responsibilities
            accessible_students = {} # {student_id: (student_obj, [reasons])}
            
            # Helper to add students
            def add_students(queryset, reason):
                for s in queryset:
                    if s.id not in accessible_students:
                        accessible_students[s.id] = {'obj': s, 'reasons': set()}
                    accessible_students[s.id]['reasons'].add(reason)

            # 1. VICE PRINCIPAL (Global Access)
            if 'vp' in role_scope:
                add_students(StudentDetails.objects.all(), "Vice Principal")

            # 2. HOD (Department Access)
            # Check if user is HOD (strict check)
            if 'hod' in role_scope and (faculty_info.department): 
                # Note: Logic assumes HOD role is significant. Using active_role as strong hint for HOD/VP.
                # For HOD, we check their specific department.
                dept = faculty_info.department
                if dept:
                    qs = StudentDetails.objects.filter(department=dept)
                    # Handle ML/AIML Alias
                    if "Machine Learning" in dept.Department:
                        qs = qs | StudentDetails.objects.filter(department__Department__icontains="AIML")
                    add_students(qs, f"HOD of {dept.Department}")

            # 3. CLASS ADVISOR (CA)
            # Find students where this faculty is the CA
            # Match strictly by ID strings (robust check)
            if 'ca' in role_scope:
                ca_students = self._get_students_by_role_id(
                    field_name="ca_id",
                    faculty_info=faculty_info,
                    faculty_id=faculty_id,
                    role_names=["CA", "Advisor", "Class Advisor"]
                )
                add_students(ca_students, "Class Advisor")

            # 4. MENTOR
            # Find students where this faculty is the Mentor
            if 'mentor' in role_scope:
                mentor_students = self._get_students_by_role_id(
                    field_name="mentor_id",
                    faculty_info=faculty_info,
                    faculty_id=faculty_id,
                    role_names=["Mentor"]
                )
                add_students(mentor_students, "Mentor")

            # 5. SUBJECT TEACHER
            # Find students in assigned batches/sections
            if 'subject' in role_scope:
                assignments = AssignSubjectFaculty.objects.filter(faculty=faculty_info, is_active=1)
                if assignments.exists():
                    q_objs = Q()
                    for a in assignments:
                        q_objs |= Q(department=a.department, batch=a.batch, section=a.section)
                    subject_students = StudentDetails.objects.filter(q_objs)
                    add_students(subject_students, "Subject Teacher")

            # --- FILTERING ---
            final_list = []
            
            # If no students found at all
            if not accessible_students:
                 return "No students found under your assigned responsibilities for this role."

            # Convert to list of objects
            all_students_objs = [v['obj'] for k, v in accessible_students.items()]
            
            # Apply Request Filters (Department / Batch)
            if target_dept:
                all_students_objs = [s for s in all_students_objs if s.department_id == target_dept.id]
            if target_batch:
                all_students_objs = [s for s in all_students_objs if s.batch == target_batch]

            # Sort by name
            all_students_objs.sort(key=lambda s: s.name)

            if not all_students_objs:
                 return f"No students matched your criteria within your accessible scope."

            # Format Output
            student_lines = []
            for s in all_students_objs[:100]: # Limit to 100
                reasons = accessible_students[s.id]['reasons']
                # Determine relationship label
                rel_label = ""
                if "Vice Principal" in reasons: rel_label = ""
                elif "Class Advisor" in reasons: rel_label = "[My Class]"
                elif "Mentor" in reasons: rel_label = "[Mentee]"
                elif "Subject Teacher" in reasons: rel_label = "[Student]"
                elif "HOD" in reasons: rel_label = "" # Implicit for HOD
                
                student_lines.append(f"- {s.name} ({s.reg_no}) {rel_label}")

            count_str = f"Total: {len(all_students_objs)}"
            if len(all_students_objs) > 100: count_str += " (Showing first 100)"
            
            header = "👨‍🎓 **Student List**"
            if target_batch: header += f" (Batch {target_batch})"
            
            return f"{header}:\n\n" + "\n".join(student_lines) + f"\n\n{count_str}"

        except Exception as e:
            return f"❌ Error retrieving student list: {str(e)}"

    def _handle_my_students(self, faculty_id, relations=None, target_dept=None, target_batch=None):
        """
        Lists students strictly based on CA and/or Mentor assignments.
        This is used for queries like "my students", "my class", "my mentees".
        """
        try:
            faculty_info = self._get_faculty_info(faculty_id)
            if not faculty_info:
                return "❌ Error: Could not find your faculty record."

            relations = relations or {"ca", "mentor"}

            accessible_students = {}

            def add_students(queryset, reason):
                for s in queryset:
                    if s.id not in accessible_students:
                        accessible_students[s.id] = {'obj': s, 'reasons': set()}
                    accessible_students[s.id]['reasons'].add(reason)

            if "ca" in relations:
                ca_students = self._get_students_by_role_id(
                    field_name="ca_id",
                    faculty_info=faculty_info,
                    faculty_id=faculty_id,
                    role_names=["CA", "Advisor", "Class Advisor"]
                )
                add_students(ca_students, "Class Advisor")

            if "mentor" in relations:
                mentor_students = self._get_students_by_role_id(
                    field_name="mentor_id",
                    faculty_info=faculty_info,
                    faculty_id=faculty_id,
                    role_names=["Mentor"]
                )
                add_students(mentor_students, "Mentor")

            if not accessible_students:
                subject_assignments = AssignSubjectFaculty.objects.filter(faculty=faculty_info, is_active=1)
                if subject_assignments.exists():
                    if relations == {"mentor"}:
                        return "No students found under your Mentor role ID. If you want students from your subject handling, ask: 'list subject students'."
                    if relations == {"ca"}:
                        return "No students found under your CA role ID. If you want students from your subject handling, ask: 'list subject students'."
                    return "No students found under your CA/Mentor assignments. If you want students from your subject handling, ask: 'list subject students'."
                if relations == {"mentor"}:
                    return "No students found under your Mentor role ID."
                if relations == {"ca"}:
                    return "No students found under your CA role ID."
                return "No students found under your CA/Mentor assignments."

            all_students_objs = [v['obj'] for k, v in accessible_students.items()]
            if target_dept:
                all_students_objs = [s for s in all_students_objs if s.department_id == target_dept.id]
            if target_batch:
                all_students_objs = [s for s in all_students_objs if s.batch == target_batch]

            all_students_objs.sort(key=lambda s: s.name)

            if not all_students_objs:
                return "No students matched your criteria within your CA/Mentor scope."

            student_lines = []
            for s in all_students_objs[:100]:
                reasons = accessible_students[s.id]['reasons']
                rel_label = ""
                if "Class Advisor" in reasons and "Mentor" in reasons:
                    rel_label = "[My Class, Mentee]"
                elif "Class Advisor" in reasons:
                    rel_label = "[My Class]"
                elif "Mentor" in reasons:
                    rel_label = "[Mentee]"

                student_lines.append(f"- {s.name} ({s.reg_no}) {rel_label}")

            count_str = f"Total: {len(all_students_objs)}"
            if len(all_students_objs) > 100:
                count_str += " (Showing first 100)"

            if relations == {"mentor"}:
                header = "👨‍🎓 **My Mentees**"
            elif relations == {"ca"}:
                header = "👨‍🎓 **My Students (CA)**"
            else:
                header = "👨‍🎓 **My Students**"
            if target_batch:
                header += f" (Batch {target_batch})"

            return f"{header}:\n\n" + "\n".join(student_lines) + f"\n\n{count_str}"

        except Exception as e:
            return f"❌ Error retrieving my students: {str(e)}"

    def _handle_subjects_handled(self, faculty_id, active_role):
        """
        Lists the subjects a faculty member is currently handling, based strictly on DB assignments.
        """
        try:
            faculty_info = self._get_faculty_info(faculty_id)
            if not faculty_info:
                return "❌ Error: Could not find your faculty record."

            allowed_roles = ['Vice Principal', 'HOD', 'Advisor', 'CA', 'Mentor', 'Teacher', 'Faculty']
            if active_role not in allowed_roles:
                return "❌ Access Denied: Your current role is not permitted to view subject handling."

            assignments = AssignSubjectFaculty.objects.filter(is_active=1).filter(
                Q(faculty=faculty_info) |
                Q(faculty__faculty_id=faculty_id) |
                Q(faculty__id=faculty_id)
            ).select_related('course', 'department', 'regulation')

            if not assignments.exists():
                return "No active subject assignments found for your profile."

            seen = set()
            lines = []
            ordered = assignments.order_by(
                'department__Department', 'batch', 'section', 'course__course_code', 'course__title'
            )
            for a in ordered:
                course_title = a.course.title if a.course else "Unknown Course"
                course_code = a.course.course_code if a.course and a.course.course_code else ""
                dept_name = None
                if a.department and a.department.Department:
                    dept_name = a.department.Department
                elif a.course and a.course.department and a.course.department.Department:
                    dept_name = a.course.department.Department
                else:
                    dept_name = "N/A"

                batch = a.batch or "N/A"
                section = a.section or "N/A"
                academic_year = a.academic_year or "N/A"
                regulation = a.regulation.year if a.regulation else "N/A"

                key = (course_title, course_code, dept_name, batch, section, academic_year, regulation)
                if key in seen:
                    continue
                seen.add(key)

                subject_label = f"{course_title}"
                if course_code:
                    subject_label += f" ({course_code})"

                lines.append(
                    f"- {subject_label} | Dept: {dept_name} | Batch: {batch} | Section: {section} | AY: {academic_year} | Reg: {regulation}"
                )

            header = "📚 **Subjects You Are Handling**"
            count_str = f"Total: {len(lines)}"
            return f"{header}:\n\n" + "\n".join(lines) + f"\n\n{count_str}"

        except Exception as e:
            return f"❌ Error retrieving subject assignments: {str(e)}"

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
                ca_id_str = str(student.ca_id).strip() if student.ca_id else ""
                _, ca_candidate_ids = self._get_candidate_ids(
                    faculty_id, faculty_info, ["CA", "Advisor", "Class Advisor"]
                )
                is_authorized = (ca_id_str in ca_candidate_ids)
            
            elif active_role == 'Mentor': 
                mentor_id_str = str(student.mentor_id).strip() if student.mentor_id else ""
                _, mentor_candidate_ids = self._get_candidate_ids(
                    faculty_id, faculty_info, ["Mentor"]
                )
                is_authorized = (mentor_id_str in mentor_candidate_ids)
            
            elif active_role in ['Teacher', 'Faculty']:
                # SMART ROLE DETECTION: Check if this teacher is actually the CA for this student
                # If so, auto-elevate to CA access level
                # Robust check: allow matching against Faculty PK (standard) or Employee ID (legacy)
                ca_id_str = str(student.ca_id).strip() if student.ca_id else ""
                faculty_pk = str(faculty_info.id)
                faculty_emp_id = str(faculty_info.faculty_id) if faculty_info.faculty_id else ""
                _, ca_candidate_ids = self._get_candidate_ids(
                    faculty_id, faculty_info, ["CA", "Advisor", "Class Advisor"]
                )
                
                is_ca_for_student = (ca_id_str in ca_candidate_ids)
                
                if is_ca_for_student:
                    # Auto-elevate to CA access
                    is_authorized = True
                    active_role = 'CA'  # Upgrade role to CA for this query
                    auth_reason = f"Auto-elevated to Class Advisor access (you are CA for this student)"
                else:
                    # Mentor auto-elevation (if they are mentor for this student)
                    mentor_id_str = str(student.mentor_id).strip() if student.mentor_id else ""
                    _, mentor_candidate_ids = self._get_candidate_ids(
                        faculty_id, faculty_info, ["Mentor"]
                    )
                    is_mentor_for_student = (mentor_id_str in mentor_candidate_ids)

                    if is_mentor_for_student:
                        is_authorized = True
                        active_role = 'Mentor'  # Upgrade role to Mentor for this query
                        auth_reason = "Auto-elevated to Mentor access (you are Mentor for this student)"
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
            analysis_keywords = [
                'performance', 'analyze', 'analysis', 'report', 'evaluate', 'assessment',
                'recommend', 'recommendation', 'suggest', 'suggestion', 'advice',
                'improve', 'improvement', 'guidance', 'plan', 'action plan'
            ]
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

    def _get_role_ids(self, faculty_id, role_names):
        role_ids = set()
        try:
            base_qs = ControlRoomUser.objects.using('approval_system').filter(
                Employee_id=faculty_id,
                is_active=1
            )
            if role_names:
                qs = base_qs.select_related('role').filter(role__role__in=role_names)
                for u in qs:
                    if u.id is not None:
                        role_ids.add(str(u.id))
        except Exception:
            pass
        return role_ids

    def _get_candidate_ids(self, faculty_id, faculty_info, role_names):
        role_ids = self._get_role_ids(faculty_id, role_names)
        candidate_ids = set(role_ids)
        if faculty_info:
            if faculty_info.id is not None:
                candidate_ids.add(str(faculty_info.id))
            if faculty_info.faculty_id:
                candidate_ids.add(str(faculty_info.faculty_id))
        if faculty_id:
            candidate_ids.add(str(faculty_id))
        return role_ids, candidate_ids

    def _get_students_by_role_id(self, field_name, faculty_info, faculty_id, role_names):
        role_ids = self._get_role_ids(faculty_id, role_names)
        if role_ids:
            qs = StudentDetails.objects.filter(**{f"{field_name}__in": list(role_ids)})
            if qs.exists():
                return qs

        fallback_ids = set()
        if faculty_info:
            if faculty_info.id is not None:
                fallback_ids.add(str(faculty_info.id))
            if faculty_info.faculty_id:
                fallback_ids.add(str(faculty_info.faculty_id))
        if not fallback_ids and faculty_id:
            fallback_ids.add(str(faculty_id))

        if fallback_ids:
            return StudentDetails.objects.filter(**{f"{field_name}__in": list(fallback_ids)})

        return StudentDetails.objects.none()

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
            # Legacy/Approval System lookup (ORM only)
            try:
                cr_user = ControlRoomUser.objects.using('approval_system').select_related('department').filter(
                    Employee_id=faculty_id
                ).first()
                if cr_user:
                    name = cr_user.username
                    dept_name = cr_user.department.department if cr_user.department else None
                    dept = Add_Department.objects.filter(Department__iexact=dept_name).first() if dept_name else None
                    if not dept and dept_name and "Machine Learning" in dept_name:
                        dept = Add_Department.objects.filter(Department__icontains="AIML").first()
                    class TransientFaculty:
                        def __init__(self, name, dept): self.name, self.department, self.id = name, dept, 0
                    return TransientFaculty(name, dept)
            except Exception:
                pass
        except: pass
        return None

    def _handle_send_report(self, faculty_id, query, active_role=None):
        return "Not implemented in undo mode."
