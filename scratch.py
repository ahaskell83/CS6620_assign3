from flask import Flask, request, jsonify
import datetime
from dateutil.relativedelta import relativedelta

def helper_date_parser(date_string):
    try:
        us_format = '%m/%d/%Y'
        return datetime.datetime.strptime(date_string,us_format).date()
    except ValueError:
        py_format = '%Y-%m-%d'
        return datetime.datetime.strptime(date_string,py_format).date()

#relative import issue with test code
class Clowder():
    clowder = {}

    def __init__(self,name):
        self.clowder_name = name
        self.clowder_dict = {self.clowder_name: self.clowder}
        
    def get_clowder_dict(self):
        clowder_dict = {}
        clowder_dict_all = {}
        for key, value in self.clowder.items():
            clowder_dict[key] = [value[0].info_dict, value[1]]
        clowder_dict_all[self.get_clowder_name()] = clowder_dict
        return clowder_dict_all
    
    def get_member_info(self,name):
        return self.clowder[name]
        
    def get_clowder_name(self):
        return self.clowder_name

app = Flask(__name__)
    
clowders = {}

@app.route("/clowders",methods=["GET"])
def return_all_clowders():
    return jsonify(Clowders =list(clowders.keys())), 200

@app.route("/clowders/<string:clowder_name>",methods=["GET"])
def return_named_clowders(clowder_name):
    if clowder_name not in clowders:
        return jsonify (Error = "Please enter a valid clowder name"), 400
    else:
        return jsonify(Clowders = clowders[clowder_name]), 200

@app.route('/clowders', methods=['POST'])
def return_post_clowder():
    data = request.get_json()
    name = list(data.keys())[0]
    new_clowder_obj = Clowder(name)
    new_clowder = new_clowder_obj.get_clowder_dict()
    clowders[name] = new_clowder[name]
    return jsonify(Clowder_Name = list(new_clowder.keys())[0], Clowder_Size = len(clowders)), 201

@app.put('/clowders/<string:clowder_name>')
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
    return jsonify (Deleted_Clowder = del_data, Clowders_size = len(clowders)), 203


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=3000) 