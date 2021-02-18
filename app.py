from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import json
import psycopg2
import psycopg2.extras
from itertools import zip_longest


PORT=3000
DB_HOST = "localhost"
DB_NAME = "cart"
DB_USER = "admin"
DB_PASS = "admin"
conn=psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST)
l1=['id','name','price','category'] #products
l2=['id','name','home','email','phone_no','office','other_add','password'] #users 
l3=['order_id','product_id','user_id','quantity','paid','shipping_address','transaction_id'] #carts
cuid=0
users=[]

################################################################## PRODUCTS ##################################################################
class TodoItems(RequestHandler):
	def get(self):
		with conn:
			with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
				cur.execute("SELECT * FROM products;")
				products=[]
				products1=cur.fetchall()
				for i in products1:
					i["price"]=int(i["price"])
				for i in products1:
					d1=dict(zip_longest(l1,i))
					products.append(d1)
		self.write({"products":products})

class TodoItem(RequestHandler):
	def post(self, _):
		dummy=json.loads(self.request.body)
		with conn:
			with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
				cur.execute("INSERT INTO products (name,price,category) VALUES (%s,%s,%s) ;",(dummy["name"],dummy["price"],dummy["category"],))
		self.write({'message': 'New product has been sucessfully registered'})

	def put(self, _):
		dummy=json.loads(self.request.body)
		with conn:
			with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
				cur.execute("UPDATE products SET name=%s,price=%s,category=%s WHERE id=%s ;",(dummy["name"],dummy["price"],dummy["category"],dummy["id"],))
		self.write({'message': 'Product %s has been updated' % dummy["name"]})

	def delete(self, id):
		with conn:
			with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
				cur.execute("DELETE FROM products WHERE id =%s;",(id,))
		self.write({'message': 'Product with id %s has been deleted' % id})

#################################################################### USERS #####################################################################
class SendUsers(RequestHandler):
	def get(self):
		with conn:
			with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
				cur.execute("SELECT * FROM users;")
				users=[]
				users1=cur.fetchall()
				for i in users1:
					d1=dict(zip_longest(l2,i))
					users.append(d1)
		self.write({"users":users})

class UserHandler(RequestHandler):
	def post(self, _):
		dummy=json.loads(self.request.body)
		with conn:
			with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
				cur.execute("INSERT INTO users (name,home,email,phone_no,office,other_add,password) VALUES (%s,%s,%s,%s,%s,%s,crypt(%s,gen_salt('bf')));",(dummy["name"],dummy["home"],dummy["email"],dummy["phone_no"],dummy["office"],dummy["other_add"],dummy["password"],))
		self.write({'message': 'Hello %s, Welcome to the website' % dummy["name"]})

	def put(self, _):
		dummy=json.loads(self.request.body)
		with conn:
			with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
				cur.execute("UPDATE users SET name=%s,home=%s,email=%s,phone_no=%s,office=%s,other_add=%s WHERE id=%s;",(dummy["name"],dummy["home"],dummy["email"],dummy["phone_no"],dummy["office"],dummy["other_add"],dummy["id"],))
		self.write({'message': 'Hello %s, Your details have been updated' % dummy["name"]})
	
	def delete(self, id):
		with conn:
			with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
				cur.execute("DELETE FROM users WHERE id =%s;",(id,))
		self.write({'message': 'User with id %s was deleted' % id})

###################################################################### CART #####################################################################
class SendCarts(RequestHandler):
	def get(self):
		with conn:
			with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
				cur.execute("SELECT * FROM orders;")
				carts=[]
				carts1=cur.fetchall()
				for i in carts1:
					i["quantity"]=int(i["quantity"])
				for i in carts1:
					d1=dict(zip_longest(l3,i))
					carts.append(d1)
		self.write({"carts":carts})

class CartHandler(RequestHandler):
	def post(self, _):
		dummy=json.loads(self.request.body)
		with conn:
			with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
				cur.execute("SELECT id from users WHERE email=%s",(dummy["email"],))
				userid=cur.fetchone()[0]
				cur.execute("INSERT INTO orders (product_id,user_id,quantity,shipping_address) VALUES (%s,%s,%s,%s);",(dummy["product_id"],userid,dummy["quantity"],dummy["shipping_address"]))
		self.write({'message': 'Product with ID %s is added to the cart' % dummy["product_id"]})

	def put(self, _):
		dummy=json.loads(self.request.body)
		with conn:
			with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
				cur.execute("UPDATE orders SET product_id=%s,user_id=%s,quantity=%s,shipping_address=%s WHERE order_id=%s;",(dummy["product_id"],dummy["user_id"],dummy["quantity"],dummy["shipping_address"],dummy["order_id"],))
		self.write({'message': 'Product with ID %s has been updated in the cart' % dummy["product_id"]})

	def delete(self, id):
		with conn:
			with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
				cur.execute("DELETE FROM orders WHERE id =%s;",(id,))
		self.write({'message': 'order with id %s was deleted' % id})

############################################################################ BILL ################################################################
class BillHandler(RequestHandler):
	def get(self, id):
		with conn:
			with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
				cur.execute("SELECT product_id,quantity FROM orders WHERE user_id=%s AND paid=FALSE;",(id,))
				dummy=cur.fetchall()
				bill = 0
				prices=[]
				for i in dummy:
					cur.execute("SELECT price FROM products WHERE id=%s;",([i["product_id"]]),)
					prices.append((cur.fetchone()))
					i["quantity"]=int(i["quantity"])
				for i in range(0,len(dummy)):
					bill=bill+(dummy[i]["quantity"]*prices[i]["price"])
		self.write({'message': 'the outstanding amount is %s Rs' % bill})

	def post(self, _):
		transact=json.loads(self.request.body)
		with conn:
			with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
				cur.execute("SELECT id FROM users WHERE email=%s",(transact["email"],))
				buid=cur.fetchone()
				cur.execute("SELECT product_id,quantity FROM orders WHERE user_id=%s AND paid=FALSE;",(buid,))
				dummy=cur.fetchall()
				flag = 0
				bill = 0
				prices=[]
				for i in dummy:
					cur.execute("SELECT price FROM products WHERE id=%s",([i["product_id"]]),)
					prices.append((cur.fetchone()))
					i["quantity"]=int(i["quantity"])
				for i in range(0,len(dummy)):
					bill=bill+(dummy[i]["quantity"]*prices[i]["price"])
				if transact["paid_amount"] == bill:
					flag = 1
					cur.execute("UPDATE orders SET paid=TRUE,transaction_id=%s WHERE user_id=%s;",(transact["transaction_id"],buid,))
				cur.execute("SELECT name from USERS WHERE id=%s;",(transact["user_id"],))
				name = cur.fetchone()
		if flag==1:
			self.write({'message': 'Thank you %s, Your order will be shipped soon' % name[0]})
		else:
			self.write({'message': 'We are sorry %s, Transaction was unsuccessfull'% name[0]})				


##################################################################################################################################################
class LoginHandler(RequestHandler):
	def get(self ):
		self.write({'email': '','password':''})

	def post(self, ):
		cred=json.loads(self.request.body)
		with conn:
			with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
				cur.execute("SELECT id FROM users WHERE email=%s AND password=crypt(%s,password);",(cred["email"],cred["password"]))
				dummy=cur.fetchone()
				cur.execute("SELECT name from USERS WHERE id=%s;",(dummy[0],))
				name=cur.fetchone()
		if dummy[0]!=0:
			cuid=dummy[0]
			self.write({'message': 'You have successfully logged in %s'% name[0]})
		else:
			self.write({'message': 'Email or password is incorrect'})					

##################################################################################################################################################
##################################################################################################################################################

def make_app():
	urls = [
	(r"/items", TodoItems),
	(r"/api/item/([^/]+)?", TodoItem),
	(r"/users", SendUsers),
	(r"/api/user/([^/]+)?", UserHandler),
	(r"/carts",SendCarts),
	(r"/api/cart/([^/]+)?",CartHandler),
	(r"/bill/([^/]+)?",BillHandler),
	("/login/",LoginHandler)
	]
	return Application(urls, debug=True)

if __name__ == '__main__':
	app = make_app()
	app.listen(PORT)
	print("serving at port", PORT)
	IOLoop.instance().start()

conn.close()

