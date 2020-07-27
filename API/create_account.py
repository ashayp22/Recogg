import json, boto3, base64, email


def lambda_handler(event, context):
    '''
    First, load in all of the AWS services and their tables/containers/features
    '''
    dynamodb = boto3.resource('dynamodb')  # add the aws secret access key
    accountsTable = dynamodb.Table('accounts')

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

        '''
        Get Data from the Request
        '''

        try:
            username = json.loads(multipart_content["Account"])["username"]
            password = json.loads(multipart_content["Account"])["password"]
            organization = json.loads(multipart_content["Account"])["organization"]
        except:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": True, "message": "Incorrect Data in the Request, Please Try Again!"})
            }

        # first, check if an account already exists with this username
        all_accounts = accountsTable.scan()["Items"]
        for a in all_accounts:
            if a["username"] == username:  # username already exists
                return {
                    'statusCode': 500,
                    'body': json.dumps({"error": True, "message": "This account has already been created!"})
                }

        # Next, Add the account to the accounts table in dynamodb

        try:
            accountsTable.put_item(
                Item={
                    'username': username,  # username
                    'password': password,  # encrypted password
                    'organization': organization,  # name of the org
                    'classes': []  # will store dictionaries with the classroom UIDS:
                }
            )

            # good response
            return {
                'statusCode': 200,
                'body': json.dumps({"error": False, "message": "The account has been created!"})
            }

        except:
            return {
                'statusCode': 500,
                'body': json.dumps({"error": True, "message": "Failed to input data!"})
            }
    else:
        # on upload failure
        return {
            'statusCode': 500,
            'body': json.dumps({"error": True, "message": "Data is not multipart!"})
        }
