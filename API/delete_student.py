import json, boto3, base64, email, random, string, csv
from datetime import datetime


def lambda_handler(event, context):
    '''
    First, load in all of the AWS services and their tables/containers/features
    '''
    dynamodb = boto3.resource('dynamodb')
    s3_client = boto3.client('s3')
    rek_client = boto3.client('rekognition')
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

        try:
            uid = json.loads(multipart_content["Account"])["uid"]
            name = json.loads(multipart_content["Account"])["name"]
        except:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": True, "message": "Incorrect Data in the Request, Please Try Again!"})
            }

        '''
        First, we delete the student from the dynamodb table
        '''

        result = classroomsTable.update_item(
            Key={
                'uid': uid,
            },
            UpdateExpression="SET students = list_delete(students, :i)",
            ExpressionAttributeValues={
                ':i': [name],
            },
            ReturnValues="UPDATED_NEW"
        )

        # bad response
        if result['ResponseMetadata']['HTTPStatusCode'] != 200:
            return {
                'statusCode': result['ResponseMetadata']['HTTPStatusCode'],
                'body': json.dumps({"error": True, "message": "There has been an error deleting the student"})
            }

        '''
        Now, we delete the face from facial recognition collection
        '''
        collection_id = uid
        maxResults = 100
        response = rek_client.list_faces(CollectionId=collection_id,
                                         MaxResults=maxResults)

        # first, find the face id for every image with the label the same as the student's name
        tokens = True
        face_ids = []
        while tokens:

            faces = response['Faces']

            for face in faces:
                if face["ExternalImageId"] == name:
                    face_ids.append(face['FaceId'])
            if 'NextToken' in response:
                nextToken = response['NextToken']
                response = rek_client.list_faces(CollectionId=collection_id,
                                                 NextToken=nextToken, MaxResults=maxResults)
            else:
                tokens = False

        # delete the faces from facial recognition
        response = rek_client.delete_faces(CollectionId=collection_id,
                                           FaceIds=face_ids)

        # good response
        return {
            'statusCode': 200,
            'body': json.dumps({"error": False, "message": "The student has been deleted!"})
        }

    else:
        # on upload failure
        return {
            'statusCode': 500,
            'body': json.dumps({"error": True, "message": "Data is not multipart!"})
        }





