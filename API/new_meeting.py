# -*- coding: utf-8 -*-
import json
import base64
import boto3
import email
from datetime import datetime
import csv


def write_to_file(save_path, data):
    with open(save_path, "wb") as f:
        f.write(data)


def getDate():
    return datetime.today().strftime('%m-%d-%Y')


def lambda_handler(event, context):
    '''
    First, load in all of the AWS services and their tables/containers/features
    '''
    dynamodb = boto3.resource('dynamodb')  # add the aws secret access key
    classroomsTable = dynamodb.Table('classrooms')
    accountsTable = dynamodb.Table('accounts')
    s3_client = boto3.client('s3')

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

    # checking if the message is multipart
    print("Multipart check: ", msg.is_multipart())

    # if message is multipart
    if msg.is_multipart():
        multipart_content = {}
        # retrieving form-data
        for part in msg.get_payload():
            multipart_content[part.get_param('name', header='content-disposition')] = part.get_payload(decode=True)

        try:
            uid = json.loads(multipart_content["Account"])["uid"]
        except:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": True, "message": "Incorrect Data in the Request, Please Try Again!"})
            }

        '''
        First, update S3
        '''

        # increment the meeting count
        result = classroomsTable.update_item(
            Key={'uid': uid},
            UpdateExpression="ADD meeting_count :inc",
            ExpressionAttributeValues={":inc": 1},
            ReturnValues="UPDATED_NEW"
        )

        # bad response
        if result['ResponseMetadata']['HTTPStatusCode'] != 200:
            return {
                'statusCode': result['ResponseMetadata']['HTTPStatusCode'],
                'body': json.dumps({"error": True, "message": "Error starting a new meeting"})
            }

        # update the latest meeting date
        result = classroomsTable.update_item(
            Key={'uid': uid},
            UpdateExpression="SET last_date = :date",
            ExpressionAttributeValues={":date": getDate()},
            ReturnValues="UPDATED_NEW"
        )

        if result['ResponseMetadata']['HTTPStatusCode'] != 200:
            return {
                'statusCode': result['ResponseMetadata']['HTTPStatusCode'],
                'body': json.dumps({"error": True, "message": "Error starting a new meeting"})
            }

        '''
        Next, add the new meeting to the spreadsheet
        '''

        # first, download from s3
        filename = uid + ".csv"

        bucket = 'classattendance'  # S3 bucket name
        s3_client.download_file(bucket, filename, "/tmp/" + filename)
        filename = "/tmp/" + filename  # update the filename

        # next, read the csv

        all_rows = []
        with open(filename, 'r+') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                all_rows.append(row)

        # after that, update the csv
        all_rows[0].append(getDate())  # add the new date

        with open(filename, 'w+', newline='') as outfile:
            writer = csv.writer(outfile)
            # update the csv
            for z in all_rows:
                writer.writerow(z)

        # finally, push to s3
        s3 = boto3.resource('s3')
        s3_bucket = s3.Bucket(bucket)
        file_name = uid + ".csv"
        s3_bucket.upload_file(filename, str(file_name))  # Upload image directly inside bucket

        # good response
        return {
            'statusCode': 200,
            'body': json.dumps({"error": False, "message": "A new meeting has been started!"})
        }


    else:
        # on upload failure
        return {
            'statusCode': 500,
            'body': json.dumps({"error": True, "message": "Form is not multipart!"})
        }
