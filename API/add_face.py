# -*- coding: utf-8 -*-
import json, base64, boto3, email, csv


def lambda_handler(event, context):
    '''
    First, load in all of the AWS services and their tables/containers/features
    '''
    s3_client = boto3.client('s3')  # s3 - for storing files
    dynamodb = boto3.resource('dynamodb')  # dynamodb - for storing json data
    rek_client = boto3.client('rekognition')  # facial rekognition - for facial recognition
    classroomsTable = dynamodb.Table('classrooms')  # table for storing classroom data

    '''
    Now, we format the response into the proper format. The response should be multipart, meaning that it allows for 
    regular json data as well as files.
    '''

    # decoding form-data into bytes
    post_data = base64.b64decode(event['body'])
    # fetching content-type
    content_type = ""

    # the content-type header may be upper case or lowercase - this makes sure that we get the correct
    if 'Content-Type' in event["headers"]:
        content_type = event["headers"]['Content-Type']
    elif 'content-type' in event["headers"]:
        content_type = event["headers"]['content-type']

    # concate Content-Type: with content_type from event
    ct = "Content-Type: " + content_type + "\n"

    # parsing message from bytes
    msg = email.message_from_bytes(ct.encode() + post_data)

    # check to make sure the message is multipart
    if msg.is_multipart():
        multipart_content = {}
        # retrieving form-data
        for part in msg.get_payload():
            multipart_content[part.get_param('name', header='content-disposition')] = part.get_payload(decode=True)

        '''
        Get Data from the Request. Since this is multipart, there is a Metadata JSON value passsed in as well as a file.
        '''

        try:
            uid = json.loads(multipart_content["Metadata"])["uid"]
            filename = json.loads(multipart_content["Metadata"])["filename"]
            label = json.loads(multipart_content["Metadata"])["label"]
            file_multipart = multipart_content["file"]  # Get File from the Request
        except:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": True, "message": "Incorrect Data in the Request, Please Try Again!"})
            }

        '''
        Now, we add the face to the Facial Recognition collection and DynamoDb table
        '''

        collectionId = uid  # set the collection id

        list_response = rek_client.list_collections(MaxResults=100)  # collections

        # create the collection if it doesn't exist
        if collectionId not in list_response['CollectionIds']:
            rek_client.create_collection(CollectionId=collectionId)
        try:
            # now, we add the face
            index_response = rek_client.index_faces(CollectionId=collectionId,
                                                    Image={'Bytes': file_multipart},
                                                    ExternalImageId=label,
                                                    MaxFaces=1,
                                                    QualityFilter="AUTO",
                                                    DetectionAttributes=['ALL'])
        except:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": True, "message": "Error in adding the student, please try again"})
            }

        '''
        Now, we add the file to the list of classrooms
        '''

        # first, check if the student already exists in the classroom
        all_classes = classroomsTable.scan()["Items"]

        # iterate through all classes to see if the
        data = {}
        for a in all_classes:
            if a["uid"] == uid:
                if label in a["students"]:
                    return {
                        'statusCode': 200,
                        'body': json.dumps({"error": False,
                                            "message": "The student image has been saved but not added as a new student!"})
                    }
                break

        # since they do not already exist, add them to the list of students
        result = classroomsTable.update_item(
            Key={
                'uid': uid,  # the key that identifies the item is the uid
            },
            UpdateExpression="SET students = list_append(students, :i)",
            # append the students name to the list of students
            ExpressionAttributeValues={
                ':i': [label],
            },
            ReturnValues="UPDATED_NEW"
        )

        # bad result - return an error
        if result['ResponseMetadata']['HTTPStatusCode'] != 200:
            return {
                'statusCode': result['ResponseMetadata']['HTTPStatusCode'],
                'body': json.dumps({"error": True, "message": "There has been an error adding the UID to the table"})
            }

        # now, we must add the student to the attendance csv
        filename = uid + ".csv"
        bucket = 'classattendance'  # S3 bucket name

        s3_client.download_file(bucket, filename, "/tmp/" + filename)  # download the file
        filename = "/tmp/" + filename  # update the filename

        # next, append the student to the end
        with open(filename, 'a+', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow([label])

        # finally, push to s3
        s3 = boto3.resource('s3')
        s3_bucket = s3.Bucket(bucket)
        file_name = uid + ".csv"
        s3_bucket.upload_file(filename, str(file_name))  # Upload image directly inside bucket

        # return a response
        return {
            'statusCode': result['ResponseMetadata']['HTTPStatusCode'],
            'body': json.dumps(
                {"error": False, "message": "The student image has been saved and added as a new student!"})
        }


    else:
        # on upload failure
        return {
            'statusCode': 500,
            'body': json.dumps({"error": True, "message": "Form is not multipart!"})
        }