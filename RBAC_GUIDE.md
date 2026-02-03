
# Strict Role-Based Access Control (RBAC) Implementation

The chatbot now enforces strict data access policies based on the official ERP assignment records (`AssignSubjectFaculty` table). This ensures that faculty members can only access student data relevant to their specific classes and sections.

## 1. Faculty/Teacher Access Scope
When logged in as a **Teacher** or **Faculty**, your access is automatically restricted to:
- **Assigned Sections only**: If you are assigned to Section A, you cannot query or list students from Section B or C.
- **Assigned Batches only**: You can only access students within the specific batch years (e.g., 2024, 2025) linked to your subjects.
- **Subject-Specific View**: Marks and performance analysis are filtered to show only the subjects you are officially teaching.

## 2. HOD Access Scope
As an **HOD**, your access is governed by your department:
- **Major Department**: Full access to all students, marks, and batches within your primary department.
- **Service Higher-Order Access**: You can access students in other departments (e.g., a Physics HOD viewing CSE students) **only if** your department has faculty assigned to teach subjects in those specific sections.

## 3. Advisor/Mentor Access Scope
- **Class Advisor (CA)**: **FULL UNRESTRICTED ACCESS** to all students in your assigned class, including:
  - Complete student profiles
  - **All subject marks** (not limited to subjects you personally teach)
  - All assessments across all subjects
  - Complete academic performance data
  - *Note: CAs have class-level authority equivalent to HOD-level visibility for their specific class*
- **Mentor**: Full mentorship/performance access to your specific assigned mentees (all subjects)

## 4. Institutional Access
- **Vice Principal**: Universal access across all departments, batches, sections, and students.

## Access Denial Example
If a faculty member attempts to access a student outside their assigned scope, the chatbot will respond with:
> *Access Denied: You are not assigned to [Department Name] - Section [Section Letter].*

---
*Implementation Note: This logic uses the `AssignSubjectFaculty` table as the single source of truth for all teacher-student associations.*
