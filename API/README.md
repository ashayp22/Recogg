# Recogg - API

###  ###

![Preview]()

type a brief summary here.

### Features

The API has the following functionalities:

* Accurate Facial Recognition using AWS Facial Rekognition
  * Upload User Image and Convert to Facial Encoding
  * Save Facial Encodings to Collections in the Cloud
  * Refer to Previous Facial Encodings to perform Facial Verification
* Read/Write User Data to AWS DynamoDB
  * Create/Delete Organization Accounts, Individual Classrooms, and Students
  * Get Specific Data on Classrooms and Live Attendance
* Read/Write/Get Attendance Data (CSV) from AWS S3
  * Get CSV file
  * Update CSV file based on Facial Verification

### Built With
![Python](https://img.shields.io/badge/python-3.6-blue)

* [Python](https://www.python.org/)
* [Amazon Rekognition](https://aws.amazon.com/rekognition/?blog-cards.sort-by=item.additionalFields.createdDate&blog-cards.sort-order=desc)
* [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)
* [Amazon S3](https://aws.amazon.com/s3/)

## Getting Started

This is an example of how you can get the API running in the cloud using AWS Lambda and AWS API Gateway

### Prerequisites

You need to have the following:

* An AWS account
* Prior knowledge on Python 3.6 and AWS Lambda/AWS API Gateway

### Installation

#### AWS Lambda

![Image](https://github.com/ashayp22/Recogg/blob/master/API/screenshots/pict1.PNG)

1. Download the source code from this repository folder.
2. For each of the Python script files, create a new Lambda Function with the following settings:
   * Language: Python 3.6
   * Timeout: >= 30 seconds
   * Trigger: API Gateway
3. Add an execution role with the following properties:
   * AmazonS3FullAccess
   * AmazonDynamoDBFullAccess
   * AmazonRekognitionFullAccess
   * AWSLambdaBasicExecutionRole

![Image](https://github.com/ashayp22/Recogg/blob/master/API/screenshots/pict2.PNG)

#### DynamoDB

1. Create a table called **accounts** with the following properties:
 * Partition Key: username (String)
 * Sort Key: password (String)
2. Create a table called **classrooms** with the following properties:
 * Partition Key: uid (String)
 
#### S3

1. Create an S3 bucket called classattendance. Leave the options to the default options.

#### API Gateway

![Image](https://github.com/ashayp22/Recogg/blob/master/API/screenshots/pict3.PNG)

1. Create a new regional REST API in the API Gateway console
2. Create a new resource for each of the Lambda Functions with the following properties:
 * Resource Name: Same as the Lambda Function
3. Create a new POST request under each resource with the following properties:
 * Integration Type: Lambda Function
 * Use Lambda Proxy integration: True
 * Lambda Region: Same Region as the Lambda Functions
 * Lambda Function: Select the corresponding Lambda Function
 * Use Default Timeout: True
4. Add the Binary Media Types under the Settings Tab:
 * */*
 * image/jpeg
 * image/png
 * multipart/form-data
 * application/json
 * application/octet-stream
5. Create a new stage and deploy the API for testing

#### Connect to other components

At this point, you should have a functioning API running with an endpoint for each of the lambda functions. You should also have the Lambda Functions connected to data storages, specifically an S3 bucket, two DyanmoDB tables, and AWS Rekognition Collections. Now, you are reading to add the endpoints to the other components so they can call the API.

##### IoT


###### Web Interface


<!-- USAGE EXAMPLES -->
## Usage

Since Recogg was developed as a prototype, we highly encourage you to continue improving what we have created. **Make sure to list us as the original authors, especially if you use any of our code, documentation, or instructions.**

Some examples of how the Recogg API can be expanded:

* Deploy the API using another Cloud Platform
* Add additional security to the API (ex: API keys)
* Add more functionality to the API

## More Information ##

For more information licenses, contributing, errors, and other components, visit the [front of the repository](https://github.com/ashayp22/Recogg).
