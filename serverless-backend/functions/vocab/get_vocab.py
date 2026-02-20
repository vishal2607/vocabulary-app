import json
import boto3
import os
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['VOCAB_TABLE'])

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def handler(event, context):
    """Get all vocabulary entries for the authenticated user"""
    try:
        # Get user ID from Cognito authorizer
        user_id = event['requestContext']['authorizer']['claims']['sub']
        
        # Query parameters for filtering/searching
        query_params = event.get('queryStringParameters') or {}
        search = query_params.get('search', '')
        
        # Query DynamoDB
        response = table.query(
            KeyConditionExpression='userId = :userId',
            ExpressionAttributeValues={
                ':userId': user_id
            }
        )
        
        entries = response.get('Items', [])
        
        # Filter by search term if provided
        if search:
            search_lower = search.lower()
            entries = [
                entry for entry in entries
                if search_lower in entry.get('word', '').lower()
                or search_lower in entry.get('meaning', '').lower()
                or search_lower in entry.get('synonym', '').lower()
            ]
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'entries': entries}, cls=DecimalEncoder)
        }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Internal server error'})
        }
