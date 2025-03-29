import csv
from typing import List


class CSVService:
    @staticmethod
    def save_to_csv(data: List[List[str]], csv_file: str) -> str:
        if not data:
            return ""

        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(data)

        return csv_file
