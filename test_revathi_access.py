"""
Quick test to verify B.Revathi can now access student 953624243079
This simulates what happens when she queries via the chatbot interface.
"""
import os
import django
import sys

sys.path.append(r'c:\Users\ramro\OneDrive\Documents\chatbot for teacher')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_backend.settings')
django.setup()

from chatbot.chatbot_logic import ERPBot

# B.Revathi's employee ID
REVATHI_EMP_ID = 1603  # Correct ID for B.Revathi (PK 5)

bot = ERPBot()

print("Testing B.Revathi's access to student 953624243079...")
print("Role: Teacher (will auto-elevate to CA)")
print("-" * 60)

response = bot.process_query(
    "give information of 953624243079",
    REVATHI_EMP_ID,
    role='Teacher'
)

print("\nChatbot Response:")
print("=" * 60)
print(response)
print("=" * 60)

# Check if the response is successful
if "Access restricted to your assigned subjects only" in response:
    print("\nSTATUS: FAILED - Still showing subject restriction")
    sys.exit(1)
elif "RAMROJITH" in response and ("Registration No" in response or "Academic Marks" in response):
    print("\nSTATUS: SUCCESS - Full student info shown!")
    print("B.Revathi now has CA-level access to this student")
    sys.exit(0)
else:
    print("\nSTATUS: UNCLEAR - Check response above")
    sys.exit(1)
