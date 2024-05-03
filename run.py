import psycopg2

def create_database():
    conn = psycopg2.connect(database='postgres', user='postgres', password='1231', host='localhost')
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)  # Enable autocommit mode
    cur = conn.cursor()
    
    cur.execute("DROP DATABASE IF EXISTS comp9120")
    cur.execute("CREATE DATABASE comp9120")
    
    cur.close()
    conn.close()

def run_schema():
    conn = psycopg2.connect(database='comp9120', user='postgres', password='1231', host='localhost')
    cur = conn.cursor()
    
    with open('FFKSchema.sql', 'r') as file:
        sql_script = file.read()
    cur.execute(sql_script)
    conn.commit()
    
    cur.close()
    conn.close()

create_database()
run_schema()

print("Database and schema setup completed successfully.")