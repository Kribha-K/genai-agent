import pandas as pd
import sqlite3
import os

dataset_folder = "datasets"

db_path = "db/ecommerce.db"

os.makedirs("db", exist_ok=True)

conn = sqlite3.connect(db_path)

file_table_map = {
    "product_ad_sales.csv": "product_ad_sales",
    "product_total_sales.csv": "product_total_sales",
    "product_eligibility.csv": "product_eligibility"
}

for filename, table_name in file_table_map.items():
    file_path = os.path.join(dataset_folder, filename)

  
    df = pd.read_csv(file_path)

    df.to_sql(table_name, conn, if_exists="replace", index=False)

    print(f"Loaded {filename} into table `{table_name}`")

conn.close()
print("All tables created successfully.")

