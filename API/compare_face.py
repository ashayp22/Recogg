# -*- coding: utf-8 -*-
import json, base64, boto3, email, csv


def lambda_handler(event, context):
    '''
    First, load in all of the AWS services and their tables/containers/features
    '''
    s3_client = boto3.client('s3')
    rek_client = boto3.client('rekognition')
    bucket = 'verifiedimages'  # S3 bucket name
    all_objects = s3_client.list_objects(Bucket=bucket)

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

    # if message is multipart
    if msg.is_multipart():
        multipart_content = {}
        # retrieving form-data
        for part in msg.get_payload():
            multipart_content[part.get_param('name', header='content-disposition')] = part.get_payload(decode=True)

        # Get Data from the Request

        try:
            uid = json.loads(multipart_content["Metadata"])["uid"]
            file_multipart = multipart_content["file"]
            decoded_image = base64.b64decode(file_multipart)
        except:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": True, "message": "Incorrect Data in the Request, Please Try Again!"})
            }

        collectionId = uid  # get the collection id for AWS facial recognition

        # get all collections
        list_response = rek_client.list_collections(MaxResults=100)

        # Check if the collection exists
        if collectionId not in list_response['CollectionIds']:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": True, "found": False,
                                    "message": "No faces have been added. Please add a face and try again."})
            }

        try:
            # match the saved images from the s3 bucket to the image passed in
            match_response = rek_client.search_faces_by_image(CollectionId=collectionId,
                                                              Image={'Bytes': file_multipart},
                                                              MaxFaces=1, FaceMatchThreshold=85)
        except:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": True, "message": "Improper image, please try again"})
            }

        if match_response['FaceMatches']:  # match found
            person_name = match_response['FaceMatches'][0]['Face']['ExternalImageId']

            '''
            Now we update the attendance.
            '''

            # first, we read in the attendance file from s3
            filename = uid + ".csv"
            bucket = 'classattendance'  # S3 bucket name
            s3_client.download_file(bucket, filename, "/tmp/" + filename)  # download the file in a temporary location
            filename = "/tmp/" + filename  # update the filename

            # next, we mark the correspondning date and student cell
            rows = []

            # first, read the csv
            with open(filename, 'r+') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    rows.append(row)

            # now, we add in the x
            c = len(rows[0]) - 1  # this represents the column of the cell that we will be marking

            if c == 0:  # no meeting has been started
                return {
                    'statusCode': 200,
                    'body': json.dumps({"error": False, "found": True, "message": "A meeting hasn't been started",
                                        "name": match_response['FaceMatches'][0]['Face']['ExternalImageId']})
                }

            r = -1  # this represents the row of the cell that we will be marking
            for i in range(1, len(rows)):
                if rows[i][0] == person_name:  # found the row that matches the person in the image's name
                    r = i
                    break

            # we may need to add empty spaces
            if r >= 1:
                while len(rows[r]) < c + 1:  # add an empty space
                    rows[r].append("")

                # mark the cell
                rows[r][c] = "X"

            # overwrite the csv
            with open(filename, 'w+', newline='') as outfile:
                writer = csv.writer(outfile)
                # write for eachrow
                for z in rows:
                    writer.writerow(z)

            # finally, add the file to s3
            s3 = boto3.resource('s3')
            s3_bucket = s3.Bucket(bucket)
            file_name = uid + ".csv"
            s3_bucket.upload_file(filename, str(file_name))  # Upload csv directly inside bucket

            # return a good response
            return {
                'statusCode': 200,
                'body': json.dumps({"error": False, "found": True, "message": "The attendance has been updated",
                                    "name": match_response['FaceMatches'][0]['Face']['ExternalImageId']})
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": True, "found": False, "message": "No face has been found"})
            }
    else:
        # on upload failure
        return {
            'statusCode': 500,
            'body': json.dumps({"error": True, "message": "Incorrect data format, not multipart"})
        }