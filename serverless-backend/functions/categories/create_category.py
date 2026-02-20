import json
import boto3
import os
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['CATEGORY_TABLE'])

def handler(event, context):
    """Create a new category"""
    try:
        user_id = event['requestContext']['authorizer']['claims']['sub']
        body = json.loads(event['body'])
        
        if not body.get('name'):
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Category name is required'})
            }
        
        category_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        category = {
            'userId': user_id,
            'categoryId': category_id,
            'name': body['name'],
            'createdAt': timestamp
        }
        
        table.put_item(Item=category)
        
        return {
            'statusCode': 201,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'category': category})
        }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Internal server error'})
        }
