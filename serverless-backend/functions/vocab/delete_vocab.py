import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['VOCAB_TABLE'])

def handler(event, context):
    """Delete a vocabulary entry"""
    try:
        user_id = event['requestContext']['authorizer']['claims']['sub']
        entry_id = event['pathParameters']['id']
        
        # Delete item
        table.delete_item(
            Key={'userId': user_id, 'entryId': entry_id}
        )
        
        return {
            'statusCode': 204,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': ''
        }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Internal server error'})
        }
