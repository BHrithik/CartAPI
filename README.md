# CartAPI
This is an API made using tornado framework in python and I psycog to connect to the postgres db

To run this api we have to have a postgres db with the following tables 

Users - ['id','name','home','email','phone_no','office','other_add','password'] where id is primary key

Products - ['id','name','price','category'] where id is primary key

category is a enum field

Cart - ['order_id','product_id','user_id','quantity','paid','shipping_address','transaction_id'] 

shipping_address is a enum field

In the cart table the productid is a foreign key referencing id in product table the same with user_id referencing id from user table 
and it has a composite primary key (order_id,product_id,user_id,paid)

After creating these tables change the credentials inside app.py file by replacing with DB_HOST, DB_PASS, DB_NAME, DB_USER to match your credentials 
so that a connection can be established

run app.py file to start the server

http://localhost:3000/l/api/user/ (POST,PUT,DELETE) - to add update and delete users to delete use the url followed by the user id

http://localhost:3000/l/items (GET) - this request will give us all the products along with categories and prices 

http://localhost:3000/l/api/item/ (POST,PUT,DELETE) -  to add update and delete products 

http://localhost:3000/l/users (GET) - request to get info about all the users who signed up

http://localhost:3000/l/api/cart/ (POST,PUT,DELETE) - to add update and delete orders send cart json

http://localhost:3000/l/carts (GET) - get request to this url will give us all the orders placed by the user

http://localhost:3000/l/bill/ (GET,POST) - request to the url followed by user id will yeild the bill for that user and post request will accept a json with transaction

http://localhost:3000/l/login/ (POST) - send email and password json to authenticate and login

Product Template
{
    "name":"pants",
    "price":2000,
    "category1”:”clothes"
}

User Template
{
            "name": "hrithik",
            "home": "kothapet",
            "email": "hrithik@hotmail.com",
            "phone_no": "9121891018",
            "office":"kompally",
            "other_add": null,
            "password": ""
}


Order Template
{
    "product_id":1,
    "email":"hrithik@hotmail.com",
    "quantity":3
}


Transaction Template
{
    "user_id":1,
    "transaction_id":5,
    "paid_amount":12
}
