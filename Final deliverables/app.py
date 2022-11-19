from flask import *
import ibm_db
import uuid
import hashlib
import os
from mailjet_rest import Client

con = ibm_db.connect("DATABASE=bludb;HOSTNAME=19af6446-6171-4641-8aba-9dcff8e1b6ff.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30699;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=psn93818;PWD=bnFxnbbGszyGKiLJ",'','')

app = Flask(__name__)
app.secret_key = '!@#GCEECE*&^'

api_key = '71ccb22303b75f55a1e4592f6fe367e8'
api_secret = 'b2413e0c9f02e44e895032fd13c1800b'
mailjet = Client(auth=(api_key, api_secret), version='v3.1')
def registration(email):
   data = {
      'Messages': [
         {
            "From": {
            "Email": "plasmadonorapplication@protonmail.com",
            "Name": "IBM-GCE"
            },
            "To": [
            {
               "Email": email,
            }
            ],
            "Subject": "Registration successful",
            "TextPart": "Welcome to our project website.",
            # "HTMLPart": "<h3>Dear passenger 1, welcome to <a href='https://www.mailjet.com/'>Mailjet</a>!</h3><br />May the delivery force be with you!",
            "CustomID": "AppGettingStartedTest"
         }
      ]
   }
   result = mailjet.send.create(data=data)
   print (result.status_code)
   print (result.json())

def plasmarequest(name,phone,bg,city,hosp):
   sql1 = """SELECT EMAIL FROM "PSN93818"."USERS" where CITY = '{C}';""".format(C=city)
   stmt = ibm_db.exec_immediate(con, sql1)
   dictionary = ibm_db.fetch_both(stmt)
   while dictionary != False:
      data = {
         'Messages': [
            {
               "From": {
               "Email": "plasmadonorapplication@protonmail.com",
               "Name": "IBM-GCE"
               },
               "To": [
               {
                  "Email": dictionary[0],
               }
               ],
               "Subject": "Donor needed",
               "TextPart": "Name:"+name+"\nPhone Number:"+phone+"\nBlood:"+bg+"\nLocation:"+city+"\nHospital:"+hosp+"\n",
               "CustomID": "ibm project"
            }
         ]
      }
      result = mailjet.send.create(data=data)
      print (result.status_code)
      print (result.json())
      dictionary = ibm_db.fetch_both(stmt)


@app.route('/')
def home():
   return render_template('home.html')

@app.route('/profile//<FLAG>/<UNIQID>')
def profile(UNIQID,FLAG):
   flag = FLAG
   users = []
   if flag == "hospital":
      sql = f"SELECT * FROM HOSPITAL WHERE uniqid='{escape(UNIQID)}'"
   else:
      sql = f"SELECT * FROM USERS WHERE uniqid='{escape(UNIQID)}'"
   stmt = ibm_db.exec_immediate(con, sql)
   dictionary = ibm_db.fetch_both(stmt)
   while dictionary != False:
      users.append(dictionary)
      dictionary = ibm_db.fetch_both(stmt)
   if users:
      print(flag)
      return render_template('profile.html', users=users,flag=flag)


@app.route('/about')
def about():
   return render_template('about.html')

@app.route("/dashboard",methods=["get"])
def dashboard():
    
   uid = str(session.get("uniqid")+'')
   sql = f"""select * from "PSN93818"."REQUEST" Where "UNIQID"!='{uid}' AND "STATUS"='waiting';"""

   # if(hosp != "" and hosp != None):
   #    sql += f""" AND "HOSP" ='{hosp}'"""
   # if(CITY != "" and CITY != None):
   #    sql += f""" AND "CITY" ='{CITY}' """
   # if(BG != "" and BG!=None):
   #    sql += f""" AND "BG" ='{BG}' """

   arr = []
   larr = []
   barr = []
   harr = []

   sql2 = f"""select distinct city from "PSN93818"."REQUEST" Where "UNIQID"!='{uid}' AND "STATUS"='waiting';"""
   sql3 = f"""select distinct hosp from "PSN93818"."REQUEST" Where "UNIQID"!='{uid}' AND "STATUS"='waiting';"""
   sql4 = f"""select distinct bg from "PSN93818"."REQUEST" Where "UNIQID"!='{uid}' AND "STATUS"='waiting';"""
   
   stmt = ibm_db.exec_immediate(con, sql)
   tuple = ibm_db.fetch_tuple(stmt)
   while tuple != False:
      arr.append(tuple)
      tuple = ibm_db.fetch_tuple(stmt)
   
   stmt = ibm_db.exec_immediate(con, sql2)
   tuple = ibm_db.fetch_tuple(stmt)
   while tuple != False:
      larr.append(tuple)
      tuple = ibm_db.fetch_tuple(stmt)
   
   
   stmt = ibm_db.exec_immediate(con, sql3)
   tuple = ibm_db.fetch_tuple(stmt)
   while tuple != False:
      harr.append(tuple)
      tuple = ibm_db.fetch_tuple(stmt)
   
   
   stmt = ibm_db.exec_immediate(con, sql4)
   tuple = ibm_db.fetch_tuple(stmt)
   while tuple != False:
      barr.append(tuple)
      tuple = ibm_db.fetch_tuple(stmt)

   print(arr)
   print(larr)
   print(harr)
   print(barr)
   return render_template("dashboard.html",requestarray=arr,locarr=larr,bgarr=barr,hosarr=harr)

@app.route("/hospitaldetails",methods=["get"])
def hospitaldetails():
    
   uid = str(session.get("uniqid")+'')
   sql = f"""select * from "PSN93818"."HOSPITAL";"""

   arr = []
   larr = []

   sql2 = f"""select distinct city from "PSN93818"."HOSPITAL" ;"""

   
   stmt = ibm_db.exec_immediate(con, sql)
   tuple = ibm_db.fetch_tuple(stmt)
   while tuple != False:
      arr.append(tuple)
      tuple = ibm_db.fetch_tuple(stmt)
   
   stmt = ibm_db.exec_immediate(con, sql2)
   tuple = ibm_db.fetch_tuple(stmt)
   while tuple != False:
      larr.append(tuple)
      tuple = ibm_db.fetch_tuple(stmt)
   
   print(arr)
   print(larr)

   return render_template("hospitaldetails.html",dataarray=arr,LOCarr=larr)

@app.route("/changestatus/<id>",methods=["get"])
def chngstatus(id):

   print(id)
   uid = str(session.get("uniqid"))+""
   name = str(session.get("name"))+""
   sql = f"""UPDATE "PSN93818"."REQUEST" SET "DONORID" = '{uid}', "DONORNAME" = '{name}',"STATUS"='accepted' WHERE "FUNIQID" = '{id}';"""
   stmt = ibm_db.prepare(con, sql)
   ibm_db.execute(stmt)

   return "success"


@app.route("/signin",methods=["POST"])
def signin():

   users = request.form['users']
   username = request.form['email']
   password = request.form['password']

   flag = "hospital" if users=="hospital" else "individual"
   
   if users == "individual":
      sql = """SELECT * FROM "PSN93818"."USERS" where email = '{usr}' AND password = '{pas}';""".format(usr=username,pas=password)

      stmt = ibm_db.exec_immediate(con, sql)
      user = ""
      while ibm_db.fetch_row(stmt) != False:
         user = ibm_db.result(stmt, 1)

      name = ""
      if(user == username):

         sql1 = """SELECT * FROM "PSN93818"."USERS" where email = '{usr}';""".format(usr=username)
         stmt1 = ibm_db.exec_immediate(con, sql1)
         uniqid = ""
         while ibm_db.fetch_row(stmt1) != False:
            uniqid = ibm_db.result(stmt1, 6)
            name = ibm_db.result(stmt1, 0)
         print(name)
         session['username'] = username
         session['name'] = name
         session['uniqid'] = uniqid
         session['flag'] = flag
         

   if users == "hospital":
      sql = """SELECT * FROM "PSN93818"."HOSPITAL" where email = '{usr}' AND password = '{pas}';""".format(usr=username,pas=password)

      stmt = ibm_db.exec_immediate(con, sql)
      user = ""
      while ibm_db.fetch_row(stmt) != False:
         user = ibm_db.result(stmt, 1)

      name = ""
      if(user == username):

         sql1 = """SELECT * FROM "PSN93818"."HOSPITAL" where email = '{usr}';""".format(usr=username)
         stmt1 = ibm_db.exec_immediate(con, sql1)
         uniqid = ""
         while ibm_db.fetch_row(stmt1) != False:
            uniqid = ibm_db.result(stmt1, 6)
            name = ibm_db.result(stmt1, 0)
         print(name)
         session['username'] = username
         session['name'] = name
         session['uniqid'] = uniqid
         session['flag'] = flag

   return redirect(url_for("profile",UNIQID=session["uniqid"],FLAG=session["flag"]))

   return render_template("signin.html")

@app.route("/signin",methods=["GET"])
def signin_get():

    print(con)
    return render_template("signin.html")

@app.route('/signup',methods = ["POST"])
def signup():
   if request.method == 'POST':
      users = request.form['users']
      name = request.form['name']
      email = request.form['email']
      phone = request.form['phone']
      city = request.form['city']
      blood_group = request.form['blood_group']
      address = request.form['address']
      password = request.form['password']
      password1 = request.form['password1']

      uniqid = uuid.uuid4().hex

      print(name,email,phone,city,blood_group,password)

      if users=="individual":
         sql = """INSERT INTO  "PSN93818"."USERS"  VALUES(?,?,?,?,?,?,?);"""
         stmt = ibm_db.prepare(con, sql)

         ibm_db.bind_param(stmt, 1, name)
         ibm_db.bind_param(stmt, 2, email)
         ibm_db.bind_param(stmt, 3, phone)
         ibm_db.bind_param(stmt, 4, city)
         ibm_db.bind_param(stmt, 5, blood_group)
         ibm_db.bind_param(stmt, 6, password)
         ibm_db.bind_param(stmt, 7, uniqid)
         ibm_db.execute(stmt)
         return redirect("/signin")

      if users=="hospital":
         sql = """INSERT INTO  "PSN93818"."HOSPITAL"  VALUES(?,?,?,?,?,?,?);"""
         stmt = ibm_db.prepare(con, sql)

         ibm_db.bind_param(stmt, 1, name)
         ibm_db.bind_param(stmt, 2, email)
         ibm_db.bind_param(stmt, 3, phone)
         ibm_db.bind_param(stmt, 4, city)
         ibm_db.bind_param(stmt, 5, address)
         ibm_db.bind_param(stmt, 6, password)
         ibm_db.bind_param(stmt, 7, uniqid)
         ibm_db.execute(stmt)
         return redirect("/signin")

      registration(email)

   


   return render_template("signup.html")

@app.route("/signup",methods=["GET"])
def signup_get():
   return render_template("signup.html")

@app.route("/requestform",methods=["get"])
def reqform_get():
   return render_template("form.html")


@app.route("/requestform",methods=["post"])
def reqform_post():
   name = request.form['name']
   phone = request.form['phone']
   bg = request.form['bg']
   city = request.form['city']
   hosp = request.form['hosp']

   formid = (hashlib.sha1((uuid.uuid4().hex + session.get("uniqid")).encode())).hexdigest() + ""
   print(formid)
   uid = str(session.get("uniqid")) + ""
   
   sql = f"""INSERT INTO  "PSN93818"."REQUEST" ("UNIQID","FUNIQID","NAME","BG","CITY","HOSP","STATUS","PHONE") VALUES('{uid}','{formid}','{name}','{bg}','{city}','{hosp}','waiting','{phone}');"""

   stmt = ibm_db.prepare(con, sql)
   ibm_db.execute(stmt)

   plasmarequest(name,phone,bg,city,hosp)

   return redirect("/myreq")

@app.route("/myreq",methods=["get"])
def myreq():
   print(session.get("uniqid") )

   reqarr = []
   accptarr = []
   uid = str(session.get("uniqid")+'')
   sql = f"""select * from "PSN93818"."REQUEST" Where "UNIQID"='{uid}';"""
   stmt = ibm_db.exec_immediate(con, sql)
   tuple = ibm_db.fetch_tuple(stmt)
   while tuple != False:
      if(tuple[6]=="waiting"):
         reqarr.append(tuple)
      else:
         accptarr.append(tuple)
      tuple = ibm_db.fetch_tuple(stmt)

   print(reqarr)
   return render_template("myreq.html",requestarray = reqarr,accptedarr=accptarr)

@app.route('/logout')
def logout():
   session.clear()
   return redirect(url_for("signin"))


if __name__ == '__main__':
   app.run(debug = True)

