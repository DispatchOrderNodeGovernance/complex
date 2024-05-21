import json
import boto3
import os
import time

CACHE_FILE_PATH = '/tmp/cache.json'
CACHE_EXPIRATION_SECONDS = 300  # Set cache expiration time (e.g., 5 minutes)

def fetch_data_from_dynamodb():
    # Initialize a session using Amazon DynamoDB
    dynamodb = boto3.resource('dynamodb')
    
    # Get the table name from environment variables
    table_name = os.environ['CONTRACT_TEMPLATES_TABLE_NAME']
    
    # Select your DynamoDB table
    table = dynamodb.Table(table_name)
    
    # Scan the table
    response = table.scan()
    items = response.get('Items', [])
    
    # Extract the required fields
    result = []
    for item in items:
        result.append({
            'id': float(item.get('id')),
            'total_contract_value': float(item.get('total_contract_value'))
        })
    
    return result

def lambda_handler(event, context):
    current_time = time.time()
    
    # Check if the cache file exists and is not expired
    if os.path.exists(CACHE_FILE_PATH):
        file_modification_time = os.path.getmtime(CACHE_FILE_PATH)
        if current_time - file_modification_time < CACHE_EXPIRATION_SECONDS:
            # Read data from cache file
            with open(CACHE_FILE_PATH, 'r') as cache_file:
                cached_data = json.load(cache_file)
            return {
                'statusCode': 200,
                'body': json.dumps(cached_data)
            }
    
    # Fetch data from DynamoDB and update the cache file
    data = fetch_data_from_dynamodb()
    
    with open(CACHE_FILE_PATH, 'w') as cache_file:
        json.dump(data, cache_file)

    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }
