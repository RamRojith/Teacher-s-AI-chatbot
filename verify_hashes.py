import MySQLdb
def verify():
    db = MySQLdb.connect(host='localhost', user='root', passwd='', db='rit_approval_system')
    cursor = db.cursor()
    cursor.execute("SELECT username, password FROM control_room_user LIMIT 5")
    for row in cursor.fetchall():
        print(f"User: {row[0]} | Pass: {row[1][:25]}...")
    db.close()

if __name__ == "__main__":
    verify()
