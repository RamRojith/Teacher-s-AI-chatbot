from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Faculty, Student, Notification
from .chatbot_logic import ERPBot # We'll move the logic here

from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from django.db import connections
from django.contrib.auth.hashers import check_password

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    # 1. Try External Approval System Database
    try:
        with connections['approval_system'].cursor() as cursor:
            # Fetch ALL role entries for this user (same Employee_id can have multiple roles)
            cursor.execute("""
                SELECT u.password, u.Employee_id, u.username, r.role, u.id
                FROM control_room_user u
                LEFT JOIN control_room_role r ON u.role_id = r.id
                WHERE (u.username = %s OR u.Employee_id = %s) AND u.is_active = 1
            """, [username, username])
            rows = cursor.fetchall()
            
            if rows:
                # Check password using the first entry (all should have same password)
                stored_pass, employee_id, ext_username, _, _ = rows[0]
                
                password_valid = False
                if stored_pass == password:  # Plain text match
                    password_valid = True
                else:
                    try:
                        password_valid = check_password(password, stored_pass)
                    except:
                        password_valid = False
                
                if password_valid:
                    # Collect all roles for this Employee_id
                    all_roles = []
                    for row in rows:
                        role_name = row[3]
                        if role_name:
                            all_roles.append(role_name)
                    
                    # Determine primary role (highest priority)
                    # Priority: HOD > Advisor > Mentor > Faculty > Teacher > Staff
                    role_priority = {
                        'Vice Principal': 0,
                        'HOD': 1,
                        'Advisor': 2,
                        'Mentor': 3,
                        'Faculty': 4,
                        'Teacher': 5,
                        'Staff': 6
                    }
                    
                    primary_role = 'Faculty'  # Default
                    if all_roles:
                        sorted_roles = sorted(all_roles, key=lambda r: role_priority.get(r, 99))
                        primary_role = sorted_roles[0]
                    
                    # CRITICAL: Fetch faculty name from ERP system (same table chatbot uses)
                    # Try multiple lookup strategies to ensure we find the record
                    from .models import FacultyManagementGeneralInformation
                    from django.db.models import Q
                    
                    faculty_name = None
                    try:
                        # Strategy 1: By employee_id (faculty_id field)
                        faculty_record = FacultyManagementGeneralInformation.objects.filter(faculty_id=employee_id).first()
                        
                        # Strategy 2: By primary key if employee_id is numeric
                        if not faculty_record:
                            try:
                                emp_pk = int(employee_id)
                                faculty_record = FacultyManagementGeneralInformation.objects.filter(id=emp_pk).first()
                            except (ValueError, TypeError):
                                pass
                        
                        # Extract and validate name
                        if faculty_record and faculty_record.name:
                            faculty_name = faculty_record.name.strip()
                            if not faculty_name:  # Empty after strip
                                faculty_name = None
                    except Exception as lookup_err:
                        print(f"Faculty name lookup error for employee_id {employee_id}: {lookup_err}")
                    
                    # Fallback to username from control_room_user only if no ERP record found
                    if not faculty_name:
                        faculty_name = ext_username or None
                    
                    # AUTHENTICATION FAILURE: Name is mandatory
                    if not faculty_name:
                        return Response({
                            'error': f'Authentication Error: Unable to retrieve profile information for ID {employee_id}. Please contact administrator.'
                        }, status=500)
                    
                    return Response({
                        'faculty_id': employee_id,
                        'name': faculty_name,
                        'role': primary_role,
                        'all_roles': all_roles
                    })
    except Exception as e:
        print(f"External login error: {e}")

    # 2. Fallback to local Django auth (for admin/test accounts)
    user = authenticate(username=username, password=password)
    if user:
        return Response({
            'faculty_id': user.id,
            'name': user.name,
            'role': user.role,
            'all_roles': [user.role]
        })
    
    return Response({'error': 'Invalid credentials'}, status=401)

# Standard Django View (Alternative to DRF)
@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        query = data.get('query')
        faculty_id = data.get('faculty_id')
        role = data.get('role')
        all_roles = data.get('all_roles', [role] if role else [])
        
        bot = ERPBot()
        # Session-based greeting tracking
        greeted_key = f'greeted_{faculty_id}'
        is_first = not request.session.get(greeted_key, False)
        
        response_text = bot.process_query(query, faculty_id, role, all_roles=all_roles, is_first_message=is_first)
        
        if is_first:
            request.session[greeted_key] = True

        return JsonResponse({'response': response_text})

# DRF version (Recommended for cleaner code)
class ChatView(APIView):
    # permission_classes = [IsAuthenticated] # Uncomment once auth is integrated
    
    def post(self, request):
        query = request.data.get('query')
        faculty_id = request.data.get('faculty_id')
        role = request.data.get('role')
        all_roles = request.data.get('all_roles', [role] if role else [])
        
        bot = ERPBot()
        # Session-based greeting tracking
        greeted_key = f'greeted_{faculty_id}'
        is_first = not request.session.get(greeted_key, False)
        
        response_text = bot.process_query(query, faculty_id, role, all_roles=all_roles, is_first_message=is_first)
        
        if is_first:
            request.session[greeted_key] = True

        return Response({'response': response_text})

from django.utils import timezone

class NotificationView(APIView):
    def get(self, request):
        faculty_id = request.query_params.get('faculty_id')
        # Determine if user is Vice Principal
        is_vp = False
        user = Faculty.objects.filter(id=faculty_id).first() or \
               Faculty.objects.filter(username=faculty_id).first()
        if user and user.role == 'Vice Principal':
            is_vp = True

        # Using Django ORM instead of raw query
        if is_vp:
            # Vice Principal sees all relevant academic reports/notifications
            notifications = Notification.objects.all().select_related('sender', 'student')
        else:
            notifications = Notification.objects.filter(
                receiver_id=faculty_id, 
                is_read=False
            ).select_related('sender', 'student')
        
        data = []
        for n in notifications:
            # Convert to local time before formatting
            local_time = timezone.localtime(n.timestamp)
            data.append({
                'id': n.id,
                'sender_name': n.sender.name,
                'student_name': n.student.name if n.student else 'General',
                'message': n.message,
                'timestamp': local_time.strftime("%I:%M %p | %m/%d/%Y")
            })
        return Response(data)

    def post(self, request):
        notification_ids = request.data.get('ids', [])
        Notification.objects.filter(id__in=notification_ids).update(is_read=True)
        return Response({'status': 'success'})
