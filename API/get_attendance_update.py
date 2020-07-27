# -*- coding: utf-8 -*-
import json
import base64
import boto3
import email
import csv


def lambda_handler(event, context):
    '''
    First, load in all of the AWS services and their tables/containers/features
    '''
    s3_client = boto3.client('s3')
    bucket = 'verifiedimages'  # S3 bucket name
    all_objects = s3_client.list_objects(Bucket=bucket)

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

        try:
            # filename from form-data
            uid = json.loads(multipart_content["Account"])["uid"]
        except:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": True, "message": "Incorrect Data in the Request, Please Try Again!"})
            }

        '''
        Now, we figure out which students are here and which students are not based off of the attendance csv.        
        '''

        # first, we read in the attendance and save it temporarily
        filename = uid + ".csv"
        s3_client = boto3.client('s3')
        bucket = 'classattendance'  # S3 bucket name
        s3_client.download_file(bucket, filename, "/tmp/" + filename)
        filename = "/tmp/" + filename  # update the filename

        # next, read the csv
        rows = []
        with open(filename, 'r+') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                rows.append(row)

        # now, we add in the x
        c = len(rows[0]) - 1

        if c == 0:  # no meeting has been started
            return {
                'statusCode': 200,
                'body': json.dumps({"error": False, 'students': []})
            }

        names = []

        # now, we get the names of students whose name is marked for this date
        for i in range(1, len(rows)):
            if len(rows[i]) < c + 1:
                continue
            elif len(rows[i]) == c + 1:
                if rows[i][c] == "X":
                    names.append(rows[i][0])

        # good response
        return {
            'statusCode': 200,
            'body': json.dumps({"error": False, "students": names})
        }


    else:
        # on upload failure
        return {
            'statusCode': 500,
            'body': json.dumps({"error": True, "message": "Incorrect data format, not multipart"})
        }