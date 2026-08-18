import csv
from pathlib import Path
from datetime import datetime


class IngestionLogger:

    def __init__(self, metadata_file: str):

        self.metadata_file = Path(metadata_file)

        self.metadata_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.metadata_file.exists():

            with open(
                self.metadata_file,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    "run_id",
                    "dataset_name",
                    "source_type",
                    "source_name",
                    "start_time",
                    "end_time",
                    "records_read",
                    "status",
                    "error_message"
                ])

    def log(
        self,
        run_id,
        dataset_name,
        source_type,
        source_name,
        start_time,
        end_time,
        records_read,
        status,
        error_message=""
    ):

        with open(
            self.metadata_file,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                run_id,
                dataset_name,
                source_type,
                source_name,
                start_time,
                end_time,
                records_read,
                status,
                error_message
            ])
from datetime import datetime


def generate_run_id():

    return datetime.now().strftime(
        "RUN_%Y%m%d_%H%M%S"
    )