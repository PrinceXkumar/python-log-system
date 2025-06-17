'''A lightweight Python-based log parsing and tracking system that can efficiently process log entries,
group them by user, count log levels (like INFO, ERROR, WARN),
filter logs by keywords, and maintain a rolling window of recent logs.
'''

from collections import defaultdict, deque
from functools import wraps

logs = [
    "[2025-06-16T10:00:00] INFO user1: Started process",
    "[2025-06-16T10:00:01] ERROR user1: Failed to connect",
    "[2025-06-16T10:00:02] INFO user2: Login successful",
    "[2025-06-16T10:00:03] WARN user3: Low memory",
    "[2025-06-16T10:00:04] ERROR user2: Timeout occurred",
    "[2025-06-16T10:00:05] INFO user1: Retrying connection"
]

user_logs = defaultdict(list)
level_counts = defaultdict(int)
recent_logs = deque(maxlen=3)

def parse_log(func):
    @wraps(func)
    def wrapper(log_str):
        parts = log_str.split(" ", 3)
        log_dict = {
            "timestamp": parts[0].strip("[]"),
            "level": parts[1],
            "user": parts[2].strip(":"),
            "message": parts[3]
        }
        print(" Parsed log:", log_dict)
        return func(log_dict)
    return wrapper

@parse_log
def add_log(log):
    user_logs[log["user"]].append(log)
    level_counts[log["level"]] += 1
    recent_logs.append(log)

def get_user_logs(user):
    return user_logs.get(user, [])

def count_levels():
    return dict(level_counts)

def filter_logs(keyword):
    keyword = keyword.lower()
    return [log for logs in user_logs.values() for log in logs if keyword in log["message"].lower()]

def get_recent_logs():
    return list(recent_logs)

for entry in logs:
    add_log(entry)

print("\n Logs for user1:")
print(get_user_logs("user1"))

print("\n Log level counts:")
print(count_levels())

print("\n Logs containing 'Timeout':")
print(filter_logs("timeout"))

print("\n Recent logs:")
print(get_recent_logs())

