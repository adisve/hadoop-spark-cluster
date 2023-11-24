import sqlite3
import pandas as pd
from halo import Halo
import sys
import os

class CSVConverter:
    def __init__(self, db_path, db_table_name, chunk_size=10000):
        self.db_path = db_path
        self.db_table_name = db_table_name
        self.chunk_size = chunk_size

    def convert_to_csv(self, output_path):
        spinner = Halo(text=f"Exporting data from {self.db_path} to {output_path} as CSV")
        spinner.start()
        try:
            with sqlite3.connect(self.db_path) as conn:
                for chunk in pd.read_sql_query(f"SELECT * FROM {self.db_table_name};", conn, chunksize=self.chunk_size):
                    chunk.to_csv(output_path, mode='a', index=False, header=not os.path.exists(output_path))
            spinner.succeed("Data exported successfully")
        except Exception as e:
            spinner.fail(f"Error exporting data: {e}")
            raise e

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 scripts/csv_converter.py <path_to_sqlite_db> <database_table_name>")
        sys.exit(1)

    db_path = sys.argv[1]
    db_table_name = sys.argv[2]
    output_path = "./data/output.csv"

    converter = CSVConverter(db_path, db_table_name)
    converter.convert_to_csv(output_path)