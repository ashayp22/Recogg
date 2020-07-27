# -*- coding: utf-8 -*-
import json
import base64
import boto3
import email


def write_to_file(save_path, data):
    with open(save_path, "wb") as f:
        f.write(data)


def lambda_handler(event, context):
    '''
    First, load in all of the AWS services and their tables/containers/features
    '''
    bucket = 'classattendance'  # S3 bucket name

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

        try:
            uid = json.loads(multipart_content["Account"])["uid"]
        except:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": True, "message": "Incorrect Data in the Request, Please Try Again!"})
            }

        '''
        Now, we get the attendance file from s3 and return it
        '''

        # first, download the attendance from s3
        filename = uid + ".csv"
        s3 = boto3.client('s3')
        s3.download_file(bucket, filename, "/tmp/" + filename)

        # next, read the temporary saved file and return it to the user
        csv_path = '/tmp/' + filename
        csv_processed = open(csv_path, 'rb')
        csv_data = csv_processed.read()
        csv_processed.close()

        # good response
        return {
            "isBase64Encoded": True,
            "statusCode": 200,
            "headers": {"content-type": "text/csv"},
            "body": base64.b64encode(csv_data).decode("utf-8")
        }


    else:
        # on upload failure
        return {
            'statusCode': 500,
            'body': json.dumps({"error": True, "message": "Form is not multipart!"})
        }