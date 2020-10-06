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

def float_key_handler(insert_dict):
    """
    Parameters
    ----------
    insert_dict : dict
        Dictionary form of query filter converted by json.loads()

    Returns
    -------
    insert_dict : dict
        Dictionary representing query folder with numeric fields converted to 
        float

    """
    float_keys = ['regular_price_value','offer_price_value']
    for key in insert_dict.keys():
        if key in float_keys:
            insert_dict[key] = float(insert_dict[key])
    return insert_dict
            

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
class Product(Resource):
    """
    This class which represents an endpoint is used to perform CURD operations or to view 
    only one product document at a time.
    """
    def get(self):
        """
        Please specify -X GET after the URL.
        Returns
        -------
        result : json
            A database read is performed based on a string query found in args['filter']
            This result is converted to json and returned.
        """
        args = parser.parse_args()
        search_key = json.loads(args['filter'])
        search_key = float_key_handler(search_key)
        response = products.find_one(search_key)
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
        search_key = json.loads(args['filter'])
        search_key = float_key_handler(search_key)
        del_res = products.delete_one(search_key)
        return '{} product was deleted'.format(del_res.deleted_count)
    
    def put(self): #update
        """
        Returns
        -------
        "1 product was updated" iff a product was updated
        "0 product was updated" iff a product was not updated
        """
        args = parser.parse_args()
        search_key = json.loads(args['filter'])
        search_key = float_key_handler(search_key)
        update_key = json.loads(args['update'])
        l = list(update_key.values())
        key = list(update_key.keys())[0]
        update_key[key] = float_key_handler(l[0])
        update_res = products.update_one(search_key,update_key)
        return '{} product was updated'.format(update_res.modified_count)

class Products(Resource):
    """
    This class which represents an endpoint is used to perform CURD operations or view 
    multiple products at a time.
    """
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
            This result is converted to json and returned. This allows multiple records
            to be displayed.

        """
        args = parser.parse_args()
        search_key = json.loads(args['filter'])
        search_key = float_key_handler(search_key)
        cur = products.find(search_key) ###CHECK CHECK
        response = list(cur)
        if len(response) == 0:
            abort(404, message="No Results for the applied filter")
        out = {}
        doc_count = 0
        for doc in response:
            if '_id' in doc.keys():
                del doc['_id']
            out[doc_count] = doc
            doc_count += 1
        result = json.dumps(out)
        return result
    
    def delete(self): #delete
        """
        Returns
        -------
        "n products were deleted" iff n products are deleted
        "0 products were deleted" iff 0 products were deleted
        """
        args = parser.parse_args()
        search_key = json.loads(args['filter'])
        del_res = products.delete_many(search_key)
        return '{} products were deleted'.format(del_res.deleted_count)
    
    def put(self): #update
        """
        Returns
        -------
        "n products were updated" iff n products were updated
        "0 products were updated" iff 0 products were updated
        """
        args = parser.parse_args()
        search_key = json.loads(args['filter'])
        search_key = float_key_handler(search_key)
        update_key = json.loads(args['update'])
        l = list(update_key.values())
        key = list(update_key.keys())[0]
        update_key[key] = float_key_handler(l[0])
        update_res = products.update_many(search_key,update_key)
        return '{} products were updated'.format(update_res.modified_count)

#Create or Replace Product Documents
class Create(Resource):
    """
    This class which represents an end point is used to insert or replace one product
    document at a time.
    """
    def post(self): #create/insert a new product document
        """
        Returns
        -------
        When a new document is added to mongodb it assigns it with an inbuilt Id
        This id is displayed as confirmation of insert operation.
        """
        args = parser.parse_args()
        insert_dict = json.loads(args['record'])
        insert_dict = float_key_handler(insert_dict)
        in_res = products.insert_one(insert_dict)
        return 'Added Product has ID {}'.format(in_res.inserted_id), 201
    
    def put(self): #replace an existing product with a new product.
        """
        Returns
        -------
        "1 product was replaced" iff a product was replaced
        "0 product was replaced" iff a product matching the search filter was not found
        """
        args = parser.parse_args()
        search_key = json.loads(args['filter'])
        search_key = float_key_handler(search_key)
        replace_key = json.loads(args['replacedby'])
        search_key = float_key_handler(search_key)
        rep_res = products.replace_one(search_key,replace_key)
        return '{} product was replaced'.format(rep_res.modified_count)

##
## Actually setup the Api resource routing here
##
api.add_resource(Create, '/create/')
api.add_resource(Products, '/products/')
api.add_resource(Product, '/oneproduct/')



if __name__ == '__main__':
        app.run(debug=True, host = '0.0.0.0')
        
        
