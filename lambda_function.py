import json
import boto3
from time import gmtime, strftime
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ContactDatabase')
now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
def lambda_handler(event, context):
    name = event['firstName'] +' '+ event['lastName']
    email = event['email']
    message = event['message']
    source= 'jin.han@wustl.edu'
    receipt = [email]
    response = table.put_item(
        Item={
            'id': name,
            'Time':now,
            'Email':email,
            'Message':message
        })
    client = boto3.client('ses' )  
    response = client.send_email(
        Destination={
            'ToAddresses': receipt
            },
        Message={
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': "Hi, here is a copy of the message you sent to us, you will hear from us soon: "+message,
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': name,
            },
        },
        Source=source,)
# return a properly formatted JSON object
    return {
        'statusCode': 200,
        'body': json.dumps('Your requests have been submitted')
    }
    


 
