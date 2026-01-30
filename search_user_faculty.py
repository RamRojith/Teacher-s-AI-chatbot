import MySQLdb

try:
    db = MySQLdb.connect(host="localhost", user="root", passwd="")
    cursor = db.cursor()
    cursor.execute("SELECT TABLE_SCHEMA, TABLE_NAME FROM information_schema.TABLES WHERE TABLE_NAME LIKE '%user%' OR TABLE_NAME LIKE '%faculty%'")
    results = cursor.fetchall()
    for r in results:
        # Filter out system DBs
        if r[0] in ['information_schema', 'mysql', 'performance_schema']:
            continue
        print(f"DB: {r[0]} | Table: {r[1]}")
    db.close()
except Exception as e:
    print(f"Error: {e}")
