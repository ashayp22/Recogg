import json, boto3, base64, email, random, string, csv
from datetime import datetime


def lambda_handler(event, context):
    '''
    First, load in all of the AWS services and their tables/containers/features
    '''
    dynamodb = boto3.resource('dynamodb')
    s3_client = boto3.client('s3')
    rek_client = boto3.client('rekognition')
    accountsTable = dynamodb.Table('accounts')
    classroomsTable = dynamodb.Table('classrooms')

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

    # checking if the message is multipart
    print("Multipart check : ", msg.is_multipart())

    # if message is multipart
    if msg.is_multipart():
        multipart_content = {}
        # retrieving form-data
        for part in msg.get_payload():
            multipart_content[part.get_param('name', header='content-disposition')] = part.get_payload(decode=True)

        '''
        Get Data from the Request
        '''

        try:
            username = json.loads(multipart_content["Account"])["username"]
            password = json.loads(multipart_content["Account"])["password"]
        except:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": True, "message": "Incorrect Data in the Request, Please Try Again!"})
            }

        '''
        Now, we can delete every classroom. We first need to get all of the uids.
        '''

        all_accounts = accountsTable.scan()["Items"]
        all_uids = None

        for a in all_accounts:
            if a["username"] == username:  # found the item
                all_uids = a["classes"]  # got the uid for each class
                break

        # the username passed in was incorrect and no uids were found
        if all_uids is None:
            return {
                'statusCode': 200,
                'body': json.dumps({"error": False, "message": "Incorrect username, please try again!"})
            }

        # next, delete each classroom and its saved data
        for u in all_uids:
            # delete from the classroom table
            result = classroomsTable.delete_item(
                Key={
                    'uid': u,
                },
            )

            # bad response
            if result['ResponseMetadata']['HTTPStatusCode'] != 200:
                return {
                    'statusCode': result['ResponseMetadata']['HTTPStatusCode'],
                    'body': json.dumps({"error": True, "message": "There has been an error deleting the account"})
                }

            # delete attendance from s3
            s3 = boto3.resource('s3')
            s3.Object('classattendance', u + '.csv').delete()

        # finally, delete the account from dynamodb
        result = accountsTable.delete_item(
            Key={
                'username': username,
                'password': password
            },
        )

        if result['ResponseMetadata']['HTTPStatusCode'] != 200:
            return {
                'statusCode': result['ResponseMetadata']['HTTPStatusCode'],
                'body': json.dumps({"error": True, "message": "There has been an error deleting the account"})
            }

        # good response
        return {
            'statusCode': 200,
            'body': json.dumps({"error": False, "message": "The account has been deleted!"})
        }

    else:
        # on upload failure
        return {
            'statusCode': 500,
            'body': json.dumps({"error": True, "message": "Data is not multipart!"})
        }


