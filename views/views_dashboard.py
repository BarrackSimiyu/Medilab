# Import the required modules
import pymysql
from flask_restful import *
from flask import *
from functions import *
import pymysql.cursors


# JWT packages
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required
# lab signup resource 

class  LabSignUp(Resource):
    def post(self):
        data = request.json
        lab_name = data["lab_name"]
        email = data["email"]
        phone = data["phone"]
        permit_id = data["permit_id"]
        password = data["password"]

        connection = connection = pymysql.connect( host = "localhost", user = "root", password = "", database = "Medilab" )
        cursor = connection.cursor()
        # sql = "INSERT INTO `laboratories` (lab_name,email,phone,permit_id,password) VALUES (%s, %s, %s, %s,%s)"

        # data = (lab_name,email,phone,permit_id,hash_password(password))

        # try:
        #     cursor.execute(sql,data)
        #     connection.commit()
        #     return jsonify({"message":"Lab Inserted Successfully"})
        # except:
        #     return jsonify({"message":"Lab Insertion failed .Try Again"})


        # Check password validity

        response = password_validity(password)
        if response:
            if check_phone(phone):
                # phone is correct
                sql = "INSERT INTO `laboratories` (lab_name,email,phone,permit_id,password) VALUES (%s, %s, %s, %s,%s)"
                data = (lab_name,email,encrypt_data(phone),permit_id,hash_password(password))

                try:
                   cursor.execute(sql,data)
                   connection.commit()
                   code = gen_random()
                   send_sms(phone, '''Thank You for joining MediLab.
                            Your secret number: {}. Do not share.''' .format(code))
                   return jsonify({"message":"Lab Inserted Successfully"})
                except:
                    return jsonify({"message":"Lab Insertion failed .Try Again"})

            else:
                # Phone is note in correct format
                return jsonify ({"message":"Phone number is not in correct format"})
            


        else:
            return jsonify({"message": response})
        

class LabSignIn(Resource):
    def post(self):
        data = request.json
        email = data["email"]
        password = data["password"]

        connection = pymysql.connect( host = "localhost", user = "root", password = "", database = "Medilab" )
        
         # check if email exists
        sql = "SELECT * FROM `laboratories` WHERE `email` = %s"
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute( sql, email )

        if cursor.rowcount == 0:
            return  jsonify( { "message" : "Email does not exist" } )
        else:
            # check password
            lab = cursor.fetchone()
            hashed_password = lab["password"]
            is_matchpassword = verify_password(password, hashed_password)
            if is_matchpassword == True:
                # create token
                access_token = create_access_token(identity=lab, fresh=True)
                return jsonify( { "access_token": access_token,'Lab': lab} )
            elif is_matchpassword == False:
                return jsonify({"message": "Login Failed"})
            else:
                return jsonify({"message":"Something went wrong"})
            

class ViewLabProfile(Resource):
    @jwt_required(fresh=True)
    def post(self):
         data = request.json
         lab_id=data["lab_id"]
    # connect to db
         connection = pymysql.connect( host = "localhost", user = "root", password = "", database = "Medilab" )
         sql = "SELECT * FROM `laboratories` WHERE `lab_id` = %s"
         cursor = connection.cursor(pymysql.cursors.DictCursor)
         cursor.execute( sql, lab_id )
         count = cursor.rowcount
         if count == 0:
                return jsonify ( { "message" : "Laboratory does not exist" } )
         else:
                lab = cursor.fetchone()
                return jsonify ({"message":  lab})
         


class AddLabTest(Resource):
    @jwt_required(fresh=True)
    def post(self):
        data = request.json
        lab_id = data["lab_id"]
        test_name = data["test_name"]
        test_description = data["test_description"]
        test_cost = data["test_cost"]
        test_discount = data["test_discount"]
        connection = pymysql.connect( host = "localhost", user = "root", password = "", database = "Medilab" )
        
        
        sql = "INSERT into lab_tests (lab_id,test_name,test_description,test_cost,test_discount) values (%s,%s,%s,%s,%s)"

        cursor = connection.cursor(pymysql.cursors.DictCursor)
        data = (lab_id,test_name,test_description,test_cost,test_discount)

        try:
            cursor.execute( sql, data )
            connection.commit()
            return  jsonify ( { "message" : "Test added successfully" } )
        except:
            return   jsonify ( { "message" : "Test Addition Failed" } )
        

class ViewLabTest(Resource):
    @jwt_required(fresh=True)
    def post(self):
        data = request.json

        lab_id = data["lab_id"]

        connection =  pymysql.connect( host = "localhost", user = "root", password = "", database = "Medilab" )
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT  * FROM `lab_tests` WHERE `lab_id` = %s"
        data = (lab_id)

        
        cursor.execute(sql,data)
        count = cursor.rowcount
        if count == 0:
                return jsonify ( { "message" : "Lab test does not exist." } )
        else:
                labtest = cursor.fetchall()
                return jsonify ({"message":  labtest})
        

class ViewLabBookings(Resource):
     @jwt_required(fresh=True)
     def post(self):
          
          data = request.json
          lab_id = data["lab_id"]
          connection =  pymysql.connect( host = "localhost", user = "root", password = "", database = "Medilab" )
          cursor = connection.cursor(pymysql.cursors.DictCursor)
          sql = "SELECT  * FROM `bookings` WHERE `lab_id` = %s"
          data = (lab_id)
          cursor.execute( sql, data )
          if cursor.rowcount == 0:
               return jsonify  ( { "message" : "No bookings found." } )
          else:
               bookings = cursor.fetchall()
            #    associate member_id with the booking 
            #    we want to loop all the bookings 
               #    and then loop all the members
               for  booking in bookings:
                    member_id = booking["member_id"]
                    # return jsonify (member_id)
                    sql = "SELECT * FROM `members` WHERE `member_id` = %s"
                    cursor = connection.cursor(pymysql.cursors.DictCursor)
                    cursor.execute( sql, member_id )
                    member = cursor.fetchone()
                    # The result is attached  to the booking dictionary under key
                    booking['key'] = member
                    # return jsonify (member)
               import json
                # we pass our bookings to json.dumps
               our_bookings = json.dumps( bookings, indent=1,sort_keys= True, default= str )
               return json.loads (our_bookings)
          


class AddNurse(Resource):
     @jwt_required(fresh=True)
     def post(self):
          data = request.json

          surname = data["surname"]
          others = data["others"]
          gender = data["gender"]
          phone=data["phone"]
          password = data["password"]
          lab_id = data["lab_id"]

          connection =   pymysql.connect( host = "localhost", user = "root", password = "", database = "Medilab" )
          cursor = connection.cursor()
          sql = "INSERT INTO nurses (surname,others, gender,phone,password,lab_id) VALUES (%s, %s, %s, %s,%s,%s)"
          data = (surname, others, gender,phone,hash_password(password),lab_id)

          try:
               cursor.execute( sql, data )
               connection.commit()
               return jsonify ({"message" : "Nurse added successfully."})
          except:
               connection.rollback()
               return jsonify ({"message" : "Nurse not added."})
          


class ViewNurse(Resource):
     @jwt_required(fresh=True)
     def post(self):
          data = request.json
          nurse_id = data["nurse_id"]

          connection =    pymysql.connect( host = "localhost", user = "root", password = "", database = "Medilab" )
          cursor = connection.cursor(pymysql.cursors.DictCursor)
          sql = "SELECT * FROM `nurses` WHERE `nurse_id` = %s"
          data = (nurse_id)
          cursor.execute( sql, data )
          count = cursor.rowcount
          if count == 0:
                return jsonify ( { "message" : "Nurse does not exist." } )
          else:
                nurse = cursor.fetchone()
                return jsonify ({"message":  nurse})



class NurseLabAllocation(Resource):
     @jwt_required(fresh=True)
     def post(self):
          data = request.json
          nurse_id = data["nurse_id"]
          invoice_no=data["invoice_no"]  
          connection =    pymysql.connect( host = "localhost", user = "root", password = "", database = "Medilab" )
          sql = "SELECT * FROM bookings  WHERE `status` = 'Pending'"
          cursor = connection.cursor(pymysql.cursors.DictCursor)
          cursor.execute( sql )
          count = cursor.rowcount
          if count == 0:
               return jsonify ( { "message" : "No pending tasks." } )
        
          else:
               sql1 =  "INSERT  INTO nurse_lab_allocation (nurse_id,invoice_no)  VALUES (%s,%s)"
               data = (nurse_id,invoice_no)
               cursor1 = connection.cursor()
               try:
                  cursor1.execute( sql1, data )
                  connection.commit()
                  return jsonify ({"message" : "Nurse allocated successfully."})
               except:
                  connection.rollback()
                  return jsonify ({"message" : "Nurse allocation failed."})
          
               
               
          

          



         
        

































































































