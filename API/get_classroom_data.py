import json, boto3, base64, email


def lambda_handler(event, context):
    '''
    First, load in all of the AWS services and their tables/containers/features
    '''
    dynamodb = boto3.resource('dynamodb')  # add the aws secret access key
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

        # filename from form-data
        try:
            uid = json.loads(multipart_content["Account"])["uid"]
        except:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": True, 'message': "Improper request"})
            }

        '''
        Now, we just read the classroom table and get the class data based on the uid
        '''

        all_classes = classroomsTable.scan()["Items"]

        data = {}
        for a in all_classes:
            if a["uid"] == uid:
                data["meeting_count"] = str(a["meeting_count"])
                data["name"] = a["name"]
                data["students"] = a["students"]
                data["last_date"] = a["last_date"]
                break

        # no data found
        if data == {}:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": True, 'message': "This classroom doesn't exist"})
            }

        return {
            'statusCode': 200,
            'body': json.dumps({"error": False, 'data': data})
        }


    else:
        # on upload failure
        return {
            'statusCode': 500,
            'body': json.dumps({"error": True, "message": "Incorrect Data, Please Try Again!!"})
        }
