from flask import Flask, render_template, request, jsonify
import boto3
from datetime import datetime

app = Flask(__name__)

#from provider.tf
ENDPOINT_URL = "http://host.docker.internal:4566"
#from variables.tf
bucket = "assign-3-bucket-adh"
#from main.tf
table_name = 'clowder'

#from provider.tf
s3_client = boto3.client('s3', region_name="us-east-1", endpoint_url = ENDPOINT_URL,aws_access_key_id="test",aws_secret_access_key="test")
dynamo_client = boto3.client('dynamodb', region_name="us-east-1", endpoint_url = ENDPOINT_URL,aws_access_key_id="test",aws_secret_access_key="test")
dynamo = boto3.resource('dynamodb', region_name="us-east-1",endpoint_url = ENDPOINT_URL,aws_access_key_id="test",aws_secret_access_key="test")
table = dynamo.Table(table_name)


def parse_update_expression_helper(json_dict):
    update_expression = ""
    update_values = {}
    
    for key,value in json_dict.items():
        rename_key = ":" +str(key)
        update_expression += " " + str(key) + " = " + rename_key + ","
        
        dtype = type(value)
        if isinstance(dtype, dict):
            update_values[rename_key] = {"M": value}
        elif isinstance(dtype, bool):
            update_values[rename_key] = {"BOOL": value}
        else: #store numbers as strings
            update_values[rename_key] = {"S": value}

    update_expression_no_comma = "SET " + update_expression[:-1]
    
    return update_expression_no_comma, update_values
    

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

    response = table.get_item(
    Key={'Clowder_Id': id})

   #Sending a GET request that finds no results returns the appropriate response
    if not 'Item' in response:
        return jsonify (Error = "Clowder Id Not in Database"), 401
    
    #Sending a GET request with appropriate parameters returns expected JSON from the database    
    else:
        return jsonify(Clowder_Information = response['Item']), 201


@app.route('/', methods=['GET','POST'])
def post():
    #Sending a GET request with no parameters returns the appropriate response
    if request.method == 'GET':
        return render_template('post.html')

    name = request.form.get('name')
    id = request.form.get('id')
    
    response = table.get_item(
    Key={'Clowder_Id': id})
    if 'Item' in response:
        return jsonify (Error = "Clowder ID already exists. Please select a new id, or add /<Clowder_Id> to the above url to see clowder info."), 403
    
    date = str(datetime.now())    

    clowder = {'Clowder_Id':{'S':id},
               'Clowder_Name':{'S':name},
               'Entry_Date' :{'S':date}
               }

    response = dynamo_client.put_item(
        TableName = table_name,
        Item = clowder)

    start(id)
    
    return render_template('post.html',name=name, id=id)

#curl -X PUT http://127.0.0.1:5000/update/1  -H "Content-Type: application/json" -d '{"Clowder_Name": "new_name", "cat_info":{"cat_name":"Baxter","gender":"male"}}'
@app.put('/update/<string:id>')
def update_clowder_info(id):
    
    new_clowder_info = request.get_json(silent=True)
    if new_clowder_info:
        new_clowder_info['Entry_Date'] = str(datetime.now()) #no datetime dtype in dynamodb 
        
        ue,eav = parse_update_expression_helper(new_clowder_info)
        #return jsonify(Expression=ue)
        response = table.update_item(
            Key={'Clowder_Id': id},
            UpdateExpression = ue,
            ExpressionAttributeValues=eav,
            ReturnValues = 'ALL_NEW'
            )
            
       
        return jsonify(New_Clowder_info = response['Attributes'] ),202
    else:
        return jsonify(Error='No updates provided'), 403


'''@app.delete('/clowders/<string:clowder_name>')
def return_delete_clowder(clowder_name):
    if clowder_name not in clowders:
        return jsonify(Error = "Please enter a valid clowder name"), 403
    
    del_data = clowders[clowder_name]
    del clowders[clowder_name]
    return jsonify (Deleted_Clowder = del_data, Clowders_size = len(clowders)), 203'''


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)