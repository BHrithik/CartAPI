## CartAPI
### This is an API made using tornado framework in python and I psycog to connect to the postgres db

To run this api we have to have a postgres db with the following tables 

Follow the sql commands below to create the database required to run this api 

`CREATE TYPE category1 AS ENUM (‘fruits’,’vegetables’,’clothes’,’fastfood’);`

`CREATE TYPE add AS ENUM (‘home’,’office’,’add’);`

`CREATE TABLE products (id serial PRIMARY KEY,name VARCHAR(255),price NUMERIC,category category1)`

`CREATE TABLE users (id serial PRIMARY KEY,name VARCHAR(255),home TEXT,email TEXT UNIQUE NOT NULL,phone_no TEXT,office TEXT,other_add TEXT,password TEXT NOT NULL);`

`CREATE TABLE orders (order_id serial,user_id INT NOT NULL,product_id INT NOT NULL,quantity numeric,paid BOOLEAN DEFAULT false,shipping_address add,transaction_id TEXT,PRIMARY KEY (order_id,user_id,product_id,paid),FOREIGN KEY (user_id) REFERENCES users(id),FOREIGN KEY (product_id) REFERENCES products(id));`

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

Json templates for POST requests

Product Template
{
    "name":"pants",
    "price":2000,
    "category1”:”clothes"
}

User Template
{
            "name": "hrithik",
            "home": "lb nagar",
            "email": "hrithik@hotmail.com",
            "phone_no": "9139018031",
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
