import MySQLdb

def find_ca_link():
    dbs = ['ramco_academic_system', 'rit_approval_system']
    for db_name in dbs:
        print(f"\n--- Searching in {db_name} ---")
        try:
            db = MySQLdb.connect(host='localhost', user='root', passwd='', db=db_name)
            cursor = db.cursor()
            
            # Find tables with 'student' and 'advisor' or 'ca'
            cursor.execute("SHOW TABLES")
            tables = [t[0] for t in cursor.fetchall()]
            
            for t in tables:
                cursor.execute(f"DESC {t}")
                cols = [c[0].lower() for c in cursor.fetchall()]
                if 'ca' in cols or 'advisor' in cols or 'ca_id' in cols or 'advisor_id' in cols:
                    print(f"Table '{t}' has columns: {cols}")
                
            db.close()
        except Exception as e:
            print(f"Error in {db_name}: {e}")

if __name__ == "__main__":
    find_ca_link()
