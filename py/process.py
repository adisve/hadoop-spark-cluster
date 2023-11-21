import sqlite3
import csv
import os
from halo import Halo

def export_sqlite_to_csv(database_path, table_name, output_file_path):
    if os.path.exists(output_file_path):
        print(f"{output_file_path} already exists. Skipping database export.")
        return
    try:
        spinner = Halo(text=f'Attempting to connect to database {database_path}')
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        spinner.succeed(f'Successfully connected to database at {database_path}')

        try:
            spinner = Halo(text=f"Fetching all data from {table_name}")
            query = f"SELECT * FROM {table_name}"
            cursor.execute(query)
            spinner.succeed(f'Successfully fetched all data from {table_name}')
            spinner = Halo(text=f'Writing database to {output_file_path} file')

            with open(output_file_path, 'w', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow([i[0] for i in cursor.description])
                for row in cursor:
                    csv_writer.writerow(row)
            spinner.succeed(f'Successfully wrote data to {output_file_path}')
        except Exception as e:
            spinner.fail(f'Failed to fetch/write from {table_name} data to {output_file_path}: {e}')
    except Exception as e:
        spinner.fail(f'Failed to connect to database: {e}')
    finally:
        cursor.close()
        conn.close()

def main():
    database_path = './data/database.sqlite'
    table_name = 'May2015'
    output_file_path = './data/output.csv'

    export_sqlite_to_csv(database_path, table_name, output_file_path)

if __name__ == '__main__':
    main()
