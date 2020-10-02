from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from pymongo import MongoClient
import json

app = Flask(__name__)
api = Api(app)

##Set Up Link with MongoDatabase
client = MongoClient("mongodb+srv://anidev:1357902468@cluster0.rfnbk.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client.green_deck
products = db.gd_products

def abort_if_filter_matchless(length):
    if length == 0:
        abort(404, message="No Results for the applied filter")

def string_util_one(query_string):
    s = query_string.split(',')
    d = {}
    float_attrs = ['regular_price_value','offer_price_value']
    for attr in s:
        pair = attr.split('=')
        if pair[0] in float_attrs:
            d[pair[0]] = float(pair[1])
        else:
            d[pair[0]] = pair[1]
    return d

def string_util_two(query_string):
    pass
    

parser = reqparse.RequestParser()
parser.add_argument('update')
parser.add_argument('replacedby')

#View, Delete, or Update Product Documents
class Products(Resource):
    
    def get(self, search_key):
        d_find = string_util_one(search_key)
        response = products.find_one(d_find)
        if response == None:
            abort(404, message="No Results for the applied filter")
        if '_id' in response.keys():
            del response['_id']
        result = json.dumps({'result': response}, sort_keys=True )
        return result
    
    def delete(self, search_key):
        d_find = string_util_one(search_key)
        del_res = products.delete_one(d_find)
        return '{} product was deleted'.format(del_res.deleted_count)
    
    def put(self, search_key):
        d_find = string_util_one(search_key)
        args = parser.parse_args()
        s = args['update'].split(':')
        s[0] = '$'+s[0]
        d_up = string_util_one(s[1])
        d_update = {}
        d_update[s[0]] = d_up
        update_res = products.update_one(d_find,d_update)
        return '{} product was updated'.format(update_res.modified_count)

#Create or Replace Product Documents
class Create(Resource):
    def post(self, insert_string):
        d_insert = string_util_one(insert_string)
        products.insert_one(d_insert)
        return 'Product was added to the database', 201
    
    def put(self, insert_string):
        d_find = string_util_one(insert_string)
        args = parser.parse_args()
        d_rep = string_util_one(args['replacedby'])
        rep_res = products.replace_one(d_find,d_rep)
        return '{} product was updated'.format(rep_res.modified_count)

##
## Actually setup the Api resource routing here
##
api.add_resource(Create, '/create/<insert_string>')
api.add_resource(Products, '/products/<search_key>')



if __name__ == '__main__':
        app.run(debug=True,host='0.0.0.0')
