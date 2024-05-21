import json
import boto3
import os

def lambda_handler(event, context):
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
            'id': item.get('id'),
            'total_contract_value': item.get('total_contract_value')
        })
    
    # Return the result as a JSON object
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
