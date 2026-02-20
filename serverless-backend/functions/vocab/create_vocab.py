import json
import boto3
import os
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['VOCAB_TABLE'])

def handler(event, context):
    """Create a new vocabulary entry"""
    try:
        # Get user ID from Cognito authorizer
        user_id = event['requestContext']['authorizer']['claims']['sub']
        
        # Parse request body
        body = json.loads(event['body'])
        
        # Validate required fields
        if not body.get('word'):
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Word is required'})
            }
        
        # Create entry
        entry_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        entry = {
            'userId': user_id,
            'entryId': entry_id,
            'word': body['word'],
            'meaning': body.get('meaning', ''),
            'synonym': body.get('synonym', ''),
            'antonym': body.get('antonym', ''),
            'example': body.get('example', ''),
            'category': body.get('category', ''),
            'createdAt': timestamp,
            'updatedAt': timestamp
        }
        
        # Save to DynamoDB
        table.put_item(Item=entry)
        
        return {
            'statusCode': 201,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'entry': entry})
        }
    
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Invalid JSON'})
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Internal server error'})
        }
