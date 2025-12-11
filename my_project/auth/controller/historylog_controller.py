from flask import jsonify
from my_project.auth.service.HistoryLogService import HistoryLogService

history_log_service = HistoryLogService()

def get_all_logs():
    logs = history_log_service.get_all_logs()
    return jsonify(logs), 200
