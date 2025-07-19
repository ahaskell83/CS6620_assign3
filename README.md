# CS6620_assign3
# CI/CD pipeline (part 3) - Orchestration and CRUD

### Add functionality to create, read, update, and destroy items in a DynamoDB table and an S3 bucket. 

### Use Localstack to run a mock of AWS as part of your application stack. 

first start localstack containger run_local_stock.sh

### Create two compose files and corresponding shell scripts: one will run the stack until manually stopped, 

### the other will run the tests and exit with a zero status if the tests pass and a non-zero status if the tests fail. 

### Put all relevant files into a repository, and enable automatic and manual runs of the tests using a workflow. 

### Include a README along with instructions for running the stack and tests

- Sending a GET request with appropriate parameters returns expected JSON from the database
- Sending a GET request that finds no results returns the appropriate response
- Sending a GET request with no parameters returns the appropriate response
- Sending a GET request with incorrect parameters returns the appropriate response
- Sending a POST request results in the JSON body being stored as an item in the database, and an object in an S3 bucket
- Sending a duplicate POST request returns the appropriate response
- Sending a PUT request that targets an existing resource results in updates to the appropriate item in the database and object in the S3 bucket
- Sending a PUT request with no valid target returns the appropriate response
- Sending a DELETE request results in the appropriate item being removed from the database and object being removed from the S3 bucket
- Sending a DELETE request with no valid target returns the appropriate response

For each test, the database item and S3 object should match.



### References:
- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html

- https://medium.com/@pushpam.ankit/setting-up-localstack-and-dynamodb-tables-with-docker-and-terraform-44e2811d554d

- https://docs.localstack.cloud/aws/tutorials/s3-static-website-terraform/

- https://docs.localstack.cloud/aws/integrations/infrastructure-as-code/terraform/

- https://github.com/aws-samples/localstack-terraform-test/tree/main

- https://python.plainenglish.io/python-flask-taking-user-input-using-forms-5032bd2a5333

- https://github.com/clinton-pillay7/localstack-tutorial/blob/master/localstack/wsgi.py

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html

- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html

- https://www.fernandomc.com/posts/ten-examples-of-getting-data-from-dynamodb-with-python-and-boto3/

- https://stackoverflow.com/questions/61749489/getting-could-not-connect-to-the-endpoint-url-error-with-boto3-when-deploying

- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.UpdateExpressions.html

- Google AI Overview. Search terms: ["localstack dynamodb docker compose", "terraform dynamodb localstack", "run flask app localstack", "update item dynamodb with python dictionary"]