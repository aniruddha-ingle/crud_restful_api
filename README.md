# greendeck_interview
This is Aniruddha Ingle's submission for the SDE/DS internship role.
- Atlas (MongoDB) was used to host the product data.
- 

### Using URLs to perform CRUD operations.
There are two endpoints that implement the CRUD operations.
1. /products/ --> This endpoint can be used to view, delete, or update the product documents.
  a) View One Product Document 
    -    http://localhost:5000/products/<search_key>
    e.g. http://localhost:5000/products/brand_name=jellycat,name=Jellycat Blossom Tulip Bunny Grabber, Pink
  b) Delete One Product Document
  c) Update One Product Document
2. /create/ --> This endpoint can be used to create a new product document or replace an existing product document with another. 
