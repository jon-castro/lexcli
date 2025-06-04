import csv
import os

from pathlib import Path

csv_base_path = os.getenv("CSV_EXPORT_BASE_PATH")

def export_csv(results):
    csv_path = Path(csv_base_path + "export.csv")
    try:
        with csv_path.open(encoding="utf-8", mode="w", newline="") as cf:
            writer = csv.writer(cf)
            writer.writerow(["caseName", "dateFiled", "url"])
            for item in results:
                case_name = item.get("caseName", "")
                date_filed = item.get("dateFiled", "")
                url = item.get("opinions")[0].get("download_url", "None")
                writer.writerow([case_name, date_filed, url])
    except Exception as e:
        raise e