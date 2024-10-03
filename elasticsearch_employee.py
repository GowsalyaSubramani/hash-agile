import csv
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError


# Initialize Elasticsearch client
es = Elasticsearch(
    [{'scheme': 'http', 'host': 'localhost', 'port': 9200}],
    basic_auth=('elastic', 's_A0pGy+sJY-Z5OvyO8-') ,
     timeout = 30 # Replace 'your_password' with the actual password
)
try:
    es.ping()
    print("Successfully connected to Elasticsearch!")
except Exception as e:
    print(f"Connection failed: {e}")


# Function to create a collection (index)
def createCollection(p_collection_name):
    if not es.indices.exists(index=p_collection_name):
        es.indices.create(index=p_collection_name)
        print(f"Index '{p_collection_name}' created.")
    else:
        print(f"Index '{p_collection_name}' already exists.")

# Function to index data
def indexData(p_collection_name, p_exclude_column):
    with open(r'C:\Users\Hi\Downloads\Employee Sample Data 1.csv', newline='') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            if p_exclude_column in row:
                del row[p_exclude_column]
            es.index(index=p_collection_name, id=i+1, document=row)
    print(f"Data indexed into '{p_collection_name}', excluding column '{p_exclude_column}'.")

# Function to search by column
def searchByColumn(p_collection_name, p_column_name, p_column_value):
    query = {
        "query": {
            "match": {
                p_column_name: p_column_value
            }
        }
    }
    response = es.search(index=p_collection_name, body=query)
    for hit in response['hits']['hits']:
        print(hit['_source'])

# Function to get employee count
def getEmpCount(p_collection_name):
    count = es.count(index=p_collection_name)['count']
    print(f"Total employees in '{p_collection_name}': {count}")
    return count

# Function to list
def list_documents(p_collection_name):
    response = es.search(index=p_collection_name, body={"query": {"match_all": {}}})
    documents = response['hits']['hits']
    if not documents:
        print(f"No documents found in index '{p_collection_name}'.")
    else:
        print(f"Documents in index '{p_collection_name}':")
        for doc in documents:
            print(f"ID: {doc['_id']}, Source: {doc['_source']}")

# Function to get documentID
def getDocumentIdByEmployeeId(p_collection_name, employee_id):
    response = es.search(index=p_collection_name, body={
        "query": {
            "match": {
                "Employee ID": employee_id
            }
        }
    })
    if response['hits']['total']['value'] > 0:
        for hit in response['hits']['hits']:
            print(f"Found Document ID: {hit['_id']} for Employee ID: {employee_id}")
            return hit['_id']  # Return the Elasticsearch document ID
    else:
        print(f"No employee found with Employee ID {employee_id}")
        return None


# Function to delete employee by ID
def delEmpById(p_collection_name, p_employee_id):
    try:
        es.delete(index=p_collection_name, id=p_employee_id)
        print(f"Employee with ID '{p_employee_id}' deleted from '{p_collection_name}'.")
    except NotFoundError as e:
        print(f"Error: Employee with ID '{p_employee_id}' not found in '{p_collection_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Function to get department facet
def getDepFacet(p_collection_name):
    query = {
        "size": 0,
        "aggs": {
            "group_by_department": {
                "terms": {
                    "field": "Department.keyword"
                }
            }
        }
    }
    response = es.search(index=p_collection_name, body=query)
    buckets = response['aggregations']['group_by_department']['buckets']
    for bucket in buckets:
        print(f"Department: {bucket['key']}, Count: {bucket['doc_count']}")

# Function execution
v_nameCollection = 'hash_gowsalya'  # Use lowercase
v_phoneCollection = 'hash_1234'      # Replace '1234' with your last four digits

createCollection(v_nameCollection)
createCollection(v_phoneCollection)

getEmpCount(v_nameCollection)

indexData(v_nameCollection, 'Department')
indexData(v_phoneCollection, 'Gender')


# Call this function to list documents before trying to delete
list_documents(v_nameCollection)

# Change this to the actual Employee ID you want to delete
employee_id_to_delete = 'E02591'  # Employee ID you want to delete
doc_id = getDocumentIdByEmployeeId(v_nameCollection, employee_id_to_delete)

if doc_id:
    delEmpById(v_nameCollection, doc_id)  # Use the Elasticsearch document ID for deletion


delEmpById(v_nameCollection, 'E02591')

getEmpCount(v_nameCollection)

searchByColumn(v_nameCollection, 'Department', 'IT')
searchByColumn(v_nameCollection, 'Gender', 'Male')
searchByColumn(v_phoneCollection, 'Department', 'IT')

getDepFacet(v_nameCollection)
getDepFacet(v_phoneCollection)
