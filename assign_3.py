from flask import Flask, render_template, request, jsonify
import boto3

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


@app.route('/<string:id>', methods=['GET'])
def start(id):

#Sending a GET request with incorrect parameters returns the appropriate response
    try:
        int(id)
    except:
        return jsonify (Error = "Please enter a numeric Clowder ID"), 400
    

    response = dynamo_client.get_item(
    TableName='clowder',
    Key={'Clowder_Id': {'S': id}},
    ConsistentRead=True)
    

   #Sending a GET request that finds no results returns the appropriate response
    if not 'Item' in response:
        return jsonify (Error = "Clowder Id Not in Database"), 401
    else:
    #Sending a GET request with appropriate parameters returns expected JSON from the database
        return jsonify(Clowder_Information = response['Item']), 201


@app.route('/', methods=['GET','POST'])
def post():
    if request.method == 'GET':
        return render_template('post.html')

    name = request.form.get('name')
    id = request.form.get('id')


    return render_template('post.html')

'''@app.put('/clowders/<string:clowder_name>')
def update_clowder_info(clowder_name):
    new_clowder_info = request.get_json()
    clowders[clowder_name] = new_clowder_info
    return jsonify(New_Clowder_info = new_clowder_info, Clowder_Updated = clowder_name), 202


@app.delete('/clowders/<string:clowder_name>')
def return_delete_clowder(clowder_name):
    if clowder_name not in clowders:
        return jsonify(Error = "Please enter a valid clowder name"), 403
    
    del_data = clowders[clowder_name]
    del clowders[clowder_name]
    return jsonify (Deleted_Clowder = del_data, Clowders_size = len(clowders)), 203'''


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)