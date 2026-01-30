import requests
import json

BASE_URL = "http://127.0.0.1:8001/api"

def test_migration():
    print("--- 1. Testing Login ---")
    login_data = {"username": "mentor1", "password": "pass123"}
    try:
        login_res = requests.post(f"{BASE_URL}/login/", json=login_data)
        if login_res.status_code == 200:
            user = login_res.json()
            print(f"✅ Login Successful: Welcome {user['name']} ({user['role']})")
            faculty_id = user['faculty_id']
        else:
            print(f"❌ Login Failed: {login_res.status_code} - {login_res.text}")
            return
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return

    print("\n--- 2. Testing Chat (Performance Analysis) ---")
    chat_data = {"query": "analyze 101", "faculty_id": faculty_id}
    try:
        chat_res = requests.post(f"{BASE_URL}/chat/", json=chat_data)
        if chat_res.status_code == 200:
            resp = chat_res.json()
            print("✅ Chat Successful. AI Response received:")
            print("-" * 30)
            print(resp['response'][:500] + "...") # Print first 500 chars
            print("-" * 30)
        else:
            print(f"❌ Chat Failed: {chat_res.status_code} - {chat_res.text}")
    except Exception as e:
        print(f"❌ Chat Error: {e}")

    print("\n--- 3. Testing Notifications ---")
    try:
        notif_res = requests.get(f"{BASE_URL}/notifications/", params={"faculty_id": faculty_id})
        if notif_res.status_code == 200:
            notifs = notif_res.json()
            print(f"✅ Notifications fetched: Found {len(notifs)} unread notifications.")
        else:
            print(f"❌ Notif Failed: {notif_res.status_code}")
    except Exception as e:
        print(f"❌ Notif Error: {e}")

if __name__ == "__main__":
    test_migration()
