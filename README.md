# greendeck_interview (Submission Status: READY)
//Submission Status will be changed to READY when it is ready for your evaluation  
//Code file is functional, but documentation is in progress and some more functionalities may be added.  
### This is Aniruddha Ingle's submission for the SDE/DS internship role.  

### Introduction
- Atlas (MongoDB) was used to host the product data.
- Flask, Flask_Restful are used to implement the RESTful API

### Set Up

1. Download the zip file
2. Unzip the file which should give you a directory called 'greendeck_interview-main'
3. Open a terminal from that directory and enter the following docker commands (make sure you have docker intsalled)   
```
sudo docker build --tag greendeck_interview-main .
sudo docker run --name greendeck_interview-main -p 5000:5000 dockerize_flask_api

```

### Using URLs to perform CRUD operations.
There are two endpoints that implement the CRUD operations.
There are four added arguments that facilitate the functioning. Will be further explained in the end-points section.
  1. "record" //used to create a new document
  2. "filter" //used to set up the filter for querying the database
  3. "update" //used to set up the update query in the database
  4. "replacedby" //used to set up the replacedby query in the database
  
### End Points
#### /oneproduct/ --> This endpoint can be used to view, delete, or update one product document per operation.  
  a) View One Product Document    
  http://localhost:5000/oneproduct/ -d 'filter={"brand_name":"jellycat","name":"Jellycat Blossom Tulip Bunny Grabber, Pink"}' -X GET  
  ![](Screenshots/one%20product%20get%20operation.PNG)
  
  b) Delete One Product Document  
  http://localhost:5000/oneproduct/ -d 'filter={"brand_name":"jellycat";"name":"Jellycat Blossom Tulip Bunny Grabber, Pink"}' -X DELETE  
  ![](Screenshots/one%20product%20delete%20operation.PNG)
  
  c) Update One Product Document    
  http://localhost:5000/oneproduct/ -d 'filter={"brand_name":"jellycat";"name":"Jellycat Blossom Tulip Bunny Grabber, Pink"}' -d 'update={"$inc":{"regular_price_value":"50", "offer_price_value":"25"}' -X PUT    
  ![](Screenshots/one%20product%20update%20operation.PNG)
  
#### /products/ --> This endpoint can be used to view, delete, or update multiple product documents per operation.  
  a) View Multiple Product Documents    
  http://localhost:5000/oneproduct/ -d 'filter={"brand_name":"jellycat"}' -X GET 
  ![](Screenshots/multiple%20products%20get%20operation.PNG)
  
  b) Delete Multiple Product Documents  
  http://localhost:5000/products/ -d 'filter={"brand_name":"jellycat"}' -X DELETE  
  ![](Screenshots/multiple%20products%20delete%20operation.PNG)
  
  c) Update Multiple Product Documents    
  http://localhost:5000/products/ -d 'filter={"brand_name":"jellycat"}' -d 'update={"regular_price_value":"50","offer_price_value":"25"} -X PUT  
  ![](Screenshots/multiple%20products%20update%20operation.PNG)
  
#### /create/ --> This endpoint can be used to create a new product document or replace an existing product document with another.  
  a)Create and Insert One Product Document     
  http://localhost:5000/create/ -d 'record={"brand_name":"glammy soaps","name":"peach extract soap","regular_price_value":"1000","offer_price_value":"990"}' -X POST
  ![](Screenshots/create%20operation.PNG)

  b)Replace One Product Document by Another    
  http://localhost:5000/create/ -d 'filter={"brand_name":"glammy soaps"}' -d 'replacedby={"brand_name":"glammy";"name":"soap soap"}' -X PUT
  ![](Screenshots/replace%20operation.PNG)
