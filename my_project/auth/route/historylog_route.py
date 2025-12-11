from flask import Blueprint
from my_project.auth.controller.historylog_controller import get_all_logs

history_log_bp = Blueprint('history_log', __name__)


history_log_bp.route('/history/logs', methods=['GET'])(get_all_logs)
