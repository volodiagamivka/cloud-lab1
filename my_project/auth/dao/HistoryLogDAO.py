from my_project.db_init import db
from sqlalchemy import text


class HistoryLogDAO:
    def get_all_logs(self):
        query = text("SELECT * FROM History_Log ORDER BY timestamp DESC")
        result = db.session.execute(query).fetchall()

        # Перетворення кожного запису в словник
        logs = []
        for row in result:
            logs.append(dict(row._mapping))  # Використовуємо _mapping для доступу до ключів
        return logs
