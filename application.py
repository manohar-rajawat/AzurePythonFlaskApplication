#!/usr/bin/python3.7

from azure.cosmos import exceptions, CosmosClient, PartitionKey
from flask import Flask,render_template,session,request,redirect,flash,url_for
from flask import jsonify,flash
import random

#Initializing the cosmos db
url = "https://azurecosmosdbiot.documents.azure.com:443/"
key = "RBMzWoOiHRDoS93QrSaAnLT973qc3nIuW1ebmRaPJuQfrT5W7AUQwRf03l81siNf3sSuZOJnMIKLZyab7ijPLA=="

#Cosmos Client Initialization
client = CosmosClient(url,key)

#Database Setting
db_name = 'MyIoTDatabase'
db = client.create_database_if_not_exists(id=db_name)

#Container Setting
c_name = 'UserLoginContainer'
cont = db.create_container_if_not_exists(id=c_name,
                        partition_key=PartitionKey(path="/country"),
                        offer_throughput=400
                        )

app = Flask(__name__)
app.secret_key = 'thisisthesecretkeydonotstealit'

@app.route("/api",methods=['POST'])
def api():
 response = request.get_json()
 print('The response from the client is :',response)
 lat_lon = [random.uniform(10,100),random.uniform(10,100)]
 return jsonify(lat_lon)

@app.route("/")
def home():
 if session.get('logged_in'):
  return redirect(url_for("profile"))
 else:
  return render_template("index.html")

@app.route("/login",methods=['POST','GET'])
def login():
 if request.method == 'POST':
  username = request.form['username']
  password = request.form['pass']
  if len(username) > 0 and len(password) > 0 :
   query = 'SELECT TOP 1 c.id FROM c where c.username="'+username+'" and c.password="'+password+'"'
   #print (query)
   items = list(cont.query_items(
        query=query,
        enable_cross_partition_query=True
   ))
   if(len(items) == 1):
    session['logged_in'] = True
    return redirect(url_for("profile"))
   else:
    flash("Wrong Credentials !")
    return redirect(url_for("home"))
  else:
    flash("Username or Password Can't be blank!")
    return recirect(url_for("home"))
 else:
  if not session.get('logged_in'):
   return redirect(url_for("home"))
  else:
   return redirect(url_for("profile"))

@app.route("/logout")
def logout():
 session['logged_in'] = False
 return redirect(url_for("home"))

@app.route("/profile")
def profile():
 if not session.get('logged_in'):
  return redirect(url_for("home"))
 else:
   return render_template("profile.html")

if __name__ == "__main__":
 app.run()
