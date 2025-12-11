import sys
from app import app
from my_project.db_init import db

def init_database_sqlalchemy():
    with app.app_context():
        try:
        
            db.create_all()
        except Exception as e:
            print(f"error: {e}")
            raise

def init_database_from_sql():
 
    try:
        from init_from_sql import init_database_from_sql
        return init_database_from_sql()
    except ImportError:
        print("file not found")
        return False

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--sql':
        success = init_database_from_sql()
        if not success:
            init_database_sqlalchemy()
    else:
        init_database_sqlalchemy()

if __name__ == '__main__':
    main()

