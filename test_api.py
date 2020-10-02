from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from pymongo import MongoClient
import json

#set up the flas app
app = Flask(__name__)
api = Api(app)

#using the MongoClient to establish a link with ATLAS using the url
client = MongoClient("mongodb+srv://anidev:1357902468@cluster0.rfnbk.mongodb.net/<dbname>?retryWrites=true&w=majority")

#access the database 'green_deck' via the MongoClient instance
db = client.green_deck

#access the collection 'gd_products' via the database instance
products = db.gd_products

##
#Utility function to process the string passed in the url
#Refer the read.me to understand how urls are passed
#float_attrs are a list of attributes of the product that need type conversion
##

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

##
#Using reqparser to specify special arguments within the URL
#'update' is used in the update operation
#'replacedby' is used in the replace operation
##
parser = reqparse.RequestParser()
parser.add_argument('update')
parser.add_argument('replacedby')

#View, Delete, or Update Product Documents
class Products(Resource):
    
    def get(self, search_key): #view
        d_find = string_util_one(search_key)
        response = products.find_one(d_find)
        if response == None:
            abort(404, message="No Results for the applied filter")
        if '_id' in response.keys():
            del response['_id']
        result = json.dumps({'result': response}, sort_keys=True )
        return result
    
    def delete(self, search_key): #delete
        d_find = string_util_one(search_key)
        del_res = products.delete_one(d_find)
        return '{} product was deleted'.format(del_res.deleted_count)
    
    def put(self, search_key): #update
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
    def post(self, insert_string): #create/insert a new product document
        d_insert = string_util_one(insert_string)
        products.insert_one(d_insert)
        return 'Product was added to the database', 201
    
    def put(self, insert_string): #replace an existing product with a new product.
        d_find = string_util_one(insert_string)
        args = parser.parse_args()
        d_rep = string_util_one(args['replacedby'])
        rep_res = products.replace_one(d_find,d_rep)
        return '{} product was replaced'.format(rep_res.modified_count)

##
## Actually setup the Api resource routing here
##
api.add_resource(Create, '/create/<insert_string>')
api.add_resource(Products, '/products/<search_key>')



if __name__ == '__main__':
        app.run(debug=True)
