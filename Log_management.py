'''A lightweight Python-based log parsing and tracking system that can efficiently process log entries,
group them by user, count log levels (like INFO, ERROR, WARN),
filter logs by keywords, and maintain a rolling window of recent logs.
'''

from collections import defaultdict, deque
from typing import List, Dict

class LogSystem:
    def __init__(self, capacity: int):

        self.capacity = capacity
        self.logs_by_user = defaultdict(list)
        self.recent_logs = deque(maxlen=capacity)
        self.log_level_counts = defaultdict(int)

    def add_log(self, log_line: str) -> None:

        end_idx = log_line.find("]")
        timestamp = log_line[1:end_idx]

        remainder = log_line[end_idx + 2:]
        level, rest = remainder.split(" ", 1)
        user_id, message = rest.split(":", 1)
        user_id = user_id.strip()
        message = message.strip()

        log = {
            "timestamp": timestamp,
            "level": level,
            "user_id": user_id,
            "message": message
        }

        self.logs_by_user[user_id].append(log)
        self.recent_logs.append(log)
        self.log_level_counts[level] += 1

    def get_user_logs(self, user_id: str) -> List[Dict]:

        return self.logs_by_user.get(user_id, [])

    def count_levels(self) -> Dict[str, int]:

        return dict(self.log_level_counts)

    def filter_logs(self, keyword: str) -> List[Dict]:

        keyword = keyword.lower()
        results = []

        for logs in self.logs_by_user.values():
            for log in logs:
                if keyword in log['message'].lower():
                    results.append(log)

        return results

    def get_recent_logs(self) -> List[Dict]:

        return list(self.recent_logs)


if __name__ == "__main__":
    logs = [
        "[2025-06-16T10:00:00] INFO user1: Started process",
        "[2025-06-16T10:00:01] ERROR user1: Failed to connect",
        "[2025-06-16T10:00:02] INFO user2: Login successful",
        "[2025-06-16T10:00:03] WARN user3: Low memory",
        "[2025-06-16T10:00:04] ERROR user2: Timeout occurred",
        "[2025-06-16T10:00:05] INFO user1: Retrying connection"
    ]


    system = LogSystem(capacity=3)


    for entry in logs:
        system.add_log(entry)


    print("🔹 Logs for user1:")
    for log in system.get_user_logs("user1"):
        print(log)


    print("\n🔹 Log level frequencies:")
    print(system.count_levels())


    print("\n🔹 Logs with keyword 'Timeout':")
    for log in system.filter_logs("timeout"):
        print(log)


    print("\n🔹 Most recent logs:")
    for log in system.get_recent_logs():
        print(log)
