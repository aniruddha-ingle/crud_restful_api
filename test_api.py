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
    """
    Parameters
    ----------
    query_string : string
        All queries must be string in REST APIs, these queries are held by the
        query string.

    Returns
    -------
    d : dictionary
        All the queries to the mongodb database use filters which accept dictionaries. 
        This utility function accepts a string query and maps it to a dictionary according
        to some conventions stated in the readme.md file.

    """
    if query_string == None:
        abort(400 , 
              message = 'Bad Request: Make sure you have used the correct argument,operation pair. Furthermore, make sure there is no space between the argument and the following equal to sign. Spaces after that are handled.')
    
    #In the above error message arguments refer to any one of the four added arguments
    #E.g. record, filter, update, replacedby
    #Each argument should be immediately followed by the equal to sign
    #E.g. record=
    #However, spaces in the quert after this equal to sign are handled.
    
    s = query_string.split(';')
    d = {}
    float_attrs = ['regular_price_value','offer_price_value']
    for attr in s:
        pair = attr.split(':')
        if pair[0].strip() in float_attrs:
            d[pair[0].strip()] = float(pair[1].strip())
        else:
            d[pair[0].strip()] = pair[1].strip()
    return d

##
#Using reqparser to specify special arguments within the URL
#'record' is used to create a document before inserting it in the database
#'filter' is used to query the database
#'update' is used in the update operation
#'replacedby' is used in the replace operation
##

parser = reqparse.RequestParser()
parser.add_argument('record')
parser.add_argument('filter')
parser.add_argument('update')
parser.add_argument('replacedby')

#View, Delete, or Update Product Documents
class Products(Resource):
    
    def get(self):
        """
        It is important to note that the default status of the GET function is not
        functional for handling spaces in query fields like "name" in the product 
        documents.
        Please specify -X GET after the URL.

        Returns
        -------
        result : json
            A database read is performed based on a string query found in args['filter']
            This result is converted to json and returned.

        """
        args = parser.parse_args()
        search_key = args['filter']
        d_find = string_util_one(search_key)
        response = products.find_one(d_find)
        if response == None:
            abort(404, message="No Results for the applied filter")
        if '_id' in response.keys():
            del response['_id']
        result = json.dumps({'result': response}, sort_keys=True )
        return result
    
    def delete(self): #delete
        """
        Returns
        -------
        "1 product was deleted" iff a product was deleted
        "0 product was deleted" iff a product was not deleted
        """
        args = parser.parse_args()
        search_key = args['filter']
        d_find = string_util_one(search_key)
        del_res = products.delete_one(d_find)
        return '{} product was deleted'.format(del_res.deleted_count)
    
    def put(self): #update
        """
        Returns
        -------
        "1 product was updated" iff a product was deleted
        "0 product was updated" iff a product was not deleted
        """
        args = parser.parse_args()
        search_key = args['filter']
        d_find = string_util_one(search_key)   
        s = args['update'].split('>')
        s[0] = '$'+s[0].strip()
        d_up = string_util_one(s[1])
        d_update = {}
        d_update[s[0]] = d_up
        update_res = products.update_one(d_find,d_update)
        return '{} product was updated'.format(update_res.modified_count)

#Create or Replace Product Documents
class Create(Resource):

    def post(self): #create/insert a new product document
        """
        Returns
        -------
        When a new document is added to mongodb it assigns it with an inbuilt Id
        This id is displayed as confirmation of insert operation.
        """
        args = parser.parse_args()
        insert_string = args['record']
        d_insert = string_util_one(insert_string)
        in_res = products.insert_one(d_insert)
        return 'Added Product has ID {}'.format(in_res.inserted_id), 201
    
    def put(self): #replace an existing product with a new product.
        """
        Returns
        -------
        "1 product was replaced" iff a product was replaced
        "0 product was replaced" iff a product matching the search filter was not found
        """
        args = parser.parse_args()
        search_key = args['filter']
        d_find = string_util_one(search_key)
        d_rep = string_util_one(args['replacedby'])
        rep_res = products.replace_one(d_find,d_rep)
        return '{} product was replaced'.format(rep_res.modified_count)

##
## Actually setup the Api resource routing here
##
api.add_resource(Create, '/create/')
api.add_resource(Products, '/products/')



if __name__ == '__main__':
        app.run(debug=True)
