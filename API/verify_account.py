import json, boto3, base64, email


def lambda_handler(event, context):
    '''
    First, load in all of the AWS services and their tables/containers/features
    '''
    dynamodb = boto3.resource('dynamodb')  # add the aws secret access key

    accountsTable = dynamodb.Table('accounts')

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
            username = json.loads(multipart_content["Account"])["username"]
        except:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": True, "message": "Incorrect Data in the Request, Please Try Again!"})
            }

        # read all of the accounts
        all_accounts = accountsTable.scan()["Items"]

        for a in all_accounts:
            if a["username"] == username:  # check if the username matches
                return {  # return the password
                    'statusCode': 200,
                    'body': json.dumps({"error": False, "username": username, "password": a["password"],
                                        "organization": a["organization"]})
                }

        # bad response
        return {
            'statusCode': 500,
            'body': json.dumps({"error": True, "message": "Incorrect Username!"})
        }

    else:
        # on upload failure
        return {
            'statusCode': 500,
            'body': json.dumps({"error": True, "message": "Incorrect Data, Please Try Again!!"})
        }
