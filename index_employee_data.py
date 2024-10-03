# Import necessary libraries
import csv
from elasticsearch import Elasticsearch

# Initialize Elasticsearch client
es = Elasticsearch(
    [{'scheme': 'http', 'host': 'localhost', 'port': 9200}],
    basic_auth=('elastic', 's_A0pGy+sJY-Z5OvyO8-')  # Replace 'your_password' with the actual password
)


# Create an index (collection) in Elasticsearch
index_name = 'employee_data'
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name)

# Read employee data from CSV and index it
def index_employee_data(csv_file):
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            es.index(index=index_name, id=i+1, document=row)

# Path to your CSV file
csv_file_path = r'C:\Users\Hi\Downloads\Employee Sample Data 1.csv'

# Index the data
index_employee_data(csv_file_path)

print("Data indexed successfully!")
