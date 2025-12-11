from my_project.auth.dao.HistoryLogDAO import HistoryLogDAO

class HistoryLogService:
    def __init__(self):
        self.history_log_dao = HistoryLogDAO()

    def get_all_logs(self):
        return self.history_log_dao.get_all_logs()
