from flask import Flask, render_template, request, jsonify, redirect
import boto3
import botocore
from datetime import datetime
import json

app = Flask(__name__)

#for docker container runs
#ENDPOINT_URL = "http://host.docker.internal:4566"
ENDPOINT_URL = "http://localhost:4566"
#from variables.tf
bucket_name = "assign-3-bucket-adh"
#from main.tf
table_name = 'clowder'

#from provider.tf
s3_client = boto3.client('s3', region_name="us-east-1", endpoint_url = ENDPOINT_URL,aws_access_key_id="test",aws_secret_access_key="test")
dynamo_client = boto3.client('dynamodb', region_name="us-east-1", endpoint_url = ENDPOINT_URL,aws_access_key_id="test",aws_secret_access_key="test")

s3 = boto3.resource('s3', region_name="us-east-1", endpoint_url = ENDPOINT_URL,aws_access_key_id="test",aws_secret_access_key="test")
bucket = s3.Bucket(bucket_name)

dynamo = boto3.resource('dynamodb', region_name="us-east-1",endpoint_url = ENDPOINT_URL,aws_access_key_id="test",aws_secret_access_key="test")
table = dynamo.Table(table_name)


#HELPER FUNCTIONS
def parse_update_expression_helper(json_dict):
    update_expression = ""
    update_values = {}
    
    for key,value in json_dict.items():
        rename_key = ":" +str(key)

        update_expression += " " + str(key) + " = " + rename_key + ","
      
        update_values[rename_key] = value

    update_expression_no_comma = "SET " + update_expression[:-1]
    
    return update_expression_no_comma, update_values
    
def check_in_database(id):
    response = table.get_item(
    Key={'Clowder_Id': id})
    if 'Item' in response:
        return True
    else:
        return False

def check_in_bucket(id):
    try:
        s3_client.head_object(Bucket=bucket_name,Key=id)
        return True
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False

def return_from_bucket_dict(id):
    response = s3_client.get_object(
    Bucket = bucket_name,
    Key=id)
    
    json_data = json.loads(response['Body'].read().decode('utf-8'))
    
    return json_data

def return_from_database_dict(id):
    response = dynamo_client.get_item(
        TableName = table_name,
        Key={'Clowder_Id': {'S':id}})

    return response['Item']


# REST API
@app.route('/<string:id>', methods=['GET'])
def start(id):

    if id == 'all':
        # add code to return json all items
        pass
    
    #Sending a GET request with incorrect parameters returns the appropriate response
    try:
        int(id)
    except:
        return jsonify (Error = "Please enter a numeric Clowder ID"), 400

    response = dynamo_client.get_item(TableName = table_name,
    Key={'Clowder_Id': {'S':id}})
    
   #Sending a GET request that finds no results returns the appropriate response
    if not 'Item' in response:
        return jsonify (Error = "Clowder Id Not in Database"), 401
    
    #Sending a GET request with appropriate parameters returns expected JSON from the database    
    else:
        #s3 check in here to avoid key error
        response_bucket = s3_client.get_object(
        Bucket = bucket_name,
        Key=id)
    
        mod_date = response_bucket['LastModified']
        return jsonify(Clowder_Information_DB = response['Item'], s3_data = return_from_bucket_dict(id),s3_Modified_Date=mod_date), 201


@app.route('/', methods=['GET','POST'])
def post():
    #Sending a GET request with no parameters returns the appropriate response
    if request.method == 'GET':
        return render_template('post.html') , 200

    name = request.form.get('name')
    id = request.form.get('id')
    
    #- Sending a POST request results in the JSON body being stored as an item in the database, and an object in an S3 bucket
    #- Sending a duplicate POST request returns the appropriate response
    id_check = check_in_database(id)
    
    if id_check:
        return jsonify (Error = "Clowder ID already exists. Please select a new id, or add /<Clowder_Id> to the above url to see clowder info."), 403
    
    date = str(datetime.now())    
 
    clowder = {'Clowder_Id':{'S':id},
               'Clowder_Name':{'S':name},
               'Entry_Date' :{'S':date}
               }
               

    json_string_clowder = json.dumps(clowder,default=str)
    
    response = dynamo_client.put_item(
        TableName = table_name,
        Item = clowder)

    response_bucket = s3_client.put_object(
        Body=json_string_clowder,
        Bucket=bucket_name,
        Key=id)
        
    if not check_in_bucket(id): 
        return jsonify(Bucket_Error="Error uploading to s3"), 501
    
    new_page = "/"+id
    
    return redirect(new_page), 201


#curl -X PUT http://127.0.0.1:5000/update/1  -H "Content-Type: application/json" -d '{"Clowder_Name": "new_name", "cat_info":{"cat_name":"Baxter","gender":"male"}}'
@app.put('/update/<string:id>')
def update_clowder_info(id):
#- Sending a PUT request that targets an existing resource results in updates to the appropriate item in the database and object in the S3 bucket
#- Sending a PUT request with no valid target returns the appropriate response
    
    id_check = check_in_database(id)
    
    if id_check:
    
        new_clowder_info = request.get_json(silent=True)
        if new_clowder_info:
            new_clowder_info['Entry_Date'] = str(datetime.now()) #no datetime dtype in dynamodb 
            
            ue,eav = parse_update_expression_helper(new_clowder_info)
     
            response = table.update_item(
                Key={'Clowder_Id': id},
                UpdateExpression = ue,
                ExpressionAttributeValues=eav,
                ReturnValues = 'ALL_NEW'
                )
            
            #no update in s3, overwrites
            json_string_clowder = json.dumps(return_from_database_dict(id),default=str)

            response_bucket = bucket.put_object(
                Body=json_string_clowder,
                Key=id)
                
            return jsonify(New_Clowder_info = return_from_database_dict(id), s3_data = return_from_bucket_dict(id)),202
        
        else:
            return jsonify(Error='No updates provided'), 403

    else:
        return jsonify(Error="No such ID in database"),404

#curl -i -H "Content-Type: application/json" -X DELETE http://127.0.0.1:5000/delete/1
@app.delete('/delete/<string:id>')
def return_delete_clowder(id):
#- Sending a DELETE request results in the appropriate item being removed from the database and object being removed from the S3 bucket
#- Sending a DELETE request with no valid target returns the appropriate response
    id_check = check_in_database(id)
    
    if not id_check:
        return jsonify(Error = "No such ID in database"), 404
    
    response = table.delete_item(
                Key={'Clowder_Id': id},
                ReturnValues = 'ALL_OLD'
                )
    response_bucket = bucket.delete_objects(
        Delete={
            'Objects': [{'Key': id}]
                }
            )
    
    return jsonify(Deleted_Clowder_Info_DB = response['Attributes'], Deleted_Clowder_Info_s3 = response_bucket['Deleted']  ),202

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)