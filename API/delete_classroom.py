import json, boto3, base64, email, random, string, csv
from datetime import datetime


def lambda_handler(event, context):
    '''
    First, load in all of the AWS services and their tables/containers/features
    '''
    dynamodb = boto3.resource('dynamodb')
    rek_client = boto3.client('rekognition')
    accountsTable = dynamodb.Table('accounts')
    classroomsTable = dynamodb.Table('classrooms')

    '''
    Now, we format the response into the proper format. The response should be multipart, meaning that it allows for 
    regular json data as well as files.
    '''

    # decoding form-data into bytes
    post_data = base64.b64decode(event['body'])
    # fetching content-type
    content_type = ""
    if 'Content-Type' in event["headers"]:
        content_type = event["headers"]['Content-Type']
    elif 'content-type' in event["headers"]:
        content_type = event["headers"]['content-type']

    # concate Content-Type: with content_type from event
    ct = "Content-Type: " + content_type + "\n"

    # parsing message from bytes
    msg = email.message_from_bytes(ct.encode() + post_data)

    # if message is multipart
    if msg.is_multipart():
        multipart_content = {}
        # retrieving form-data
        for part in msg.get_payload():
            multipart_content[part.get_param('name', header='content-disposition')] = part.get_payload(decode=True)

        '''
        Get Data from the Request. Since this is multipart, there is a Metadata JSON value passsed in as well as a file.
        '''

        try:
            uid = json.loads(multipart_content["Account"])["uid"]
            username = json.loads(multipart_content["Account"])["username"]
            password = json.loads(multipart_content["Account"])["password"]
        except:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": True, "message": "Incorrect Data in the Request, Please Try Again!"})
            }

        '''
        Now, we delete the classroom. First, we must remove it from the list of uids associated with the user account
        '''

        result = accountsTable.update_item(
            Key={
                'username': username,
                'password': password
            },
            UpdateExpression="SET classes = list_delete(classes, :i)",
            ExpressionAttributeValues={
                ':i': [uid],
            },
            ReturnValues="UPDATED_NEW"
        )

        # bad response
        if result['ResponseMetadata']['HTTPStatusCode'] != 200:
            return {
                'statusCode': result['ResponseMetadata']['HTTPStatusCode'],
                'body': json.dumps({"error": True, "message": "There has been an error deleting the classroom"})
            }

        '''
        Now, we delete the classroom from the table
        '''

        result = classroomsTable.delete_item(
            Key={
                'uid': uid,
            },
        )

        if result['ResponseMetadata']['HTTPStatusCode'] != 200:
            return {
                'statusCode': result['ResponseMetadata']['HTTPStatusCode'],
                'body': json.dumps({"error": True, "message": "There has been an error deleting the classroom"})
            }

        '''
        Finally, delete the attendance csv from s3
        '''

        s3 = boto3.resource('s3')
        s3.Object('classattendance', uid + '.csv').delete()

        return {
            'statusCode': 200,
            'body': json.dumps({"error": False, "message": "The classroom has been deleted!"})
        }

    else:
        # on upload failure
        return {
            'statusCode': 500,
            'body': json.dumps({"error": True, "message": "Data is not multipart!"})
        }



