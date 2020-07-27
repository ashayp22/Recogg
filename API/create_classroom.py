import json, boto3, base64, email, random, string, csv
from datetime import datetime
import random


# returns a random uid
def simpleUID(length):
    chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D']
    uid = ""
    for _ in range(length):
        uid += chars[random.randint(0, len(chars) - 1)]
    return uid


# generates a uid
def generateUID():
    global uid_length
    old_uids = []  # all of the uids already created

    while True:
        new_uid = simpleUID(uid_length)
        while new_uid in old_uids:
            new_uid = simpleUID(uid_length)
        old_uids.append(new_uid)
        yield new_uid


uid_length = 6
uid_generate = generateUID()


def lambda_handler(event, context):
    '''
    First, load in all of the AWS services and their tables/containers/features
    '''

    dynamodb = boto3.resource('dynamodb')
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

        # Get Data from the Request

        try:
            username = json.loads(multipart_content["Account"])["username"]
            password = json.loads(multipart_content["Account"])["password"]
            classroom_name = json.loads(multipart_content["Account"])["classroom"]
        except:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": True, "message": "Incorrect Data in the Request, Please Try Again!"})
            }

        '''
        Now, we create the classroom
        '''

        # first, generate a UID for the classroom
        uid = next(uid_generate)

        # next, add the UID to the passed in user's classroom list
        result = accountsTable.update_item(
            Key={
                'username': username,
                'password': password
            },
            UpdateExpression="SET classes = list_append(classes, :i)",
            ExpressionAttributeValues={
                ':i': [uid],
            },
            ReturnValues="UPDATED_NEW"
        )

        # bad response
        if result['ResponseMetadata']['HTTPStatusCode'] != 200:
            return {
                'statusCode': result['ResponseMetadata']['HTTPStatusCode'],
                'body': json.dumps({"error": True, "message": "There has been an error adding the UID to the table"})
            }

        # next, add the UID to table
        try:
            classroomsTable.put_item(
                Item={
                    'uid': uid,
                    'students': [],
                    'name': classroom_name,
                    'meeting_count': 0,
                    'last_date': ""
                }
            )
        except:

            return {
                'statusCode': 500,
                'body': json.dumps({"error": True, "message": "Failed to input data!"})
            }

        # finally, create an csv for the attendance and add it to s3
        filename = "/tmp/" + uid + ".csv"

        with open(filename, 'w+', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["Students"])

        # add to bucket
        bucket = 'classattendance'  # S3 bucket name

        s3 = boto3.resource('s3')
        s3_bucket = s3.Bucket(bucket)
        file_name = uid + ".csv"
        s3_bucket.upload_file(filename, str(file_name))  # Upload csv directly inside bucket

        # good response
        return {
            'statusCode': 200,
            'body': json.dumps({"error": False, "message": "The classroom has been created!"})
        }

    else:
        # on upload failure
        return {
            'statusCode': 500,
            'body': json.dumps({"error": True, "message": "Data is not multipart!"})
        }
