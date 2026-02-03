import os
import django
import sys

# Setup Django environment
sys.path.append(r'c:\Users\ramro\OneDrive\Documents\chatbot for teacher')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from chatbot.chatbot_logic import ERPBot

def test_actual_isolation():
    bot = ERPBot()
    faculty_id = 1611
    student_reg = "953625243001"
    
    print(f"Testing Faculty {faculty_id} querying Student {student_reg}")
    
    # Test as Teacher
    response = bot.process_query(f"Performance of {student_reg}", faculty_id, role='Teacher')
    print("\n--- Teacher Role Response ---")
    print(response)

if __name__ == "__main__":
    test_actual_isolation()
