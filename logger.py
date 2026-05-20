import os
from datetime import datetime


class Logger:
    def __init__(self, log_file_path: str):
        self.__log_file_path = log_file_path

    def log(self, message: str) -> None:
        os.makedirs(os.path.dirname(self.__log_file_path), exist_ok=True)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.__log_file_path, 'a') as f:
            f.write(f"[{timestamp}] {message}\n")

    def load_logs(self) -> list[str]:
        if not os.path.exists(self.__log_file_path):
            return []
        with open(self.__log_file_path, 'r') as f:
            return f.readlines()

    def clear_logs(self) -> None:
        if os.path.exists(self.__log_file_path):
            open(self.__log_file_path, 'w').close()
