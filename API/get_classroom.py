import json, boto3, base64, email


def lambda_handler(event, context):
    '''
    First, load in all of the AWS services and their tables/containers/features
    '''
    dynamodb = boto3.resource('dynamodb')
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

    # if message is multipart
    if msg.is_multipart():
        multipart_content = {}
        # retrieving form-data
        for part in msg.get_payload():
            multipart_content[part.get_param('name', header='content-disposition')] = part.get_payload(decode=True)

        try:
            username = json.loads(multipart_content["Account"])["username"]
        except:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": True, "message": "Incorrect Data in the Request, Please Try Again!"})
            }

        # first, get all of the classroom uids
        all_accounts = accountsTable.scan()["Items"]

        found = False
        classes = None

        for a in all_accounts:
            if a["username"] == username:
                found = True
                classes = a["classes"]
                break

        if not found:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": True, "message": "Incorrect Username!"})
            }

        '''
        Next, get the name of each classroom based on the uid
        '''

        # create a dictionary that maps uids to class names
        class_dict = {}
        for c in classes:
            class_dict[c] = ""

        all_classes = classroomsTable.scan()["Items"]

        for a in all_classes:
            if a["uid"] in class_dict:
                class_dict[a["uid"]] = a["name"]

        return {
            'statusCode': 200,
            'body': json.dumps({"error": False, 'data': class_dict})
        }


    else:
        # on upload failure
        return {
            'statusCode': 500,
            'body': json.dumps({"error": True, "message": "Incorrect Data, Please Try Again!!"})
        }
