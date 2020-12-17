# Restful API for CRUD Operations on MongoDB hosted on Atlas

### Introduction
- Atlas (MongoDB) was used to host the product data.
- Flask, Flask_Restful are used to implement the RESTful API

### Set Up

1. Download the zip file
2. Unzip the file which should give you a directory called 'crud_restful_api-main'
3. Open a terminal from that directory and enter the following docker commands (make sure you have docker intsalled)   
```
sudo docker build --tag greendeck_interview-main .
sudo docker run --name greendeck_interview-main -p 5000:5000 greendeck_interview-main

```

### Using URLs to perform CRUD operations.
There are two endpoints that implement the CRUD operations.
There are four added arguments that facilitate the functioning. Will be further explained in the end-points section.
  1. "record" //used to create a new document
  2. "filter" //used to set up the filter for querying the database
  3. "update" //used to set up the update query in the database
  4. "replacedby" //used to set up the replacedby query in the database
  
### End Points  
(Note: If you are seeing alt-text instead of image then go to screenshot folder and find image with name = alt-text)
#### /oneproduct/ --> This endpoint can be used to view, delete, or update one product document per operation.  
  a) View One Product Document    
  ```
  http://localhost:5000/oneproduct/ -d 'filter={"brand_name":"jellycat","name":"Jellycat Blossom Tulip Bunny Grabber, Pink"}' -X GET  
  ```
  ![one product get operation](Screenshots/one%20product%20get%20operation.PNG)  
  
  ```
  b) Delete One Product Document  
  http://localhost:5000/oneproduct/ -d 'filter={"brand_name":"jellycat","name":"Jellycat Blossom Tulip Bunny Grabber, Pink"}' -X DELETE  
  ```
  ![one product delete operation](Screenshots/one%20product%20delete%20operation.PNG)  
  
  c) Update One Product Document    
  ```
  http://localhost:5000/oneproduct/ -d 'filter={"brand_name":"jellycat","name":"Jellycat Blossom Tulip Bunny Grabber, Pink"}' -d 'update={"$inc":{"regular_price_value":"50", "offer_price_value":"25"}' -X PUT    
  ```
  ![one product update operation](Screenshots/one%20product%20update%20operation%20inc.PNG)  
  
#### /products/ --> This endpoint can be used to view, delete, or update multiple product documents per operation.  
  a) View Multiple Product Documents    
  ```
  http://localhost:5000/oneproduct/ -d 'filter={"brand_name":"jellycat"}' -X GET   
  ```
  ![multiple products get operation](Screenshots/multiple%20products%20get%20operation.PNG)
  
  b) Delete Multiple Product Documents  
  ```
  http://localhost:5000/products/ -d 'filter={"brand_name":"jellycat"}' -X DELETE   
  ```
  ![multiple products delete operation](Screenshots/multiple%20products%20delete%20operation.PNG)
  
  c) Update Multiple Product Documents    
  ```
  http://localhost:5000/products/ -d 'filter={"brand_name":"jellycat"}' -d 'update={"regular_price_value":"50","offer_price_value":"25"} -X PUT     
  ```
  ![multiple products update operation](Screenshots/multiple%20products%20update%20operation.PNG)
  
#### /create/ --> This endpoint can be used to create a new product document or replace an existing product document with another.  
  a)Create and Insert One Product Document     
  ```
  http://localhost:5000/create/ -d 'record={"brand_name":"glammy soaps","name":"peach extract soap","regular_price_value":"1000","offer_price_value":"990"}' -X POST      
  ```
  ![create operation](Screenshots/create%20operation.PNG)

  b)Replace One Product Document by Another    
  ```
  http://localhost:5000/create/ -d 'filter={"brand_name":"glammy soaps"}' -d 'replacedby={"brand_name":"glammy";"name":"soap soap"}' -X PUT  
  ```
  ![replace operation](Screenshots/replace%20operation.PNG)
