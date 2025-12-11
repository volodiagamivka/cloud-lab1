from flask import request, jsonify
from my_project.auth.service.AggregateService import AggregateService

aggregate_service = AggregateService()


def aggregate_column():
    table_name = request.args.get('table_name')
    column_name = request.args.get('column_name')
    operation = request.args.get('operation')

    if not table_name or not column_name or not operation:
        return jsonify({'error': 'Missing required parameters'}), 400

    result = aggregate_service.get_aggregate_result(table_name, column_name, operation)

    if result is None:
        return jsonify({'error': 'No result found or invalid query'}), 404

    return jsonify({'result': result}), 200
