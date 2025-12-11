from my_project.auth.dao.AggregateDAO import AggregateDAO

class AggregateService:
    def __init__(self):
        self.aggregate_dao = AggregateDAO()

    def get_aggregate_result(self, table_name, column_name, operation):
        try:
            return self.aggregate_dao.aggregate_column(table_name, column_name, operation)
        except Exception as e:
            return {'error': str(e)}
