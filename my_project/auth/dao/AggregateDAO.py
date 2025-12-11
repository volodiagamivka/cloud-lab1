from my_project.db_init import db
from sqlalchemy import text


class AggregateDAO:
    @staticmethod
    def aggregate_column(table_name, column_name, operation):

        query = text("CALL AggregateColumn(:table_name, :column_name, :operation, @result)")
        db.session.execute(query, {
            'table_name': table_name,
            'column_name': column_name,
            'operation': operation
        })


        result = db.session.execute(text("SELECT @result")).fetchone()


        return result[0] if result else None
