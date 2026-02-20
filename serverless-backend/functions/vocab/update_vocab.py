import json
import boto3
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['VOCAB_TABLE'])

def handler(event, context):
    """Update an existing vocabulary entry"""
    try:
        user_id = event['requestContext']['authorizer']['claims']['sub']
        entry_id = event['pathParameters']['id']
        body = json.loads(event['body'])
        
        # Build update expression
        update_expr = "SET updatedAt = :updatedAt"
        expr_values = {':updatedAt': datetime.utcnow().isoformat()}
        
        if 'word' in body:
            update_expr += ", word = :word"
            expr_values[':word'] = body['word']
        if 'meaning' in body:
            update_expr += ", meaning = :meaning"
            expr_values[':meaning'] = body['meaning']
        if 'synonym' in body:
            update_expr += ", synonym = :synonym"
            expr_values[':synonym'] = body['synonym']
        if 'antonym' in body:
            update_expr += ", antonym = :antonym"
            expr_values[':antonym'] = body['antonym']
        if 'example' in body:
            update_expr += ", example = :example"
            expr_values[':example'] = body['example']
        if 'category' in body:
            update_expr += ", category = :category"
            expr_values[':category'] = body['category']
        
        # Update item
        response = table.update_item(
            Key={'userId': user_id, 'entryId': entry_id},
            UpdateExpression=update_expr,
            ExpressionAttributeValues=expr_values,
            ReturnValues='ALL_NEW'
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'entry': response['Attributes']}, default=str)
        }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Internal server error'})
        }
