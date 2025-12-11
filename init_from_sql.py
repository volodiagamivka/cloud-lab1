import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

def init_database_from_sql():
    
    
    db_host = os.getenv('DB_HOST', 'localhost')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', 'password')
    db_name = os.getenv('DB_NAME', 'hospitalss')
    db_port = int(os.getenv('DB_PORT', '3306'))
    
    
    print(f"connect to {db_host}:{db_port}")
    print(f"database: {db_name}")
    print()
    
    try:
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            port=db_port,
            charset='utf8mb4',
            ssl_verify_cert=False,
            ssl_verify_identity=False
        )
        
        with connection.cursor() as cursor:

            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")

            
            cursor.execute(f"USE {db_name}")
            
            sql_file_path = os.path.join(os.path.dirname(__file__), 'database_schema.sql')
            
            if not os.path.exists(sql_file_path):
                print(f"file not found: {sql_file_path}")
                return False
            
          
            with open(sql_file_path, 'r', encoding='utf-8') as file:
                sql_content = file.read()
            
           
            sql_queries = [query.strip() for query in sql_content.split(';') if query.strip()]
            
            
            
            for i, query in enumerate(sql_queries, 1):
                if query.upper().startswith('USE '):
                    continue  
                
                try:
                    cursor.execute(query)
                    if i % 10 == 0: 
                        
                except Exception as e:
                    print(f"error {i}: {e}")
                    continue
            
            connection.commit()
            
            
            
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall() 
            for table in tables:
                print(f"   - {table[0]}")
            
           
            cursor.execute("SELECT COUNT(*) FROM hospitals")
            hospitals_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM patients")
            patients_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM doctors")
            doctors_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM medications")
            medications_count = cursor.fetchone()[0]
            
    
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"\n error: {e}")
       
        return False

if __name__ == '__main__':
    init_database_from_sql()
