import re
import random
from datetime import datetime
from django.db.models import Avg, Max, Min, Count, Q
from .models import (
    Faculty, Notification, Mentorship, ClassAdvisorship,
    Add_Department, Regulations, Course_category, Degree,
    InternalAssessment, Course, CourseEnrollment, AssignSubjectFaculty,
    StudentDetails, CourseOutcome, BloomsLevel, Assessments,
    Assessment_master, AssessmentMark, FacultyManagementGeneralInformation
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

        # 0.1 Subsequent Optional Greetings (No authorization details)
        if any(word in query for word in ["hi", "hello", "hey", "start", "good morning", "good afternoon", "good evening"]):
            return f"Hello {faculty_name} 👋, What would you like me to help you with today?"
        
        # 1. Detect IDs (Registration Numbers or Codes)
        # Match numeric IDs (like 101) or alphanumeric registration numbers (like 21CS001)
        student_identifiers = re.findall(r'\b(\d{3,}|\d+[A-Z]+\d+)\b', query.upper())
        
        # Guard clause: "class report", "class analysis" - Pre-calculation
        is_report_query = any(k in query for k in ["report", "analysis", "performance", "stats", "statistics", "marks", "scores", "results", "summary"])
        
        # 2. Intent: ERP Metadata (Departments, Courses, Regulations, etc.)
        # Fix: Don't trigger if user is asking for students in a department
        if "department" in query and "student" not in query:
            depts = Add_Department.objects.all()
            if depts.exists():
                dept_list = "\n".join([f"- {d.Department}" for d in depts if d.Department])
                return f"🏢 **Departments**:\n{dept_list}"
            return "No departments found in the system."

        if ("course" in query or "subject" in query) and not is_report_query:
            if not student_identifiers:
                courses = Course.objects.filter(is_active=True)[:10] # Limit for readability
                if courses.exists():
                    course_list = "\n".join([f"- {c.course_code}: {c.title}" for c in courses])
                    return f"📚 **Active Courses** (Showing first 10):\n{course_list}"
                return "No active courses found."

        if "regulation" in query:
            regs = Regulations.objects.all()
            if regs.exists():
                reg_list = "\n".join([f"- {r.year}" for r in regs])
                return f"📜 **Regulations**:\n{reg_list}"
            return "No regulations found."

        # 3. Intent: List Students
        list_keywords = ["my students", "list students", "list my students", "show my students", "assigned students", "mentees", "mentors", "mentor", "mentee", "advisor", "ca", "class", "show students", "list all students", "all students", "students in", "students of"]
        
        # Guard clause: "class report", "class analysis" should NOT be caught here.
        # is_report_query is pre-calculated above
        
        if any(k in query for k in list_keywords) and not is_report_query:
             target_role = None
             target_dept = None
             target_batch = None
             
             # Extract Department if mentioned
             depts = Add_Department.objects.all()
             for d in depts:
                 if d.Department and d.Department.lower() in query:
                     target_dept = d
                     break
            
             # Extract Batch if mentioned (e.g. "2024 batch", "batch 2024", "students of 2024")
             # Look for 4 digit year starting with 20
             batch_match = re.search(r'\b(20\d{2})\b', query)
             if batch_match:
                 target_batch = batch_match.group(1)

             if any(k in query for k in ["mentor", "mentee"]):
                 target_role = 'Mentor'
             elif any(k in query for k in ["advisor", "ca", "class"]):
                 target_role = 'CA'
             elif any(k in query for k in ["all", "combined", "both"]):
                 target_role = 'Combined'
             elif active_role == 'Vice Principal': # Default for VP
                 target_role = 'Vice Principal'
             
             return self._handle_list_students(faculty_id, active_role, target_role, target_dept, target_batch)

        # 4. Intent: Marks/Chart
        if student_identifiers and any(k in query for k in ["mark", "score", "chart"]):
            return self._handle_marks_chart(faculty_id, student_identifiers, user_query, active_role)

        # 4. Intent: Student Info
        if len(student_identifiers) == 1:
            return self._handle_student_query(faculty_id, student_identifiers[0], user_query, active_role)
        elif len(student_identifiers) > 1:
             return f"Found multiple identifiers: {', '.join(student_identifiers)}. Please specify what you need for them."

        # 5. Intent: View Narrative Log (Moved above Class Analysis)
        if ("view report" in query or "show report" in query) or ("report" in query and any(word in query for word in ["view", "show", "history"])):
             return self._handle_view_subject_reports(faculty_id, user_query, active_role)

        # 6. Intent: Live Class Analysis (Stats)
        class_keywords = ["class", "subject", "overall", "my"]
        report_keywords = ["report", "analysis", "performance", "stats", "statistics", "marks", "scores", "results", "summary"]
        
        is_class_report_query = any(k in query for k in ["class report", "subject report", "class analysis", "subject analysis"]) or \
                               (any(ck in query for ck in class_keywords) and any(rk in query for rk in report_keywords))
        
        if is_class_report_query:
            clean_query = query
            for k in (class_keywords + report_keywords):
                clean_query = re.sub(rf'\b{k}\b', '', clean_query)
            for filler in ["of", "for", "in", "the", "details", "data", "info", "information"]:
                clean_query = re.sub(rf'\b{filler}\b', '', clean_query)
            
            subject_query = clean_query.strip()
            return self._handle_class_report(faculty_id, subject_query, active_role)

        # 7. Intent: Send Class Report
        if query.startswith("send report") or query.startswith("submit report"):
            return self._handle_send_report(faculty_id, user_query, active_role)

        # 8. Intent: ERP Help
        help_response = self.kb.search_help(query)
        if help_response:
            return help_response

        return "I'm sorry, I didn't understand that. You can ask:\n- 'List my students'\n- 'Show active courses'\n- 'Student 21CS101 Info'\n- 'Class Report for Physics'"

    def _handle_list_students(self, faculty_id, active_role, target_role=None, target_dept=None, target_batch=None):
        """
        Retrieves and lists students strictly based on the active role.
        """
        # SAFE DENIAL for irrelevant roles
        if active_role in ['Office', 'Lab', 'Staff', 'Maintenance']:
             return "I’m unable to provide that information under your current role selection."

        try:
            # Get the faculty info
            faculty_info = self._get_faculty_info(faculty_id)
            if not faculty_info:
                return "❌ Error: Could not find your faculty record."

            # Vice Principal Logic: List all students (Full access)
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

                student_list = "\n".join([f"- {s.name} ({s.reg_no})" for s in students[:100]]) # Limit for display
                return f"🏫 **Vice Principal View: Student List{limit_str}**:\n\n{student_list}\n\nTotal Students: {students.count()}"

            # HOD Logic: List departmental students (Strictly HOD context)
            if active_role == 'HOD':
                dept = faculty_info.department
                if not dept: return "⚠️ Access Denied: No department assigned."
                
                # If target dept requested, ensure it matches HOD's dept
                if target_dept and target_dept.id != dept.id:
                     return f"⚠️ Access Denied: As HOD of {dept.Department}, you cannot view students of {target_dept.Department}."
                
                students = StudentDetails.objects.filter(department=dept)
                
                if target_batch:
                    students = students.filter(batch=target_batch)
                    limit_str = f" (Batch {target_batch})"
                else:
                    limit_str = ""

                student_list = "\n".join([f"- {s.name} ({s.reg_no})" for s in students[:60]])
                return f"🏢 **HOD View: {dept.Department}{limit_str}**:\n\n{student_list}\n\nTotal: {students.count()}"

            # Faculty/Advisor/Mentor Logic: Only assigned students
            faculty_pk = faculty_info.id
            ca_students = StudentDetails.objects.filter(ca_id=str(faculty_pk))
            mentor_students = StudentDetails.objects.filter(mentor_id=str(faculty_pk))

            if active_role == 'Mentor':
                if not mentor_students.exists(): return "No mentees assigned under Mentor role."
                student_list = "\n".join([f"- {s.name} ({s.reg_no})" for s in mentor_students])
                return f"🤝 **Mentor View: Your Mentees**:\n\n{student_list}\n\nTotal: {mentor_students.count()}"

            if active_role in ['Advisor', 'CA', 'Teacher', 'Faculty']:
                if not ca_students.exists(): return "No class students assigned under Advisor/Faculty role."
                student_list = "\n".join([f"- {s.name} ({s.reg_no})" for s in ca_students])
                return f"👨‍🎓 **Advisor View: Your Students**:\n\n{student_list}\n\nTotal: {ca_students.count()}"

            return "I’m unable to provide that information under your current role selection."
        except FacultyManagementGeneralInformation.DoesNotExist:
            return "❌ Error: Could not find your faculty record in the system."
        except Exception as e:
            return f"❌ Error retrieving student list: {str(e)}"

    def _handle_send_report(self, faculty_id, query, active_role=None):
        try:
            # Check the active role
            if active_role not in ['Teacher', 'Faculty', 'Advisor']:
                 return "I’m unable to provide that information under your current role selection."

            # ERP allocation logic: Look up by faculty_id (Employee ID)
            alloc = AssignSubjectFaculty.objects.filter(faculty__faculty_id=faculty_id).first()
            if not alloc:
                return "❌ You are not allocated to any subject in the ERP."

            query_lower = query.lower()
            msg = query_lower.replace("send report", "").replace("submit report", "").strip()
            
            if len(msg) < 5:
                 return "Please provide a summary. Ex: 'Send Report Python class is performing well'"
            
            # In a real ERP, we'd lookup the advisor for this dept/batch/section
            # Assuming we still use the ClassAdvisorship table for this assignment link
            advisor = ClassAdvisorship.objects.filter(department=alloc.department.Department if alloc.department else "", year=alloc.academic_year[:4] if alloc.academic_year else "").first()
            
            if not advisor:
                return f"❌ No Class Advisor record found for this scope."
                
            # Notification logic
            # For notification sender, we need the local Faculty user ID
            # Search for a local user with this employee ID or username
            sender_user = Faculty.objects.filter(id=faculty_id).first() or \
                          Faculty.objects.filter(username=faculty_id).first()
            
            if not sender_user:
                 return "❌ Error: Could not link your account for notification sending."

            Notification.objects.create(
                sender=sender_user,
                receiver=advisor.faculty,
                message=f"REPORT|{alloc.course.title if alloc.course else 'Subject'}|{msg}"
            )
            return f"✅ **Report sent to Class Advisor for {alloc.course.title if alloc.course else 'subject'}.**"
        except Exception as e:
            return f"Error sending report: {str(e)}"

    def _handle_send_to_advisor(self, faculty_id, query):
        try:
            # Look up by faculty_id (Employee ID)
            alloc = AssignSubjectFaculty.objects.filter(faculty__faculty_id=faculty_id).first()
            if not alloc:
                return "❌ You are not assigned to any subject in the ERP."
                
            advisor = ClassAdvisorship.objects.filter(department=alloc.department.Department if alloc.department else "").first()
            if not advisor:
                return f"❌ No Class Advisor found."
                
            msg = query.replace("send to advisor", "").replace("Send to Advisor", "").strip()
            subject_title = alloc.course.title if alloc.course else "Subject"
            full_msg = f"[{subject_title}] Update: {msg}" if msg else f"[{subject_title}] Update: Subject teacher sent an update"
            
            sender_user = Faculty.objects.filter(id=faculty_id).first() or \
                          Faculty.objects.filter(username=faculty_id).first()
            if not sender_user:
                 return "❌ Error: Could not link your account."

            Notification.objects.create(
                sender=sender_user,
                receiver=advisor.faculty,
                message=full_msg
            )
            return f"✅ **Notification sent to Class Advisor.**"
        except Exception as e:
            return f"Error sending update: {str(e)}"

    def _handle_student_query(self, faculty_id, student_reg_no, query, active_role):
        try:
            # Match by reg_no in StudentDetails
            student = StudentDetails.objects.filter(reg_no__icontains=student_reg_no).first()
            if not student:
                 return f"Student with Registration Number '{student_reg_no}' not found."
            
            # Intelligent RBAC: Check access strictly based on active_role
            is_authorized = False
            
            try:
                faculty_info = self._get_faculty_info(faculty_id)
                if faculty_info:
                    # 0. Vice Principal: Universal access
                    if active_role == 'Vice Principal':
                        is_authorized = True

                    # 1. HOD: Department-wide access
                    elif active_role == 'HOD' and student.department == faculty_info.department:
                        is_authorized = True
                    
                    # 2. CA/Advisor: Class-specific access
                    elif active_role in ['Advisor', 'CA', 'Teacher', 'Faculty']:
                        if str(student.ca_id) == str(faculty_info.id) and student.department == faculty_info.department:
                            is_authorized = True
                    
                    # 3. Mentor: Mentee-specific access
                    elif active_role == 'Mentor':
                        if str(student.mentor_id) == str(faculty_info.id) and student.department == faculty_info.department:
                            is_authorized = True
            except:
                pass
            
            if not is_authorized:
                return "I’m unable to provide that information under your current role selection."

            # Proceed with data retrieval if authorized...

        except Exception as e:
            return f"Error accessing record: {str(e)}"

        # Authorization Logic (Basic)
        # In a real ERP, we'd check against CourseEnrollment or Mentorship tables
        # For now, let's look at the student's department vs faculty's department (if available)
        
        query_lower = query.lower()

        # Performance Analysis (LLM)
        if any(k in query_lower for k in ["analyze", "performance", "recommend", "insight", "review", "report", "evaluate", "assess", "suggestion", "feedback", "improvement", "status", "summary", "progress"]):
            # Get Context via ORM from ERP tables
            marks = AssessmentMark.objects.filter(student=student)
            marks_str = ", ".join([f"{m.assessment.Assessmentname}: {m.marks_raw}" for m in marks if m.assessment]) if marks.exists() else "No specific assessment marks available"
            
            client = OpenAI(api_key="ollama", base_url="http://172.16.71.183:11434/v1")

            system_prompt_template = """You are a strict academic performance analyst.
Your goal: Generate a student report based ONLY on the provided data. Output sections: Student Details, Strength, Weakness, Recommendation, Conclusion."""

            user_message = f"""
Student Data:
Name: {student.name or 'N/A'}
Reg No: {student.reg_no or 'N/A'}
Department: {student.department.Department if student.department else 'N/A'}
Batch: {student.batch or 'N/A'}
Year/Sem: {student.year or 'N/A'} / {student.semester or 'N/A'}
Recent Marks: {marks_str}

Generate the report."""

            try:
                response = client.chat.completions.create(
                    model="sam860/deepseek-r1-qwen-distill:1.5b",
                    messages=[
                        {"role": "system", "content": system_prompt_template},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=0.1
                )
                full_resp = response.choices[0].message.content
                clean_resp = re.sub(r'<think>.*?(?:</think>|$)', '', full_resp, flags=re.DOTALL | re.IGNORECASE).strip()
                return clean_resp
            except Exception as e:
                return f"⚠️ **AI Service Error**: {str(e)}"

        # Default Info Response using ERP fields
        dept_name = student.department.Department if student.department else "N/A"
        info = [
            f"👤 **Student Profile: {student.name}**",
            f"**Reg No**: {student.reg_no}",
            f"**Department**: {dept_name}",
            f"**Batch**: {student.batch or 'N/A'}",
            f"**Year/Semester**: {student.year or 'N/A'} / {student.semester or 'N/A'}",
            f"**Email**: {student.email or 'N/A'}",
            f"**Mobile**: {student.mobile_no or 'N/A'}",
            f"**Gender**: {student.gender or 'N/A'}",
            f"**DOB**: {student.date_of_birth or 'N/A'}"
        ]
        
        # Check for Course Enrollments
        enrollments = CourseEnrollment.objects.filter(student=student)
        if enrollments.exists():
            courses = ", ".join([e.course.title for e in enrollments if e.course])
            info.append(f"**Enrolled Courses**: {courses}")

        return "\n".join(info)

    def _handle_view_subject_reports(self, faculty_id, query, active_role=None):
        # Role Check: Only Advisors or Specific roles can view subject reports
        if active_role not in ['Advisor', 'HOD', 'Admin', 'Faculty', 'Vice Principal']:
            return "I’m unable to provide that information under your current role selection."

        # Extract Subject Name
        # E.g., "class report of physics subject" -> subject = "Physics"
        query_clean = query.lower().replace("view report", "").replace("show report", "").replace("subject report", "") \
                                   .replace("class report", "").replace("for", "").replace("of", "").replace("subject", "") \
                                   .replace("view", "").replace("show", "").replace("history", "").strip()
        
        if not query_clean:
             # If no subject, list available subjects that have reports
             if active_role == 'Vice Principal':
                 reports = Notification.objects.filter(message__startswith="REPORT|")
             else:
                 reports = Notification.objects.filter(receiver_id=faculty_id, message__startswith="REPORT|")
             
             subjects = set()
             for r in reports:
                 parts = r.message.split('|')
                 if len(parts) >= 2: subjects.add(parts[1])
             
             if not subjects:
                 return "No class reports have been submitted yet."
             
             return f"Please specify a subject. Available reports: {', '.join(subjects)}"

        subject_query = query_clean.capitalize() # Basic normalization

        # Filter reports for this advisor and specific subject
        if active_role == 'Vice Principal':
            reports = Notification.objects.filter(
                message__icontains=f"REPORT|{subject_query}|"
            ).order_by('-timestamp')
        else:
            reports = Notification.objects.filter(
                receiver_id=faculty_id, 
                message__icontains=f"REPORT|{subject_query}|"
            ).order_by('-timestamp')

        if not reports.exists():
            return f"No reports found for subject: {subject_query}."

        # Optional extra info for header
        scope_info = ""
        adv = ClassAdvisorship.objects.filter(faculty_id=faculty_id).first()
        if adv:
            scope_info = f" ({adv.department} - Year {adv.year})"

        resp = f"📋 **Class Reports for {subject_query}**{scope_info}\n\n"
        for r in reports:
            parts = r.message.split('|')
            content = parts[2] if len(parts) >= 3 else r.message
            status = " [NEW]" if not r.is_read else ""
            date_str = r.timestamp.strftime("%d %b %Y")
            resp += f"• **{date_str}** (from {r.sender.name}):\n  {content}{status}\n\n"
            
            # Mark as read when viewed
            r.is_read = True
            r.save()

        return resp

    def _handle_class_report(self, faculty_id, subject_query="", active_role=None):
        # Role Check
        if active_role not in ['Teacher', 'Faculty', 'Advisor', 'HOD', 'Vice Principal']:
            return "I’m unable to provide that information under your current role selection."
        try:
            # Authorization and Subject Scope (ERP logic)
            # Vice Principal can view any subject
            if active_role == 'Vice Principal':
                if not subject_query:
                    return "Please specify a subject for the class report. (e.g., 'Class report for Physics')"
                alloc = AssignSubjectFaculty.objects.filter(course__title__icontains=subject_query).first()
                if not alloc:
                    return f"No allocation or course records found for '{subject_query}'."
            else:
                # Find the most relevant allocation for this teacher/subject
                # Using faculty_id directly in filters
                alloc_qs = AssignSubjectFaculty.objects.filter(faculty_id=faculty_id)
                if subject_query:
                    alloc_qs = alloc_qs.filter(course__title__icontains=subject_query)
                
                alloc = alloc_qs.first()
                if not alloc:
                    if subject_query:
                        return f"No allocation found for subject '{subject_query}' for you."
                    return "No subject allocations found for you."

            dept = alloc.department
            batch = alloc.batch
            section = alloc.section
            course = alloc.course
            
            students = StudentDetails.objects.filter(department=dept, batch=batch, section=section)
            marks = AssessmentMark.objects.filter(student__in=students, assessment__course=course)
            
            if not marks.exists():
                return f"No assessment marks available for {course.title} in {dept.Department if dept else 'N/A'} (Batch: {batch}, Section: {section})."
            
            stats = marks.aggregate(avg=Avg('marks_raw'), highest=Max('marks_raw'), lowest=Min('marks_raw'))
            
            resp = f"📊 **ERP Class Performance: {course.title}**\n"
            resp += f"📍 **Scope**: {dept.Department if dept else 'N/A'} - Batch {batch} (Sec: {section})\n"
            resp += f"🔹 Average: {float(stats['avg'] or 0):.1f}\n"
            resp += f"🔹 Highest: {float(stats['highest'] or 0)}\n"
            resp += f"🔹 Lowest: {float(stats['lowest'] or 0)}\n\n"

            def get_gender_report(gender_label, gender_db_val, students_qs, target_course):
                gender_group = students_qs.filter(gender__iexact=gender_db_val)
                gender_marks = AssessmentMark.objects.filter(student__in=gender_group, assessment__course=target_course).order_by('-marks_raw')
                
                if not gender_marks.exists():
                    return f"**{gender_label} Performance:** No data.\n\n"

                g_avg = gender_marks.aggregate(Avg('marks_raw'))['marks_raw__avg']
                g_total = gender_group.count()
                
                top_3 = gender_marks[:3]

                report = f"**{gender_label} Performance ({g_total} students):**\n"
                report += "Top Scorers:\n"
                for m in top_3:
                    report += f"- {m.student.name} ({m.student.reg_no}): {m.marks_raw}\n"
                
                report += f"Average: {float(g_avg or 0):.1f}\n\n"
                return report

            resp += get_gender_report("Boys", "Male", students, course)
            resp += get_gender_report("Girls", "Female", students, course)
            
            return resp
        except Exception as e:
            return f"Error generating class report: {str(e)}"

    def _handle_marks_chart(self, faculty_id, student_identifiers, query, active_role):
        """
        Handles requests for student marks in a chart format strictly using active_role.
        """
        try:
            # Filter students by identifiers
            students = StudentDetails.objects.filter(reg_no__in=student_identifiers)
            
            try:
                # Vice Principal bypasses connection checks
                if active_role == 'Vice Principal':
                    pass # Keep all filtered students
                else:
                    faculty_info = self._get_faculty_info(faculty_id)
                    if faculty_info:
                        if active_role == 'HOD':
                            students = students.filter(department=faculty_info.department)
                        elif active_role in ['Advisor', 'CA', 'Teacher', 'Faculty']:
                            students = students.filter(ca_id=str(faculty_info.id), department=faculty_info.department)
                        elif active_role == 'Mentor':
                            students = students.filter(mentor_id=str(faculty_info.id), department=faculty_info.department)
                        else:
                            return "I’m unable to provide that information under your current role selection."
                    else:
                        return "⚠️ Access Denied: Faculty record not found."
            except:
                if active_role != 'Vice Principal':
                    return "I’m unable to provide that information under your current role selection."
            
            if not students.exists():
                return "Student(s) not found or I’m unable to provide that information under your current role selection."

            query_lower = query.lower()
            
            # Identify Subject/Assessment Mentioned
            # We'll check AssessmentNames and CourseTitles
            target_label = None
            
            potential_assessments = Assessment_master.objects.values_list('Assessmentname', flat=True).distinct()
            potential_courses = Course.objects.values_list('title', flat=True).distinct()
            
            all_labels = sorted(list(set(potential_assessments) | set(potential_courses)), key=len, reverse=True)
            
            for label in all_labels:
                if label and label.lower() in query_lower:
                    target_label = label
                    break

            # RBAC and Queryset filtering
            marks = AssessmentMark.objects.filter(student__in=students)
            
            if target_label:
                # Filter marks that match the label in either assessment name or course title
                marks = marks.filter(Q(assessment__Assessmentname__icontains=target_label) | Q(assessment__course__title__icontains=target_label))

            if not marks.exists():
                return f"No assessment marks found for '{target_label or 'any subject'}' for the specified student(s)."

            # Format Chart Data
            if len(students) == 1:
                # Single student: show breakdown of their marks
                student = students[0]
                chart_data = {}
                for m in marks.filter(student=student):
                    label = m.assessment.Assessmentname if m.assessment else (m.assessment.course.title if m.assessment and m.assessment.course else "Unknown")
                    chart_data[label] = float(m.marks_raw or m.marks or 0)
                
                return {
                    "text": f"📊 Assessment Marks for {student.name} ({student.reg_no})",
                    "type": "chart",
                    "data": chart_data
                }
            else:
                # Multiple students: show comparison for the specific target
                if not target_label:
                    # Comparisons without a specific subject use average raw marks
                    chart_data = {}
                    for s in students:
                        avg_calc = marks.filter(student=s).aggregate(Avg('marks_raw'))['marks_raw__avg']
                        if avg_calc is not None:
                            chart_data[f"{s.name} ({s.reg_no})"] = round(float(avg_calc), 1)
                    
                    return {
                        "text": f"📊 Average Performance Comparison (All Assessments)",
                        "type": "chart",
                        "data": chart_data
                    }
                else:
                    # Comparison for a specific assessment/course
                    chart_data = {f"{m.student.name} ({m.student.reg_no})": float(m.marks_raw or m.marks or 0) for m in marks}
                    return {
                        "text": f"📊 Comparison for {target_label}",
                        "type": "chart",
                        "data": chart_data
                    }

        except Exception as e:
            return f"Error in marks processing: {str(e)}"

    def _get_faculty_info(self, faculty_id):
        """
        Robust helper to find faculty record across databases and handle ID inconsistencies.
        """
        try:
            # 1. ERP ID lookup
            f = FacultyManagementGeneralInformation.objects.filter(faculty_id=faculty_id).first()
            if f: return f

            # 2. ERP PK lookup
            try:
                pk_val = int(faculty_id)
                f = FacultyManagementGeneralInformation.objects.filter(id=pk_val).first()
                if f: return f
            except: pass

            # 3. Approval System Fallback + Name Bridge
            from django.db import connections
            with connections['approval_system'].cursor() as cursor:
                cursor.execute("SELECT username FROM control_room_user WHERE Employee_id = %s OR username = %s LIMIT 1", [faculty_id, faculty_id])
                row = cursor.fetchone()
                if row and row[0]:
                    name = row[0].strip()
                    # Bridge: Use name from approval DB to find ERP info
                    f = FacultyManagementGeneralInformation.objects.filter(name__iexact=name).first()
                    return f
        except Exception as e:
            print(f"Robust faculty lookup error: {str(e)}")
        return None

